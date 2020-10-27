import discord
from redbot.core.bot import Red
from redbot.core import checks, commands, Config
from redbot.core.i18n import cog_i18n, Translator, set_contextual_locales_from_guild
from redbot.core.utils._internal_utils import send_to_owners_with_prefix_replaced
from redbot.core.utils.chat_formatting import escape, pagify

from .streamtypes import (
    HitboxStream,
    PicartoStream,
    Stream,
    TwitchStream,
    YoutubeStream,
)
from .errors import (
    APIError,
    InvalidTwitchCredentials,
    InvalidYoutubeCredentials,
    OfflineStream,
    StreamNotFound,
    StreamsError,
)
from . import streamtypes as _streamtypes

import re
import logging
import asyncio
import aiohttp
import contextlib
from datetime import datetime
from collections import defaultdict
from typing import Optional, List, Tuple, Union, Dict

_ = Translator("Streams", __file__)
log = logging.getLogger("red.core.cogs.Streams")


@cog_i18n(_)
class Streams(commands.Cog):
    """Various commands relating to streaming platforms.

    You can check if a Twitch, YouTube or Picarto stream is
    currently live.
    """

    global_defaults = {
        "refresh_timer": 300,
        "tokens": {},
        "streams": [],
        "notified_owner_missing_twitch_secret": False,
    }

    guild_defaults = {
        "autodelete": False,
        "mention_everyone": False,
        "mention_here": False,
        "live_message_mention": False,
        "live_message_nomention": False,
        "ignore_reruns": False,
    }

    role_defaults = {"mention": False}

    def __init__(self, bot: Red):
        super().__init__()
        self.config: Config = Config.get_conf(self, 26262626)
        self.ttv_bearer_cache: dict = {}
        self.config.register_global(**self.global_defaults)
        self.config.register_guild(**self.guild_defaults)
        self.config.register_role(**self.role_defaults)

        self.bot: Red = bot

        self.streams: List[Stream] = []
        self.task: Optional[asyncio.Task] = None

        self.yt_cid_pattern = re.compile("^UC[-_A-Za-z0-9]{21}[AQgw]$")

        self._ready_event: asyncio.Event = asyncio.Event()
        self._init_task: asyncio.Task = self.bot.loop.create_task(self.initialize())

    async def red_delete_data_for_user(self, **kwargs):
        """ Nothing to delete """
        return

    def check_name_or_id(self, data: str) -> bool:
        matched = self.yt_cid_pattern.fullmatch(data)
        if matched is None:
            return True
        return False

    async def initialize(self) -> None:
        """Should be called straight after cog instantiation."""
        await self.bot.wait_until_ready()

        try:
            await self.move_api_keys()
            await self.get_twitch_bearer_token()
            self.streams = await self.load_streams()
            self.task = self.bot.loop.create_task(self._stream_alerts())
        except Exception as error:
            log.exception("Failed to initialize Streams cog:", exc_info=error)

        self._ready_event.set()

    @commands.Cog.listener()
    async def on_red_api_tokens_update(self, service_name, api_tokens):
        if service_name == "twitch":
            await self.get_twitch_bearer_token(api_tokens)

    async def cog_before_invoke(self, ctx: commands.Context):
        await self._ready_event.wait()

    async def move_api_keys(self) -> None:
        """Move the API keys from cog stored config to core bot config if they exist."""
        tokens = await self.config.tokens()
        youtube = await self.bot.get_shared_api_tokens("youtube")
        twitch = await self.bot.get_shared_api_tokens("twitch")
        for token_type, token in tokens.items():
            if token_type == "YoutubeStream" and "api_key" not in youtube:
                await self.bot.set_shared_api_tokens("youtube", api_key=token)
            if token_type == "TwitchStream" and "client_id" not in twitch:
                # Don't need to check Community since they're set the same
                await self.bot.set_shared_api_tokens("twitch", client_id=token)
        await self.config.tokens.clear()

    async def get_twitch_bearer_token(self, api_tokens: Optional[Dict] = None) -> None:
        tokens = (
            await self.bot.get_shared_api_tokens("twitch") if api_tokens is None else api_tokens
        )
        if tokens.get("client_id"):
            notified_owner_missing_twitch_secret = (
                await self.config.notified_owner_missing_twitch_secret()
            )
            try:
                tokens["client_secret"]
                if notified_owner_missing_twitch_secret is True:
                    await self.config.notified_owner_missing_twitch_secret.set(False)
            except KeyError:
                message = _(
                    "You need a client secret key if you want to use the Twitch API on this cog.\n"
                    "Follow these steps:\n"
                    "1. Go to this page: https://dev.twitch.tv/console/apps.\n"
                    '2. Click "Manage" on your application.\n'
                    '3. Click on "New secret".\n'
                    "5. Copy your client ID and your client secret into:\n"
                    "{command}"
                    "\n\n"
                    "Note: These tokens are sensitive and should only be used in a private channel "
                    "or in DM with the bot."
                ).format(
                    command="`[p]set api twitch client_id {} client_secret {}`".format(
                        _("<your_client_id_here>"), _("<your_client_secret_here>")
                    )
                )
                if notified_owner_missing_twitch_secret is False:
                    await send_to_owners_with_prefix_replaced(self.bot, message)
                    await self.config.notified_owner_missing_twitch_secret.set(True)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://id.twitch.tv/oauth2/token",
                params={
                    "client_id": tokens.get("client_id", ""),
                    "client_secret": tokens.get("client_secret", ""),
                    "grant_type": "client_credentials",
                },
            ) as req:
                try:
                    data = await req.json()
                except aiohttp.ContentTypeError:
                    data = {}

                if req.status == 200:
                    pass
                elif req.status == 400 and data.get("message") == "invalid client":
                    log.error(
                        "Twitch API request failed authentication: set Client ID is invalid."
                    )
                elif req.status == 403 and data.get("message") == "invalid client secret":
                    log.error(
                        "Twitch API request failed authentication: set Client Secret is invalid."
                    )
                elif "message" in data:
                    log.error(
                        "Twitch OAuth2 API request failed with status code %s"
                        " and error message: %s",
                        req.status,
                        data["message"],
                    )
                else:
                    log.error("Twitch OAuth2 API request failed with status code %s", req.status)

                if req.status != 200:
                    return

        self.ttv_bearer_cache = data
        self.ttv_bearer_cache["expires_at"] = datetime.now().timestamp() + data.get("expires_in")

    async def maybe_renew_twitch_bearer_token(self) -> None:
        if self.ttv_bearer_cache:
            if self.ttv_bearer_cache["expires_at"] - datetime.now().timestamp() <= 60:
                await self.get_twitch_bearer_token()

    @commands.command()
    async def twitchstream(self, ctx: commands.Context, channel_name: str):
        """Check if a Twitch channel is live."""
        await self.maybe_renew_twitch_bearer_token()
        token = (await self.bot.get_shared_api_tokens("twitch")).get("client_id")
        stream = TwitchStream(
            name=channel_name,
            token=token,
            bearer=self.ttv_bearer_cache.get("access_token", None),
        )
        await self.check_online(ctx, stream)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def youtubestream(self, ctx: commands.Context, channel_id_or_name: str):
        """Check if a YouTube channel is live."""
        # TODO: Write up a custom check to look up cooldown set by botowner
        # This check is here to avoid people spamming this command and eating up quota
        apikey = await self.bot.get_shared_api_tokens("youtube")
        is_name = self.check_name_or_id(channel_id_or_name)
        if is_name:
            stream = YoutubeStream(name=channel_id_or_name, token=apikey)
        else:
            stream = YoutubeStream(id=channel_id_or_name, token=apikey)
        await self.check_online(ctx, stream)

    @commands.command()
    async def smashcast(self, ctx: commands.Context, channel_name: str):
        """Check if a smashcast channel is live."""
        stream = HitboxStream(name=channel_name)
        await self.check_online(ctx, stream)

    @commands.command()
    async def picarto(self, ctx: commands.Context, channel_name: str):
        """Check if a Picarto channel is live."""
        stream = PicartoStream(name=channel_name)
        await self.check_online(ctx, stream)

    async def check_online(
        self,
        ctx: commands.Context,
        stream: Union[PicartoStream, HitboxStream, YoutubeStream, TwitchStream],
    ):
        try:
            info = await stream.is_online()
        except OfflineStream:
            await ctx.send(_("That user is offline."))
        except StreamNotFound:
            await ctx.send(_("That channel doesn't seem to exist."))
        except InvalidTwitchCredentials:
            await ctx.send(
                _("The Twitch token is either invalid or has not been set. See {command}.").format(
                    command=f"`{ctx.clean_prefix}streamset twitchtoken`"
                )
            )
        except InvalidYoutubeCredentials:
            await ctx.send(
                _(
                    "The YouTube API key is either invalid or has not been set. See {command}."
                ).format(command=f"`{ctx.clean_prefix}streamset youtubekey`")
            )
        except APIError:
            await ctx.send(
                _("Something went wrong whilst trying to contact the stream service's API.")
            )
        else:
            if isinstance(info, tuple):
                embed, is_rerun = info
                ignore_reruns = await self.config.guild(ctx.channel.guild).ignore_reruns()
                if ignore_reruns and is_rerun:
                    await ctx.send(_("That user is offline."))
                    return
            else:
                embed = info
            await ctx.send(embed=embed)

    @commands.group()
    @commands.guild_only()
    @checks.mod_or_permissions(manage_channels=True)
    async def streamalert(self, ctx: commands.Context):
        """Manage automated stream alerts."""
        pass

    @streamalert.group(name="twitch", invoke_without_command=True)
    async def _twitch(self, ctx: commands.Context, channel_name: str = None):
        """Manage Twitch stream notifications."""
        if channel_name is not None:
            await ctx.invoke(self.twitch_alert_channel, channel_name)
        else:
            await ctx.send_help()

    @_twitch.command(name="channel")
    async def twitch_alert_channel(self, ctx: commands.Context, channel_name: str):
        """Toggle alerts in this channel for a Twitch stream."""
        if re.fullmatch(r"<#\d+>", channel_name):
            await ctx.send(
                _("Please supply the name of a *Twitch* channel, not a Discord channel.")
            )
            return
        await self.stream_alert(ctx, TwitchStream, channel_name.lower())

    @streamalert.command(name="youtube")
    async def youtube_alert(self, ctx: commands.Context, channel_name_or_id: str):
        """Toggle alerts in this channel for a YouTube stream."""
        await self.stream_alert(ctx, YoutubeStream, channel_name_or_id)

    @streamalert.command(name="smashcast")
    async def smashcast_alert(self, ctx: commands.Context, channel_name: str):
        """Toggle alerts in this channel for a Smashcast stream."""
        await self.stream_alert(ctx, HitboxStream, channel_name)

    @streamalert.command(name="picarto")
    async def picarto_alert(self, ctx: commands.Context, channel_name: str):
        """Toggle alerts in this channel for a Picarto stream."""
        await self.stream_alert(ctx, PicartoStream, channel_name)

    @streamalert.command(name="stop", usage="[disable_all=No]")
    async def streamalert_stop(self, ctx: commands.Context, _all: bool = False):
        """Disable all stream alerts in this channel or server.

        `[p]streamalert stop` will disable this channel's stream
        alerts.

        Do `[p]streamalert stop yes` to disable all stream alerts in
        this server.
        """
        streams = self.streams.copy()
        local_channel_ids = [c.id for c in ctx.guild.channels]
        to_remove = []

        for stream in streams:
            for channel_id in stream.channels:
                if channel_id == ctx.channel.id:
                    stream.channels.remove(channel_id)
                elif _all and ctx.channel.id in local_channel_ids:
                    if channel_id in stream.channels:
                        stream.channels.remove(channel_id)

            if not stream.channels:
                to_remove.append(stream)

        for stream in to_remove:
            streams.remove(stream)

        self.streams = streams
        await self.save_streams()

        if _all:
            msg = _("All the stream alerts in this server have been disabled.")
        else:
            msg = _("All the stream alerts in this channel have been disabled.")

        await ctx.send(msg)

    @streamalert.command(name="list")
    async def streamalert_list(self, ctx: commands.Context):
        """List all active stream alerts in this server."""
        streams_list = defaultdict(list)
        guild_channels_ids = [c.id for c in ctx.guild.channels]
        msg = _("Active alerts:\n\n")

        for stream in self.streams:
            for channel_id in stream.channels:
                if channel_id in guild_channels_ids:
                    streams_list[channel_id].append(stream.name.lower())

        if not streams_list:
            await ctx.send(_("There are no active alerts in this server."))
            return

        for channel_id, streams in streams_list.items():
            channel = ctx.guild.get_channel(channel_id)
            msg += "** - #{}**\n{}\n".format(channel, ", ".join(streams))

        for page in pagify(msg):
            await ctx.send(page)

    async def stream_alert(self, ctx: commands.Context, _class, channel_name):
        stream = self.get_stream(_class, channel_name)
        if not stream:
            token = await self.bot.get_shared_api_tokens(_class.token_name)
            is_yt = _class.__name__ == "YoutubeStream"
            is_twitch = _class.__name__ == "TwitchStream"
            if is_yt and not self.check_name_or_id(channel_name):
                stream = _class(id=channel_name, token=token)
            elif is_twitch:
                await self.maybe_renew_twitch_bearer_token()
                stream = _class(
                    name=channel_name,
                    token=token.get("client_id"),
                    bearer=self.ttv_bearer_cache.get("access_token", None),
                )
            else:
                stream = _class(name=channel_name, token=token)
            try:
                exists = await self.check_exists(stream)
            except InvalidTwitchCredentials:
                await ctx.send(
                    _(
                        "The Twitch token is either invalid or has not been set. See {command}."
                    ).format(command=f"`{ctx.clean_prefix}streamset twitchtoken`")
                )
                return
            except InvalidYoutubeCredentials:
                await ctx.send(
                    _(
                        "The YouTube API key is either invalid or has not been set. See "
                        "{command}."
                    ).format(command=f"`{ctx.clean_prefix}streamset youtubekey`")
                )
                return
            except APIError:
                await ctx.send(
                    _("Something went wrong whilst trying to contact the stream service's API.")
                )
                return
            else:
                if not exists:
                    await ctx.send(_("That channel doesn't seem to exist."))
                    return

        await self.add_or_remove(ctx, stream)

    @commands.group()
    @checks.mod_or_permissions(manage_channels=True)
    async def streamset(self, ctx: commands.Context):
        """Manage stream alert settings."""
        pass

    @streamset.command(name="timer")
    @checks.is_owner()
    async def _streamset_refresh_timer(self, ctx: commands.Context, refresh_time: int):
        """Set stream check refresh time."""
        if refresh_time < 60:
            return await ctx.send(_("You cannot set the refresh timer to less than 60 seconds"))

        await self.config.refresh_timer.set(refresh_time)
        await ctx.send(
            _("Refresh timer set to {refresh_time} seconds".format(refresh_time=refresh_time))
        )

    @streamset.command()
    @checks.is_owner()
    async def twitchtoken(self, ctx: commands.Context):
        """Explain how to set the twitch token."""
        message = _(
            "To set the twitch API tokens, follow these steps:\n"
            "1. Go to this page: https://dev.twitch.tv/dashboard/apps.\n"
            "2. Click *Register Your Application*.\n"
            "3. Enter a name, set the OAuth Redirect URI to `http://localhost`, and "
            "select an Application Category of your choosing.\n"
            "4. Click *Register*.\n"
            "5. Copy your client ID and your client secret into:\n"
            "{command}"
            "\n\n"
            "Note: These tokens are sensitive and should only be used in a private channel\n"
            "or in DM with the bot.\n"
        ).format(
            command="`{}set api twitch client_id {} client_secret {}`".format(
                ctx.clean_prefix, _("<your_client_id_here>"), _("<your_client_secret_here>")
            )
        )

        await ctx.maybe_send_embed(message)

    @streamset.command()
    @checks.is_owner()
    async def youtubekey(self, ctx: commands.Context):
        """Explain how to set the YouTube token."""

        message = _(
            "To get one, do the following:\n"
            "1. Create a project\n"
            "(see https://support.google.com/googleapi/answer/6251787 for details)\n"
            "2. Enable the YouTube Data API v3 \n"
            "(see https://support.google.com/googleapi/answer/6158841 for instructions)\n"
            "3. Set up your API key \n"
            "(see https://support.google.com/googleapi/answer/6158862 for instructions)\n"
            "4. Copy your API key and run the command "
            "{command}\n\n"
            "Note: These tokens are sensitive and should only be used in a private channel\n"
            "or in DM with the bot.\n"
        ).format(
            command="`{}set api youtube api_key {}`".format(
                ctx.clean_prefix, _("<your_api_key_here>")
            )
        )

        await ctx.maybe_send_embed(message)

    @streamset.group()
    @commands.guild_only()
    async def message(self, ctx: commands.Context):
        """Manage custom message for stream alerts."""
        pass

    @message.command(name="mention")
    @commands.guild_only()
    async def with_mention(self, ctx: commands.Context, *, message: str = None):
        """Set stream alert message when mentions are enabled.

        Use `{mention}` in the message to insert the selected mentions.
        Use `{stream}` in the message to insert the channel or user name.

        For example: `[p]streamset message mention {mention}, {stream} is live!`
        """
        if message is not None:
            guild = ctx.guild
            await self.config.guild(guild).live_message_mention.set(message)
            await ctx.send(_("Stream alert message set!"))
        else:
            await ctx.send_help()

    @message.command(name="nomention")
    @commands.guild_only()
    async def without_mention(self, ctx: commands.Context, *, message: str = None):
        """Set stream alert message when mentions are disabled.

        Use `{stream}` in the message to insert the channel or user name.

        For example: `[p]streamset message nomention {stream} is live!`
        """
        if message is not None:
            guild = ctx.guild
            await self.config.guild(guild).live_message_nomention.set(message)
            await ctx.send(_("Stream alert message set!"))
        else:
            await ctx.send_help()

    @message.command(name="clear")
    @commands.guild_only()
    async def clear_message(self, ctx: commands.Context):
        """Reset the stream alert messages in this server."""
        guild = ctx.guild
        await self.config.guild(guild).live_message_mention.set(False)
        await self.config.guild(guild).live_message_nomention.set(False)
        await ctx.send(_("Stream alerts in this server will now use the default alert message."))

    @streamset.group()
    @commands.guild_only()
    async def mention(self, ctx: commands.Context):
        """Manage mention settings for stream alerts."""
        pass

    @mention.command(aliases=["everyone"])
    @commands.guild_only()
    async def all(self, ctx: commands.Context):
        """Toggle the `@\u200beveryone` mention."""
        guild = ctx.guild
        current_setting = await self.config.guild(guild).mention_everyone()
        if current_setting:
            await self.config.guild(guild).mention_everyone.set(False)
            await ctx.send(_("`@\u200beveryone` will no longer be mentioned for stream alerts."))
        else:
            await self.config.guild(guild).mention_everyone.set(True)
            await ctx.send(_("When a stream is live, `@\u200beveryone` will be mentioned."))

    @mention.command(aliases=["here"])
    @commands.guild_only()
    async def online(self, ctx: commands.Context):
        """Toggle the `@\u200bhere` mention."""
        guild = ctx.guild
        current_setting = await self.config.guild(guild).mention_here()
        if current_setting:
            await self.config.guild(guild).mention_here.set(False)
            await ctx.send(_("`@\u200bhere` will no longer be mentioned for stream alerts."))
        else:
            await self.config.guild(guild).mention_here.set(True)
            await ctx.send(_("When a stream is live, `@\u200bhere` will be mentioned."))

    @mention.command()
    @commands.guild_only()
    async def role(self, ctx: commands.Context, *, role: discord.Role):
        """Toggle a role mention."""
        current_setting = await self.config.role(role).mention()
        if current_setting:
            await self.config.role(role).mention.set(False)
            await ctx.send(
                _("`@\u200b{role.name}` will no longer be mentioned for stream alerts.").format(
                    role=role
                )
            )
        else:
            await self.config.role(role).mention.set(True)
            msg = _(
                "When a stream or community is live, `@\u200b{role.name}` will be mentioned."
            ).format(role=role)
            if not role.mentionable:
                msg += " " + _(
                    "Since the role is not mentionable, it will be momentarily made mentionable "
                    "when announcing a streamalert. Please make sure I have the correct "
                    "permissions to manage this role, or else members of this role won't receive "
                    "a notification."
                )
            await ctx.send(msg)

    @streamset.command()
    @commands.guild_only()
    async def autodelete(self, ctx: commands.Context, on_off: bool):
        """Toggle alert deletion for when streams go offline."""
        await self.config.guild(ctx.guild).autodelete.set(on_off)
        if on_off:
            await ctx.send(_("The notifications will be deleted once streams go offline."))
        else:
            await ctx.send(_("Notifications will no longer be deleted."))

    @streamset.command(name="ignorereruns")
    @commands.guild_only()
    async def ignore_reruns(self, ctx: commands.Context):
        """Toggle excluding rerun streams from alerts."""
        guild = ctx.guild
        current_setting = await self.config.guild(guild).ignore_reruns()
        if current_setting:
            await self.config.guild(guild).ignore_reruns.set(False)
            await ctx.send(_("Streams of type 'rerun' will be included in alerts."))
        else:
            await self.config.guild(guild).ignore_reruns.set(True)
            await ctx.send(_("Streams of type 'rerun' will no longer send an alert."))

    async def add_or_remove(self, ctx: commands.Context, stream):
        if ctx.channel.id not in stream.channels:
            stream.channels.append(ctx.channel.id)
            if stream not in self.streams:
                self.streams.append(stream)
            await ctx.send(
                _(
                    "I'll now send a notification in this channel when {stream.name} is live."
                ).format(stream=stream)
            )
        else:
            stream.channels.remove(ctx.channel.id)
            if not stream.channels:
                self.streams.remove(stream)
            await ctx.send(
                _(
                    "I won't send notifications about {stream.name} in this channel anymore."
                ).format(stream=stream)
            )

        await self.save_streams()

    def get_stream(self, _class, name):
        for stream in self.streams:
            # if isinstance(stream, _class) and stream.name == name:
            #    return stream
            # Reloading this cog causes an issue with this check ^
            # isinstance will always return False
            # As a workaround, we'll compare the class' name instead.
            # Good enough.
            if _class.__name__ == "YoutubeStream" and stream.type == _class.__name__:
                # Because name could be a username or a channel id
                if self.check_name_or_id(name) and stream.name.lower() == name.lower():
                    return stream
                elif not self.check_name_or_id(name) and stream.id == name:
                    return stream
            elif stream.type == _class.__name__ and stream.name.lower() == name.lower():
                return stream

    @staticmethod
    async def check_exists(stream):
        try:
            await stream.is_online()
        except OfflineStream:
            pass
        except StreamNotFound:
            return False
        except StreamsError:
            raise
        return True

    async def _stream_alerts(self):
        await self.bot.wait_until_ready()
        while True:
            try:
                await self.check_streams()
            except asyncio.CancelledError:
                pass
            await asyncio.sleep(await self.config.refresh_timer())

    async def check_streams(self):
        for stream in self.streams:
            with contextlib.suppress(Exception):
                try:
                    if stream.__class__.__name__ == "TwitchStream":
                        await self.maybe_renew_twitch_bearer_token()
                        embed, is_rerun = await stream.is_online()
                    else:
                        embed = await stream.is_online()
                        is_rerun = False
                except OfflineStream:
                    if not stream._messages_cache:
                        continue
                    for message in stream._messages_cache:
                        with contextlib.suppress(Exception):
                            if await self.bot.cog_disabled_in_guild(self, message.guild):
                                continue
                            autodelete = await self.config.guild(message.guild).autodelete()
                            if autodelete:
                                await message.delete()
                    stream._messages_cache.clear()
                    await self.save_streams()
                else:
                    if stream._messages_cache:
                        continue
                    for channel_id in stream.channels:
                        channel = self.bot.get_channel(channel_id)
                        if not channel:
                            continue
                        if await self.bot.cog_disabled_in_guild(self, channel.guild):
                            continue
                        ignore_reruns = await self.config.guild(channel.guild).ignore_reruns()
                        if ignore_reruns and is_rerun:
                            continue

                        await set_contextual_locales_from_guild(self.bot, channel.guild)

                        mention_str, edited_roles = await self._get_mention_str(
                            channel.guild, channel
                        )

                        if mention_str:
                            alert_msg = await self.config.guild(
                                channel.guild
                            ).live_message_mention()
                            if alert_msg:
                                content = alert_msg  # Stop bad things from happening here...
                                content = content.replace(
                                    "{stream.name}", str(stream.name)
                                )  # Backwards compatibility
                                content = content.replace("{stream}", str(stream.name))
                                content = content.replace("{mention}", mention_str)
                            else:
                                content = _("{mention}, {stream} is live!").format(
                                    mention=mention_str,
                                    stream=escape(
                                        str(stream.name), mass_mentions=True, formatting=True
                                    ),
                                )
                        else:
                            alert_msg = await self.config.guild(
                                channel.guild
                            ).live_message_nomention()
                            if alert_msg:
                                content = alert_msg  # Stop bad things from happening here...
                                content = content.replace(
                                    "{stream.name}", str(stream.name)
                                )  # Backwards compatibility
                                content = content.replace("{stream}", str(stream.name))
                            else:
                                content = _("{stream} is live!").format(
                                    stream=escape(
                                        str(stream.name), mass_mentions=True, formatting=True
                                    )
                                )

                        m = await channel.send(
                            content,
                            embed=embed,
                            allowed_mentions=discord.AllowedMentions(roles=True, everyone=True),
                        )
                        stream._messages_cache.append(m)
                        if edited_roles:
                            for role in edited_roles:
                                await role.edit(mentionable=False)
                        await self.save_streams()

    async def _get_mention_str(
        self, guild: discord.Guild, channel: discord.TextChannel
    ) -> Tuple[str, List[discord.Role]]:
        """Returns a 2-tuple with the string containing the mentions, and a list of
        all roles which need to have their `mentionable` property set back to False.
        """
        settings = self.config.guild(guild)
        mentions = []
        edited_roles = []
        if await settings.mention_everyone():
            mentions.append("@everyone")
        if await settings.mention_here():
            mentions.append("@here")
        can_manage_roles = guild.me.guild_permissions.manage_roles
        can_mention_everyone = channel.permissions_for(guild.me).mention_everyone
        for role in guild.roles:
            if await self.config.role(role).mention():
                if not can_mention_everyone and can_manage_roles and not role.mentionable:
                    try:
                        await role.edit(mentionable=True)
                    except discord.Forbidden:
                        # Might still be unable to edit role based on hierarchy
                        pass
                    else:
                        edited_roles.append(role)
                mentions.append(role.mention)
        return " ".join(mentions), edited_roles

    async def filter_streams(self, streams: list, channel: discord.TextChannel) -> list:
        filtered = []
        for stream in streams:
            tw_id = str(stream["channel"]["_id"])
            for alert in self.streams:
                if isinstance(alert, TwitchStream) and alert.id == tw_id:
                    if channel.id in alert.channels:
                        break
            else:
                filtered.append(stream)
        return filtered

    async def load_streams(self):
        streams = []
        for raw_stream in await self.config.streams():
            _class = getattr(_streamtypes, raw_stream["type"], None)
            if not _class:
                continue
            raw_msg_cache = raw_stream["messages"]
            raw_stream["_messages_cache"] = []
            for raw_msg in raw_msg_cache:
                chn = self.bot.get_channel(raw_msg["channel"])
                if chn is not None:
                    try:
                        msg = await chn.fetch_message(raw_msg["message"])
                    except discord.HTTPException:
                        pass
                    else:
                        raw_stream["_messages_cache"].append(msg)
            token = await self.bot.get_shared_api_tokens(_class.token_name)
            if token:
                if _class.__name__ == "TwitchStream":
                    raw_stream["token"] = token.get("client_id")
                    raw_stream["bearer"] = self.ttv_bearer_cache.get("access_token", None)
                else:
                    raw_stream["token"] = token
            streams.append(_class(**raw_stream))

        return streams

    async def save_streams(self):
        raw_streams = []
        for stream in self.streams:
            raw_streams.append(stream.export())

        await self.config.streams.set(raw_streams)

    def cog_unload(self):
        if self.task:
            self.task.cancel()

    __del__ = cog_unload

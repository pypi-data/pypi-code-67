import logging
import time

from abc import ABCMeta, abstractmethod

from .managers import BasePathManager, TokenManager, TokenManagerProperties
from .builders import SubscribeBuilder
from .builders import UnsubscribeBuilder
from .endpoints.time import Time
from .endpoints.history import History
from .endpoints.access.audit import Audit
from .endpoints.access.grant import Grant
from .endpoints.access.grant_token import GrantToken
from .endpoints.access.revoke import Revoke
from .endpoints.channel_groups.add_channel_to_channel_group import AddChannelToChannelGroup
from .endpoints.channel_groups.list_channels_in_channel_group import ListChannelsInChannelGroup
from .endpoints.channel_groups.remove_channel_from_channel_group import RemoveChannelFromChannelGroup
from .endpoints.channel_groups.remove_channel_group import RemoveChannelGroup
from .endpoints.presence.get_state import GetState
from .endpoints.presence.heartbeat import Heartbeat
from .endpoints.presence.set_state import SetState
from .endpoints.pubsub.publish import Publish
from .endpoints.pubsub.fire import Fire
from .endpoints.presence.here_now import HereNow
from .endpoints.presence.where_now import WhereNow
from .endpoints.history_delete import HistoryDelete
from .endpoints.message_count import MessageCount
from .endpoints.signal import Signal
from .endpoints.users.get_users import GetUsers
from .endpoints.users.create_user import CreateUser
from .endpoints.users.get_user import GetUser
from .endpoints.users.update_user import UpdateUser
from .endpoints.users.delete_user import DeleteUser
from .endpoints.space.get_spaces import GetSpaces
from .endpoints.space.get_space import GetSpace
from .endpoints.space.update_space import UpdateSpace
from .endpoints.space.delete_space import DeleteSpace
from .endpoints.space.create_space import CreateSpace
from .endpoints.membership.get_space_memberships import GetSpaceMemberships
from .endpoints.membership.get_members import GetMembers
from .endpoints.membership.manage_members import ManageMembers
from .endpoints.membership.manage_memberships import ManageMemberships
from .endpoints.fetch_messages import FetchMessages
from .endpoints.message_actions.add_message_action import AddMessageAction
from .endpoints.message_actions.get_message_actions import GetMessageActions
from .endpoints.message_actions.remove_message_action import RemoveMessageAction
from .endpoints.file_operations.list_files import ListFiles
from .endpoints.file_operations.delete_file import DeleteFile
from .endpoints.file_operations.get_file_url import GetFileDownloadUrl
from .endpoints.file_operations.fetch_upload_details import FetchFileUploadS3Data
from .endpoints.file_operations.send_file import SendFileNative
from .endpoints.file_operations.download_file import DownloadFileNative
from .endpoints.file_operations.publish_file_message import PublishFileMessage

from .endpoints.push.add_channels_to_push import AddChannelsToPush
from .endpoints.push.remove_channels_from_push import RemoveChannelsFromPush
from .endpoints.push.remove_device import RemoveDeviceFromPush
from .endpoints.push.list_push_provisions import ListPushProvisions
from .managers import TelemetryManager

logger = logging.getLogger("pubnub")


class PubNubCore:
    """A base class for PubNub Python API implementations"""
    SDK_VERSION = "4.6.1"
    SDK_NAME = "PubNub-Python"

    TIMESTAMP_DIVIDER = 1000
    MAX_SEQUENCE = 65535

    __metaclass__ = ABCMeta

    def __init__(self, config):
        self.config = config
        self.config.validate()
        self.headers = {
            'User-Agent': self.sdk_name
        }

        self._subscription_manager = None
        self._publish_sequence_manager = None
        self._telemetry_manager = TelemetryManager()
        self._base_path_manager = BasePathManager(config)
        self._token_manager = TokenManager()

    @property
    def base_origin(self):
        return self._base_path_manager.get_base_path()

    @property
    def sdk_name(self):
        return "%s%s/%s" % (PubNubCore.SDK_NAME, self.sdk_platform(), PubNubCore.SDK_VERSION)

    @abstractmethod
    def sdk_platform(self):
        pass

    @property
    def uuid(self):
        return self.config.uuid

    def add_listener(self, listener):
        self._validate_subscribe_manager_enabled()

        return self._subscription_manager.add_listener(listener)

    def remove_listener(self, listener):
        self._validate_subscribe_manager_enabled()

        return self._subscription_manager.remove_listener(listener)

    def get_subscribed_channels(self):
        self._validate_subscribe_manager_enabled()

        return self._subscription_manager.get_subscribed_channels()

    def get_subscribed_channel_groups(self):
        self._validate_subscribe_manager_enabled()

        return self._subscription_manager.get_subscribed_channel_groups()

    def add_channel_to_channel_group(self):
        return AddChannelToChannelGroup(self)

    def remove_channel_from_channel_group(self):
        return RemoveChannelFromChannelGroup(self)

    def list_channels_in_channel_group(self):
        return ListChannelsInChannelGroup(self)

    def remove_channel_group(self):
        return RemoveChannelGroup(self)

    def subscribe(self):
        return SubscribeBuilder(self._subscription_manager)

    def unsubscribe(self):
        return UnsubscribeBuilder(self._subscription_manager)

    def unsubscribe_all(self):
        return self._subscription_manager.unsubscribe_all()

    def reconnect(self):
        return self._subscription_manager.reconnect()

    def heartbeat(self):
        return Heartbeat(self)

    def set_state(self):
        return SetState(self, self._subscription_manager)

    def get_state(self):
        return GetState(self)

    def here_now(self):
        return HereNow(self)

    def where_now(self):
        return WhereNow(self)

    def publish(self):
        return Publish(self)

    def grant(self):
        return Grant(self)

    def grant_token(self):
        return GrantToken(self)

    def revoke(self):
        return Revoke(self)

    def audit(self):
        return Audit(self)

    # Push Related methods
    def list_push_channels(self):
        return ListPushProvisions(self)

    def add_channels_to_push(self):
        return AddChannelsToPush(self)

    def remove_channels_from_push(self):
        return RemoveChannelsFromPush(self)

    def remove_device_from_push(self):
        return RemoveDeviceFromPush(self)

    def history(self):
        return History(self)

    def message_counts(self):
        return MessageCount(self)

    def fire(self):
        return Fire(self)

    def signal(self):
        return Signal(self)

    def get_users(self):
        return GetUsers(self)

    def create_user(self):
        return CreateUser(self)

    def get_user(self):
        return GetUser(self)

    def update_user(self):
        return UpdateUser(self)

    def delete_user(self):
        return DeleteUser(self)

    def get_spaces(self):
        return GetSpaces(self)

    def get_space(self):
        return GetSpace(self)

    def update_space(self):
        return UpdateSpace(self)

    def delete_space(self):
        return DeleteSpace(self)

    def create_space(self):
        return CreateSpace(self)

    def get_space_memberships(self):
        return GetSpaceMemberships(self)

    def get_members(self):
        return GetMembers(self)

    def manage_members(self):
        return ManageMembers(self)

    def manage_memberships(self):
        return ManageMemberships(self)

    def fetch_messages(self):
        return FetchMessages(self)

    def add_message_action(self):
        return AddMessageAction(self)

    def get_message_actions(self):
        return GetMessageActions(self)

    def remove_message_action(self):
        return RemoveMessageAction(self)

    def time(self):
        return Time(self)

    def delete_messages(self):
        return HistoryDelete(self)

    def set_token(self, token):
        self._token_manager.set_token(token)

    def set_tokens(self, tokens):
        self._token_manager.set_tokens(tokens)

    def get_token(self, tms_properties):
        return self._token_manager.get_token(tms_properties)

    def get_token_by_resource(self, resource_id, resource_type):
        return self._token_manager.get_token(TokenManagerProperties(
            resource_id=resource_id,
            resource_type=resource_type
        ))

    def get_tokens(self):
        return self._token_manager.get_tokens()

    def get_tokens_by_resource(self, resource_type):
        return self._token_manager.get_tokens_by_resource(resource_type)

    def send_file(self):
        if not self.sdk_platform():
            return SendFileNative(self)
        elif "Asyncio" in self.sdk_platform():
            from .endpoints.file_operations.send_file_asyncio import AsyncioSendFile
            return AsyncioSendFile(self)
        else:
            raise NotImplementedError

    def download_file(self):
        if not self.sdk_platform():
            return DownloadFileNative(self)
        elif "Asyncio" in self.sdk_platform():
            from .endpoints.file_operations.download_file_asyncio import DownloadFileAsyncio
            return DownloadFileAsyncio(self)
        else:
            raise NotImplementedError

    def list_files(self):
        return ListFiles(self)

    def get_file_url(self):
        return GetFileDownloadUrl(self)

    def delete_file(self):
        return DeleteFile(self)

    def _fetch_file_upload_s3_data(self):
        return FetchFileUploadS3Data(self)

    def publish_file_message(self):
        return PublishFileMessage(self)

    def decrypt(self, cipher_key, file):
        return self.config.file_crypto.decrypt(cipher_key, file)

    def encrypt(self, cipher_key, file):
        return self.config.file_crypto.encrypt(cipher_key, file)

    @staticmethod
    def timestamp():
        return int(time.time())

    def _validate_subscribe_manager_enabled(self):
        if self._subscription_manager is None:
            raise Exception("Subscription manager is not enabled for this instance")

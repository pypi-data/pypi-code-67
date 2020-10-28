
from __future__ import annotations

import asyncio
import os.path
import uuid
from argparse import ArgumentParser, Namespace
from contextlib import closing, asynccontextmanager
from datetime import datetime, timezone
from secrets import token_bytes
from typing import Any, Optional, Tuple, Sequence, Mapping, Dict, Awaitable, \
    AsyncIterator
from typing_extensions import Final

from pkg_resources import resource_listdir, resource_stream
from pysasl.creds import AuthenticationCredentials
from pysasl.hashing import Cleartext

from pymap.config import BackendCapability, IMAPConfig
from pymap.exceptions import AuthorizationFailure, NotAllowedError, \
    UserNotFound
from pymap.interfaces.backend import BackendInterface, ServiceInterface
from pymap.interfaces.login import LoginTokenData, LoginInterface, \
    IdentityInterface
from pymap.parsing.message import AppendMessage
from pymap.parsing.specials.flag import Flag, Recent
from pymap.user import UserMetadata

from .filter import FilterSet
from .mailbox import Message, MailboxData, MailboxSet
from ..session import BaseSession

__all__ = ['DictBackend', 'Config']


class DictBackend(BackendInterface):
    """Defines a backend that uses an in-memory dictionary for example usage
    and integration testing.

    """

    def __init__(self, login: Login, config: Config) -> None:
        super().__init__()
        self._login = login
        self._config = config

    @property
    def login(self) -> Login:
        return self._login

    @property
    def config(self) -> Config:
        return self._config

    @classmethod
    def add_subparser(cls, name: str, subparsers: Any) -> ArgumentParser:
        parser = subparsers.add_parser(name, help='in-memory backend')
        parser.add_argument('--demo-data', action='store_true',
                            help='load initial demo data')
        parser.add_argument('--demo-user', default='demouser',
                            metavar='VAL', help='demo user ID')
        parser.add_argument('--demo-password', default='demopass',
                            metavar='VAL', help='demo user password')
        return parser

    @classmethod
    async def init(cls, args: Namespace) -> Tuple[DictBackend, Config]:
        config = Config.from_args(args)
        login = Login(config)
        return cls(login, config), config

    async def start(self, services: Sequence[ServiceInterface]) -> Awaitable:
        tasks = [await service.start() for service in services]
        return asyncio.gather(*tasks)


class Config(IMAPConfig):
    """The config implementation for the dict backend."""

    def __init__(self, args: Namespace, *, demo_data: bool,
                 demo_user: str, demo_password: str,
                 demo_data_resource: str = __name__, **extra: Any) -> None:
        super().__init__(args, hash_context=Cleartext(), **extra)
        self._demo_data = demo_data
        self._demo_user = demo_user
        self._demo_password = demo_password
        self._demo_data_resource = demo_data_resource
        self.set_cache: Dict[str, Tuple[MailboxSet, FilterSet]] = {}

    @property
    def backend_capability(self) -> BackendCapability:
        return BackendCapability(idle=True, object_id=True, multi_append=True)

    @property
    def demo_data(self) -> bool:
        """True if demo data should be loaded at startup."""
        return self._demo_data

    @property
    def demo_data_resource(self) -> str:
        """Resource path of demo data files."""
        return self._demo_data_resource

    @property
    def demo_user(self) -> str:
        """A login name that is valid at startup, which defaults to
        ``demouser``.

        """
        return self._demo_user

    @property
    def demo_password(self) -> str:
        """The password for the :attr:`.demo_user` login name, which defaults
        to ``demopass``.

        """
        return self._demo_password

    @classmethod
    def parse_args(cls, args: Namespace) -> Mapping[str, Any]:
        return {**super().parse_args(args),
                'demo_data': args.demo_data,
                'demo_user': args.demo_user,
                'demo_password': args.demo_password}


class Session(BaseSession[Message]):
    """The session implementation for the dict backend."""

    def __init__(self, owner: str, config: Config, mailbox_set: MailboxSet,
                 filter_set: FilterSet) -> None:
        super().__init__(owner)
        self._config = config
        self._mailbox_set = mailbox_set
        self._filter_set = filter_set

    @property
    def config(self) -> Config:
        return self._config

    @property
    def mailbox_set(self) -> MailboxSet:
        return self._mailbox_set

    @property
    def filter_set(self) -> FilterSet:
        return self._filter_set


class Login(LoginInterface):
    """The login implementation for the dict backend."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config
        self.users = {config.demo_user: UserMetadata(
            config, password=config.demo_password)}
        self.tokens: Dict[str, Tuple[str, bytes]] = {}

    async def authenticate(self, credentials: AuthenticationCredentials) \
            -> Identity:
        authcid = credentials.authcid
        token_key: Optional[bytes] = None
        role: Optional[str] = None
        if credentials.authcid_type == 'login-token':
            if authcid in self.tokens:
                authcid, token_key = self.tokens[authcid]
        elif credentials.authcid_type == 'admin-token':
            authcid = credentials.identity
            role = 'admin'
        try:
            metadata = await Identity(authcid, self, None).get()
        except UserNotFound:
            metadata = UserMetadata(self.config)
        await metadata.check_password(credentials, token_key=token_key)
        role = role or metadata.role
        if role != 'admin' and authcid != credentials.identity:
            raise AuthorizationFailure()
        return Identity(credentials.identity, self, role)


class Identity(IdentityInterface):
    """The identity implementation for the dict backend."""

    def __init__(self, name: str, login: Login, role: Optional[str]) -> None:
        super().__init__()
        self.login: Final = login
        self.config: Final = login.config
        self._name = name
        self._role = role

    @property
    def name(self) -> str:
        return self._name

    async def new_token(self, *, expiration: datetime = None) \
            -> LoginTokenData:
        token_id = uuid.uuid4().hex
        token_key = token_bytes()
        self.login.tokens[token_id] = (self.name, token_key)
        return LoginTokenData(self.name, token_id, token_key)

    @asynccontextmanager
    async def new_session(self) -> AsyncIterator[Session]:
        identity = self.name
        config = self.config
        _ = await self.get()
        mailbox_set, filter_set = config.set_cache.get(identity, (None, None))
        if not mailbox_set or not filter_set:
            mailbox_set = MailboxSet()
            filter_set = FilterSet()
            if config.demo_data and identity == config.demo_user:
                await self._load_demo(config.demo_data_resource,
                                      mailbox_set, filter_set)
            config.set_cache[identity] = (mailbox_set, filter_set)
        yield Session(identity, config, mailbox_set, filter_set)

    async def _load_demo(self, resource: str, mailbox_set: MailboxSet,
                         filter_set: FilterSet) -> None:
        inbox = await mailbox_set.get_mailbox('INBOX')
        await self._load_demo_mailbox(resource, 'INBOX', inbox)
        mbx_names = sorted(resource_listdir(resource, 'demo'))
        for name in mbx_names:
            if name == 'sieve':
                await self._load_demo_sieve(resource, name, filter_set)
            elif name != 'INBOX':
                await mailbox_set.add_mailbox(name)
                mbx = await mailbox_set.get_mailbox(name)
                await self._load_demo_mailbox(resource, name, mbx)

    async def _load_demo_sieve(self, resource: str, name: str,
                               filter_set: FilterSet) -> None:
        path = os.path.join('demo', name)
        with closing(resource_stream(resource, path)) as sieve_stream:
            sieve = sieve_stream.read()
        await filter_set.put('demo', sieve)
        await filter_set.set_active('demo')

    async def _load_demo_mailbox(self, resource: str, name: str,
                                 mbx: MailboxData) -> None:
        path = os.path.join('demo', name)
        msg_names = sorted(resource_listdir(resource, path))
        for msg_name in msg_names:
            if msg_name == '.readonly':
                mbx._readonly = True
                continue
            elif msg_name.startswith('.'):
                continue
            msg_path = os.path.join(path, msg_name)
            with closing(resource_stream(resource, msg_path)) as msg_stream:
                flags_line = msg_stream.readline()
                msg_timestamp = float(msg_stream.readline())
                msg_data = msg_stream.read()
            msg_dt = datetime.fromtimestamp(msg_timestamp, timezone.utc)
            msg_flags = {Flag(flag) for flag in flags_line.split()}
            if Recent in msg_flags:
                msg_flags.remove(Recent)
                msg_recent = True
            else:
                msg_recent = False
            append_msg = AppendMessage(msg_data, msg_dt, frozenset(msg_flags))
            await mbx.append(append_msg, recent=msg_recent)

    async def get(self) -> UserMetadata:
        data = self.login.users.get(self.name)
        if data is None:
            raise UserNotFound(self.name)
        return data

    async def set(self, data: UserMetadata) -> None:
        if self._role != 'admin' and data.role:
            raise NotAllowedError('Cannot assign role.')
        self.login.users[self.name] = data

    async def delete(self) -> None:
        try:
            del self.login.users[self.name]
        except KeyError as exc:
            raise UserNotFound(self.name) from exc
        self.config.set_cache.pop(self.name, None)
        for token_id, (name, _) in list(self.login.tokens.items()):
            if name == self.name:
                del self.login.tokens[token_id]

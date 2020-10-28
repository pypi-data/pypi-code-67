
import re
from typing import Optional, Tuple, Sequence

from .. import (ServerMechanism, ClientMechanism, UnexpectedChallenge,
                ServerChallenge, AuthenticationError, ChallengeResponse)
from ..creds import StoredSecret, AuthenticationCredentials

__all__ = ['OAuth2Mechanism']


class OAuth2Credentials(AuthenticationCredentials):
    """Simple container for the user and token received from the client by the
    ``XOAUTH2`` mechanism.

    Note:
        The token string will be contained in :attr:`.secret` so that it can be
        externally verified. However to avoid being confused with an actual
        password string, :attr:`.has_secret` will be False and
        :meth:`.check_secret` will always return False.

    """

    def __init__(self, user: str, token: str) -> None:
        super().__init__(user, token)

    @property
    def has_secret(self) -> bool:
        return False

    def check_secret(self, secret: Optional[StoredSecret], **other) -> bool:
        return False


class OAuth2Mechanism(ServerMechanism, ClientMechanism):
    """Implements the `XOAUTH2`_ authentication mechanism, used by `OAuth 2.0`_
    systems to authenticate using access tokens.

    .. _XOAUTH2: https://developers.google.com/gmail/xoauth2_protocol
    .. _OAuth 2.0: https://tools.ietf.org/html/rfc6749

    """

    _pattern = re.compile(br'^user=(.*?)\x01auth=Bearer (.*?)\x01\x01$')

    name = b'XOAUTH2'

    def server_attempt(self, responses: Sequence[ChallengeResponse]) \
            -> Tuple[OAuth2Credentials, None]:
        try:
            first = responses[0]
        except IndexError as exc:
            raise ServerChallenge(b'') from exc

        match = re.match(self._pattern, first.response)
        if not match:
            raise AuthenticationError('Invalid XOAUTH2 response')
        user, token = match.groups()

        user_str = user.decode('utf-8')
        token_str = token.decode('utf-8')
        return OAuth2Credentials(user_str, token_str), None

    def client_attempt(self, creds: AuthenticationCredentials,
                       challenges: Sequence[ServerChallenge]) \
            -> ChallengeResponse:
        if len(challenges) == 0:
            challenge = b''
        elif len(challenges) == 1:
            challenge = challenges[0].data
        else:
            raise UnexpectedChallenge()
        user = creds.authcid.encode('utf-8')
        token = creds.secret.encode('utf-8')
        response = b''.join((b'user=', user, b'\x01auth=Bearer ', token,
                             b'\x01\x01'))
        return ChallengeResponse(challenge, response)

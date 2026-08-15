import time

import praw
from prawcore import Authorizer
from prawcore import session as prawcore_session


def build_reddit_from_access_token(
    client_id: str,
    client_secret: str,
    user_agent: str,
    access_token: str,
    expires_in: int,
) -> praw.Reddit:
    """Build a praw.Reddit authorized with a token we already obtained via Authlib.

    PRAW has no public API for attaching a pre-existing access token to a
    confidential ("web app") client - reddit.auth.implicit() only works for
    installed apps without a client_secret, and reddit.auth.authorize(code)
    performs its own token exchange. This mirrors what authorize(code) does
    internally (see praw.models.auth.Auth.authorize) but skips the exchange
    since the token is already in hand.
    """
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )

    authenticator = reddit._read_only_core._authorizer._authenticator
    authorizer = Authorizer(authenticator)
    authorizer.access_token = access_token
    authorizer._expiration_timestamp = time.time() + expires_in
    authorizer.scopes = {"identity", "history"}

    authorized_session = prawcore_session(
        authorizer=authorizer, window_size=reddit.config.window_size
    )
    reddit._core = reddit._authorized_core = authorized_session
    return reddit

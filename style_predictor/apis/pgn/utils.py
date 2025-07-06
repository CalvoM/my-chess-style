import logging
import os
import time

import berserk
import requests
from chessdotcom import ChessDotComClient
from dotenv import load_dotenv

LOG = logging.getLogger(__name__)

_ = load_dotenv()
headers = {
    "User-Agent": "My Chess Style App",
    "Accept-Encoding": "gzip",
    "Accept": "application/json, text/plain, */*",
}
session = berserk.TokenSession(os.getenv("LICHESS_API_KEY", ""))
chessdotcomClient: ChessDotComClient = ChessDotComClient(
    user_agent="My Chess Style App"
)
lichessClient = berserk.Client(session=session)


def does_lichess_player_exists(username: str):
    """Checks if the `username` provided is a registered user of lichess.

    We try getting the user's details from lichess. If not successful,
    it will raise a 404 error.

    Args:
        username: username to check if registered on lichess.

    Return:
        True: if data of user is found on lichess.

    Raises:
    ResponseError: if user is not Found

    """
    _ = lichessClient.users.get_public_data(username)
    return True


def get_lichess_games(username: str) -> str:
    """Get all games of `username` from lichess platform.

    Args:
        username: Username of user to get games from lichess.

    Returns:
        string of all games.
    """
    games: list[str] = []
    games = list(lichessClient.games.export_by_player(username, as_pgn=True))
    return "\r\n".join(games)


def does_chess_dot_com_player_exists(username: str):
    """Checks if the `username` provided is a registered user of chess.com.

    We try getting the user's details from chess.com. If not successful,
    it will raise a 404 error.

    Args:
        username: username to check if registered on chess.com.

    Return:
        True: if data of user is found on chess.com.

    Raises:
    ChessDotComClientError: if user is not Found
    """
    _ = chessdotcomClient.get_player_profile(username)
    return True


def get_chess_dot_com_games(username: str) -> str:
    """Get all games of `username` from chess.com platform.

    Args:
        username: Username of user to get games from chess.com.

    Returns:
        string of all games.
    """
    all_pgns: str = ""
    response = chessdotcomClient.get_player_game_archives(username)
    archives: dict[str, list[str]] = response.json
    for archive in archives.get("archives", []):
        resp = requests.get(f"{archive}/pgn", headers=headers, timeout=60)
        if resp.status_code == 200:
            all_pgns += f"{resp.text}\n\n"
        elif resp.status_code == 429:
            LOG.warning(f"Rate limiting encountered for {archive}")
            time.sleep(45)
            resp = requests.get(f"{archive}/pgn", headers=headers, timeout=60)
            if resp.status_code == 200:
                all_pgns += f"{resp.text}\n\n"
            else:
                LOG.error(f"Failed to fetch url {archive}/pgn")
    return all_pgns

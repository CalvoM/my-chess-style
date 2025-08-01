import asyncio
import logging
import os

import aiohttp
import berserk
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
    LOG.info(f"Checking if {username} exists on Lichess")
    try:
        _ = lichessClient.users.get_public_data(username)
    except Exception as e:
        LOG.error(e)
        return False
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
    LOG.info(f"Checking if {username} exists on Chess.com")
    try:
        _ = chessdotcomClient.get_player_profile(username)
    except Exception as e:
        LOG.error(e)
        return False
    return True


async def fetch_archive(
    archive_url: str, session: aiohttp.ClientSession, semaphore: asyncio.Semaphore
):
    async with semaphore:
        while True:
            async with session.get(f"{archive_url}/pgn") as resp:
                if resp.status == 429:
                    retry_after = resp.headers.get("Retry-After")
                    if retry_after:
                        LOG.info(f"Rate limited. Retrying after {retry_after} seconds.")
                        await asyncio.sleep(int(retry_after))
                    else:
                        # Implement exponential backoff here if no Retry-After
                        await asyncio.sleep(45)  # Example fixed delay
                elif resp.status == 200:
                    return await resp.text()
                else:
                    LOG.error(f"Failed to fetch {archive_url}: {resp.status}")
                    return ""


async def get_chess_dot_com_games(username: str) -> str:
    """Get all games of `username` from chess.com platform.

    Args:
        username: Username of user to get games from chess.com.

    Returns:
        string of all games.
    """
    conn_limit = 15
    semaphore = asyncio.Semaphore(conn_limit)
    all_pgns: list[str] = []
    response = chessdotcomClient.get_player_game_archives(username)
    archives: dict[str, list[str]] = response.json
    connection = aiohttp.TCPConnector(limit=conn_limit)
    async with aiohttp.ClientSession(connector=connection) as session:
        tasks = [
            fetch_archive(archive, session, semaphore)
            for archive in archives.get("archives", [])
        ]
        all_pgns = await asyncio.gather(*tasks)
    return "\n\n".join(all_pgns)

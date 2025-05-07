import inspect
import logging
import os
import re
import time
from typing import Any

import berserk
import requests
from chessdotcom import ChessDotComClient
from dotenv import load_dotenv

from style_predictor.schemas import (
    LichessGame,
)

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


def camel_to_snake(name: str):
    # Convert camelCase or PascalCase to snake_case
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def dict_to_class(cls: type[LichessGame], data: dict[str, Any]) -> LichessGame:
    cls_fields = list(dict(inspect.getmembers(cls))["__dataclass_fields__"].keys())
    snake_data = {camel_to_snake(k): v for k, v in data.items()}
    excluded_fields = list(set(snake_data.keys()) - set(cls_fields))
    LOG.warning(f"Unsupported Lichess fields: {excluded_fields}")
    for f in excluded_fields:
        try:
            del snake_data[f]
        except KeyError:
            LOG.error(f"Key '{f}' is not found.")
    return cls(**snake_data)


def does_lichess_player_exists(username: str):
    lichessClient.users.get_public_data(username)
    return True


def get_lichess_games(username: str) -> str:
    games: list[str] = []
    games = list(lichessClient.games.export_by_player(username, as_pgn=True))
    return "\r\n".join(games)


def does_chess_dot_com_player_exists(username: str):
    chessdotcomClient.get_player_profile(username)
    return True


def get_chess_dot_com_games(username: str) -> str:
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

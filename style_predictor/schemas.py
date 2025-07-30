import datetime
from dataclasses import dataclass
from typing import Literal

from ninja import Schema

SupportedPlatforms = Literal["lichess", "chess.com"]
LichessSpeed = Literal[
    "bullet", "correspondence", "blitz", "rapid", "classical", "ultraBullet"
]
LichessPerf = Literal[
    "ultraBullet",
    "bullet",
    "blitz",
    "rapid",
    "classical",
    "correspondence",
    "chess960",
    "crazyhouse",
    "antichess",
    "atomic",
    "horde",
    "kingOfTheHill",
    "racingKings",
    "threeCheck",
]
LichessVariant = Literal[
    "standard",
    "chess960",
    "crazyhouse",
    "antichess",
    "atomic",
    "horde",
    "kingOfTheHill",
    "racingKings",
    "threeCheck",
    "fromPosition",
]

LichessGameEndStatus = Literal["outoftime", "mate", "resign"]


class FormDetails(Schema):
    usernames: str
    include_roast: bool = False


class ExternalUser(Schema):
    username: str
    platform: SupportedPlatforms = "chess.com"
    include_roast: bool = False


class MessageError(Schema):
    message: str


@dataclass
class LichessGameClock:
    initial: int
    increment: int
    totalTime: int


@dataclass
class LichessUser:
    name: str
    id: str


@dataclass
class LichessPlayer:
    rating: int
    ratingDiff: int
    user: dict[str, str]


@dataclass
class LichessGame:
    rated: bool
    variant: LichessVariant
    speed: LichessSpeed
    perf: LichessPerf
    created_at: datetime.datetime
    last_move_at: datetime.datetime
    status: Literal["outoftime", "mate", "resign"]
    source: Literal["pool", "ai"]
    moves: str
    winner: Literal["white", "black"]
    clock: LichessGameClock
    players: dict[str, LichessPlayer]


#     {
#   "id": "XQRoA4k4",
#   "rated": true,
#   "variant": "standard",
#   "speed": "bullet",
#   "perf": "bullet",
#   "createdAt": "2025-03-04T19:25:05.294Z",
#   "lastMoveAt": "2025-03-04T19:25:57.369Z",
#   "status": "outoftime",
#   "source": "pool",
#   "players": {
#     "white": {
#       "user": {
#         "name": "cherryblossombaby",
#         "id": "cherryblossombaby"
#       },
#       "rating": 743,
#       "ratingDiff": 9
#     },
#     "black": {
#       "user": {
#         "name": "d1r3ct0r",
#         "id": "d1r3ct0r"
#       },
#       "rating": 629,
#       "ratingDiff": -6
#     }
#   },
#   "fullId": "XQRoA4k4zhTn",
#   "winner": "white",
#   "moves": "d4 e6 Bf4 d5 e3 c6 Nf3 Bd6 Bg3 Nf6 Ne5 O-O Qd3",
#   "clock": {
#     "initial": 120,
#     "increment": 1,
#     "totalTime": 160
#   }
# },

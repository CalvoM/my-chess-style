__all__ = ("PGNGame",)

from style_predictor.pgn_parser.file_processing.lexer import Lexer, Token
from style_predictor.pgn_parser.file_processing.parser import Parser
from .game import PGNGame


def get_games(data: str) -> list[PGNGame] | None:
    tokens: list[Token] | None = Lexer(data).lex()
    games: list[PGNGame] | None = None
    if tokens:
        games = Parser(tokens).parse()
    return games

from style_predictor.pgn_parser.exceptions import PGNParserError
from style_predictor.pgn_parser.game import PGNGame
from style_predictor.pgn_parser.game.game import PGNMove

from .lexer import MoveToken, Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        self._tokens: list[Token] = tokens

    def parse(self) -> list[PGNGame]:
        games: list[PGNGame] = list()
        game: PGNGame = PGNGame()
        tokens = iter(self._tokens)
        while True:
            try:
                token = next(tokens)
            except StopIteration:
                break
            if token.ttype == TokenType.GAMETERM:
                games.append(game)
                game = PGNGame()
            elif token.ttype == TokenType.TAGNAME:
                tag_name = token.tvalue
                token_tvalue = next(tokens)
                if token_tvalue.ttype != TokenType.TAGVALUE:
                    raise PGNParserError(f"Invalid Tag value: {token_tvalue.ttype}")
                tag_value = token_tvalue.tvalue
                game.add_tag(tag_name, tag_value)
            elif token.ttype == TokenType.MOVENUMBER and isinstance(token, MoveToken):
                move_token = token
                while True:
                    mod_black_comment = None
                    mod_white_comment = None
                    if move_token.twhitemovecomment:
                        mod_white_comment = move_token.twhitemovecomment[1:-1]
                    if move_token.tblackmovecomment:
                        mod_black_comment = move_token.tblackmovecomment[1:-1]
                    move_obj: dict[str, str | None] = {
                        "move_number": move_token.tvalue,
                        "white_move": move_token.twhitemove,
                        "white_move_comment": mod_white_comment,
                        "black_move": move_token.tblackmove,
                        "black_move_comment": mod_black_comment,
                    }
                    game.add_move(PGNMove(move_obj))
                    move_token = next(tokens)
                    if move_token.ttype == TokenType.GAMETERM:
                        break
                games.append(game)
                game = PGNGame()

        return games

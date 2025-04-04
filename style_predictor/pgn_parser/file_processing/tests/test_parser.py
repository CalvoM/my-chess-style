from style_predictor.pgn_parser.file_processing import Lexer, Parser, Token
from style_predictor.pgn_parser.game import PGNGame

PgnFileWithMoves = """
[Event "46th URS-ch selection"]
[Site "Daugavpils URS"]
[Date "1978.07.??"]
[EventDate "?"]
[Round "9"]
[Result "1/2-1/2"]
[White "Garry Kasparov"]
[Black "Igor Vasilievich Ivanov"]
[ECO "B32"]
[WhiteElo "?"]
[BlackElo "?"]
[PlyCount "79"]

1.d4 Nf6 2.Nf3 d5 3.e3 Bf5 4.c4 c6 5.Nc3 e6 6.Bd3 Bxd3 7.Qxd3 Nbd7 8.b3 Bd6
9.O-O O-O 10.Bb2 Qe7 11.Rad1 Rad8 12.Rfe1 dxc4 13.bxc4 e5 14.dxe5 Nxe5 15.Nxe5 Bxe5
16.Qe2 Rxd1 17.Rxd1 Rd8 18.Rxd8+ Qxd8 19.Qd1 Qxd1+ 20.Nxd1 Bxb2 21.Nxb2 b5
22.f3 Kf8 23.Kf2 Ke7  1/2-1/2
"""


class TestParser:
    def test_parse(self):
        tokens: list[Token] = Lexer(PgnFileWithMoves).lex()
        games: list[PGNGame] = Parser(tokens).parse()
        assert len(games) == 1  # nosec
        assert games[0].Result == "1/2-1/2"  # nosec
        assert games[0].White == "Garry Kasparov"  # nosec

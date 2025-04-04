import pytest

from style_predictor.pgn_parser.exceptions import PGNLexerError
from style_predictor.pgn_parser.file_processing import Lexer, TokenType

PgnFileTagsOnly = """
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
"""

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

ErrPgnFile = """
[Event "46th URS-ch selection"]
[Site "Daugavpils URS"]
[Date "1978.07.??"]
[EventDate "?"]
[Round ]
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


class TestLexer:
    def test_lex_tags_only(self):
        tokens = Lexer(PgnFileTagsOnly).lex()
        if tokens:
            assert len(tokens) == 48  # nosec
            assert (
                len([token for token in tokens if token.ttype == TokenType.LSQB]) == 12
            )  # nosec
            assert (
                len([token for token in tokens if token.ttype == TokenType.MOVENUMBER])
                == 0
            )  # nosec

    def test_lex_with_moves(self):
        tokens = Lexer(PgnFileWithMoves).lex()
        if tokens:
            assert len(tokens) == 72  # nosec
            assert (
                len([token for token in tokens if token.ttype == TokenType.MOVENUMBER])
                == 23
            )  # nosec
            assert [token for token in tokens if token.ttype == TokenType.GAMETERM]  # nosec

    def test_lex_with_error(self):
        with pytest.raises(PGNLexerError) as pgn_err:
            Lexer(ErrPgnFile).lex()
        assert pgn_err.value.args[0] == "TagPair Not correctly structured"  # nosec

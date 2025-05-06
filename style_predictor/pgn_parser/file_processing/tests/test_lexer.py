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

PgnFileWithSeparatedMoves = """
[Event "Live Chess"]
[Site "Chess.com"]
[Date "2025.05.01"]
[Round "-"]
[White "Schnitzel_21"]
[Black "Mwadime-Makokha"]
[Result "0-1"]
[CurrentPosition "4kb1r/1pBb1ppp/8/1B1p4/8/2P2N2/r4nPP/n2K3R w k - 0 20"]
[Timezone "UTC"]
[ECO "B10"]
[ECOUrl "https://www.chess.com/openings/Caro-Kann-Defense"]
[UTCDate "2025.05.01"]
[UTCTime "18:55:56"]
[WhiteElo "102"]
[BlackElo "120"]
[TimeControl "60"]
[Termination "Mwadime-Makokha won on time"]
[StartTime "18:55:56"]
[EndDate "2025.05.01"]
[EndTime "18:58:00"]
[Link "https://www.chess.com/game/live/137996751542"]

1. e4 {[%clk 0:00:59.2]} 1... c6 {[%clk 0:00:59.9]} 2. Qf3 {[%clk 0:00:58.9]} 2... d5 {[%clk 0:00:58.6]} 3. Bc4 {[%clk 0:00:58.8]} 3... e6 {[%clk 0:00:56.7]} 4. exd5 {[%clk 0:00:57.9]} 4... cxd5 {[%clk 0:00:55.2]} 5. Bb3 {[%clk 0:00:56.8]} 5... Nf6 {[%clk 0:00:51.7]} 6. c4 {[%clk 0:00:55.8]} 6... Nc6 {[%clk 0:00:46.9]} 7. cxd5 {[%clk 0:00:54.8]} 7... exd5 {[%clk 0:00:45.9]} 8. Nc3 {[%clk 0:00:42.7]} 8... Be6 {[%clk 0:00:42]} 9. Nb5 {[%clk 0:00:38.4]} 9... a6 {[%clk 0:00:39.8]} 10. d4 {[%clk 0:00:31.2]} 10... axb5 {[%clk 0:00:38]} 11. Bf4 {[%clk 0:00:29.1]} 11... Ng4 {[%clk 0:00:31.1]} 12. Qh3 {[%clk 0:00:23]} 12... Nxd4 {[%clk 0:00:29.2]} 13. Qc3 {[%clk 0:00:19.7]} 13... Qc8 {[%clk 0:00:24.7]} 14. Ba4 {[%clk 0:00:12.9]} 14... Qxc3+ {[%clk 0:00:21.2]} 15. bxc3 {[%clk 0:00:10.5]} 15... Nc2+ {[%clk 0:00:20]} 16. Kd1 {[%clk 0:00:09.1]} 16... Nxa1 {[%clk 0:00:18.7]} 17. Bxb5+ {[%clk 0:00:07.7]} 17... Bd7 {[%clk 0:00:15.3]} 18. Bc7 {[%clk 0:00:03.5]} 18... Rxa2 {[%clk 0:00:09]} 19. Nf3 {[%clk 0:00:01.2]} Nxf2+ 0-1
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

    def test_lex_with_moves_separated(self):
        tokens = Lexer(PgnFileWithSeparatedMoves).lex()
        if tokens:
            assert len(tokens) == 104  # nosec
            assert (
                len([token for token in tokens if token.ttype == TokenType.MOVENUMBER])
                == 19
            )  # nosec

    def test_lex_with_error(self):
        with pytest.raises(PGNLexerError) as pgn_err:
            Lexer(ErrPgnFile).lex()
        assert pgn_err.value.args[0] == "TagPair Not correctly structured"  # nosec

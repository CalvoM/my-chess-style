import pytest

from style_predictor.pgn_parser.game import PGNGame
from style_predictor.pgn_parser.game.game import PGNMove


class TestPGNGame:
    @pytest.mark.parametrize(
        "keys,values",
        (
            (
                ("event", "white", "black", "site"),
                ("WCC", "playerOne", "playerTwo", "Kenya"),
            ),
        ),
    )
    def test_add_tags(self, keys: list[str], values: list[str]):
        game = PGNGame()
        for i in range(len(keys)):
            game.add_tag(keys[i], values[i])
        for i in range(len(keys)):
            assert game.tag_pairs[keys[i]] == values[i]  # nosec

        assert len(game.tag_pairs) == len(keys)  # nosec

    @pytest.mark.parametrize(
        "move_objects",
        (
            (
                {
                    "move_number": "1",
                    "white_move": "d4",
                    "white_move_comment": "Book Opening",
                    "black_move": "d5",
                    "black_move_comment": "Book response",
                },
                {
                    "move_number": "2",
                    "white_move": "e4",
                    "black_move": "dxe4",
                    "black_move_comment": "Attack",
                },
                {
                    "move_number": "3",
                    "white_move": "Qxe4",
                    "white_move_comment": "Queening",
                    "black_move": "Nc3",
                },
            ),
        ),
    )
    def test_add_move(self, move_objects: list[dict[str, str | None]]):
        game = PGNGame()
        for moveobject in move_objects:
            move = PGNMove(moveobject)
            game.add_move(move)
        assert game.white_moves == " ".join(
            [move["white_move"] for move in move_objects]
        )  # nosec
        assert game.black_moves == " ".join(
            [move["black_move"] for move in move_objects]
        )  # nosec
        white_comments: list[str] = list()
        for move in move_objects:
            if comment := move.get("white_move_comment", None):
                white_comments.append(comment)
            else:
                white_comments.append("~")
        assert game.white_comments == " ".join(white_comments)  # nosec

        black_comments: list[str] = list()
        for move in move_objects:
            if comment := move.get("black_move_comment", None):
                black_comments.append(comment)
            else:
                black_comments.append("~")
        assert game.black_comments == " ".join(black_comments)  # nosec
        assert len(game.moves) == len(move_objects)  # nosec

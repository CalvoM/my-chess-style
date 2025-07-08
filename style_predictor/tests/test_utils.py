import pytest

from style_predictor.utils import (
    average_rating,
    group_openings_with_eco,
    merge_game_objects,
    sort_openings,
)


class TestUtils:
    @pytest.mark.parametrize(
        "opening_data,expected",
        [
            (
                (
                    ("E1", "Opening_1", 1),
                    ("E2", "Opening_2", 2),
                    ("E3", "Opening_3", 3),
                    ("E1", "Opening_1", 4),
                ),
                {
                    "Opening_1": {"total": 5, "eco_codes": ["E1"]},
                    "Opening_2": {"total": 2, "eco_codes": ["E2"]},
                    "Opening_3": {"total": 3, "eco_codes": ["E3"]},
                },
            ),
            ((), {}),
            (
                (
                    ("E1", "Opening_1", 1),
                    ("E2", "Opening_2", 2),
                    ("E3", "Opening_3", 3),
                    ("E5", "Opening_1", 4),
                ),
                {
                    "Opening_1": {"total": 5, "eco_codes": ["E1", "E5"]},
                    "Opening_2": {"total": 2, "eco_codes": ["E2"]},
                    "Opening_3": {"total": 3, "eco_codes": ["E3"]},
                },
            ),
            (
                (
                    ("E1", "Opening_1", 1),
                    ("E1", "Opening_2", 2),
                ),
                {
                    "Opening_1": {"total": 1, "eco_codes": ["E1"]},
                    "Opening_2": {"total": 2, "eco_codes": ["E1"]},
                },
            ),
        ],
    )
    def test_group_openings_with_eco(self, opening_data, expected):
        assert group_openings_with_eco(opening_data) == expected  # nosec

    @pytest.mark.parametrize(
        "openings,expected",
        [
            (
                {
                    "Opening_1": {"total": 5, "eco_codes": ["E1", "E5"]},
                    "Opening_2": {"total": 2, "eco_codes": ["E2"]},
                    "Opening_3": {"total": 3, "eco_codes": ["E3"]},
                },
                [
                    ("Opening_1", {"total": 5, "eco_codes": ["E1", "E5"]}),
                    ("Opening_3", {"total": 3, "eco_codes": ["E3"]}),
                    ("Opening_2", {"total": 2, "eco_codes": ["E2"]}),
                ],
            ),
            (
                {
                    "Opening_1": {"total": 5, "eco_codes": ["E1", "E5"]},
                    "Opening_2": {"total": 2, "eco_codes": ["E2"]},
                    "Opening_3": {"total": 3, "eco_codes": ["E3"]},
                },
                [
                    ("Opening_1", {"total": 5, "eco_codes": ["E1", "E5"]}),
                    ("Opening_3", {"total": 3, "eco_codes": ["E3"]}),
                    ("Opening_2", {"total": 2, "eco_codes": ["E2"]}),
                ],
            ),
            ({}, []),
            (
                {
                    "Opening_1": {"total": 2, "eco_codes": ["E1"]},
                    "Opening_2": {"total": 1, "eco_codes": ["E2"]},
                },
                [
                    ("Opening_1", {"total": 2, "eco_codes": ["E1"]}),
                    ("Opening_2", {"total": 1, "eco_codes": ["E2"]}),
                ],
            ),
            (
                {
                    "Opening_1": {"total": 3, "eco_codes": ["E1"]},
                    "Opening_2": {"total": 3, "eco_codes": ["E2"]},
                    "Opening_3": {"total": 2, "eco_codes": ["E3"]},
                },
                [
                    ("Opening_1", {"total": 3, "eco_codes": ["E1"]}),
                    ("Opening_2", {"total": 3, "eco_codes": ["E2"]}),
                    ("Opening_3", {"total": 2, "eco_codes": ["E3"]}),
                ],
            ),
            (
                {
                    "Opening_A": {"total": 10, "eco_codes": ["A"]},
                    "Opening_B": {"total": 8, "eco_codes": ["B"]},
                    "Opening_C": {"total": 15, "eco_codes": ["C"]},
                    "Opening_D": {"total": 5, "eco_codes": ["D"]},
                    "Opening_E": {"total": 12, "eco_codes": ["E"]},
                    "Opening_F": {"total": 7, "eco_codes": ["F"]},
                    "Opening_G": {"total": 9, "eco_codes": ["G"]},
                },
                [
                    ("Opening_C", {"total": 15, "eco_codes": ["C"]}),
                    ("Opening_E", {"total": 12, "eco_codes": ["E"]}),
                    ("Opening_A", {"total": 10, "eco_codes": ["A"]}),
                    ("Opening_G", {"total": 9, "eco_codes": ["G"]}),
                    ("Opening_B", {"total": 8, "eco_codes": ["B"]}),
                ],
            ),
        ],
    )
    def test_sort_openings(self, openings, expected):
        assert sort_openings(openings) == expected  # nosec

    @pytest.mark.parametrize(
        "game_rating,expected",
        [
            (
                {"hyper": (10, 2), "bullet": (15, 2), "classical": (20, 2)},
                {"hyper": 5.0, "bullet": 7.5, "classical": 10.0},
            ),
            (
                {"hyper": (10, 0), "bullet": (0, 0), "classical": (20, 2)},
                {"hyper": 0, "bullet": 0, "classical": 10.0},
            ),
            ({}, {}),
            (
                {"hyper": 5},
                {"hyper": 0},
            ),
            (
                {"hyper": (10,)},
                {"hyper": 0},
            ),
            # Tuple with incorrect length (3 elements)
            (
                {"hyper": (10, 2, 3)},
                {"hyper": 0},
            ),
            # Negative values
            (
                {"hyper": (-10, 2)},
                {"hyper": 0.0},
            ),
            (
                {"hyper": (10, -2)},
                {"hyper": 0},
            ),
            (
                {"hyper": (-10, -2)},
                {"hyper": 0},
            ),
        ],
    )
    def test_average_rating(self, game_rating, expected):
        assert average_rating(game_rating) == expected  # nosec

    @pytest.mark.parametrize(
        "game_objects,expected",
        [
            (
                [
                    {"count": 1, "wins": 2, "losses": 3},
                    {"count": 2, "wins": 4, "losses": 6},
                ],
                {"count": 3, "wins": 6, "losses": 9},
            ),
            (
                [
                    {"count": 1, "wins": 2},
                    {
                        "count": 1,
                        "losses": 3,
                    },
                ],
                {"count": 2, "wins": 2, "losses": 3},
            ),
            # Test with extra keys in some objects
            (
                [
                    {"count": 1, "wins": 2, "losses": 3, "draws": 1},
                    {"draws": 1, "wins": 2, "losses": 3},
                ],
                {"count": 1, "wins": 4, "losses": 6, "draws": 2},
            ),
            # Test with all objects missing all keys (empty dicts)
            (
                [{}, {}, {}],
                {},
            ),
        ],
    )
    def test_merge_game_objects(self, game_objects, expected):
        res = game_objects[0]
        res = merge_game_objects(res, game_objects[1])
        assert res == expected  # nosec

    @pytest.mark.parametrize(
        "game_objects,expected",
        [
            (
                [
                    {
                        "opponents_avg_rating": {
                            "bullet": [941.0, 1],
                            "blitz": [201.0, 1],
                            "rapid": [401.0, 98],
                            "classical": [0.0, 0],
                        },
                        "openings": [
                            ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                            ["B01", "Scandinavian Defense", 8],
                            [
                                "C20",
                                "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                                6,
                            ],
                            ["B20", "Sicilian Defense", 5],
                            ["C20", "King's Pawn Game: Napoleon Attack", 4],
                        ],
                    },
                    {
                        "opponents_avg_rating": {
                            "bullet": [500.0, 4],
                            "blitz": [201.0, 1],
                            "rapid": [401.0, 98],
                            "classical": [0.0, 0],
                        },
                        "openings": [
                            ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                            ["B01", "Scandinavian Defense", 8],
                            [
                                "C20",
                                "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                                6,
                            ],
                            ["B20", "Sicilian Defense", 5],
                            ["C20", "King's Pawn Game: Napoleon Attack", 4],
                        ],
                    },
                ],
                {
                    "opponents_avg_rating": {
                        "bullet": (2941.0, 5),
                        "blitz": (402.0, 2),
                        "rapid": (39699.0, 196),
                        "classical": (0.0, 0),
                    },
                    "openings": [
                        ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                        ["B01", "Scandinavian Defense", 8],
                        [
                            "C20",
                            "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                            6,
                        ],
                        ["B20", "Sicilian Defense", 5],
                        ["C20", "King's Pawn Game: Napoleon Attack", 4],
                        ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                        ["B01", "Scandinavian Defense", 8],
                        [
                            "C20",
                            "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                            6,
                        ],
                        ["B20", "Sicilian Defense", 5],
                        ["C20", "King's Pawn Game: Napoleon Attack", 4],
                    ],
                },
            ),
            (
                [
                    {
                        "opponents_avg_rating": {
                            "bullet": [941.0, 1],
                            "blitz": [201.0, 1],
                            "rapid": [401.1, 98],
                            "classical": [0.0, 0],
                        },
                        "openings": [
                            ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                            ["B01", "Scandinavian Defense", 8],
                            [
                                "C20",
                                "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                                6,
                            ],
                            ["B20", "Sicilian Defense", 5],
                            ["C20", "King's Pawn Game: Napoleon Attack", 4],
                        ],
                    },
                    {
                        "opponents_avg_rating": {
                            "bullet": [941.0, 1],
                            "blitz": [201.0, 1],
                            "rapid": [401.1, 98],
                            "classical": [0.0, 0],
                        },
                        "openings": [
                            ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                            ["B01", "Scandinavian Defense", 8],
                            [
                                "C20",
                                "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                                6,
                            ],
                            ["B20", "Sicilian Defense", 5],
                            ["C20", "King's Pawn Game: Napoleon Attack", 4],
                        ],
                    },
                ],
                {
                    "opponents_avg_rating": {
                        "bullet": (1882.0, 2),
                        "blitz": (402.0, 2),
                        "rapid": (39708.9, 196),
                        "classical": (0.0, 0),
                    },
                    "openings": [
                        ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                        ["B01", "Scandinavian Defense", 8],
                        [
                            "C20",
                            "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                            6,
                        ],
                        ["B20", "Sicilian Defense", 5],
                        ["C20", "King's Pawn Game: Napoleon Attack", 4],
                        ["C20", "King's Pawn Game: Wayward Queen Attack", 23],
                        ["B01", "Scandinavian Defense", 8],
                        [
                            "C20",
                            "King's Pawn Game: Wayward Queen Attack, Kiddie Countergambit",
                            6,
                        ],
                        ["B20", "Sicilian Defense", 5],
                        ["C20", "King's Pawn Game: Napoleon Attack", 4],
                    ],
                },
            ),
        ],
    )
    def test_nested_merge_game_objects(self, game_objects, expected):
        res = game_objects[0]
        res = merge_game_objects(res, game_objects[1])
        assert res == expected  # nosec

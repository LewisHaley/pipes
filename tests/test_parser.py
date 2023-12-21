"""Tests for parser.py."""

from pipes_game import parser
from pipes_game.grid import UNSET

# pylint: disable=missing-function-docstring


def test_parse_from_lines__parses_lines_of_text_into_a_grid():
    lines = [
        "A A",
        "B B",
        "C C",
    ]
    grid = parser.parse_from_lines(lines)

    assert grid.num_cols == 3
    assert grid.num_rows == 3
    assert grid.array == [
        ["A", UNSET, "A"],
        ["B", UNSET, "B"],
        ["C", UNSET, "C"],
    ]
    assert grid.pipe_labels == {"A", "B", "C"}


def test_parse_from_file__parses_a_text_file_into_a_grid(tmp_path):
    the_file = tmp_path / "the_file.txt"
    the_file.write_text(
        "\n".join(
            [
                "A A",
                "B B",
                "C C",
            ]
        )
    )
    grid = parser.parse_from_file(the_file)

    assert grid.num_cols == 3
    assert grid.num_rows == 3
    assert grid.array == [
        ["A", UNSET, "A"],
        ["B", UNSET, "B"],
        ["C", UNSET, "C"],
    ]
    assert grid.pipe_labels == {"A", "B", "C"}

"""Tests for drawer.py."""

import pytest

from pipes_game import drawer
from pipes_game.grid import Point

# pylint: disable=missing-function-docstring, too-many-arguments


@pytest.mark.parametrize(
    ["text_size", "frame_position", "cell_width", "cell_height", "expected_origin"],
    [
        ((0, 0), Point(0, 0), 100, 100, (50, 50)),
        ((10, 10), Point(0, 0), 100, 100, (45, 55)),
        ((10, 10), Point(10, 10), 100, 100, (55, 65)),
        ((10, 10), Point(10, 10), 50, 50, (30, 40)),
    ],
)
def test_get_text_origin_for_cell(
    mocker, text_size, frame_position, cell_width, cell_height, expected_origin
):
    mocker.patch("cv2.getTextSize", return_value=(text_size, None))
    actual = drawer.get_text_origin_for_cell(
        "doesn't matter",
        {"doesn't": "matter"},
        frame_position,
        cell_width,
        cell_height,
    )
    assert actual == expected_origin

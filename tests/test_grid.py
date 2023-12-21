"""Tests for grid.py."""

import pytest

from pipes_game import grid
from pipes_game.grid import PipesGrid, UNSET

# pylint: disable=missing-class-docstring, missing-function-docstring


@pytest.fixture(name="test_grid")
def _test_grid() -> PipesGrid:
    """Return a simple test pipes grid.

    :returns the test grid
    """
    array = [
        ["A", UNSET, "A"],
        ["B", UNSET, "B"],
        ["C", UNSET, "C"],
    ]
    grid_ = grid.PipesGrid(
        num_cols=3,
        num_rows=3,
        array=array,
        pipe_labels={"A", "B", "C"},
    )
    return grid_


class TestGetCell:
    @pytest.mark.parametrize(
        ["position", "expected_value"],
        [
            (grid.Point(0, 0), "A"),
            (grid.Point(1, 0), UNSET),
            (grid.Point(0, 1), "B"),
            (grid.Point(0, 2), "C"),
        ],
    )
    def test_returns_the_value(self, test_grid, position, expected_value):
        value = test_grid.get_cell(position)
        assert value == expected_value

    @pytest.mark.parametrize(
        ["position"],
        [
            (grid.Point(-1, 0),),
            (grid.Point(0, -1),),
            (grid.Point(3, 0),),
            (grid.Point(0, 3),),
        ],
    )
    def test_raises_value_error_due_to_out_of_bounds(self, test_grid, position):
        with pytest.raises(
            ValueError,
            match=r"Position is out-of-bounds of the grid",
        ):
            test_grid.get_cell(position)

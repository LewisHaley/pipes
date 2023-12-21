"""Tests for grid.py."""

import re

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


def test_iterate_yields_each_point_and_value():
    array = [
        ["A", UNSET, UNSET, "A"],
        ["B", UNSET, UNSET, "B"],
    ]
    test_grid = grid.PipesGrid(
        num_cols=4,
        num_rows=2,
        array=array,
        pipe_labels={"A", "B"},
    )
    elems = list(test_grid)
    expected_elems = [
        (grid.Point(0, 0), "A"),
        (grid.Point(1, 0), UNSET),
        (grid.Point(2, 0), UNSET),
        (grid.Point(3, 0), "A"),
        (grid.Point(0, 1), "B"),
        (grid.Point(1, 1), UNSET),
        (grid.Point(2, 1), UNSET),
        (grid.Point(3, 1), "B"),
    ]
    assert elems == expected_elems


class TestPipeEndpoints:
    def test_pipe_endpoints_are_initialised_on_creation(self, test_grid):
        expected = {
            "A": {
                "start": grid.Point(0, 0),
                "end": grid.Point(2, 0),
            },
            "B": {
                "start": grid.Point(0, 1),
                "end": grid.Point(2, 1),
            },
            "C": {
                "start": grid.Point(0, 2),
                "end": grid.Point(2, 2),
            },
        }
        assert test_grid.pipe_endpoints == expected

    def test_value_error_raised_if_only_one_endpoint_found(self):
        array = [["A"]]

        with pytest.raises(
            ValueError,
            match=r"Only found 1 endpoint for pipe 'A'",
        ):
            grid.PipesGrid(
                num_cols=1,
                num_rows=1,
                array=array,
                pipe_labels={"A"},
            )

    def test_value_error_raised_if_more_than_two_endpoints_found(self):
        array = [["A", "A", "A"]]

        with pytest.raises(
            ValueError,
            match=r"Found more than 2 endpoints for pipe 'A'",
        ):
            grid.PipesGrid(
                num_cols=3,
                num_rows=1,
                array=array,
                pipe_labels={"A"},
            )

    def test_pipe_is_complete_if_endpoints_are_immediately_adjacent(self):
        array = [
            ["A", "A", "B", "B"],
            ["C", UNSET, UNSET, "C"],
        ]
        test_grid = grid.PipesGrid(
            num_cols=4,
            num_rows=2,
            array=array,
            pipe_labels={"A", "B", "C"},
        )
        assert test_grid.is_pipe_complete("A")
        assert test_grid.is_pipe_complete("B")
        assert not test_grid.is_pipe_complete("C")


class TestSetCell:
    def test_cell_is_set_and_endpoint_updated(self):
        array = [["A", UNSET, "A"]]
        test_grid = grid.PipesGrid(
            num_cols=3,
            num_rows=1,
            array=array,
            pipe_labels={"A"},
        )
        # Check the initial endpoints to demonstrate the update
        assert test_grid.pipe_endpoints == {
            "A": {
                "start": grid.Point(0, 0),
                "end": grid.Point(2, 0),
            },
        }

        test_grid.set_cell(grid.Point(1, 0), "A")
        assert test_grid.array == [["A", "A", "A"]]
        assert test_grid.pipe_endpoints == {
            "A": {
                "start": grid.Point(1, 0),  # this was updated
                "end": grid.Point(2, 0),
            },
        }

    def test_value_error_is_raised_if_out_of_bounds(self, test_grid):
        with pytest.raises(
            ValueError,
            match=r"Position is out-of-bounds of the grid",
        ):
            test_grid.set_cell(grid.Point(100, 100), "A")

    def test_value_error_is_raised_if_invalid_pipe_label(self, test_grid):
        with pytest.raises(
            ValueError,
            match=r"'D' is not a known pipe label",
        ):
            test_grid.set_cell(grid.Point(1, 0), "D")

    def test_runtime_error_is_raised_if_cell_already_has_value(self, test_grid):
        with pytest.raises(
            RuntimeError,
            match=r"Position Point\(x=0, y=0\) already has a value A",
        ):
            test_grid.set_cell(grid.Point(0, 0), "B")

    @pytest.mark.parametrize(
        ["array", "num_cols", "num_rows", "position"],
        [
            (
                [["A", UNSET, UNSET, UNSET, "A"]],
                5,
                1,
                grid.Point(2, 0),
            ),
            (
                [["A"], [UNSET], [UNSET], [UNSET], ["A"]],
                1,
                5,
                grid.Point(0, 2),
            ),
        ],
    )
    def test_runtime_error_is_raised_if_not_neighbor(
        self, array, num_cols, num_rows, position
    ):
        test_grid = grid.PipesGrid(
            num_cols=num_cols,
            num_rows=num_rows,
            array=array,
            pipe_labels={"A"},
        )

        with pytest.raises(
            RuntimeError,
            match=re.escape(f"{position} is not a neighbor of A's endpoint"),
        ):
            test_grid.set_cell(position, "A")

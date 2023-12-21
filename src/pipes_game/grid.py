"""Define the pipe grid storage."""

import dataclasses
from typing import Generator, List, Optional, Set, Tuple

UNSET = "unset"


@dataclasses.dataclass(order=True)
class Point:
    """A point in 2D space.

    :param x: the x position
    :param y: the y position
    """

    x: int
    y: int

    def is_neighbor(self, other: "Point") -> bool:
        """Check if another point neighbors this one.

        :param other: the other point

        :returns: True if the points are neighbors, else False
        """
        adjacent_x_and_same_y = abs(self.x - other.x) == 1 and self.y == other.y
        adjacent_y_and_same_x = abs(self.y - other.y) == 1 and self.x == other.x
        return adjacent_x_and_same_y or adjacent_y_and_same_x


class PipesGrid:
    """Container class for the pipe grid array data."""

    def __init__(
        self,
        num_cols: int,
        num_rows: int,
        array: List[List[Optional[str]]],
        pipe_labels: Set[str],
    ):
        """Create a new instance of `PipesGrid`.

        :param num_cols: the number of columns in the grid
        :param num_rows: the number of rows in the grid
        :param array: the pipe grid array data
        :param pipe_labels: the set of pipe labels which can be found within the `array`
        """
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.array = array
        self.pipe_labels = pipe_labels

        self.pipe_endpoints = {}
        self._init_pipe_endpoints()

    def _init_pipe_endpoints(self) -> None:
        """Initialise the endpoints of the pipes in the grid.

        :raises ValueError: if not exactly 2 endpoints are found for any given pipe
        """
        for point, value in self:
            if value == UNSET:
                continue

            if value not in self.pipe_endpoints:
                self.pipe_endpoints[value] = {
                    "start": point,
                }
            elif "end" not in self.pipe_endpoints[value]:
                self.pipe_endpoints[value]["end"] = point
            else:
                raise ValueError(f"Found more than 2 endpoints for pipe {value!r}")

        for pipe, endpoints in self.pipe_endpoints.items():
            # We must have found "start" for it to be present at all
            if "end" not in endpoints:
                raise ValueError(f"Only found 1 endpoint for pipe {pipe!r}")

    def is_pipe_complete(self, pipe_label: str) -> bool:
        """Check whether the 2 endpoints of a pipe are joined together.

        :param pipe_label: the pipe to check

        :returns: True if the pipe is complete
        """
        start = self.pipe_endpoints[pipe_label]["start"]
        end = self.pipe_endpoints[pipe_label]["end"]
        return start.is_neighbor(end)

    def is_complete(self) -> bool:
        """Check whether the whole grid is complete.

        :returns: True if the whole grid is complete (all pipe endpoints are joined)
        """
        return all(self.is_pipe_complete(pipe_label) for pipe_label in self.pipe_labels)

    def get_cell(self, position: Point) -> str:
        """Get the value in a cell.

        :param position: the position in the grid to fill

        :returns: the value in the cell

        :raises ValueError: if `position` is out-of-bounds of the grid
        """
        if not self.is_position_in_bounds(position):
            raise ValueError("Position is out-of-bounds of the grid")

        return self.array[position.y][position.x]

    def set_cell(self, position: Point, value: str):
        """Set the value for a cell.

        :param position: the position in the grid to fill
        :param value: the value to will the cell with. Must be one of the grids known
            `pipe_labels`.

        :raises ValueError: if `position` is out-of-bounds of the grid
        :raises ValueError: if `value` is not a known pipe label
        :raises RuntimeError: if the cell in `position` already has a set value
        :raises RuntimeError: if `position` is not a neighbour of one of `value`s
            pipeline endpoints
        """
        if not self.is_position_in_bounds(position):
            raise ValueError("Position is out-of-bounds of the grid")

        if value not in self.pipe_labels:
            raise ValueError(f"{value!r} is not a known pipe label")

        if (existing := self.array[position.y][position.x]) != UNSET:
            raise RuntimeError(f"Position {position} already has a value {existing}")

        # Check if the position is a neighbor of an endpoint
        if position.is_neighbor(self.pipe_endpoints[value]["start"]):
            self.pipe_endpoints[value]["start"] = position
        elif position.is_neighbor(self.pipe_endpoints[value]["end"]):
            self.pipe_endpoints[value]["end"] = position
        else:
            raise RuntimeError(f"{position} is not a neighbor of {value}'s endpoint")

        self.array[position.y][position.x] = value

    def is_position_in_bounds(self, position: Point) -> bool:
        """Check whether a point is in-bounds of the array.

        :param position: the position to check

        :returns: True if in-bounds, else False
        """
        return 0 <= position.x < self.num_cols and 0 <= position.y < self.num_rows

    def __iter__(self) -> Generator[Tuple[Point, Optional[str]], None, None]:
        """Iterate through each element in the grid, yielding is position and value.

        :returns: a generator for each cell
        """
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                yield Point(x, y), self.array[y][x]

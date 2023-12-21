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

    def get_cell(self, position: Point) -> str:
        """Get the value in a cell.

        :param position: the position in the grid to fill

        :returns: the value in the cell

        :raises ValueError: if `position` is out-of-bounds of the grid
        """
        if not self._is_position_in_bounds(position):
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
        """
        if not self._is_position_in_bounds(position):
            raise ValueError("Position is out-of-bounds of the grid")

        if value not in self.pipe_labels:
            raise ValueError(f"{value!r} is not a known pipe label")

        if existing := self.array[position.y][position.x] != UNSET:
            raise RuntimeError(f"Position {position} already has a value {existing}")

        self.array[position.y][position.x] = value

    def _is_position_in_bounds(self, position: Point) -> bool:
        """Check whether a point is in-bounds of the array.

        :returns: True if in-bounds, else False
        """
        return 0 <= position.x < self.num_rows and 0 <= position.y < self.num_cols

    def __iter__(self) -> Generator[Tuple[Point, Optional[str]], None, None]:
        """Iterate through each element in the grid, yielding is position and value.

        :returns: a generator for each cell
        """
        for y in range(self.num_rows):
            for x in range(self.num_cols):
                yield Point(x, y), self.array[y][x]

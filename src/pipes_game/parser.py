"""Parse pipes input file."""

from pathlib import Path
from typing import List

from .grid import PipesGrid, UNSET


def parse_from_file(filepath: Path) -> PipesGrid:
    """Parse a pipes grid from the contents of a file.

    :param filepath: the path to the file containing the pipes grid spec

    :returns: the parsed pipe grid

    :raises ValueError: if the file does not contain a valid grid
    """
    lines = filepath.read_text().splitlines()
    try:
        grid = parse_from_lines(lines)
    except ValueError as e:
        raise ValueError("File does not contain a valid grid") from e
    return grid


def parse_from_lines(lines: List[str]) -> PipesGrid:
    """Parse a pipes grid from lines of text.

    :param lines: the lines of test containing the pipes grid spec

    :returns: the parsed pipe grid

    :raises ValueError: if the input lines do not define a valid grid
    """
    array = [[UNSET if val == " " else val for val in line] for line in lines]
    if len(set(len(row) for row in array)) != 1:
        raise ValueError("Not all rows in grid are of equal length")

    num_cols = len(array[0])
    num_rows = len(array)
    pipe_labels = set(val for row in array for val in row if val is not UNSET)

    grid = PipesGrid(
        num_cols=num_cols,
        num_rows=num_rows,
        array=array,
        pipe_labels=pipe_labels,
    )
    return grid

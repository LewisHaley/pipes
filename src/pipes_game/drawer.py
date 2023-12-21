"""Logic for converting a grid into an image array."""

import colorsys
from typing import Mapping, Set, Tuple

import cv2
import numpy

from .grid import PipesGrid, Point, UNSET


def grid_to_frame(grid: PipesGrid, width: int, height: int) -> numpy.array:
    """Create a frame from a pipes grid.

    :param grid: the pipes grid to draw
    :param width: the width of the frame to draw
    :param height: the height of the frame to draw

    :returns: the frame
    """
    margin = 10
    cell_width = (width - margin - margin) // grid.num_cols
    cell_height = (height - margin - margin) // grid.num_rows

    frame = numpy.zeros((height, width, 3), dtype=numpy.uint8)

    for x in range(margin, width, cell_width):
        frame = cv2.line(
            frame,
            (x, margin),
            (x, height - margin),
            color=(200, 200, 200),
            thickness=3,
        )

    for y in range(margin, height, cell_height):
        frame = cv2.line(
            frame,
            (margin, y),
            (width - margin, y),
            color=(200, 200, 200),
            thickness=3,
        )

    font_scale = min(cell_width, cell_height) / 40

    font_options = {
        "fontFace": cv2.FONT_HERSHEY_SIMPLEX,
        "fontScale": font_scale,
        "thickness": int(font_scale + 1),
    }
    color_map_for_labels = get_color_map_for_labels(grid.pipe_labels)
    _paint_cells(
        frame,
        grid,
        cell_width,
        cell_height,
        margin,
        font_options,
        color_map_for_labels,
    )
    return frame


def _paint_cells(  # pylint: disable=too-many-arguments
    frame: numpy.array,
    grid: PipesGrid,
    cell_width: int,
    cell_height: int,
    margin: int,
    font_options: dict,
    color_map_for_labels: dict,
) -> numpy.array:
    """Paint cells from a grid on to a frame."""
    for position, value in grid:
        if value == UNSET:
            continue

        frame_position = to_frame_space(position, cell_width, cell_height, margin)
        text_origin = get_text_origin_for_cell(
            value, font_options, frame_position, cell_width, cell_height
        )

        frame = cv2.rectangle(
            frame,
            (frame_position.x + 5, frame_position.y + 5),
            (frame_position.x + cell_width - 5, frame_position.y + cell_height - 5),
            color=color_map_for_labels[value],
            thickness=-1,
        )

        frame = cv2.putText(
            frame,
            value,
            org=text_origin,
            color=(0, 0, 0),
            bottomLeftOrigin=False,
            **font_options,
        )

    return frame


def to_frame_space(position: Point, width: int, height: int, margin: int) -> Point:
    """Convert a Point to frame space.

    :param position: the position to convert
    :param width: the width in pixels of a single grid cell
    :param height: the height in pixels of a single grid cell
    :param margin: the margin in pixels between the edge of the frame and the grid

    :returns: the converted point
    """
    return Point((position.x * width) + margin, (position.y * height) + margin)


def get_color_map_for_labels(labels: Set[str]) -> Mapping[str, str]:
    """Calculate a map of unique RBG colors for the set of input labels.

    :param labels: the set of labels

    :returns: the map of label to colors
    """
    num_labels = len(labels)
    hues = iter(range(0, 101, 100 // num_labels))
    color_map = {}
    for label in sorted(labels):
        hue = next(hues)
        color = tuple(map(lambda x: x * 255, colorsys.hsv_to_rgb(hue / 100, 1, 1)))
        color_map[label] = color
    return color_map


def get_text_origin_for_cell(
    text: str,
    font_options: dict,
    frame_position: Point,
    cell_width: int,
    cell_height: int,
) -> Tuple[int, int]:
    """Get the origin for centered text within a grid cell.

    :param text: the text that will be draw
    :param font_options: options to pass to `cv2.getTextSize`
    :param frame_position: the cell origin position in the frame
    :param cell_width: the width in pixels of a single grid cell
    :param cell_height: the height in pixels of a single grid cell

    :returns: a tuple of x- and y-coordinate for the origin of where text should be draw
        in order for it to be centered within a cell
    """
    (text_width, text_height), _ = cv2.getTextSize(text, **font_options)
    text_x = frame_position.x + (cell_width - text_width) // 2
    text_y = frame_position.y + (cell_height + text_height) // 2
    return text_x, text_y

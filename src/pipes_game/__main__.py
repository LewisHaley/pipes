"""CLI entry point."""

import argparse
import pathlib

from . import display, drawer, parser


def parse_args() -> argparse.Namespace:
    """Parse the command-line arguments.

    :returns: the parsed arguments
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "grid_file",
        metavar="FILE",
        type=pathlib.Path,
        help="Path to the grid file to solve",
    )
    arg_parser.add_argument(
        "--width",
        default=500,
        type=int,
        help="Default width of app in pixels",
    )
    arg_parser.add_argument(
        "--height",
        default=500,
        type=int,
        help="Default height of app in pixels",
    )
    return arg_parser.parse_args()


def main() -> None:
    """Run the CLI."""
    args = parse_args()

    display_ = display.Display((args.width, args.height), "Pipes")

    game_grid = parser.parse_from_file(args.grid_file)
    frame = drawer.grid_to_frame(game_grid, args.width, args.height)
    display_.update(frame)
    display_.start()


if __name__ == "__main__":
    main()

"""CLI entry point."""

import argparse
import pathlib

from . import display, drawer, parser, solver
from .gobject import GLib


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

    def update() -> bool:
        """Update the game grid and display.

        :returns: True while the game grid is unsolved, thus meaning that the callback
            is called against to iterate the solve
        """
        solver.iter_solve(game_grid)
        frame = drawer.grid_to_frame(game_grid, args.width, args.height)
        display_.update(frame)
        if complete := game_grid.is_complete():
            print("Game is fully solved!")
        return not complete

    GLib.timeout_add_seconds(2, update)

    display_.start()


if __name__ == "__main__":
    main()

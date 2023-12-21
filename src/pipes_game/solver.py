"""Code for solving a game grid."""

from .grid import PipesGrid, UNSET


def iter_solve(game_grid: PipesGrid) -> None:
    """Modify the game grid state with one additional solve modification.

    :param game_grid: the game grid
    """
    for pipe, endpoints in game_grid.pipe_endpoints.items():
        if game_grid.is_pipe_complete(pipe):
            continue

        for ep in (endpoints["start"], endpoints["end"]):
            unset_neighbors = [
                n
                for n in ep.get_neighbors()
                if (
                    game_grid.is_position_in_bounds(n)
                    and game_grid.get_cell(n) == UNSET
                )
            ]
            if len(unset_neighbors) == 1:
                game_grid.set_cell(unset_neighbors[0], pipe)
                return

    raise RuntimeError("Could find a solve!")

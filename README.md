Pipes Game
==========

This is a solver for games where you have to join the ends of 2 pipes in a 2D grid,
without any pipe occupying the same grid cell.

## Development

CI targets are specified in the Makefile.
Production and development depencies are installed into a virtual environment. The
virtual environment is created using a requirements file generated by pip-tools. The
pip-tools version and other dependencies are installed into a `bootstrap` virtual
environment which is separate to the main virtual environment.

`make check` will run all CI targets. See the Makefile for the separate targets.

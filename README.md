<img src="images/logo.png" alt="Bulldog Logo" width="200"></img>

# PyDis Code Jam Summer 21: Beatific Bulldogs

This is the Beatific Bulldogs' submission to the Python Discord Code Jam of Summer 2021.

A snake game playable in the terminal.

Includes offline mode and online mode (you can host your own game). The game is controlled using arrows.

To play online you can either join a server or you can host one yourself. To join a server select the `Connect to server` option or to host one select `Host A Server`.

## Installation

 1. [Install Python](https://python.org/downloads)

    You will need Python 3.9+ (3.x where x >= 9).

 2. [Install Poetry](https://python-poetry.org/docs/master/#installation)

    Installation instructions are available at the above link.

 3. Enter the Poetry shell

    ```shell
    $ poetry shell
    ```

 4. Install development dependencies

    ```shell
    $ poetry install
    ```

 5. Install pre-commit hooks

    ```shell
    $ pre-commit install
    ```

## Usage

 - Run the client

   ```shell
   $ poe main
   ```

 - Automatically order imports

   ```shell
   $ poe fix
   ```

 - Lint the code

   ```shell
   $ poe lint
   ```

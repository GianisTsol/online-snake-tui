"""Entrypoint for the server."""
import logging
import socket
import threading
import time
from threading import Thread
from typing import Any

import msgpack

from common import logic, models

SERVER_NAME = 'SnekBox'
GAME_VERSION = 0
BOX_WIDTH = 128
BOX_HEIGHT = 32
BOX_TICKRATE = 15
MAX_PLAYERS = 5

logger = logging.getLogger('snake.server')
logging.basicConfig(level=logging.INFO)


class Player(Thread):
    """Class for each client."""

    def __init__(
            self,
            conn: socket.socket,
            addr: tuple[str, int],
            model: models.Player):
        """Set up the client."""
        super().__init__()
        self.segments = []
        for _ in range(0, logic.STARTING_SNAKE_SEGMENTS):
            logic.add_segment(self.segments)
        self.player_model = model
        self.terminate_flag = threading.Event()
        self.conn = conn
        self.addr = addr    # Host, port.
        self.score = 0

    def send(self, data: dict):
        """Pack and send data to the player."""
        s = msgpack.pack(data, use_bin_type=True)  # pack the data
        self.conn.send(s)

    def handler(self, data: dict[str, Any]):
        """Handle different types of events from client."""
        if 'nick' in data:
            self.player_model.name = data['nick']
        elif 'event' in data:
            pass
            # event = data['event']
            # TODO: Allow the player to move.

    def stop(self):
        """Stop thread."""
        self.terminate_flag.set()

    def run(self):
        """Listen for events."""
        # Iterating an Unpacker waits for and yields each complete msgpack
        # object.
        reader = iter(msgpack.Unpacker(self.sock, raw=False))
        while not self.terminate_flag.is_set():
            try:
                self.handler(next(reader))
            except socket.timeout:
                pass  # ignore socket timeouts, the connection shouldnt stop


class Game(Thread):
    """Game or match filled with players."""

    def __init__(self):
        """Initialize game class."""
        super().__init__()
        self.info = models.ServerInfo(
            name=SERVER_NAME,
            version=GAME_VERSION,
            width=BOX_WIDTH,
            height=BOX_HEIGHT
        )
        self.players = []
        # TODO: Populate and update apples.
        self.apples = []
        self.tickrate = BOX_TICKRATE
        self.terminate_flag = threading.Event()

    @property
    def full(self) -> bool:
        """Check if the game is full."""
        return len(self.players) >= MAX_PLAYERS

    def add_player(self, player: Player):
        """Add a player to the current game."""
        self.players.append(player)

    def stop(self):
        """Stop thread."""
        self.terminate_flag.set()

    @property
    def game_model(self) -> models.Game:
        """Collate game data in to a data model."""
        # Collate players and entities.
        player_models = []
        entities = []
        for player in self.players:
            player_models.append(player.player_model)
            entities.extend(player.segments)
        entities.extend(self.apples)
        # Create the model.
        return models.Game(
            players=player_models,
            entities=entities,
            meta=self.info,
        )

    def run(self):
        """Run the game mainloop."""
        current_time = last_frame_time = time.time()
        while True:
            # Calculations needed for maintaining stable FPS
            sleep_time = 1 / self.tickrate - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            # Update snake segments
            for player in self.players:
                logic.move(player.segments)

            # Send players game data
            game_data = self.game_model.dict()
            for player in self.players:
                player.send(game_data)


class Server(Thread):
    """Game server process."""

    def __init__(self, host: str = '127.0.0.1', port: int = 65444):
        """Set up the game server."""
        super().__init__()
        self.terminate_flag = threading.Event()

        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.host, self.port))
        self.socket.settimeout(10)
        self.socket.listen()

        self.clients = []
        self.games = []
        self.next_player_id = 1

    def on_connect(self, conn: socket.socket, addr: tuple[str, int]):
        """Handle a new connection to the server."""
        host, port = addr
        logger.info(f'New client connected: {host}:{port}.')
        client = Player(conn, addr, models.Player(
            id=self.next_player_id,
            name='Unamed Player',
            score=0
        ))
        self.next_player_id += 1
        self.clients.append(client)
        client.start()

        for game in self.games:
            if not game.full:
                game.add_player(client)
                return
        # No game was found.
        new_game = game()
        self.games.append(new_game)
        new_game.add_player(client)
        new_game.start()

    def run(self):
        """Run the server and wait for connections."""
        logger.info(f'Server listing on {self.host}:{self.port}.')
        while not self.terminate_flag.is_set():
            try:
                conn, addr = self.socket.accept()
                self.on_connect(conn, addr)
            except socket.timeout:
                pass
            else:
                self.terminate_flag.set()

        # Stop everything.
        for thread in (*self.clients, *self.games):
            thread.stop()
            thread.join()


server = Server()
server.start()

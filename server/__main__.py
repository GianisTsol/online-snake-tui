"""Entrypoint for the server."""
import socket
import threading
import time
from threading import Thread

import msgpack

from common import logic, models


class player(Thread, models.Player):
    """Class fo each client."""

    def __init__(self, conn: socket.SocketIO, host: str):
        """Initialize layer class."""
        super(player, self).__init__()

        self.terminate_flag = threading.Event()
        self.conn = conn
        self.host = host
        self.score = 0

    def send(self, data: dict):
        """Pack and send data to the player."""
        s = msgpack.pack(data, use_bin_type=True)  # pack the data
        self.conn.send(s)

    def handler(self, data: dict):
        """Handle different types of events from client."""
        if "nick" in data:
            self.name = data['nick']
        elif "event" in data:
            pass
            # event = data["event"]
            # TODO: add game mechanics stuff

    def to_dict(self) -> dict:
        """Return game data as dict."""
        return {"name": self.name, "score": self.score}

    def stop(self):
        """Stop thread."""
        self.terminate_flag.set()

    def run(self):
        """Entrypoint for self.start() ."""
        while not self.terminate_flag.is_set():
            rec = self.conn.recv(1024)
            data = msgpack.unpackb(rec, raw=False)
            self.handler(data)


class game(Thread, models.Game, models.ServerInfo):
    """Game or mach filed with player."""

    def __init__(self):
        """Initialize game class."""
        super(game, self).__init__()
        self.segments = []
        self.apples = []
        self.tickrate = 15
        # Game setitngs
        self.maxplayers = 5
        self.full = False

    def add_player(self, player: player):
        """Add a player to the current game."""
        self.players.append(player)
        for i in range(0, logic.snek_segments):
            self.segments = logic.add_segment(self.segments)

        if len(self.players) == self.maxplayers:
            self.full = True

    def stop(self):
        """Stop thread."""
        self.terminate_flag.set()

    def run(self):
        """Man thread for each game maintaining tick rate."""
        current_time = last_frame_time = time.time()
        while True:
            # Calculations needed for maintaining stable FPS
            sleep_time = 1. / self.tickrate - (current_time - last_frame_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

            # game loop
            self.segments = logic.move(self.segments)

            # send data to players

            playerdata = []

            for i in self.players:
                playerdata.append(i.to_dict)

            gamedata = {"players": playerdata,
                        "segments": self.segments
                        }
            for i in self.players:
                i.send(gamedata)


class server(Thread):
    """docstring for server."""

    def __init__(self, host: str = '', port: int = 65444):
        """Init server clss."""
        super(server, self).__init__()
        self.terminate_flag = threading.Event()

        self.host = host
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((self.host, self.port))
        self.socket.settimeout(10)
        self.socket.listen()

        self.clients = []
        self.games = []

    def run(self):
        """Entrypoint for server.start() ."""
        print("started server")
        while not self.terminate_flag.is_set():
            try:
                conn, addr = self.socket.accept()
                print('Connected: ', addr)
                client = player(conn, addr)  # Initialize new player

                self.clients.append(client)

                client.start()  # start the client thread.

                found = False  # has a game been found
                for game in self.games:
                    if not game.full:
                        game.add_player(client)  # add player to the game
                        found = True
                        break
                if not found:
                    newgame = game()
                    self.games.append(newgame)
                    newgame.add_player(client)
                    newgame.start()

            except socket.timeout:
                pass
            else:
                self.terminate_flag.set()

        # stop everything
        for i in self.clients:
            i.stop()
            i.join()

        for i in self.games:
            i.stop()
            i.join()


new_server = server()
new_server.start()

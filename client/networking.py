"""Networking module."""
import socket
import threading
from threading import Thread

import msgpack


class Connection(Thread):
    """Used to connect to server and recieve or send game data."""

    def __init__(self):
        """Initialize connection class."""
        super().__init__()
        self.terminate_flag = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.newest = None

    def connect(self, host: str, port: int):
        """Call to connect to server."""
        self.sock.connect((host, port))

    def send(self, msg: dict):
        """Pack and send data."""
        packed = msgpack.pack(msg, use_bin_type=True)  # pack the data
        self.sock.send(packed)  # send data

    def stop(self):
        """Stop the thread."""
        self.terminate_flag.set()

    def get_newest(self) -> dict:
        """Get the newest recieved data."""
        return self.newest

    def run(self):
        """Thread to recieve data."""
        # Iterating an Unpacker waits for and yields each complete msgpack
        # object.
        reader = iter(msgpack.Unpacker(self.sock, raw=False))
        while not self.terminate_flag.is_set():
            try:
                self.newest = next(reader)
            except socket.timeout:
                pass  # ignore socket timeouts, the connection shouldnt stop

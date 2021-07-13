"""Networking module."""
import socket
import threading
from threading import Thread

import msgpack

from common import models


class Connection(Thread):
    """Used to connect to server and recieve or send game data."""

    def __init__(self):
        """Initialize connection class."""
        super().__init__()
        self.terminate_flag = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.newest = None
        self.serverinfo = None
        self.ready = False

    def connect(self, host: str, port: int):
        """Call to connect to server."""
        self.sock.connect((host, port))

    def send(self, msg: dict):
        """Pack and send data."""
        packed = msgpack.packb(msg, use_bin_type=True)  # pack the data
        self.sock.sendall(packed)  # send data

    def send_event(self, type: str, data: any):
        """Send event to server."""
        self.send({"event": {"type": type, "data": data}})

    def stop(self):
        """Stop the thread."""
        self.terminate_flag.set()

    def get_newest(self) -> dict:
        """Get the newest recieved data."""
        return self.newest

    def get_server_info(self):
        """Set the serer metadata."""
        info = self.newest['meta']
        self.serverinfo = models.ServerInfo(
            name=info['name'],
            version=info['version'],
            width=info['width'],
            height=info['height'],
        )

    def run(self):
        """Thread to recieve data."""
        unpacker = msgpack.Unpacker(raw=False)
        while not self.terminate_flag.is_set():
            try:
                r = self.sock.recv(1024)
                if r:
                    unpacker.feed(r)
                    for i in unpacker:
                        self.newest = i
                        self.get_server_info()
                        self.ready = True
            except Exception as e:
                if e is socket.timeout:
                    pass  # ignore socket timeouts, the connection shouldnt stop
                else:
                    self.terminate_flag.set()

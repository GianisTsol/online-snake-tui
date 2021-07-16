"""Module containing the game's config class."""
from configparser import ConfigParser


class SnekConfig(dict):
    """A Config class that is essentially an extension of 'dict'."""

    def __init__(
        self,
        filename: str = "snek.ini",
        write_default_config: bool = True
    ):
        """Init config class."""
        super().__init__()

        self.filename = filename
        self.config = ConfigParser()

        if write_default_config:
            self.write_default_config()

    def write_default_config(self):
        """Reset the config to default settings and writes to file."""
        self.config = ConfigParser()
        self["SERVER"] = {
            "SERVER_NAME": "SnekBox",
            "GAME_VERSION": 0,
            "BOX_WIDTH": 128,
            "BOX_HEIGHT": 32,
            "BOX_TICKRATE": 15,
            "MAX_PLAYERS": 5,
        }

        self.save()

    def read(self, filename: str) -> ConfigParser:
        """Load the config from an INI file."""
        self.config = ConfigParser()
        self.config.read(filename)
        if len(self.config.sections()) == 0:
            self.write_default_config()

    def save(self):
        """Write the current config to a file."""
        self.config = ConfigParser()
        for i in self.keys():
            self.config[i] = self.get(i)

        with open(self.filename, "w") as config_file:
            self.config.write(config_file)

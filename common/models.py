"""Pydantic models for game data."""
from typing import List, Literal, Union

import pydantic


class ServerInfo(pydantic.BaseModel):
    """Metadata on the server."""

    name: str
    version: int
    width: int
    height: int


class Player(pydantic.BaseModel):
    """A player connected to the server."""

    id: int
    name: str
    score: int


class BaseEntity(pydantic.BaseModel):
    """Base class for entities in the game.

    Each entity occupies a single square.
    """

    type: str
    x: int
    y: int


class Apple(BaseEntity):
    """An apple in the game."""

    type: Literal["apple"] = "apple"


class SnakeSegment(BaseEntity):
    """One segment of a player's snake."""

    type: Literal["snake_segment"] = "snake_segment"
    player: int  # References Player.id.
    is_head: bool
    index: int


Entity = Union[Apple, SnakeSegment]


class Game(pydantic.BaseModel):
    """All the data for a game as shared with clients."""

    meta: ServerInfo
    players: List[Player]
    entities: List[Entity]

"""Pydantic models for game data."""
from typing import Literal, Optional, Union

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
    id: int
    x: int
    y: int


class Apple(BaseEntity):
    """An apple in the game."""

    type: Literal['apple']


class SnakeSegment(BaseEntity):
    """One segment of a player's snake."""

    type: Literal['snake_segment']
    player: int                        # References Player.id.
    before: Optional[int]              # References SnakeSegment.id.
    after: Optional[int]               # References SnakeSegment.id.


Entity = Union[Apple, SnakeSegment]


class Game(pydantic.BaseModel):
    """All the data for a game as shared with clients."""

    meta: ServerInfo
    players: list[Player]
    entities: list[Entity]

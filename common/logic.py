"""Logic for the game.

This is used for calculationg position
and other game mechanics.
"""
from typing import Any

from . import models

snek_segments = 10  # Starting segments

# directions #

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


def add_segment(segments: list, head: bool = False) -> list:
    """Add segments to the snek and returns the list."""
    # Function to add segments to the snake, TODO: make apple
    if len(segments) == 0 and not head:  # figure out if seg is a head
        head = True  # also woks for server by just setting head

    curr_index = len(segments)
    segments.append(
        models.SnakeSegment(id=curr_index,
                            x=1 + curr_index,
                            y=5,
                            type='snake_segment',
                            player=0,
                            is_head=head,
                            before=curr_index - 1,
                            after=curr_index + 1
                            ))
    return segments


def change_direction(new: str, curr_direction: tuple) -> list:
    """Handle directions from new presses."""
    direction = curr_direction
    if new == "up" and curr_direction != down:
        direction = up
    if new == "down" and curr_direction != up:
        direction = down
    if new == "right" and curr_direction != left:
        direction = right
    if new == "left" and curr_direction != right:
        direction = left

    return direction


def move(direction: tuple, segments: list) -> list:
    """Move the snake. Needs to be called each frame."""
    head = segments[0]
    for i in segments[::-1]:
        if not i.is_head:  # Check if not head
            i.x = segments[i.before].x
            i.y = segments[i.before].y

    head.x += direction[0]
    head.y += direction[1]

    return segments


def has_collided_with_self(segments: list) -> bool:
    """Return True if the snake has collided with itself."""
    for i in segments[1:]:
        if (segments[0].x, segments[0].y) == (i.x, i.y):
            return True
    return False


def has_collided_with_wall(win: Any, segments: list) -> bool:
    """Return True if the snake has collided with a wall."""
    head = segments[0]
    return (
        head.x <= 0
        or head.x >= win.width - 1
        or head.y <= 0
        or head.y >= win.height - 1
    )

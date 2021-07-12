"""Logic for the game.

This is used for calculationg position
and other game mechanics.
"""
from .models import SnakeSegment

STARTING_SNAKE_SEGMENTS = 10

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def add_segment(segments: list, head: bool = False):
    """Add a new segment to a list of segments."""
    if not (segments or head):
        # If there are no segments, it must be a head.
        head = True

    curr_index = len(segments)
    segments.append(
        SnakeSegment(
            index=curr_index,
            # TODO: Find a good position (based on previous segments if any).
            x=STARTING_SNAKE_SEGMENTS - curr_index,
            y=5,
            # TODO: Accept a player to attach the snake to.
            player=0,
            is_head=head,
        )
    )


def change_direction(
        new: str, curr_direction: tuple[int, int]) -> tuple[int, int]:
    """Handle directions from new presses."""
    direction = curr_direction

    # New direction can't be opposite to the current one.
    if new == 'up' and curr_direction != DOWN:
        direction = UP
    elif new == 'down' and curr_direction != UP:
        direction = DOWN
    elif new == 'right' and curr_direction != LEFT:
        direction = RIGHT
    elif new == 'left' and curr_direction != RIGHT:
        direction = LEFT

    return direction


def move(
        direction: tuple[int, int],
        segments: list[SnakeSegment]):
    """Move the snake.

    This should be called each frame.
    """
    head = segments[0]
    for segment in segments[:0:-1]:
        before = segments[segment.index - 1]
        segment.x = before.x
        segment.y = before.y

    head.x += direction[0]
    head.y += direction[1]


def has_collided_with_self(segments: list[SnakeSegment]) -> bool:
    """Return True if the snake has collided with itself."""
    head = segments[0]
    for segment in segments[1:]:
        if (head.x, head.y) == (segment.x, segment.y):
            return True
    return False


def has_collided_with_wall(
        width: int, height: int, segments: list[SnakeSegment]) -> bool:
    """Return True if the snake has collided with a wall."""
    head = segments[0]
    return (
        head.x <= 0
        or head.x >= width - 1
        or head.y <= 0
        or head.y >= height - 1
    )

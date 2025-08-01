import time
import shutil
from itertools import cycle
from typing import List

from rich.console import Console
from rich.text import Text

console = Console(force_terminal=True)

# Skibidi song lyrics
LYRICS: List[str] = [
    "Skibidi Toilet (Uh)",
    "Skibidi Toilet (Yes-Yes-Yes)",
    "Skibidi Toilet",
    "Dob dob dob yes yes",
    "Skibidi dob dob dob skibidi",
    "Skibidi Toilet (Uh)",
    "Skibidi Toilet (Yes-Yes-Yes)",
    "Skibidi Toilet",
    "Dop dop dop yes yes",
    "Skibidi dop dop dop skibidi-bidi-bidi-",
]

# Rainbow colors for the lyrics
RAINBOW_COLORS: List[str] = [
    "red", "dark_orange", "yellow", "green", "cyan", "blue", "magenta"
]

# Skibidi head frames (mouth closed and mouth open)
_HEAD_FRAMES_RAW: List[List[str]] = [
    # Mouth closed (normal)
    [
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣴⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⢠⡿⠋⠉⠉⠛⠛⠛⠋⠉⠙⢿⡆⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀",
        "⡰⠉⠉⠁⠉⡙⠹⢠⢾⣛⠛⢶⢀⡶⠛⣛⠳⡄⡏⢋⠉⠉⠉⠉⢢",
        "⢹⠶⠶⠶⣾⠡⣾⠈⠸⡿⠷⠀⠀⠀⢾⣿⠇⠁⡶⡌⢷⠶⠶⠶⡏",
        "⢸⠀⠀⠀⠆⠀⢻⡀⠀⠀⡀⠀⠀⠀⢀⢀⡀⠀⡟⠀⠸⡀⠀⠀⡇",
        "⢸⠀⠀⢸⠀⠀⠈⡇⣠⠒⠓⠤⣀⠤⠘⠀⡘⢰⠃⠀⠀⡇⠀⠀⡇",
        "⢸⠀⠀⡎⠀⠀⠀⢻⠀⠙⣶⣶⣒⣶⣶⠋⢀⡏⠀⠀⠀⢸⠀⠀⡇",
        "⢸⠀⠀⡇⠀⠀⠀⠘⣧⡀⠈⠿⣿⡿⠁⢀⢮⠃⠀⠀⠀⢸⠀⠀⡇",
        "⢸⠀⠀⡇⠀⠀⠀⠀⢰⠑⠄⣀⠀⢀⡠⠊⡌⠀⠀⠀⠀⢸⠀⠀⡇",
        "⢸⠀⠀⠘⢄⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⡠⠃⠀⠀⡇",
        "⠈⠦⣀⣔⠂⠋⠒⠲⠶⠾⠤⠤⠤⠤⠤⠷⠶⠖⠒⠉⠒⢢⣀⠴⠃",
        "⠀⠀⠀⠅⠉⠉⠉⠉⠉⠒⠒⠒⠒⠒⠒⠊⠉⠉⠉⠉⠉⠨⡀⠀⠀",
        "⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠁⠀⠀",
        "⠀⠀⠀⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀",
        "⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠈⠢⢄⣀⡀⢀⠀⡀⢀⠀⣀⣀⡠⠔⠁⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⡌⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠸⠤⠠⠀⢀⣀⣀⣀⠀⠀⠤⠤⠖⠀⠀⠀⠀⠀⠀",
    ],
    # Mouth open
    [
        "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣴⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⢠⡿⠋⠉⠉⠛⠛⠛⠋⠉⠙⢿⡆⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⣼⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀⠀",
        "⡰⠉⠉⠁⠉⡙⠹⢠⢾⣛⠛⢶⢀⡶⠛⣛⠳⡄⡏⢋⠉⠉⠉⠉⢢",
        "⢹⠶⠶⠶⣾⠡⣾⠈⠸⡿⠷⠀⠀⠀⢾⣿⠇⠁⡶⡌⢷⠶⠶⠶⡏",
        "⢸⠀⠀⠀⠆⠀⢻⡀⠀⠀⡀⠀⠀⠀⢀⢀⡀⠀⡟⠀⠸⡀⠀⠀⡇",
        "⢸⠀⠀⢸⠀⠀⠈⡇⣠⠒⠓⠤⣀⠤⠘⠀⡘⢰⠃⠀⠀⡇⠀⠀⡇",
        "⢸⠀⠀⡎⠀⠀⠀⢻⠀⠙⣶⠀⠀⠀⣶⠋⢀⡏⠀⠀⠀⢸⠀⠀⡇",
        "⢸⠀⠀⡇⠀⠀⠀⠘⣧⡀⠈⠿⣤⡿⠁⢀⢮⠃⠀⠀⠀⢸⠀⠀⡇",
        "⢸⠀⠀⡇⠀⠀⠀⠀⢰⠑⠄⣀⠀⢀⡠⠊⡌⠀⠀⠀⠀⢸⠀⠀⡇",
        "⢸⠀⠀⠘⢄⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⡠⠃⠀⠀⡇",
        "⠈⠦⣀⣔⠂⠋⠒⠲⠶⠾⠤⠤⠤⠤⠤⠷⠶⠖⠒⠉⠒⢢⣀⠴⠃",
        "⠀⠀⠀⠅⠉⠉⠉⠉⠉⠒⠒⠒⠒⠒⠒⠊⠉⠉⠉⠉⠉⠨⡀⠀⠀",
        "⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠁⠀⠀",
        "⠀⠀⠀⠳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠀⠀⠀",
        "⠀⠀⠀⠀⠱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠈⠢⢄⣀⡀⢀⠀⡀⢀⠀⣀⣀⡠⠔⠁⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠀⡌⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀",
        "⠀⠀⠀⠀⠀⠀⠸⠤⠠⠀⢀⣀⣀⣀⠀⠀⠤⠤⠖⠀⠀⠀⠀⠀⠀",
    ],
]


def get_terminal_width() -> int:
    """Returns the current terminal width."""
    return shutil.get_terminal_size().columns


def center_block(block_lines: List[str]) -> List[str]:
    """Centers each line of a multiline ASCII block to the terminal width."""
    width = get_terminal_width()
    return [line.center(width) for line in block_lines]


def compose_toilet_frame(head_frame_index: int) -> List[str]:
    """
    Composes the full toilet frame with the singing Skibidi head inside.
    """
    full_frame = _HEAD_FRAMES_RAW[head_frame_index % len(_HEAD_FRAMES_RAW)]
    return center_block(full_frame)


def render_lyric_line(line: str, color: str) -> Text:
    """Returns a styled, centered Rich Text object for a lyric line."""
    centered_line = line.center(get_terminal_width())
    styled_text = Text(centered_line)
    styled_text.stylize(color)
    return styled_text


def rizz() -> None:
    """Skibidi karaoke with animated singing head inside the toilet and rainbow lyrics."""
    color_cycle = cycle(RAINBOW_COLORS)
    frame_index = 0

    console.clear()
    console.rule("[bold magenta]Skibidi Karaoke Toilet Show 🚽🎤", style="bold magenta")

    for lyric in LYRICS:
        console.clear()

        # Draw toilet frame with Skibidi head
        toilet_frame_lines = compose_toilet_frame(frame_index)
        for line in toilet_frame_lines:
            console.print(line, style="white")

        # Print rainbow karaoke lyric line
        color = next(color_cycle)
        lyric_line = render_lyric_line(f"🎤 {lyric} 🎤", color)
        console.print(lyric_line)

        time.sleep(0.85)
        frame_index += 1

    # Final celebration screen
    console.clear()
    console.rule("[bold green]Skibidi Complete ✅", style="bold green")
    for lyric in LYRICS:
        color = next(color_cycle)
        final_line = render_lyric_line(lyric, f"bold {color}")
        console.print(final_line)
        time.sleep(0.1)

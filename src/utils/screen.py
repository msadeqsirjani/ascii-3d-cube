import os
from src.config.settings import CLEAR_SCREEN, BACKGROUND_COLOR

def clear_terminal():
    """Clear the terminal screen and set background color"""
    print(CLEAR_SCREEN + BACKGROUND_COLOR, end='')
"""
Functions for generalization levels
"""

def remove_color_information(arena):
    for item in arena.items:
        item.colors = []

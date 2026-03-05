"""list_styles MCP tool - returns all available style presets."""

from typing import Any

from .styles import STYLE_PRESETS


def list_styles() -> list[dict[str, Any]]:
    """
    List all available style presets.
    
    Returns:
        List of style dictionaries with name, description, category, and best_for.
    """
    styles = []
    
    for slug, preset in STYLE_PRESETS.items():
        styles.append({
            "slug": slug,
            "name": preset["name"],
            "description": preset["vibe"],
            "category": preset["category"],
            "best_for": preset["best_for"],
            "animation_style": preset["animation_style"],
        })
    
    return styles

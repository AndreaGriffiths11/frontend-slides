"""get_style_details MCP tool - returns full style preset information."""

from typing import Any

from .styles import get_style_by_name


def get_style_details(style_name: str) -> dict[str, Any] | None:
    """
    Get full details for a specific style preset.
    
    Args:
        style_name: The style name or slug (e.g., "Bold Signal" or "bold-signal")
    
    Returns:
        Full style preset dictionary or None if not found.
    """
    preset = get_style_by_name(style_name)
    
    if not preset:
        return None
    
    # Return the full preset with all details
    return {
        "slug": style_name.lower().replace(" ", "-"),
        "name": preset["name"],
        "vibe": preset["vibe"],
        "best_for": preset["best_for"],
        "category": preset["category"],
        "fonts": preset["fonts"],
        "colors": preset["colors"],
        "signature_elements": preset["signature_elements"],
        "animation_style": preset["animation_style"],
    }

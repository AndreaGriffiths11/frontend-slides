"""MCP tools for frontend-slides presentation generator."""

from .create_presentation import create_presentation
from .list_styles import list_styles
from .preview_style import preview_style
from .get_style_details import get_style_details
from .publish_presentation import publish_presentation

__all__ = [
    "create_presentation",
    "list_styles",
    "preview_style",
    "get_style_details",
    "publish_presentation",
]

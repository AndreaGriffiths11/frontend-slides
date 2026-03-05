"""
Frontend Slides MCP Server

An MCP (Model Context Protocol) server for creating stunning HTML presentations.
Provides tools for presentation generation, style discovery, and previewing.
"""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from tools import (
    create_presentation,
    list_styles,
    preview_style,
    get_style_details,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("frontend-slides-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="create_presentation",
            description="""Create a complete HTML presentation with zero dependencies.
            
Generates a single, self-contained HTML file with:
- Inline CSS and JavaScript
- Responsive viewport-fitting design
- Touch/swipe navigation support
- Keyboard navigation (arrows, space)
- Scroll-triggered animations
- Progress indicator

Returns the file path to the generated presentation.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "Main topic/title of the presentation",
                    },
                    "key_messages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of 3-5 key messages to convey in the presentation",
                    },
                    "num_slides": {
                        "type": "integer",
                        "description": "Approximate number of slides (default: 10)",
                        "default": 10,
                    },
                    "audience": {
                        "type": "string",
                        "description": "Target audience",
                        "enum": ["investors", "technical", "executives", "general", "students"],
                        "default": "general",
                    },
                    "tone": {
                        "type": "string",
                        "description": "Desired tone",
                        "enum": ["professional", "casual", "energetic", "calm", "inspiring"],
                        "default": "professional",
                    },
                    "style": {
                        "type": "string",
                        "description": "Style preset name or slug (e.g., 'Bold Signal' or 'bold-signal')",
                        "default": "bold-signal",
                    },
                    "images": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string"},
                                "alt": {"type": "string"},
                                "slide_index": {"type": "integer"},
                            },
                        },
                        "description": "Optional list of images with path, alt text, and slide index",
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "Directory to save the presentation (defaults to current directory)",
                    },
                },
                "required": ["topic", "key_messages"],
            },
        ),
        Tool(
            name="list_styles",
            description="""List all available visual style presets for presentations.
            
Returns a list of styles with:
- Style name and slug
- Description/vibe
- Category (dark/light)
- Best use cases
- Animation style""",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="preview_style",
            description="""Generate a sample slide HTML to preview a specific style.
            
Creates a single-slide HTML showing:
- Typography for the style
- Color palette
- Animation style
- Overall aesthetic

Useful for comparing styles before committing to one.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "style_name": {
                        "type": "string",
                        "description": "Style name or slug to preview (e.g., 'Bold Signal' or 'bold-signal')",
                    },
                },
                "required": ["style_name"],
            },
        ),
        Tool(
            name="get_style_details",
            description="""Get full details for a specific style preset.
            
Returns complete style information including:
- Name and description
- Font pairing (display + body)
- Color palette
- Signature design elements
- Animation style
- Best use cases""",
            inputSchema={
                "type": "object",
                "properties": {
                    "style_name": {
                        "type": "string",
                        "description": "Style name or slug to get details for",
                    },
                },
                "required": ["style_name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a tool call."""
    
    try:
        if name == "create_presentation":
            result = create_presentation(
                topic=arguments.get("topic", ""),
                key_messages=arguments.get("key_messages", []),
                num_slides=arguments.get("num_slides", 10),
                audience=arguments.get("audience", "general"),
                tone=arguments.get("tone", "professional"),
                style=arguments.get("style", "bold-signal"),
                images=arguments.get("images"),
                output_dir=arguments.get("output_dir"),
            )
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}")]
            
            return [TextContent(
                type="text",
                text=f"""Presentation created successfully!

📁 File: {result['file_path']}
📊 Slides: {result['slides_count']}
🎨 Style: {result['style']}
📝 Topic: {result['topic']}

{result['preview']}

Navigation controls:
- Arrow keys (← →) or Space to navigate
- Click dots to jump to slides  
- Swipe on touch devices
- Scroll to navigate"""
            )]
        
        elif name == "list_styles":
            styles = list_styles()
            
            # Format styles as readable text
            lines = ["Available Style Presets:\n"]
            
            # Group by category
            dark_styles = [s for s in styles if s["category"] == "dark"]
            light_styles = [s for s in styles if s["category"] == "light"]
            
            lines.append("## Dark Themes")
            for style in dark_styles:
                lines.append(f"- **{style['name']}** (`{style['slug']}`): {style['description']}")
                lines.append(f"  Best for: {', '.join(style['best_for'][:2])}")
            
            lines.append("\n## Light Themes")
            for style in light_styles:
                lines.append(f"- **{style['name']}** (`{style['slug']}`): {style['description']}")
                lines.append(f"  Best for: {', '.join(style['best_for'][:2])}")
            
            return [TextContent(type="text", text="\n".join(lines))]
        
        elif name == "preview_style":
            result = preview_style(arguments.get("style_name", ""))
            
            if "error" in result:
                return [TextContent(type="text", text=f"Error: {result['error']}\n\nAvailable styles: {', '.join(result.get('available_styles', []))}")]
            
            return [TextContent(
                type="text",
                text=f"""Style Preview: {result['style_name']}

Vibe: {result['vibe']}

HTML Preview:
```html
{result['html']}
```

Copy this HTML to a file and open in a browser to see the preview."""
            )]
        
        elif name == "get_style_details":
            result = get_style_details(arguments.get("style_name", ""))
            
            if result is None:
                return [TextContent(type="text", text=f"Style not found. Use list_styles to see available options.")]
            
            lines = [
                f"# {result['name']}\n",
                f"**Vibe:** {result['vibe']}",
                f"**Category:** {result['category']}",
                f"**Animation Style:** {result['animation_style']}\n",
                "## Fonts",
                f"- Display: {result['fonts']['display']} (weight: {result['fonts']['display_weight']})",
                f"- Body: {result['fonts']['body']} (weight: {result['fonts']['body_weight']})\n",
                "## Colors",
            ]
            
            for key, value in result['colors'].items():
                if isinstance(value, str):
                    lines.append(f"- {key}: `{value}`")
            
            lines.append("\n## Signature Elements")
            for element in result['signature_elements']:
                lines.append(f"- {element}")
            
            lines.append("\n## Best For")
            for use_case in result['best_for']:
                lines.append(f"- {use_case}")
            
            return [TextContent(type="text", text="\n".join(lines))]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main():
    """Entry point for the MCP server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()

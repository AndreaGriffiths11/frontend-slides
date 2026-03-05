# Frontend Slides MCP Server

Generate stunning, zero-dependency HTML presentations with the Model Context Protocol (MCP).

## Features

- **12 Curated Style Presets** — Dark and light themes, from Neon Cyber to Paper & Ink
- **Zero Dependencies** — Single HTML files with inline CSS/JS
- **Viewport-Fitting** — Every slide fits exactly, no scrolling
- **Responsive** — Works on desktop, tablet, and mobile
- **Touch Support** — Swipe navigation on mobile devices
- **Keyboard Navigation** — Arrow keys and spacebar
- **Entrance Animations** — Smooth reveal animations per slide

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or uv package manager

### Install

```bash
# Clone the repository
git clone https://github.com/AndreaGriffiths11/frontend-slides.git
cd frontend-slides/mcp

# Install with pip
pip install -e .

# Or with uv
uv pip install -e .
```

## Usage

### Run the MCP Server

```bash
frontend-slides-mcp
```

The server communicates via stdio, ready for MCP clients like Claude Desktop, Cursor, or other MCP-compatible tools.

### Configure with Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "frontend-slides": {
      "command": "frontend-slides-mcp"
    }
  }
}
```

Or with a specific path:

```json
{
  "mcpServers": {
    "frontend-slides": {
      "command": "python",
      "args": ["/path/to/frontend-slides/mcp/server.py"]
    }
  }
}
```

## Available Tools

### `create_presentation`

Create a stunning HTML presentation.

**Parameters:**
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `topic` | string | Yes | — | Main topic/title |
| `key_messages` | array | Yes | — | Key messages to distribute across slides |
| `num_slides` | integer | No | 5 | Number of slides (3-30) |
| `audience` | string | No | "general" | Target audience |
| `tone` | string | No | "professional" | Tone: professional, casual, energetic, elegant, technical |
| `style` | string | No | "neon-cyber" | Style preset slug |
| `images` | array | No | [] | Optional image URLs |
| `output_path` | string | No | cwd | Output directory |

**Returns:** File path to the generated HTML file.

**Example:**
```json
{
  "topic": "Building AI Products",
  "key_messages": [
    "AI is transforming every industry",
    "User experience matters more than ever",
    "Start small, iterate quickly",
    "Measure what matters"
  ],
  "num_slides": 5,
  "audience": "developers",
  "tone": "technical",
  "style": "terminal-green"
}
```

### `list_styles`

List all available style presets.

**Returns:** Array of style objects with slug, name, description, category, best_for, and animation_style.

### `preview_style`

Generate a sample HTML preview for a specific style.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `style_name` | string | Yes | Style name or slug |

**Returns:** HTML string of the preview slide.

### `get_style_details`

Get complete details for a specific style preset.

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `style_name` | string | Yes | Style name or slug |

**Returns:** Full style configuration including fonts, colors, signature elements, and best use cases.

## Style Presets

### Dark Themes

| Style | Vibe | Best For |
|-------|------|----------|
| **bold-signal** | Confident, bold, modern | Pitch decks, keynotes |
| **electric-studio** | Bold, clean, professional | Agency presentations |
| **creative-voltage** | Energetic, retro-modern | Creative pitches |
| **dark-botanical** | Elegant, sophisticated | Premium brands |
| **neon-cyber** | Futuristic, techy | Tech startups, dev tools |
| **terminal-green** | Developer-focused, hacker | API docs, technical content |

### Light Themes

| Style | Vibe | Best For |
|-------|------|----------|
| **notebook-tabs** | Editorial, organized | Reports, documentation |
| **pastel-geometry** | Friendly, modern | Product overviews |
| **split-pastel** | Playful, creative | Marketing presentations |
| **vintage-editorial** | Witty, personality-driven | Personal brands |
| **swiss-modern** | Clean, precise | Corporate, data viz |
| **paper-and-ink** | Editorial, literary | Storytelling |

## Output Format

Generated presentations are:
- **Self-contained** — Single HTML file, no external dependencies
- **Zero-config** — Works immediately in any browser
- **Responsive** — Adapts to any viewport size
- **Accessible** — Respects prefers-reduced-motion
- **Keyboard-friendly** — Arrow keys and spacebar navigation
- **Touch-ready** — Swipe gestures on mobile

## Generated HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Topic</title>
    <style>
        /* Viewport-fitting base CSS */
        /* Style-specific CSS */
    </style>
</head>
<body>
    <section class="slide" data-slide="1">...</section>
    <section class="slide" data-slide="2">...</section>
    <!-- ... -->
    <nav class="nav-dots">...</nav>
    <script>
        /* Intersection Observer for animations */
        /* Keyboard navigation */
        /* Touch navigation */
    </script>
</body>
</html>
```

## Content Density Limits

To ensure viewport fitting, each slide has content limits:
- **Title slide:** 1 heading + 1 subtitle
- **Content slide:** 1 heading + 4-6 bullets (max 2 lines each)
- **Feature grid:** 1 heading + 6 cards maximum
- **Code slide:** 1 heading + 8-10 lines of code
- **Quote slide:** 1 quote (max 3 lines) + attribution

## Development

### Project Structure

```
mcp/
├── server.py              # MCP server entry point
├── pyproject.toml         # Python package config
├── styles.json            # Structured style data
├── README.md              # This file
└── tools/
    ├── __init__.py        # Tool exports
    ├── create_presentation.py  # Main generation tool
    ├── list_styles.py     # Style listing
    ├── preview_style.py   # Style preview
    ├── get_style_details.py    # Style details
    └── styles.py          # Style preset data (Python)
```

### Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Add a New Style

1. Add the style to `tools/styles.py` in the `STYLE_PRESETS` dict
2. Add font URLs to `FONT_SOURCES`
3. Update `styles.json` with the structured data
4. Test with `preview_style`

## License

MIT License — see [LICENSE](../LICENSE) for details.

## Credits

Built on the [Model Context Protocol](https://modelcontextprotocol.io/) specification.

Style presets inspired by modern editorial and product design — no generic AI aesthetics.

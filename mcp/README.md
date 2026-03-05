# Frontend Slides MCP Server

Generate HTML presentations with the Model Context Protocol.

## What It Does

- **12 style presets** — Dark and light themes, from Neon Cyber to Paper & Ink
- **Zero dependencies** — Single HTML files with inline CSS/JS
- **Fits the viewport** — Every slide fills the screen, no scrolling
- **Responsive** — Works on desktop, tablet, and mobile
- **Touch support** — Swipe to navigate on mobile
- **Keyboard navigation** — Arrow keys and spacebar
- **Entrance animations** — Smooth reveals per slide

## Installation

You'll need Python 3.10+ and pip or uv.

```bash
# Clone and install
git clone https://github.com/AndreaGriffiths11/frontend-slides.git
cd frontend-slides/mcp
pip install -e .
```

## Usage

### Run the Server

```bash
frontend-slides-mcp
```

The server runs on stdio, ready for any MCP client.

### Configure with Claude Desktop

Add this to your Claude Desktop config:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "frontend-slides": {
      "command": "frontend-slides-mcp"
    }
  }
}
```

Or point directly to the script:

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

## Tools

### `create_presentation`

Build an HTML presentation.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `topic` | string | Yes | — | Main topic/title |
| `key_messages` | array | Yes | — | Key messages to distribute across slides |
| `num_slides` | integer | No | 5 | Number of slides (3-30) |
| `audience` | string | No | "general" | Target audience |
| `tone` | string | No | "professional" | professional, casual, energetic, elegant, technical |
| `style` | string | No | "neon-cyber" | Style preset slug |
| `images` | array | No | [] | Optional image URLs |
| `output_path` | string | No | cwd | Output directory |

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

Returns the file path to the generated HTML.

### `publish_presentation`

Push an HTML presentation to GitHub Pages for instant sharing.

Creates a repo, pushes the HTML as `index.html`, and enables Pages.

**You'll need:**
- GitHub CLI (`gh`) installed and authenticated
- Git installed

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `html_path` | string | Yes | — | Path to the HTML file |
| `repo_name` | string | Yes | — | Name for the new repo |
| `public` | boolean | No | false | Public or private repo |

**Returns:**
- `repo_url`: GitHub repository URL
- `pages_url`: Live GitHub Pages URL
- `repo_name`: Repository name
- `visibility`: "private" or "public"

**Example:**
```json
{
  "html_path": "/path/to/my-presentation.html",
  "repo_name": "ai-products-slides",
  "public": true
}
```

GitHub Pages takes 1-2 minutes to deploy after publishing.

### `list_styles`

Get all available style presets.

Returns an array with slug, name, description, category, best_for, and animation_style.

### `preview_style`

Generate a sample HTML preview for a specific style.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `style_name` | string | Yes | Style name or slug |

Returns the HTML for a preview slide.

### `get_style_details`

Full details for a style preset — fonts, colors, signature elements, and use cases.

## Style Presets

### Dark Themes

| Style | Vibe | Best For |
|-------|------|----------|
| **bold-signal** | Confident, modern | Pitch decks, keynotes |
| **electric-studio** | Bold, professional | Agency presentations |
| **creative-voltage** | Energetic, retro-modern | Creative pitches |
| **dark-botanical** | Elegant, sophisticated | Premium brands |
| **neon-cyber** | Futuristic, techy | Tech startups, dev tools |
| **terminal-green** | Developer-focused | API docs, technical content |

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

Each presentation is:
- **Self-contained** — Single HTML file, no external dependencies
- **Zero-config** — Opens in any browser
- **Responsive** — Adapts to any viewport
- **Accessible** — Respects prefers-reduced-motion
- **Keyboard-friendly** — Arrow keys and spacebar
- **Touch-ready** — Swipe gestures on mobile

## Publishing to GitHub Pages

Generated HTML works great on GitHub Pages.

### Prerequisites

- [GitHub CLI](https://cli.github.com/) installed
- Authenticated with `gh auth login`

### Quick Publish

```bash
# Create repo and push
gh repo create my-presentation --public
cd my-presentation
git init
git add .
git commit -m "Add presentation"
git push -u origin main

# Enable Pages
gh api repos/{owner}/{repo}/pages -X POST -f source='{"branch":"main"}'
```

Live at `https://{username}.github.io/{repo-name}/`.

### Check GitHub CLI Setup

```bash
gh auth status
# If not authenticated:
gh auth login
```

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
    <nav class="nav-dots">...</nav>
    <script>
        /* Intersection Observer for animations */
        /* Keyboard navigation */
        /* Touch navigation */
    </script>
</body>
</html>
```

## Content Limits

To keep slides fitting the viewport:

- **Title slide:** 1 heading + 1 subtitle
- **Content slide:** 1 heading + 4-6 bullets (max 2 lines each)
- **Feature grid:** 1 heading + 6 cards max
- **Code slide:** 1 heading + 8-10 lines of code
- **Quote slide:** 1 quote (max 3 lines) + attribution

## Development

### Project Structure

```
mcp/
├── server.py              # MCP server entry point
├── pyproject.toml         # Python package config
├── styles.json            # Style data
├── README.md              # This file
└── tools/
    ├── __init__.py
    ├── create_presentation.py
    ├── list_styles.py
    ├── preview_style.py
    ├── get_style_details.py
    ├── publish_presentation.py
    └── styles.py
```

### Run Tests

```bash
pip install -e ".[dev]"
pytest
```

### Add a New Style

1. Add the style to `tools/styles.py` in `STYLE_PRESETS`
2. Add font URLs to `FONT_SOURCES`
3. Update `styles.json`
4. Test with `preview_style`

## License

MIT License — see [LICENSE](../LICENSE).

## Inspiration & Credits

Started as a [Copilot CLI-powered project](https://github.com/AndreaGriffiths11/frontend-slides) to build stunning HTML presentations from the command line. This MCP server wraps that same logic for use with AI assistants.

- [Original Project](https://github.com/AndreaGriffiths11/frontend-slides) — The SKILL.md and style presets
- [Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) — GitHub's AI-powered command line tool

Built on the [Model Context Protocol](https://modelcontextprotocol.io/).

# Copilot CLI Integration

This repository includes GitHub Copilot CLI commands for working with HTML presentations.

## Setup

Copy the skill files to your Copilot CLI skills directory:

```bash
# Create the directory if needed
mkdir -p ~/.copilot/skills/frontend-slides

# Copy skill files
cp SKILL.md STYLE_PRESETS.md ~/.copilot/skills/frontend-slides/

# Copy Copilot CLI commands (optional - for command discovery)
cp -r .copilot ~/.copilot/skills/frontend-slides/
```

## Available Commands

| Command | Description |
|---------|-------------|
| `/create-presentation` | Create a new HTML presentation from scratch with guided content and style discovery |
| `/summarize-slides` | Summarize content and structure of an HTML presentation |
| `/find-topics` | Extract and organize topics/themes from a presentation |
| `/suggest-style` | Recommend a visual style based on content and audience |
| `/convert-ppt` | Convert PowerPoint files to HTML presentations |
| `/extract-content` | Extract structured content in JSON, Markdown, or outline format |

## Usage Examples

### Summarize a Presentation

```bash
/copilot summarize-slides pitch-deck.html
```

Output includes:
- Slide count and style detection
- Narrative arc summary
- Per-slide overview
- Key topics covered

### Find Topics

```bash
/copilot find-topics conference-talk.html
```

Output includes:
- Primary and secondary topics
- Technical concepts
- Implicit themes
- Expansion suggestions

### Suggest a Style

```bash
/copilot suggest-style my-presentation.html --audience investors
```

Output includes:
- Primary recommendation with reasoning
- Alternative options
- Style mismatch warnings

### Convert PowerPoint

```bash
/copilot convert-ppt slides.pptx --style "Neon Cyber"
```

Requires Python with `python-pptx`:
```bash
pip install python-pptx
```

### Extract Content

```bash
/copilot extract-content presentation.html --format json
```

Formats: `json`, `markdown`, or `outline` (default)

## Discovery Files

The `.copilot/discovery/` directory contains context files that help Copilot understand:

- `skill-overview.md` - What the skill does and key files
- `presentation-patterns.md` - Content patterns, animation styles, responsive requirements

## Creating New Presentations

### Quick Start (Copilot CLI)

```bash
/copilot create-presentation
```

This launches an interactive workflow:
1. Gather content (topic, key messages, slides, images)
2. Ask about audience and desired feeling
3. Pick a style (direct selection or preview-based discovery)
4. Generate a self-contained HTML file

### With Style Preset

```bash
/copilot create-presentation --style "Bold Signal"
```

### Full Skill (Claude Code)

For the complete presentation creation workflow with richer style previews, use Claude Code with the SKILL.md file directly:

```bash
# In Claude Code
/frontend-slides

> "Create a pitch deck for my AI startup"
```

The Copilot CLI commands are optimized for quick creation and analysis tasks, while the full skill is best for complex projects with extensive customization.

## Extending

To add new commands:

1. Create a new `.prompt.md` file in `.copilot/commands/`
2. Include frontmatter with `name` and `description`
3. Document usage, instructions, and output format
4. Test with `/copilot <command-name>`

## Integration with Other Tools

The output from these commands can be piped to other tools:

```bash
# Export to JSON for processing
/copilot extract-content slides.html --format json > slides.json

# Generate Markdown summary
/copilot summarize-slides slides.html > SUMMARY.md
```

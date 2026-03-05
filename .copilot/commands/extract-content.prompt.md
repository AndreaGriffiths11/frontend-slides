---
name: extract-content
description: Extract structured content from an HTML presentation
---

# Extract Content

Extract structured content from an HTML presentation for reuse or analysis.

## Usage

```
/copilot extract-content <presentation.html> [--format <json|markdown|outline>]
```

## Formats

- `json` - Structured JSON with slide objects
- `markdown` - Markdown document with slide sections
- `outline` - Simple bullet outline (default)

## Instructions

1. Read the HTML presentation file
2. Extract from each slide:
   - Title/heading text
   - Body content (paragraphs, lists)
   - Image references (src attributes)
   - Any data attributes or metadata
3. Output in requested format

## Output Formats

### JSON Format

```json
{
  "title": "Presentation Title",
  "style": "neon-cyber",
  "slides": [
    {
      "number": 1,
      "type": "title",
      "title": "Welcome",
      "subtitle": "Subtitle text",
      "images": []
    },
    {
      "number": 2,
      "type": "content",
      "title": "Features",
      "bullets": ["Point 1", "Point 2", "Point 3"],
      "images": ["assets/feature-diagram.png"]
    }
  ]
}
```

### Markdown Format

```markdown
# Presentation Title

## Slide 1: Welcome
Subtitle text

## Slide 2: Features
- Point 1
- Point 2
- Point 3

![feature-diagram](assets/feature-diagram.png)
```

### Outline Format

```
Presentation Title
├── Slide 1: Welcome
│   └── Subtitle text
├── Slide 2: Features
│   ├── Point 1
│   ├── Point 2
│   └── Point 3
└── ...
```

## Notes

- Preserve content hierarchy
- Include image paths for assets
- Flag any embedded code or special content

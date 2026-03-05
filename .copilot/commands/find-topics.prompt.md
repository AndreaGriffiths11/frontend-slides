---
name: find-topics
description: Extract and organize topics/themes from a presentation
---

# Find Topics

Extract and organize all topics, themes, and concepts from a presentation.

## Usage

```
/copilot find-topics <presentation.html>
```

## Instructions

1. Read the HTML presentation file
2. Scan all content for:
   - Explicit topics (headings, section titles)
   - Implicit themes (patterns in content)
   - Technical concepts (code, terminology)
   - Business/creative concepts (if present)
3. Organize into a topic hierarchy
4. Suggest related topics that could expand the presentation

## Output Format

```
## Topics in: [Presentation Title]

### Primary Topics
- [Main topic 1]
- [Main topic 2]

### Secondary Topics
- [Supporting topic 1]
- [Supporting topic 2]

### Technical Concepts
- [Concept 1]
- [Concept 2]

### Implicit Themes
- [Theme 1]
- [Theme 2]

### Expansion Suggestions
- [Related topic to add]
- [Missing perspective to consider]
```

## Notes

- Group related concepts together
- Identify the "story" the topics tell
- Note any topics that seem disconnected or could be better integrated

---
name: summarize-slides
description: Summarize the content of an HTML presentation file
---

# Summarize Slides

Summarize the content and structure of an HTML presentation.

## Usage

```
/copilot summarize-slides <presentation.html>
```

## Instructions

1. Read the provided HTML presentation file
2. Extract all slide content:
   - Slide titles and headings
   - Main content (bullet points, paragraphs)
   - Key themes and topics
3. Generate a structured summary:
   - Total slide count
   - Main narrative arc
   - Key topics covered
   - Suggested audience (based on content depth/tone)
4. List each slide with its title and 1-sentence summary

## Output Format

```
## Presentation Summary: [Title]

**Slides:** X
**Style:** [Detected style from CSS variables]
**Audience:** [Inferred audience]

### Narrative Arc
[2-3 sentences describing the story/journey]

### Slides Overview
1. **[Title]** - [One sentence summary]
2. **[Title]** - [One sentence summary]
...

### Key Topics
- [Topic 1]
- [Topic 2]
- [Topic 3]
```

## Notes

- Detect the visual style from CSS custom properties
- Identify the presentation type (pitch, tutorial, conference talk, etc.)
- Flag any slides that might be too dense (violate content density rules)

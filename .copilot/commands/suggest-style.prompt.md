---
name: suggest-style
description: Suggest a visual style based on content and audience
---

# Suggest Style

Analyze presentation content and suggest the best visual style.

## Usage

```
/copilot suggest-style <presentation.html> [--audience <type>]
```

## Audience Types
- `investors` - Pitch deck, funding presentation
- `technical` - Developer/ engineering audience
- `executive` - C-suite, board members
- `general` - Mixed or public audience
- `academic` - Educational, research context
- `creative` - Design, marketing teams

## Instructions

1. Read the HTML presentation (or accept content description)
2. Analyze:
   - Content type (technical, business, creative, educational)
   - Tone (serious, playful, bold, elegant)
   - Complexity (simple, moderate, complex)
   - Audience context (if provided)
3. Match against available styles:
   - **Bold Signal**: Confident, high-impact, modern
   - **Electric Studio**: Bold, clean, professional
   - **Creative Voltage**: Energetic, creative, retro-modern
   - **Dark Botanical**: Elegant, sophisticated, artistic
   - **Neon Cyber**: Futuristic, techy, confident
   - **Terminal Green**: Developer-focused, hacker aesthetic
   - **Notebook Tabs**: Editorial, organized, tactile
   - **Pastel Geometry**: Friendly, modern, approachable
   - **Split Pastel**: Playful, modern, creative
   - **Vintage Editorial**: Witty, confident, personality-driven
   - **Swiss Modern**: Clean, precise, Bauhaus-inspired
   - **Paper & Ink**: Editorial, literary, thoughtful
4. Provide reasoning for recommendation

## Output Format

```
## Style Recommendation

### Primary Suggestion: [Style Name]

**Why it fits:**
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Key characteristics:**
- Display font: [Font name]
- Body font: [Font name]
- Color palette: [Brief description]

### Alternative Options

1. **[Style Name]** - [Why it could also work]
2. **[Style Name]** - [Why it could also work]

### Style Mismatch Warnings
- [Any styles that would NOT fit well and why]
```

## Notes

- Consider accessibility (contrast ratios, font readability)
- Match animation energy to content tone
- Suggest modifications if no perfect match exists

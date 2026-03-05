# Presentation Content Patterns

## Slide Types

| Type | Content Limit |
|------|---------------|
| Title | 1 heading + 1 subtitle |
| Content | 1 heading + 4-6 bullets |
| Feature Grid | 1 heading + 6 cards max |
| Code | 1 heading + 8-10 lines |
| Quote | 1 quote (3 lines max) + attribution |
| Image | 1 heading + 1 image (max 50vh) |

## Animation Patterns

- **Dramatic**: Slow fade-ins, scale transitions, spotlight effects
- **Techy**: Neon glows, grid patterns, particle backgrounds
- **Playful**: Bouncy easing, rounded corners, pastel colors
- **Professional**: Fast subtle animations, clean sans-serif
- **Editorial**: Strong typography, pull quotes, image-text interplay

## Responsive Requirements

- All sizes use `clamp(min, preferred, max)`
- Height breakpoints: 700px, 600px, 500px
- `overflow: hidden` on every slide
- Dynamic viewport height: `height: 100dvh`

## Output Structure

```
presentation.html    # Self-contained HTML
assets/              # Extracted images (for PPT conversion)
```

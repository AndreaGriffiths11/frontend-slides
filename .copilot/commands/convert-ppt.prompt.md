---
name: convert-ppt
description: Convert a PowerPoint file to HTML presentation
---

# Convert PPT

Convert a PowerPoint (.ppt/.pptx) file to a web presentation.

## Usage

```
/copilot convert-ppt <presentation.pptx> [--style <style-name>]
```

## Prerequisites

Python with `python-pptx` library:
```bash
pip install python-pptx
```

## Instructions

1. Extract content from the PowerPoint file:
   - All text content (titles, body text)
   - All images (save to assets/ folder)
   - Speaker notes (if any)
   - Slide order and structure

2. Confirm extracted content with user

3. If `--style` provided, use that style
   If not, proceed to style discovery:
   - Ask about presentation purpose
   - Ask about desired feeling
   - Generate 3 style previews
   - User picks preferred style

4. Generate HTML presentation:
   - All text preserved
   - All images referenced from assets/
   - Viewport-fitted slides
   - Keyboard navigation
   - Responsive design

## Output

```
[presentation-name].html
[presentation-name]-assets/
  ├── slide1_img1.png
  ├── slide2_img1.png
  └── ...
```

## Notes

- Warn if any slide violates content density limits
- Preserve speaker notes as HTML comments
- Handle grouped objects and charts gracefully

---
name: create-presentation
description: Create a new HTML presentation from scratch with guided content and style discovery
---

# Create Presentation

Generate a zero-dependency, animation-rich HTML presentation from scratch.

## Usage

```
/copilot create-presentation [--style <style-name>]
```

## Flags

- `--style <name>` - Skip style discovery and use a named preset (e.g., "Bold Signal", "Dark Botanical")

## Instructions

### Step 1: Gather Content

Ask the user for:

1. **Topic** - What is the presentation about?
2. **Key messages** - What are the 3-5 main points to convey?
3. **Slide count** - Approximate number of slides needed (short: 5-10, medium: 10-20, long: 20+)
4. **Images** - Any images to include? (paths, URLs, or descriptions for generation)

If the user has notes or an outline, accept them. If not, offer to help structure the content.

### Step 2: Audience and Tone

Ask:

1. **Audience** - Who will see this presentation?
   - Investors/clients
   - Technical team
   - Executives
   - General public
   - Students/educational

2. **Feeling** - What should the audience feel?
   - Impressed/Confident
   - Excited/Energized
   - Calm/Focused
   - Inspired/Moved

### Step 3: Style Selection

**If `--style` flag provided:**
- Use the specified style preset directly
- Validate the style name against available presets

**If no style flag:**

Offer two paths:

**Path A: Direct Selection**
Show the preset list and let user pick by name:
- Bold Signal
- Electric Studio
- Creative Voltage
- Dark Botanical
- Notebook Tabs
- Pastel Geometry
- Split Pastel
- Vintage Editorial
- Neon Cyber
- Terminal Green
- Swiss Modern
- Paper & Ink

**Path B: Preview-Based Discovery (recommended)**
1. Based on the "feeling" response, generate 3 mini HTML preview files
2. Each preview shows typography, colors, and animation style on a single title slide
3. Save previews to a temp location and show file paths
4. User views and picks their favorite

Preview recommendations by mood:
- **Impressed/Confident**: Bold Signal, Electric Studio, Dark Botanical
- **Excited/Energized**: Creative Voltage, Neon Cyber, Split Pastel
- **Calm/Focused**: Notebook Tabs, Paper & Ink, Swiss Modern
- **Inspired/Moved**: Dark Botanical, Vintage Editorial, Pastel Geometry

### Step 4: Generate Presentation

Create a single, self-contained HTML file with:

**Required structure:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Presentation Title]</title>
    <!-- Google Fonts -->
    <!-- All CSS inline -->
    <style>
        /* CSS variables for colors */
        /* Viewport fitting base styles */
        /* Typography with clamp() */
        /* Slide styles */
        /* Animation keyframes */
        /* Responsive breakpoints */
    </style>
</head>
<body>
    <section class="slide title-slide">...</section>
    <section class="slide">...</section>
    <!-- More slides -->
    <nav class="nav-dots">...</nav>
    <script>
        // SlidePresentation controller
        // Keyboard/touch navigation
        // Scroll-triggered animations
    </script>
</body>
</html>
```

**Critical requirements:**
- Every slide must fit exactly in viewport (100vh/100dvh, overflow: hidden)
- All font sizes use `clamp(min, preferred, max)` for responsive scaling
- Content density limits: max 5-6 bullet points per slide
- Include keyboard navigation (arrows, space)
- Include touch/swipe support
- Include progress indicator
- Respect `prefers-reduced-motion`

**Animation patterns:**
- Use CSS keyframes for entrance animations
- Trigger animations on scroll/visibility
- Stagger multiple elements with animation-delay

### Step 5: Output

Generate:
1. `[presentation-name].html` - The complete presentation

Confirm:
- File location
- How to open (browser)
- Navigation controls

## Output Format

After generation:

```
## Presentation Created

**File:** [filename].html
**Slides:** [count]
**Style:** [style name]

**To view:**
Open [filename].html in your browser

**Navigation:**
- Arrow keys or space to advance
- Click dots to jump to slides
- Swipe on touch devices
```

## Available Style Presets

| Preset | Vibe | Best For |
|--------|------|----------|
| Bold Signal | Confident, high-impact | Pitch decks, keynotes |
| Electric Studio | Clean, professional | Agency presentations |
| Creative Voltage | Energetic, retro-modern | Creative pitches |
| Dark Botanical | Elegant, sophisticated | Premium brands |
| Notebook Tabs | Editorial, organized | Reports, reviews |
| Pastel Geometry | Friendly, approachable | Product overviews |
| Split Pastel | Playful, modern | Creative agencies |
| Vintage Editorial | Witty, personality-driven | Personal brands |
| Neon Cyber | Futuristic, techy | Tech startups |
| Terminal Green | Developer-focused | Dev tools, APIs |
| Swiss Modern | Minimal, precise | Corporate, data |
| Paper & Ink | Literary, thoughtful | Storytelling |

## Notes

- Zero external dependencies (no npm, no build step)
- Works in any modern browser
- Images can be embedded as base64 or referenced externally
- Warn if content exceeds density limits per slide
- Suggest splitting content if slides feel cramped

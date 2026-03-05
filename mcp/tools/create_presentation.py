"""create_presentation MCP tool - generates HTML presentations."""

import os
import re
from pathlib import Path
from typing import Any

from .styles import STYLE_PRESETS, FONT_SOURCES, get_style_by_name


# Viewport-fitting base CSS (mandatory for all presentations)
VIEWPORT_BASE_CSS = """
/* ===========================================
   VIEWPORT FITTING: MANDATORY BASE STYLES
   =========================================== */
html, body {
    height: 100%;
    overflow-x: hidden;
}

html {
    scroll-snap-type: y mandatory;
    scroll-behavior: smooth;
}

.slide {
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
    scroll-snap-align: start;
    display: flex;
    flex-direction: column;
    position: relative;
}

.slide-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-height: 100%;
    overflow: hidden;
    padding: var(--slide-padding);
}

:root {
    --title-size: clamp(1.5rem, 5vw, 4rem);
    --h2-size: clamp(1.25rem, 3.5vw, 2.5rem);
    --h3-size: clamp(1rem, 2.5vw, 1.75rem);
    --body-size: clamp(0.75rem, 1.5vw, 1.125rem);
    --small-size: clamp(0.65rem, 1vw, 0.875rem);
    --slide-padding: clamp(1rem, 4vw, 4rem);
    --content-gap: clamp(0.5rem, 2vw, 2rem);
    --element-gap: clamp(0.25rem, 1vw, 1rem);
}

.card, .container, .content-box {
    max-width: min(90vw, 1000px);
    max-height: min(80vh, 700px);
}

.feature-list, .bullet-list {
    gap: clamp(0.4rem, 1vh, 1rem);
}

.feature-list li, .bullet-list li {
    font-size: var(--body-size);
    line-height: 1.4;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
    gap: clamp(0.5rem, 1.5vw, 1rem);
}

img, .image-container {
    max-width: 100%;
    max-height: min(50vh, 400px);
    object-fit: contain;
}

@media (max-height: 700px) {
    :root {
        --slide-padding: clamp(0.75rem, 3vw, 2rem);
        --content-gap: clamp(0.4rem, 1.5vw, 1rem);
        --title-size: clamp(1.25rem, 4.5vw, 2.5rem);
        --h2-size: clamp(1rem, 3vw, 1.75rem);
    }
}

@media (max-height: 600px) {
    :root {
        --slide-padding: clamp(0.5rem, 2.5vw, 1.5rem);
        --content-gap: clamp(0.3rem, 1vw, 0.75rem);
        --title-size: clamp(1.1rem, 4vw, 2rem);
        --body-size: clamp(0.7rem, 1.2vw, 0.95rem);
    }
    .nav-dots, .keyboard-hint, .decorative {
        display: none;
    }
}

@media (max-height: 500px) {
    :root {
        --slide-padding: clamp(0.4rem, 2vw, 1rem);
        --title-size: clamp(1rem, 3.5vw, 1.5rem);
        --h2-size: clamp(0.9rem, 2.5vw, 1.25rem);
        --body-size: clamp(0.65rem, 1vw, 0.85rem);
    }
}

@media (max-width: 600px) {
    :root {
        --title-size: clamp(1.25rem, 7vw, 2.5rem);
    }
    .grid {
        grid-template-columns: 1fr;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.2s !important;
    }
    html {
        scroll-behavior: auto;
    }
}
"""


def generate_style_css(style_slug: str) -> str:
    """Generate CSS for a specific style preset."""
    preset = get_style_by_name(style_slug)
    if not preset:
        preset = STYLE_PRESETS["neon-cyber"]
    
    colors = preset["colors"]
    fonts = preset["fonts"]
    
    # Get font URLs
    display_font = fonts["display"]
    body_font = fonts["body"]
    display_url = FONT_SOURCES.get(display_font, ("", ""))[1]
    body_url = FONT_SOURCES.get(body_font, ("", ""))[1]
    
    # Build CSS custom properties for colors
    color_vars = []
    for key, value in colors.items():
        if isinstance(value, list):
            for i, color in enumerate(value):
                color_vars.append(f"--{key}_{i}: {color};")
        else:
            color_vars.append(f"--{key}: {value};")
    
    return f"""
/* Font imports */
@import url('{display_url}');
@import url('{body_url}');

:root {{
    /* Colors */
    {chr(10).join(f'    {v}' for v in color_vars)}
    
    /* Typography */
    --font-display: '{display_font}', sans-serif;
    --font-body: '{body_font}', sans-serif;
    
    /* Animation */
    --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
    --duration-normal: 0.6s;
    --duration-fast: 0.3s;
}}

/* Base styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--font-body);
    background: var(--bg_primary);
    color: var(--text_primary);
    line-height: 1.6;
}}

h1, h2, h3 {{
    font-family: var(--font-display);
    font-weight: {fonts['display_weight']};
}}

/* Animation classes */
.reveal {{
    opacity: 0;
    transform: translateY(30px);
    transition: opacity var(--duration-normal) var(--ease-out-expo),
                transform var(--duration-normal) var(--ease-out-expo);
}}

.visible .reveal {{
    opacity: 1;
    transform: translateY(0);
}}

.reveal-delay-1 {{ transition-delay: 0.1s; }}
.reveal-delay-2 {{ transition-delay: 0.2s; }}
.reveal-delay-3 {{ transition-delay: 0.3s; }}
.reveal-delay-4 {{ transition-delay: 0.4s; }}

/* Navigation dots */
.nav-dots {{
    position: fixed;
    right: clamp(0.5rem, 2vw, 1.5rem);
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    z-index: 100;
}}

.nav-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.3);
    cursor: pointer;
    transition: all 0.3s;
}}

.nav-dot.active {{
    background: var(--accent, var(--text_primary));
    transform: scale(1.3);
}}

/* Keyboard hint */
.keyboard-hint {{
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    font-size: var(--small-size);
    color: var(--text_secondary, #888);
    opacity: 0.6;
}}
"""


def generate_slide_html(slide_num: int, total_slides: int, slide_type: str, 
                        title: str, content: list[str], style_slug: str,
                        image: str | None = None) -> str:
    """Generate HTML for a single slide."""
    preset = get_style_by_name(style_slug) or STYLE_PRESETS["neon-cyber"]
    category = preset["category"]
    
    # Animation style based on preset
    animation_style = preset["animation_style"]
    
    # Slide number indicator
    slide_indicator = f'<span class="slide-number">{str(slide_num).zfill(2)}</span>'
    
    # Build content based on slide type
    if slide_type == "title":
        content_html = f"""
        <div class="slide-content" style="text-align: center;">
            <div class="reveal">
                {slide_indicator}
                <h1 style="font-size: var(--title-size); margin-bottom: var(--content-gap);">{title}</h1>
                {f'<p style="font-size: var(--h2-size); opacity: 0.8;">{content[0]}</p>' if content else ''}
            </div>
        </div>
        """
    elif slide_type == "content":
        bullets = "\n".join(f'<li class="reveal reveal-delay-{i+1}">{item}</li>' 
                           for i, item in enumerate(content[:6]))
        content_html = f"""
        <div class="slide-content">
            <div class="reveal">
                {slide_indicator}
                <h2 style="font-size: var(--h2-size); margin-bottom: var(--content-gap);">{title}</h2>
            </div>
            <ul class="bullet-list" style="list-style: none; padding: 0;">
                {bullets}
            </ul>
        </div>
        """
    elif slide_type == "image":
        content_html = f"""
        <div class="slide-content">
            <div class="reveal">
                {slide_indicator}
                <h2 style="font-size: var(--h2-size); margin-bottom: var(--content-gap);">{title}</h2>
            </div>
            {f'<div class="reveal reveal-delay-1"><img src="{image}" alt="{title}" style="border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);"></div>' if image else ''}
        </div>
        """
    else:  # quote or default
        content_html = f"""
        <div class="slide-content" style="text-align: center;">
            <div class="reveal">
                <blockquote style="font-size: var(--h2-size); font-style: italic; max-width: 80%; margin: 0 auto;">
                    "{content[0] if content else ''}"
                </blockquote>
                {f'<p class="reveal reveal-delay-1" style="margin-top: var(--content-gap); opacity: 0.7;">— {content[1]}</p>' if len(content) > 1 else ''}
            </div>
        </div>
        """
    
    return f"""
    <section class="slide" data-slide="{slide_num}">
        {content_html}
    </section>
    """


def generate_presentation_html(topic: str, key_messages: list[str], 
                               num_slides: int, audience: str, tone: str,
                               style: str, images: list[str]) -> str:
    """Generate complete HTML presentation."""
    
    # Validate style
    preset = get_style_by_name(style)
    if not preset:
        style = "neon-cyber"
        preset = STYLE_PRESETS[style]
    
    # Distribute key messages across slides
    slides_content = []
    messages_per_slide = max(1, len(key_messages) // (num_slides - 1))
    
    # Title slide
    slides_content.append({
        "type": "title",
        "title": topic,
        "content": [f"A presentation for {audience}"]
    })
    
    # Content slides
    for i in range(1, num_slides):
        start_idx = (i - 1) * messages_per_slide
        end_idx = start_idx + messages_per_slide
        slide_messages = key_messages[start_idx:end_idx]
        
        # Determine slide type
        if images and i <= len(images):
            slide_type = "image"
            image = images[i - 1]
        elif i == num_slides - 1 and tone == "energetic":
            slide_type = "quote"
            image = None
        else:
            slide_type = "content"
            image = None
        
        # Generate slide title
        if slide_messages:
            slide_title = slide_messages[0] if slide_type == "image" else f"Key Point {i}"
        else:
            slide_title = f"Slide {i}"
        
        slides_content.append({
            "type": slide_type,
            "title": slide_title,
            "content": slide_messages[:6] if slide_type == "content" else slide_messages,
            "image": image
        })
    
    # Generate slides HTML
    slides_html = "\n".join(
        generate_slide_html(
            i + 1, 
            len(slides_content), 
            slide["type"],
            slide["title"],
            slide["content"],
            style,
            slide.get("image")
        )
        for i, slide in enumerate(slides_content)
    )
    
    # Navigation dots
    nav_dots = "\n".join(
        f'<div class="nav-dot{" active" if i == 0 else ""}" data-slide="{i + 1}"></div>'
        for i in range(len(slides_content))
    )
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    
    <style>
{VIEWPORT_BASE_CSS}
{generate_style_css(style)}
    </style>
</head>
<body>
    {slides_html}
    
    <!-- Navigation -->
    <nav class="nav-dots">
        {nav_dots}
    </nav>
    
    <div class="keyboard-hint">Use arrow keys or swipe to navigate</div>
    
    <script>
        // Intersection Observer for reveal animations
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, {{ threshold: 0.3 }});

        document.querySelectorAll('.slide').forEach(slide => {{
            observer.observe(slide);
        }});

        // Navigation
        let currentSlide = 1;
        const totalSlides = {len(slides_content)};
        const slides = document.querySelectorAll('.slide');
        const dots = document.querySelectorAll('.nav-dot');

        function goToSlide(num) {{
            if (num < 1 || num > totalSlides) return;
            currentSlide = num;
            slides[num - 1].scrollIntoView({{ behavior: 'smooth' }});
            dots.forEach((dot, i) => {{
                dot.classList.toggle('active', i === num - 1);
            }});
        }}

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight' || e.key === ' ') {{
                e.preventDefault();
                goToSlide(currentSlide + 1);
            }} else if (e.key === 'ArrowLeft') {{
                e.preventDefault();
                goToSlide(currentSlide - 1);
            }}
        }});

        // Touch navigation
        let touchStartY = 0;
        document.addEventListener('touchstart', (e) => {{
            touchStartY = e.touches[0].clientY;
        }});

        document.addEventListener('touchend', (e) => {{
            const touchEndY = e.changedTouches[0].clientY;
            const diff = touchStartY - touchEndY;
            if (Math.abs(diff) > 50) {{
                if (diff > 0) goToSlide(currentSlide + 1);
                else goToSlide(currentSlide - 1);
            }}
        }});

        // Click on dots
        dots.forEach(dot => {{
            dot.addEventListener('click', () => {{
                goToSlide(parseInt(dot.dataset.slide));
            }});
        }});

        // Track current slide via scroll
        const scrollObserver = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    currentSlide = parseInt(entry.target.dataset.slide);
                    dots.forEach((dot, i) => {{
                        dot.classList.toggle('active', i === currentSlide - 1);
                    }});
                }}
            }});
        }}, {{ threshold: 0.5 }});

        slides.forEach(slide => scrollObserver.observe(slide));
    </script>
</body>
</html>"""


def create_presentation(
    topic: str,
    key_messages: list[str],
    num_slides: int = 5,
    audience: str = "general",
    tone: str = "professional",
    style: str = "neon-cyber",
    images: list[str] = None,
    output_path: str | None = None,
) -> str:
    """
    Create an HTML presentation.
    
    Args:
        topic: Main topic/title of the presentation
        key_messages: Key messages to distribute across slides
        num_slides: Number of slides (3-30)
        audience: Target audience
        tone: Presentation tone
        style: Style preset slug
        images: Optional list of image URLs
        output_path: Output directory path
    
    Returns:
        Path to the generated HTML file
    """
    if images is None:
        images = []
    
    # Generate the HTML
    html_content = generate_presentation_html(
        topic=topic,
        key_messages=key_messages,
        num_slides=num_slides,
        audience=audience,
        tone=tone,
        style=style,
        images=images,
    )
    
    # Determine output path
    if output_path is None:
        output_path = os.getcwd()
    
    # Create safe filename from topic
    safe_topic = re.sub(r'[^\w\s-]', '', topic).strip().lower()
    safe_topic = re.sub(r'[-\s]+', '-', safe_topic)[:50]
    filename = f"{safe_topic}-presentation.html"
    
    # Write the file
    output_file = Path(output_path) / filename
    output_file.write_text(html_content, encoding="utf-8")
    
    return str(output_file.absolute())

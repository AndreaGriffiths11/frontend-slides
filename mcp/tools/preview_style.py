"""preview_style MCP tool - generates sample HTML preview for a style."""

from .styles import get_style_by_name, FONT_SOURCES, STYLE_PRESETS
from .create_presentation import VIEWPORT_BASE_CSS


def generate_preview_html(style_slug: str) -> str | None:
    """Generate a single-slide preview demonstrating the style."""
    preset = get_style_by_name(style_slug)
    if not preset:
        return None
    
    colors = preset["colors"]
    fonts = preset["fonts"]
    animation_style = preset["animation_style"]
    
    # Get font URLs
    display_font = fonts["display"]
    body_font = fonts["body"]
    display_url = FONT_SOURCES.get(display_font, ("", ""))[1]
    body_url = FONT_SOURCES.get(body_font, ("", ""))[1]
    
    # Build color CSS variables
    color_vars = []
    for key, value in colors.items():
        if isinstance(value, list):
            for i, color in enumerate(value):
                color_vars.append(f"--{key}_{i}: {color};")
        else:
            color_vars.append(f"--{key}: {value};")
    
    # Style-specific decorative elements
    if preset["category"] == "dark":
        bg_style = f"background: {colors.get('bg_primary', '#0a0f1c')};"
        if style_slug == "neon-cyber" or "neon" in style_slug.lower():
            decoration = """
            <div class="decoration" style="position: absolute; top: 20%; right: 10%; width: 200px; height: 200px; background: radial-gradient(circle, var(--accent) 0%, transparent 70%); opacity: 0.3; filter: blur(40px);"></div>
            <div class="decoration" style="position: absolute; bottom: 20%; left: 10%; width: 150px; height: 150px; background: radial-gradient(circle, var(--accent_secondary, var(--accent)) 0%, transparent 70%); opacity: 0.2; filter: blur(30px);"></div>
            """
        elif style_slug == "dark-botanical":
            decoration = """
            <div class="decoration" style="position: absolute; top: 10%; right: 15%; width: 300px; height: 300px; background: radial-gradient(ellipse, var(--accent_secondary, #e8b4b8) 0%, transparent 60%); opacity: 0.15; filter: blur(60px);"></div>
            <div class="decoration" style="position: absolute; bottom: 15%; left: 10%; width: 250px; height: 250px; background: radial-gradient(ellipse, var(--accent, #d4a574) 0%, transparent 60%); opacity: 0.1; filter: blur(50px);"></div>
            """
        elif style_slug == "bold-signal":
            decoration = f"""
            <div class="decoration" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60%; max-width: 600px; aspect-ratio: 1; background: {colors.get('card_bg', '#FF5722')}; opacity: 0.15; border-radius: 8px;"></div>
            """
        else:
            decoration = ""
    else:
        # Light theme
        bg_style = f"background: {colors.get('bg_primary', '#ffffff')};"
        if style_slug == "notebook-tabs":
            decoration = f"""
            <div class="decoration" style="position: absolute; right: 0; top: 20%; display: flex; flex-direction: column; gap: 0.5rem;">
                <div style="background: {colors.get('tab_colors', ['#98d4bb'])[0]}; padding: 0.5rem 1.5rem 0.5rem 1rem; border-radius: 4px 0 0 4px; font-size: 0.7rem; color: #333;">SECTION</div>
                <div style="background: {colors.get('tab_colors', ['#98d4bb', '#c7b8ea'])[1]}; padding: 0.5rem 1.5rem 0.5rem 1rem; border-radius: 4px 0 0 4px; font-size: 0.7rem; color: #333;">TAB</div>
            </div>
            """
        elif style_slug == "split-pastel":
            decoration = f"""
            <div class="decoration" style="position: absolute; inset: 0; display: flex; pointer-events: none;">
                <div style="flex: 1; background: {colors.get('bg_primary', '#f5e6dc')};"></div>
                <div style="flex: 1; background: {colors.get('bg_secondary', '#e4dff0')};"></div>
            </div>
            """
        else:
            decoration = ""
    
    # Animation timing based on style
    if animation_style in ["energetic", "playful"]:
        anim_duration = "0.5s"
        anim_ease = "cubic-bezier(0.34, 1.56, 0.64, 1)"
    elif animation_style in ["elegant", "literary"]:
        anim_duration = "0.8s"
        anim_ease = "cubic-bezier(0.25, 0.1, 0.25, 1)"
    elif animation_style in ["clean", "precise"]:
        anim_duration = "0.4s"
        anim_ease = "cubic-bezier(0.4, 0, 0.2, 1)"
    else:
        anim_duration = "0.6s"
        anim_ease = "cubic-bezier(0.16, 1, 0.3, 1)"
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{preset['name']} - Style Preview</title>
    
    <style>
{VIEWPORT_BASE_CSS}
        
        @import url('{display_url}');
        @import url('{body_url}');
        
        :root {{
            /* Colors */
            {chr(10).join(f'            {v}' for v in color_vars)}
            
            /* Typography */
            --font-display: '{display_font}', sans-serif;
            --font-body: '{body_font}', sans-serif;
            
            /* Animation */
            --ease-out-expo: {anim_ease};
            --duration-normal: {anim_duration};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-body);
            {bg_style}
            color: var(--text_primary, #ffffff);
            overflow: hidden;
        }}
        
        .slide {{
            width: 100vw;
            height: 100vh;
            height: 100dvh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }}
        
        h1 {{
            font-family: var(--font-display);
            font-weight: {fonts['display_weight']};
            font-size: var(--title-size);
            margin-bottom: var(--content-gap);
            text-align: center;
        }}
        
        .subtitle {{
            font-size: var(--h2-size);
            opacity: 0.8;
            text-align: center;
            margin-bottom: var(--content-gap);
        }}
        
        .style-info {{
            font-size: var(--body-size);
            opacity: 0.6;
            text-align: center;
        }}
        
        /* Animations */
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
        
        /* Badge styling for certain styles */
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: var(--small-size);
            margin: 0.25rem;
        }}
        
        /* Color swatches */
        .swatches {{
            display: flex;
            gap: 0.5rem;
            margin-top: var(--content-gap);
        }}
        
        .swatch {{
            width: 24px;
            height: 24px;
            border-radius: 4px;
            border: 1px solid rgba(128,128,128,0.3);
        }}
    </style>
</head>
<body>
    <section class="slide visible">
        {decoration}
        
        <div class="reveal">
            <h1>{preset['name']}</h1>
        </div>
        
        <p class="subtitle reveal reveal-delay-1">{preset['vibe']}</p>
        
        <p class="style-info reveal reveal-delay-2">
            {fonts['display']} + {fonts['body']} • {preset['category'].title()} theme
        </p>
        
        <div class="swatches reveal reveal-delay-3">
            {f'<div class="swatch" style="background: {colors.get("bg_primary", "#000")};"></div>'}
            {f'<div class="swatch" style="background: {colors.get("text_primary", "#fff")};"></div>'}
            {f'<div class="swatch" style="background: {colors.get("accent", "#00ffcc")};"></div>'}
        </div>
    </section>
    
    <script>
        // Trigger animations on load
        document.addEventListener('DOMContentLoaded', () => {{
            document.querySelector('.slide').classList.add('visible');
        }});
    </script>
</body>
</html>"""


def preview_style(style_name: str) -> str | None:
    """
    Generate a sample HTML preview for a specific style.
    
    Args:
        style_name: The style name or slug (e.g., "neon-cyber" or "Neon Cyber")
    
    Returns:
        HTML string of the preview, or None if style not found.
    """
    return generate_preview_html(style_name)

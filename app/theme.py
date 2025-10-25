"""
Centralized theme configuration for Fleetwise
Follows Reflex best practices for consistent styling
"""

# Color Palette - Professional Dark Blue Theme (matching target design)
COLORS = {
    # Primary - Dark blue background
    "primary_dark": "#0f1629",      # Deep navy background
    "primary_main": "#1a1f3a",      # Main background
    "primary_light": "#252b4a",     # Light background
    
    # Secondary - Bright blue accents
    "secondary_dark": "#1e40af",    # Dark blue
    "secondary_main": "#3b82f6",    # Bright blue (buttons, links)
    "secondary_light": "#60a5fa",   # Light blue (hover)
    
    # Surfaces - Card and table backgrounds
    "surface_dark": "#1a1f3a",      # Dark surface
    "surface_main": "#252b4a",      # Main surface (cards, rows)
    "surface_light": "#2d3454",     # Light surface (hover)
    
    # Text
    "text_primary": "#ffffff",      # White
    "text_secondary": "#e2e8f0",    # Light gray
    "text_tertiary": "#94a3b8",     # Medium gray
    
    # Semantic
    "success": "#10b981",           # Green
    "error": "#ef4444",             # Red
    "warning": "#f59e0b",           # Amber
    "info": "#3b82f6",              # Blue
    
    # Borders
    "border_dark": "#1e293b",
    "border_main": "#374151",       # Subtle borders
    "border_light": "#4b5563",
}

# Typography
TYPOGRAPHY = {
    "font_family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    "font_size_xs": "0.75rem",      # 12px
    "font_size_sm": "0.875rem",     # 14px
    "font_size_base": "1rem",       # 16px
    "font_size_lg": "1.125rem",     # 18px
    "font_size_xl": "1.25rem",      # 20px
    "font_size_2xl": "1.5rem",      # 24px
    "font_size_3xl": "1.875rem",    # 30px
    
    "font_weight_normal": "400",
    "font_weight_medium": "500",
    "font_weight_semibold": "600",
    "font_weight_bold": "700",
}

# Spacing
SPACING = {
    "xs": "0.25rem",    # 4px
    "sm": "0.5rem",     # 8px
    "md": "1rem",       # 16px
    "lg": "1.5rem",     # 24px
    "xl": "2rem",       # 32px
    "2xl": "3rem",      # 48px
}

# Border Radius
RADIUS = {
    "sm": "0.375rem",   # 6px
    "md": "0.5rem",     # 8px
    "lg": "0.75rem",    # 12px
    "xl": "1rem",       # 16px
    "full": "9999px",
}

# Shadows
SHADOWS = {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
}

# Responsive Breakpoints
BREAKPOINTS = {
    "mobile": "640px",
    "tablet": "768px",
    "desktop": "1024px",
    "wide": "1280px",
}

# Component-specific styles
COMPONENT_STYLES = {
    "button": {
        "primary": f"""
            bg-gradient-to-r from-{COLORS['secondary_main']} to-{COLORS['secondary_light']}
            text-{COLORS['text_primary']}
            font-{TYPOGRAPHY['font_weight_semibold']}
            px-6 py-2.5 rounded-lg
            hover:shadow-lg hover:from-{COLORS['secondary_dark']} hover:to-{COLORS['secondary_main']}
            focus:ring-2 focus:ring-{COLORS['secondary_main']} focus:ring-offset-2 focus:ring-offset-{COLORS['primary_main']}
            transition-all duration-200
            disabled:opacity-50 disabled:cursor-not-allowed
        """,
        "secondary": f"""
            bg-{COLORS['surface_light']}
            text-{COLORS['text_secondary']}
            font-{TYPOGRAPHY['font_weight_semibold']}
            px-6 py-2.5 rounded-lg
            hover:bg-{COLORS['border_light']}
            focus:ring-2 focus:ring-{COLORS['secondary_main']}
            transition-all duration-200
        """,
    },
    "input": f"""
        w-full px-4 py-2.5
        bg-{COLORS['surface_dark']}
        text-{COLORS['text_primary']}
        border border-{COLORS['border_main']}
        rounded-lg
        placeholder-{COLORS['text_tertiary']}
        focus:ring-2 focus:ring-{COLORS['secondary_main']} focus:border-transparent
        transition-all duration-200
        hover:border-{COLORS['border_light']}
    """,
    "card": f"""
        bg-gradient-to-br from-{COLORS['surface_main']} to-{COLORS['primary_light']}
        rounded-xl shadow-lg
        border border-{COLORS['border_main']}
        hover:border-{COLORS['border_light']}
        transition-colors duration-200
    """,
    "sidebar": f"""
        w-64 h-screen
        bg-gradient-to-b from-{COLORS['primary_main']} to-{COLORS['primary_dark']}
        border-r border-{COLORS['border_main']}
        flex flex-col
    """,
    "nav_item": f"""
        flex items-center gap-3 px-4 py-3
        text-{COLORS['text_secondary']}
        font-{TYPOGRAPHY['font_weight_medium']}
        rounded-lg
        hover:bg-{COLORS['secondary_main']} hover:text-{COLORS['text_primary']}
        transition-all duration-200
    """,
}

# Gradient definitions
GRADIENTS = {
    "primary": f"linear-gradient(135deg, {COLORS['primary_main']} 0%, {COLORS['primary_light']} 100%)",
    "secondary": f"linear-gradient(135deg, {COLORS['secondary_dark']} 0%, {COLORS['secondary_main']} 100%)",
    "accent": f"linear-gradient(135deg, {COLORS['secondary_main']} 0%, {COLORS['secondary_light']} 100%)",
}

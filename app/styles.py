"""
Centralized styling module for Fleetwise
Reflex best practices for responsive design and maintainability
"""

from app.theme import COLORS, TYPOGRAPHY, SPACING, RADIUS, SHADOWS

# Base styles
BASE_STYLES = {
    "font_family": TYPOGRAPHY["font_family"],
    "background": COLORS["primary_dark"],
}

# Layout styles
LAYOUT = {
    "container": f"""
        flex min-h-screen
        bg-gradient-to-br from-{COLORS['primary_dark']} via-{COLORS['primary_main']} to-{COLORS['primary_light']}
    """,
    "sidebar_container": f"""
        w-64 h-screen
        bg-gradient-to-b from-{COLORS['primary_main']} to-{COLORS['primary_dark']}
        border-r border-{COLORS['border_main']}
        flex flex-col
        shrink-0
        fixed md:relative
        z-50 md:z-auto
        transition-transform duration-300
    """,
    "main_content": f"""
        flex-1
        flex flex-col
        bg-gradient-to-br from-{COLORS['primary_dark']} via-{COLORS['surface_main']} to-{COLORS['primary_main']}
        overflow-auto
        w-full md:w-auto
        ml-0 md:ml-0
    """,
    "page_header": f"""
        flex justify-between items-center
        w-full p-6
        border-b border-{COLORS['border_main']}
        bg-gradient-to-r from-{COLORS['surface_main']} to-{COLORS['primary_light']}
        sticky top-0 z-40
    """,
    "page_content": f"""
        flex-1 p-6 space-y-6
        overflow-y-auto
    """,
}

# Typography styles
TEXT = {
    "heading_1": f"""
        text-3xl md:text-4xl
        font-{TYPOGRAPHY['font_weight_bold']}
        text-{COLORS['text_primary']}
        tracking-tight
    """,
    "heading_2": f"""
        text-2xl md:text-3xl
        font-{TYPOGRAPHY['font_weight_bold']}
        text-{COLORS['text_primary']}
    """,
    "heading_3": f"""
        text-xl md:text-2xl
        font-{TYPOGRAPHY['font_weight_semibold']}
        text-{COLORS['text_primary']}
    """,
    "body": f"""
        text-base
        font-{TYPOGRAPHY['font_weight_normal']}
        text-{COLORS['text_secondary']}
        leading-relaxed
    """,
    "body_small": f"""
        text-sm
        font-{TYPOGRAPHY['font_weight_normal']}
        text-{COLORS['text_tertiary']}
    """,
    "label": f"""
        text-sm
        font-{TYPOGRAPHY['font_weight_medium']}
        text-{COLORS['text_secondary']}
    """,
}

# Component styles
COMPONENTS = {
    "button_primary": f"""
        bg-gradient-to-r from-{COLORS['secondary_main']} to-{COLORS['secondary_light']}
        text-{COLORS['text_primary']}
        font-{TYPOGRAPHY['font_weight_semibold']}
        px-6 py-2.5
        rounded-lg
        hover:shadow-lg hover:from-{COLORS['secondary_dark']} hover:to-{COLORS['secondary_main']}
        focus:ring-2 focus:ring-{COLORS['secondary_main']} focus:ring-offset-2 focus:ring-offset-{COLORS['primary_main']}
        transition-all duration-200
        disabled:opacity-50 disabled:cursor-not-allowed
        text-sm md:text-base
    """,
    "button_secondary": f"""
        bg-{COLORS['surface_light']}
        text-{COLORS['text_secondary']}
        font-{TYPOGRAPHY['font_weight_semibold']}
        px-6 py-2.5
        rounded-lg
        hover:bg-{COLORS['border_light']} hover:text-{COLORS['text_primary']}
        focus:ring-2 focus:ring-{COLORS['secondary_main']}
        transition-all duration-200
        text-sm md:text-base
    """,
    "button_danger": f"""
        bg-{COLORS['error']}
        text-{COLORS['text_primary']}
        font-{TYPOGRAPHY['font_weight_semibold']}
        px-6 py-2.5
        rounded-lg
        hover:shadow-lg hover:bg-red-700
        focus:ring-2 focus:ring-{COLORS['error']}
        transition-all duration-200
        text-sm md:text-base
    """,
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
        text-sm md:text-base
    """,
    "card": f"""
        bg-gradient-to-br from-{COLORS['surface_main']} to-{COLORS['primary_light']}
        rounded-xl shadow-lg
        border border-{COLORS['border_main']}
        hover:border-{COLORS['border_light']}
        transition-colors duration-200
        p-6
    """,
    "modal": f"""
        fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2
        bg-gradient-to-br from-{COLORS['surface_main']} to-{COLORS['primary_light']}
        rounded-xl shadow-2xl
        border border-{COLORS['border_main']}
        p-6 w-full max-w-md z-50
        space-y-4
    """,
    "table_header": f"""
        flex px-4 py-3
        border-b border-{COLORS['border_main']}
        bg-{COLORS['surface_dark']}
        sticky top-0 z-10
    """,
    "table_row": f"""
        flex px-4 py-3
        border-b border-{COLORS['border_main']}
        hover:bg-{COLORS['surface_light']}/50
        transition-colors duration-200
        items-center text-sm md:text-base
    """,
    "badge_success": f"""
        px-3 py-1
        text-xs md:text-sm
        font-{TYPOGRAPHY['font_weight_semibold']}
        text-{COLORS['success']}
        bg-{COLORS['success']}/10
        border border-{COLORS['success']}/30
        rounded-full
    """,
    "badge_error": f"""
        px-3 py-1
        text-xs md:text-sm
        font-{TYPOGRAPHY['font_weight_semibold']}
        text-{COLORS['error']}
        bg-{COLORS['error']}/10
        border border-{COLORS['error']}/30
        rounded-full
    """,
    "alert_error": f"""
        bg-{COLORS['error']}/10
        border border-{COLORS['error']}/30
        text-{COLORS['error']}
        px-4 py-3
        rounded-lg
        text-sm md:text-base
    """,
    "alert_success": f"""
        bg-{COLORS['success']}/10
        border border-{COLORS['success']}/30
        text-{COLORS['success']}
        px-4 py-3
        rounded-lg
        text-sm md:text-base
    """,
}

# Sidebar styles
SIDEBAR = {
    "container": f"""
        w-64 h-screen
        bg-gradient-to-b from-{COLORS['primary_main']} to-{COLORS['primary_dark']}
        border-r border-{COLORS['border_main']}
        flex flex-col
        shrink-0
    """,
    "header": f"""
        flex items-center gap-3 p-4
        border-b border-{COLORS['border_main']}
    """,
    "logo": f"""
        text-2xl font-{TYPOGRAPHY['font_weight_bold']}
        text-{COLORS['text_primary']}
    """,
    "nav": f"""
        flex-1 p-4 space-y-2
    """,
    "nav_item": f"""
        flex items-center gap-3 px-4 py-3
        text-{COLORS['text_secondary']}
        font-{TYPOGRAPHY['font_weight_medium']}
        rounded-lg
        hover:bg-{COLORS['secondary_main']} hover:text-{COLORS['text_primary']}
        transition-all duration-200
        text-sm md:text-base
    """,
    "footer": f"""
        p-4 border-t border-{COLORS['border_main']}
    """,
}

# Responsive utilities
RESPONSIVE = {
    "hidden_mobile": "hidden md:block",
    "hidden_desktop": "md:hidden",
    "flex_col_mobile": "flex flex-col md:flex-row",
    "grid_mobile": "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
    "text_responsive": "text-sm md:text-base lg:text-lg",
    "padding_responsive": "p-4 md:p-6 lg:p-8",
}

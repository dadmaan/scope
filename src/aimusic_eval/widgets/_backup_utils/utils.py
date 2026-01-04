"""
Shared Utility Functions

Common utilities used across widget modules.
"""

import logging

logger = logging.getLogger(__name__)


def get_safe_value(widgets_dict, key, default=''):
    """
    Safely get widget value with fallback to default.
    
    Args:
        widgets_dict (dict): Dictionary containing widgets
        key (str): Widget key to retrieve
        default: Default value if widget not found or has no value
        
    Returns:
        Widget value or default
        
    Example:
        >>> system_name = get_safe_value(setup_widgets, 'system_name', 'Unknown')
    """
    try:
        if key in widgets_dict:
            widget = widgets_dict[key]
            if hasattr(widget, 'value'):
                return widget.value
        return default
    except Exception as e:
        logger.debug(f"Error getting safe value for key '{key}': {e}")
        return default

"""
Core Utilities Package

Pure Python utilities for validation, export, analysis, and helpers.
These utilities can be used independently of Jupyter widgets.

Modules:
    - exporters: Export data to JSON, Markdown, CSV
    - validators: Validate data structures
    - helpers: Helper functions for charts and calculations
    - comparative_analysis: Multi-system comparison logic
"""

import logging

logger = logging.getLogger(__name__)

# Re-export commonly used modules for convenience
from . import exporters
from . import validators
from . import helpers
from . import comparative_analysis

__all__ = [
    'exporters',
    'validators',
    'helpers',
    'comparative_analysis',
    'get_safe_value',
]


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

"""
AI Music Evaluation Framework

A comprehensive framework for systematic evaluation of AI music generation systems.

Main Components:
    - widgets: Interactive Jupyter widgets for data collection
    - core: Pure Python utilities for validation, export, and analysis
    - schemas: JSON schema definitions
    - templates: Data model classes

Quick Start:
    >>> from aimusic_eval.widgets import create_session_logging_tabs
    >>> from aimusic_eval.core import exporters, validators
    
    # Create session logging interface
    >>> session_tabs = create_session_logging_tabs()
    
    # Validate and export data
    >>> result = validators.validate_session_log(data)
    >>> exporters.export_to_json(data, 'output.json')

For more information, see the documentation or example notebooks.
"""

from .__version__ import __version__

__all__ = ['__version__']

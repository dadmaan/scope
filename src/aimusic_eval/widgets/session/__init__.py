"""
Session Package - Core Session Logging

This package provides all widgets for core session logging functionality,
including session setup, generation attempts, refinement, post-processing,
DAW integration, reflections, and session statistics.

Main entry point: create_session_logging_tabs()
"""

import logging
import ipywidgets as widgets

# Import all sub-tab creators
from .setup_tab import create_session_setup_tab
from .generation_tab import create_generation_attempts_tab
from .refinement_tab import create_refinement_tab
from .post_processing_tab import create_post_processing_tab
from .daw_integration_tab import create_daw_integration_tab
from .reflections_tab import create_reflections_tab
from .session_statistics_tab import create_session_statistics_tab

# Configure module logger
logger = logging.getLogger(__name__)


def create_session_logging_tabs():
    """
    Create the complete Core Session Logging section with nested tabs.
    
    This function assembles all 7 core session sub-tabs:
    - Setup: Session metadata, creative context, session management
    - Generation: Re-runnable generation attempts logging
    - Refinement: Prompt refinement process
    - Post-Processing: Audio post-processing steps
    - DAW Integration: DAW integration testing
    - Reflections: Qualitative session feedback
    - Session Statistics: Quantitative metrics and export
    
    Returns:
        dict: {
            'container': Tab widget with 7 sub-tabs,
            'widgets': {
                'setup': {...},
                'generation': {...},
                'refinement': {...},
                'post_processing': {...},
                'daw_integration': {...},
                'reflections': {...},
                'session_statistics': {...}
            }
        }
    """
    logger.debug("Assembling Core Session Logging tabs")
    
    # Create all sub-tabs
    setup = create_session_setup_tab()
    generation = create_generation_attempts_tab()
    refinement = create_refinement_tab()
    post_processing = create_post_processing_tab()
    daw_integration = create_daw_integration_tab()
    reflections = create_reflections_tab()
    session_statistics = create_session_statistics_tab()
    
    # Create nested tab container
    nested_tabs = widgets.Tab()
    nested_tabs.children = [
        setup['container'],
        generation['container'],
        refinement['container'],
        post_processing['container'],
        daw_integration['container'],
        reflections['container'],
        session_statistics['container']
    ]
    
    # Set tab titles
    nested_tabs.set_title(0, '🚀 Session Setup & Metadata')
    nested_tabs.set_title(1, 'Generation')
    nested_tabs.set_title(2, 'Refinement')
    nested_tabs.set_title(3, 'Post-Processing')
    nested_tabs.set_title(4, 'DAW Integration')
    nested_tabs.set_title(5, 'Reflections')
    nested_tabs.set_title(6, 'Session Statistics')
    
    logger.debug("✅ Core Session Logging tabs assembled (7 sub-tabs)")
    
    return {
        'container': nested_tabs,
        'widgets': {
            'setup': setup['widgets'],
            'generation': generation['widgets'],
            'refinement': refinement['widgets'],
            'post_processing': post_processing['widgets'],
            'daw_integration': daw_integration['widgets'],
            'reflections': reflections['widgets'],
            'session_statistics': session_statistics['widgets']
        }
    }


# Public API
__all__ = ['create_session_logging_tabs']

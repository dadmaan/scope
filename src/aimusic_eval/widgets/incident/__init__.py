"""
Incident Package - Critical Incident Documentation

This package provides all widgets for critical incident documentation,
including classification, context analysis, learnings, and reproducibility tracking.

Main entry point: create_incident_tabs()
"""

import logging
import ipywidgets as widgets

# Import all sub-tab creators
from .classification_tab import create_incident_classification_tab
from .context_tab import create_incident_context_tab
from .learnings_tab import create_incident_learnings_tab
from .documentation_tab import create_incident_documentation_tab

# Configure module logger
logger = logging.getLogger(__name__)


def create_incident_tabs():
    """
    Create the complete Critical Incident section with nested tabs.
    
    This function assembles all 4 critical incident sub-tabs:
    - Classification & Description: Incident metadata and description
    - Context & Analysis: Context, autoethnography, and analysis
    - Root Cause & Learnings: Root cause analysis and 3D learnings
    - Reproducibility & Documentation: Reproducibility and documentation
    
    Returns:
        dict: {
            'container': Tab widget with 4 sub-tabs,
            'widgets': {
                'classification': {...},
                'context': {...},
                'learnings': {...},
                'documentation': {...}
            }
        }
    """
    logger.debug("Assembling Critical Incident tabs")
    
    # Create all sub-tabs
    classification = create_incident_classification_tab()
    context = create_incident_context_tab()
    learnings = create_incident_learnings_tab()
    documentation = create_incident_documentation_tab()
    
    # Create nested tab container
    nested_tabs = widgets.Tab()
    nested_tabs.children = [
        classification['container'],
        context['container'],
        learnings['container'],
        documentation['container']
    ]
    
    # Set tab titles
    nested_tabs.set_title(0, 'Classification & Description')
    nested_tabs.set_title(1, 'Context & Analysis')
    nested_tabs.set_title(2, 'Root Cause & Learnings')
    nested_tabs.set_title(3, 'Reproducibility & Documentation')
    
    logger.debug("✅ Critical Incident tabs assembled (4 sub-tabs)")
    
    return {
        'container': nested_tabs,
        'widgets': {
            'classification': classification['widgets'],
            'context': context['widgets'],
            'learnings': learnings['widgets'],
            'documentation': documentation['widgets']
        }
    }


# Public API
__all__ = ['create_incident_tabs']

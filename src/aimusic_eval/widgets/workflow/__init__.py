"""
Workflow Package - Workflow Phase Documentation

This package provides all widgets for complete workflow phase documentation,
including phase setup, execution tracking, phase-specific details, outcome
analysis, and creative experience reflection.

Main entry point: create_workflow_tabs()
"""

import logging
import ipywidgets as widgets

# Import all sub-tab creators
from .setup_tab import create_workflow_setup_tab
from .execution_tab import create_workflow_execution_tab
from .phase_specific_tab import create_workflow_phase_specific_tab
from .outcome_tab import create_workflow_outcome_tab
from .experience_tab import create_workflow_experience_tab

# Configure module logger
logger = logging.getLogger(__name__)


def create_workflow_tabs():
    """
    Create the complete Workflow Phase section with nested tabs.
    
    This function assembles all 5 workflow phase sub-tabs:
    - Phase Setup: Phase metadata and pre-phase planning
    - Execution & Performance: Activity log and system performance
    - Phase-Specific Details: Conditional content based on phase type
    - Efficiency & Outcome: Efficiency metrics and outcomes
    - Creative Experience: Creative experience and reflection
    
    Returns:
        dict: {
            'container': Tab widget with 5 sub-tabs,
            'widgets': {
                'setup': {...},
                'execution': {...},
                'phase_specific': {...},
                'outcome': {...},
                'experience': {...}
            }
        }
    """
    logger.debug("Assembling Workflow Phase tabs")
    
    # Create all sub-tabs
    setup = create_workflow_setup_tab()
    execution = create_workflow_execution_tab()
    phase_specific = create_workflow_phase_specific_tab()
    outcome = create_workflow_outcome_tab()
    experience = create_workflow_experience_tab()
    
    # Create nested tab container
    nested_tabs = widgets.Tab()
    nested_tabs.children = [
        setup['container'],
        execution['container'],
        phase_specific['container'],
        outcome['container'],
        experience['container']
    ]
    
    # Set tab titles
    nested_tabs.set_title(0, 'Phase Setup')
    nested_tabs.set_title(1, 'Execution & Performance')
    nested_tabs.set_title(2, 'Phase-Specific Details')
    nested_tabs.set_title(3, 'Efficiency & Outcome')
    nested_tabs.set_title(4, 'Creative Experience')
    
    logger.debug("✅ Workflow Phase tabs assembled (5 sub-tabs)")
    
    return {
        'container': nested_tabs,
        'widgets': {
            'setup': setup['widgets'],
            'execution': execution['widgets'],
            'phase_specific': phase_specific['widgets'],
            'outcome': outcome['widgets'],
            'experience': experience['widgets']
        }
    }


# Public API
__all__ = ['create_workflow_tabs']

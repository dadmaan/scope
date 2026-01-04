"""
AI Music Evaluation - Widgets Package

This package provides interactive Jupyter widgets for systematic evaluation
of AI music generation systems. Organized into modular subpackages for
maintainability and extensibility.

Package Structure (v2.0.0 - Modularized):
    SESSION NOTEBOOK:
        session/          - Core session logging widgets (7 sub-tabs)
        incident/         - Critical incident documentation (4 sub-tabs)
        workflow/         - Workflow phase tracking (5 sub-tabs)
        export/           - Validation and JSON export

    SYNTHESIS JOURNAL:
        system_metadata/  - System & evaluator metadata
        session_import/   - Session loading & evidence extraction
        quantitative_assessment/ - 8 criteria scoring (4 sub-tabs)
        reflective_journal/ - Daily journaling (7 sub-tabs)
        validation_export_synthesis/ - Validation & export

    SHARED:
        session_state.py  - Session state management
        utils.py          - Shared utility functions

Main Entry Points:
    SESSION NOTEBOOK:
        - create_session_logging_tabs() - Core session logging UI
        - create_incident_tabs() - Critical incident UI
        - create_workflow_tabs() - Workflow phase UI
        - create_export_section() - Validation & export UI

    SYNTHESIS JOURNAL:
        - create_system_metadata_section() - System metadata UI
        - create_session_import_section() - Session import UI
        - create_assessment_tabs() - Quantitative assessment UI (4 sub-tabs)
        - create_journal_tabs() - Reflective journal UI (7 sub-tabs)
        - create_validation_export_section() - Synthesis validation & export UI

    SHARED:
        - setup_session_management_observers() - Session management

Usage Example:
    ```python
    from session import create_session_logging_tabs
    from incident import create_incident_tabs
    from workflow import create_workflow_tabs
    from export import create_export_section
    from session_state import setup_session_management_observers
    
    # Create widgets
    core_session = create_session_logging_tabs()
    critical_incident = create_incident_tabs()
    workflow_phase = create_workflow_tabs()
    
    # Assemble all widgets
    all_widgets = {
        'core_session': core_session['widgets'],
        'critical_incident': critical_incident['widgets'],
        'workflow_phase': workflow_phase['widgets']
    }
    
    # Create validation/export
    validation_export = create_export_section(all_widgets, generation_attempts)
    
    # Setup session management
    setup_session_management_observers(all_widgets, main_tabs)
    ```
"""

__version__ = '2.0.0'
__author__ = 'AI Music Evaluation Project'

# ============================================================================
# SESSION NOTEBOOK IMPORTS
# ============================================================================
from .session import create_session_logging_tabs
from .incident import create_incident_tabs
from .workflow import create_workflow_tabs
from .export import create_export_section

# ============================================================================
# SYNTHESIS JOURNAL IMPORTS
# ============================================================================
from .system_metadata import create_system_metadata_section
from .session_import import create_session_import_section
from .quantitative_assessment import create_assessment_tabs
from .reflective_journal import create_journal_tabs
from .validation_export_synthesis import create_validation_export_section as create_synthesis_export_section

# ============================================================================
# PHASE 0: SYSTEM OVERVIEW IMPORTS
# ============================================================================
from .phase0 import create_phase0_section

# ============================================================================
# SHARED UTILITIES
# ============================================================================
from .session_state import (
    setup_session_management_observers,
    save_session_state,
    load_session_state,
    clear_session_state
)

# ============================================================================
# BACKWARD COMPATIBILITY LAYER
# Maintain old import names for existing notebook cells
# ============================================================================

# Old name: create_core_session_logging_tabs → New: create_session_logging_tabs
create_core_session_logging_tabs = create_session_logging_tabs

# Old name: create_critical_incident_tabs → New: create_incident_tabs
create_critical_incident_tabs = create_incident_tabs

# Old name: create_workflow_phase_tabs → New: create_workflow_tabs
create_workflow_phase_tabs = create_workflow_tabs

# Old name: create_validation_export_section → New: create_export_section
create_validation_export_section = create_export_section

# ============================================================================
# PUBLIC API
# ============================================================================

__all__ = [
    # Session Notebook (v2.0.0)
    'create_session_logging_tabs',
    'create_incident_tabs',
    'create_workflow_tabs',
    'create_export_section',

    # Synthesis Journal (v2.0.0)
    'create_system_metadata_section',
    'create_session_import_section',
    'create_assessment_tabs',
    'create_journal_tabs',
    'create_synthesis_export_section',

    # Phase 0: System Overview (v2.1.0)
    'create_phase0_section',

    # Backward compatible names (deprecated but functional)
    'create_core_session_logging_tabs',
    'create_critical_incident_tabs',
    'create_workflow_phase_tabs',

    # Session state management
    'setup_session_management_observers',
    'save_session_state',
    'load_session_state',
    'clear_session_state',
]

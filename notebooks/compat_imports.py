"""
Compatibility layer for notebooks.

This module provides backward-compatible imports for notebooks that were
developed with the old structure. It automatically resolves imports to the
new aimusic_eval package structure.

Usage in notebooks:
    # Replace this:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd().parent))
    from widgets.system_metadata import create_system_metadata_section
    
    # With this:
    from compat_imports import create_system_metadata_section

This layer will be maintained through v2.x releases for backward compatibility.
"""

import sys
import warnings

# Try to import from installed package first
try:
    import aimusic_eval
    _USING_INSTALLED = True
    _PACKAGE_VERSION = aimusic_eval.__version__
except ImportError:
    # Fall back to local development structure
    from pathlib import Path
    _src_path = Path(__file__).parent.parent / 'src'
    
    if _src_path.exists():
        sys.path.insert(0, str(_src_path))
        import aimusic_eval
        _USING_INSTALLED = False
        _PACKAGE_VERSION = aimusic_eval.__version__
    else:
        raise ImportError(
            "Cannot find aimusic_eval package. "
            "Please install the package: pip install -e . (from repository root)"
        )

# Re-export all widget creators for convenience
from aimusic_eval.widgets import (
    # Session Notebook
    create_session_logging_tabs,
    create_incident_tabs,
    create_workflow_tabs,
    create_export_section,
    create_validation_export_section,
    # Synthesis Journal
    create_system_metadata_section,
    create_session_import_section,
    create_assessment_tabs,
    create_journal_tabs,
    create_synthesis_export_section,
    # Session Management
    setup_session_management_observers,
    save_session_state,
    load_session_state,
    clear_session_state,
)

# Re-export widget validators
from aimusic_eval.widgets.validators import (
    validate_time_format,
    validate_required_fields,
    validate_tempo,
    validate_email,
    validate_session_number,
    validate_percentage,
)

# Re-export core utilities
from aimusic_eval.core.exporters import export_to_markdown, export_to_json, export_to_csv
from aimusic_eval.core.validators import (
    validate_session_log,
    validate_quantitative,
    validate_critical_incident,
    validate_comparative,
    validate_template,
)
from aimusic_eval.core.helpers import generate_radar_chart
from aimusic_eval.core.comparative_analysis import (
    load_quantitative_assessments,
    create_score_matrix,
    calculate_statistics,
)

# Re-export schemas
from aimusic_eval.schemas import get_schema, SESSION_SCHEMA, SYNTHESIS_SCHEMA, COMPARISON_SCHEMA

# Re-export config
from aimusic_eval.config import get_output_dir, get_config

# Print initialization message
_mode = "installed package" if _USING_INSTALLED else "local development"
print(f"✅ Using aimusic_eval v{_PACKAGE_VERSION} ({_mode})")

__all__ = [
    # Widget creators
    'create_session_logging_tabs',
    'create_incident_tabs',
    'create_workflow_tabs',
    'create_export_section',
    'create_validation_export_section',
    'create_system_metadata_section',
    'create_session_import_section',
    'create_assessment_tabs',
    'create_journal_tabs',
    'create_synthesis_export_section',
    # Session management
    'setup_session_management_observers',
    'save_session_state',
    'load_session_state',
    'clear_session_state',
    # Widget validators
    'validate_time_format',
    'validate_required_fields',
    'validate_tempo',
    'validate_email',
    'validate_session_number',
    'validate_percentage',
    # Exporters
    'export_to_markdown',
    'export_to_json',
    'export_to_csv',
    # Core validators
    'validate_session_log',
    'validate_quantitative',
    'validate_critical_incident',
    'validate_comparative',
    'validate_template',
    # Helpers
    'generate_radar_chart',
    # Comparative analysis
    'load_quantitative_assessments',
    'create_score_matrix',
    'calculate_statistics',
    # Schemas
    'get_schema',
    'SESSION_SCHEMA',
    'SYNTHESIS_SCHEMA',
    'COMPARISON_SCHEMA',
    # Config
    'get_output_dir',
    'get_config',
]

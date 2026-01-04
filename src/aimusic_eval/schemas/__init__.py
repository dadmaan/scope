"""
JSON Schema definitions for aimusic_eval package.

Provides access to JSON schemas for validation of session, synthesis, and comparison data.
"""

import json
from pathlib import Path
from typing import Dict, Any

_SCHEMA_DIR = Path(__file__).parent


def get_schema(schema_name: str) -> Dict[str, Any]:
    """
    Load JSON schema by name.
    
    Args:
        schema_name: Schema name ('session_notebook', 'synthesis_journal', 'comparative_dashboard')
        
    Returns:
        dict: JSON schema definition
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
        
    Example:
        >>> from aimusic_eval.schemas import get_schema
        >>> session_schema = get_schema('session_notebook')
        >>> print(session_schema['title'])
        'The Session Notebook Schema'
    """
    schema_path = _SCHEMA_DIR / f"schema_{schema_name}.json"
    
    if not schema_path.exists():
        # Try without schema_ prefix
        schema_path = _SCHEMA_DIR / f"{schema_name}.json"
    
    if not schema_path.exists():
        raise FileNotFoundError(
            f"Schema '{schema_name}' not found. "
            f"Available schemas: session_notebook, synthesis_journal, comparative_dashboard"
        )
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Pre-load commonly used schemas for convenience
try:
    SESSION_SCHEMA = get_schema('session_notebook')
    SYNTHESIS_SCHEMA = get_schema('synthesis_journal')
    COMPARISON_SCHEMA = get_schema('comparative_dashboard')
except FileNotFoundError:
    # Schemas may not be present during installation
    SESSION_SCHEMA = None
    SYNTHESIS_SCHEMA = None
    COMPARISON_SCHEMA = None


__all__ = [
    'get_schema',
    'SESSION_SCHEMA',
    'SYNTHESIS_SCHEMA',
    'COMPARISON_SCHEMA',
]

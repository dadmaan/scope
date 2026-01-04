"""
Configuration management for aimusic_eval package.

Handles output directories, logging, and runtime configuration.
"""

from pathlib import Path
import os

# Default output directory (user's current working directory)
DEFAULT_OUTPUT_DIR = Path.cwd() / 'aimusic_eval_outputs'

# Can be overridden via environment variable
OUTPUT_DIR = Path(os.getenv('AIMUSIC_EVAL_OUTPUT_DIR', DEFAULT_OUTPUT_DIR))

# Subdirectories
SESSIONS_DIR = OUTPUT_DIR / 'sessions'
SYNTHESIS_DIR = OUTPUT_DIR / 'synthesis'
LOGS_DIR = OUTPUT_DIR / 'logs'
COMPARISONS_DIR = OUTPUT_DIR / 'comparisons'


def get_output_dir(subdir=None):
    """
    Get output directory path, creating if needed.
    
    Args:
        subdir (str, optional): Subdirectory name ('sessions', 'synthesis', 'logs', 'comparisons')
        
    Returns:
        Path: Output directory path
        
    Example:
        >>> from aimusic_eval.config import get_output_dir
        >>> sessions_dir = get_output_dir('sessions')
        >>> print(sessions_dir)
        /home/user/aimusic_eval_outputs/sessions
    """
    if subdir is None:
        path = OUTPUT_DIR
    else:
        path = OUTPUT_DIR / subdir
    
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config():
    """
    Get current configuration dictionary.
    
    Returns:
        dict: Configuration settings
    """
    return {
        'output_dir': str(OUTPUT_DIR),
        'sessions_dir': str(SESSIONS_DIR),
        'synthesis_dir': str(SYNTHESIS_DIR),
        'logs_dir': str(LOGS_DIR),
        'comparisons_dir': str(COMPARISONS_DIR),
    }


# For backward compatibility with phase1 structure
LEGACY_OUTPUT = Path('phase1/outputs')
if LEGACY_OUTPUT.exists() and not OUTPUT_DIR.exists():
    OUTPUT_DIR = LEGACY_OUTPUT
    SESSIONS_DIR = LEGACY_OUTPUT / 'sessions'
    SYNTHESIS_DIR = LEGACY_OUTPUT / 'synthesis'
    LOGS_DIR = LEGACY_OUTPUT / 'logs'

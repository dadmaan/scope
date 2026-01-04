"""
AI Music Evaluation Framework - Core Helper Functions

Author: Shayan Dadman

This module provides core utilities for the Jupyter notebook templates:
- Data validation and completeness checking
- Session and quantitative data aggregation
- Radar chart visualization (Plotly with matplotlib fallback)
- Statistical calculations
"""

from typing import Dict, List, Any, Optional, Union, Tuple
import re
from pathlib import Path
import json
import warnings


def validate_completeness(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate template data for completeness.

    Args:
        data: Dictionary containing template data with sections and fields

    Returns:
        Dictionary with validation results:
            - valid: bool - Whether data meets minimum requirements
            - completeness: float - Percentage complete (0-100)
            - missing: list - List of missing required sections
            - warnings: list - List of sections with incomplete data

    Example:
        >>> data = {
        ...     'session_info': {'date': '2025-10-10', 'system': 'MusicGen'},
        ...     'generation_attempts': []
        ... }
        >>> result = validate_completeness(data)
        >>> print(result['completeness'])
        45.0
    """
    required_sections = data.get('_required_sections', [])
    optional_sections = data.get('_optional_sections', [])
    all_sections = required_sections + optional_sections

    if not all_sections:
        # Generic validation when section structure not specified
        return _generic_validation(data)

    missing = []
    warnings_list = []
    filled_count = 0
    total_count = len(all_sections)

    for section in required_sections:
        if section not in data or not data[section]:
            missing.append(section)
        elif _has_unfilled_placeholders(data[section]):
            warnings_list.append(f"{section}: Contains unfilled placeholders")
            filled_count += 0.5  # Partial credit
        else:
            filled_count += 1

    for section in optional_sections:
        if section in data and data[section] and not _has_unfilled_placeholders(data[section]):
            filled_count += 1

    completeness = (filled_count / total_count * 100) if total_count > 0 else 0
    valid = len(missing) == 0 and completeness >= 60.0

    return {
        'valid': valid,
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings_list
    }


def _has_unfilled_placeholders(value: Any) -> bool:
    """Check if a value contains common placeholder patterns."""
    if isinstance(value, str):
        # Common placeholder patterns
        patterns = [
            r'_{3,}',  # Three or more underscores
            r'\[.*?\]',  # Bracketed placeholders like [Name]
            r'YYYY-MM-DD',  # Date placeholder
            r'HH:MM',  # Time placeholder
            r'__________',  # Long underscores
            r'^\s*$',  # Empty or whitespace only
        ]
        return any(re.search(pattern, value) for pattern in patterns)
    elif isinstance(value, dict):
        return any(_has_unfilled_placeholders(v) for v in value.values())
    elif isinstance(value, list):
        return len(value) == 0 or any(_has_unfilled_placeholders(item) for item in value)
    return False


def _generic_validation(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generic validation for unstructured data."""
    total_fields = 0
    filled_fields = 0

    def count_fields(obj, path=""):
        nonlocal total_fields, filled_fields
        if isinstance(obj, dict):
            for key, value in obj.items():
                if not key.startswith('_'):  # Skip metadata fields
                    count_fields(value, f"{path}.{key}" if path else key)
        elif isinstance(obj, list):
            total_fields += 1
            if obj and not _has_unfilled_placeholders(obj):
                filled_fields += 1
        else:
            total_fields += 1
            if obj and not _has_unfilled_placeholders(obj):
                filled_fields += 1

    count_fields(data)
    completeness = (filled_fields / total_fields * 100) if total_fields > 0 else 0

    return {
        'valid': completeness >= 60.0,
        'completeness': round(completeness, 1),
        'missing': [],
        'warnings': ['Generic validation used - specify _required_sections for detailed validation']
    }


def calculate_completeness_percentage(data: Dict[str, Any]) -> float:
    """
    Calculate completeness percentage for template data.

    Args:
        data: Template data dictionary

    Returns:
        Float between 0-100 representing completeness percentage

    Example:
        >>> data = {'field1': 'filled', 'field2': '___', 'field3': 'filled'}
        >>> calculate_completeness_percentage(data)
        66.7
    """
    result = validate_completeness(data)
    return result['completeness']


def aggregate_sessions(session_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate multiple session logs into summary statistics.

    Args:
        session_data_list: List of session log dictionaries

    Returns:
        Dictionary with aggregated statistics:
            - total_sessions: int
            - total_attempts: int
            - usable_outputs: int
            - usable_rate: float
            - avg_generation_time: float
            - systems: list of systems evaluated
            - date_range: tuple (first, last)

    Example:
        >>> sessions = [
        ...     {'system': 'MusicGen', 'attempts': 5, 'usable': 3, 'avg_time': 45.2},
        ...     {'system': 'MusicGen', 'attempts': 4, 'usable': 2, 'avg_time': 42.8}
        ... ]
        >>> result = aggregate_sessions(sessions)
        >>> print(result['total_attempts'])
        9
    """
    if not session_data_list:
        return {
            'total_sessions': 0,
            'total_attempts': 0,
            'usable_outputs': 0,
            'usable_rate': 0.0,
            'avg_generation_time': 0.0,
            'systems': [],
            'date_range': (None, None)
        }

    total_attempts = 0
    usable_outputs = 0
    total_time = 0
    time_count = 0
    systems = set()
    dates = []

    for session in session_data_list:
        # Handle different possible key names
        attempts = session.get('total_attempts', session.get('attempts', 0))
        usable = session.get('usable_outputs', session.get('usable', 0))
        avg_time = session.get('avg_generation_time', session.get('avg_time', 0))
        system = session.get('system_name', session.get('system', ''))
        date = session.get('date', session.get('session_date', ''))

        total_attempts += attempts
        usable_outputs += usable

        if avg_time > 0:
            total_time += avg_time
            time_count += 1

        if system:
            systems.add(system)

        if date:
            dates.append(date)

    usable_rate = (usable_outputs / total_attempts * 100) if total_attempts > 0 else 0
    avg_gen_time = (total_time / time_count) if time_count > 0 else 0

    date_range = (min(dates), max(dates)) if dates else (None, None)

    return {
        'total_sessions': len(session_data_list),
        'total_attempts': total_attempts,
        'usable_outputs': usable_outputs,
        'usable_rate': round(usable_rate, 1),
        'avg_generation_time': round(avg_gen_time, 1),
        'systems': sorted(list(systems)),
        'date_range': date_range
    }


def aggregate_quantitative(assessment_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregate quantitative assessments across multiple systems.

    Args:
        assessment_data_list: List of quantitative assessment dictionaries

    Returns:
        Dictionary with aggregated scores per criterion:
            - criteria_scores: dict mapping criterion to list of scores
            - criteria_stats: dict with mean, std, min, max per criterion
            - systems_evaluated: list of system names
            - overall_averages: dict of average scores per system

    Example:
        >>> assessments = [
        ...     {'system': 'MusicGen', 'scores': {'usability': 4, 'speed': 5}},
        ...     {'system': 'Riffusion', 'scores': {'usability': 3, 'speed': 4}}
        ... ]
        >>> result = aggregate_quantitative(assessments)
        >>> print(result['criteria_stats']['usability']['mean'])
        3.5
    """
    from statistics import mean, stdev

    if not assessment_data_list:
        return {
            'criteria_scores': {},
            'criteria_stats': {},
            'systems_evaluated': [],
            'overall_averages': {}
        }

    # Collect scores by criterion
    criteria_scores = {}
    system_scores = {}
    systems = []

    for assessment in assessment_data_list:
        # Try multiple locations for system name
        system = assessment.get('system_name', assessment.get('system', None))
        if not system and 'system_info' in assessment:
            system = assessment['system_info'].get('system', 'Unknown')
        if not system:
            system = 'Unknown'
        systems.append(system)
        scores = assessment.get('scores', assessment.get('criteria_scores', {}))

        system_total = []
        for criterion, score in scores.items():
            if criterion not in criteria_scores:
                criteria_scores[criterion] = []
            if score is not None:  # Skip N/A scores
                criteria_scores[criterion].append(score)
                system_total.append(score)

        if system_total:
            system_scores[system] = round(mean(system_total), 2)

    # Calculate statistics per criterion
    criteria_stats = {}
    for criterion, scores in criteria_scores.items():
        if scores:
            criteria_stats[criterion] = {
                'mean': round(mean(scores), 2),
                'std': round(stdev(scores), 2) if len(scores) > 1 else 0.0,
                'min': min(scores),
                'max': max(scores),
                'count': len(scores)
            }

    return {
        'criteria_scores': criteria_scores,
        'criteria_stats': criteria_stats,
        'systems_evaluated': systems,
        'overall_averages': system_scores
    }


def generate_radar_chart(
    scores: Dict[str, float],
    title: str = "System Performance",
    backend: str = "auto"
) -> Optional[Any]:
    """
    Generate a radar chart for the 8 evaluation criteria.

    Args:
        scores: Dictionary mapping criterion names to scores (1-5)
        title: Chart title
        backend: 'plotly', 'matplotlib', or 'auto' (try plotly, fallback to matplotlib)

    Returns:
        Plotly figure object, matplotlib figure, or None if both fail

    Example:
        >>> scores = {
        ...     'Usability': 4,
        ...     'Generation Speed': 5,
        ...     'Audio Quality': 3,
        ...     'Stylistic Accuracy': 4,
        ...     'Parameter Control': 3,
        ...     'Content Generation Control': 3,
        ...     'DAW Integration': 2,
        ...     'Creative Workflow': 4
        ... }
        >>> fig = generate_radar_chart(scores)
    """
    if not scores:
        warnings.warn("No scores provided for radar chart")
        return None

    # Try Plotly first if auto or explicitly requested
    if backend in ("auto", "plotly"):
        try:
            return _generate_radar_plotly(scores, title)
        except ImportError:
            if backend == "plotly":
                raise
            warnings.warn("Plotly not available, falling back to matplotlib")

    # Fall back to matplotlib
    if backend in ("auto", "matplotlib"):
        try:
            return _generate_radar_matplotlib(scores, title)
        except ImportError:
            if backend == "matplotlib":
                raise
            warnings.warn("Matplotlib not available")

    return None


def _generate_radar_plotly(scores: Dict[str, float], title: str) -> Any:
    """Generate radar chart using Plotly."""
    import plotly.graph_objects as go

    categories = list(scores.keys())
    values = list(scores.values())

    # Close the radar chart by appending first value
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        name=title,
        line=dict(color='rgb(99, 110, 250)', width=2),
        fillcolor='rgba(99, 110, 250, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickmode='linear',
                tick0=0,
                dtick=1
            )
        ),
        showlegend=True,
        title=dict(
            text=title,
            x=0.5,
            xanchor='center'
        ),
        font=dict(size=12),
        width=600,
        height=600
    )

    return fig


def _generate_radar_matplotlib(scores: Dict[str, float], title: str) -> Any:
    """Generate radar chart using Matplotlib."""
    import matplotlib.pyplot as plt
    import numpy as np

    categories = list(scores.keys())
    values = list(scores.values())

    # Number of variables
    num_vars = len(categories)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Close the plot
    values += values[:1]
    angles += angles[:1]
    categories += categories[:1]

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))

    # Plot data
    ax.plot(angles, values, 'o-', linewidth=2, label=title, color='#636EFA')
    ax.fill(angles, values, alpha=0.25, color='#636EFA')

    # Fix axis to go in the right order
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories[:-1], size=10)

    # Set y-axis limits and labels
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_yticklabels(['1', '2', '3', '4', '5'], size=8)
    ax.set_rlabel_position(0)

    # Add title
    plt.title(title, size=14, y=1.08)

    # Add grid
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    return fig


def calculate_statistics(scores: List[float]) -> Dict[str, float]:
    """
    Calculate basic statistics for a list of scores.

    Args:
        scores: List of numerical scores

    Returns:
        Dictionary with mean, std, min, max, median, count

    Example:
        >>> scores = [3, 4, 5, 4, 3, 4]
        >>> stats = calculate_statistics(scores)
        >>> print(stats['mean'])
        3.83
    """
    from statistics import mean, median, stdev

    if not scores:
        return {
            'mean': 0.0,
            'median': 0.0,
            'std': 0.0,
            'min': 0.0,
            'max': 0.0,
            'count': 0
        }

    return {
        'mean': round(mean(scores), 2),
        'median': round(median(scores), 2),
        'std': round(stdev(scores), 2) if len(scores) > 1 else 0.0,
        'min': round(min(scores), 2),
        'max': round(max(scores), 2),
        'count': len(scores)
    }


def format_time_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string like "2m 30s" or "1h 15m"

    Example:
        >>> format_time_duration(150)
        '2m 30s'
        >>> format_time_duration(3665)
        '1h 1m 5s'
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s" if secs > 0 else f"{minutes}m"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        parts = [f"{hours}h"]
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0:
            parts.append(f"{secs}s")
        return " ".join(parts)

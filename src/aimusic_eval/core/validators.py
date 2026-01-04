"""
AI Music Evaluation Framework - Template Validators

Author: Shayan Dadman

This module provides validation functions for each of the 6 evaluation templates:
- Session Log
- Quantitative Assessment
- Critical Incident
- Comparative Analysis
- Daily Journal
- Workflow Phase
"""

from typing import Dict, List, Any, Optional
import re
from datetime import datetime


class TemplateValidator:
    """Base class for template validation with common utilities."""

    # Common placeholder patterns
    PLACEHOLDER_PATTERNS = [
        r'_{3,}',  # Three or more underscores
        r'\[.*?\]',  # Bracketed placeholders
        r'YYYY-MM-DD',
        r'HH:MM',
        r'__________',
    ]

    @staticmethod
    def has_placeholder(text: str) -> bool:
        """Check if text contains unfilled placeholders."""
        if not isinstance(text, str):
            return False
        return any(re.search(pattern, text) for pattern in TemplateValidator.PLACEHOLDER_PATTERNS)

    @staticmethod
    def is_empty(value: Any) -> bool:
        """Check if value is empty or placeholder."""
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip() or TemplateValidator.has_placeholder(value)
        if isinstance(value, (list, dict)):
            return len(value) == 0
        return False

    @staticmethod
    def count_filled_sections(data: Dict[str, Any], required_keys: List[str]) -> tuple:
        """Count filled vs total required sections."""
        filled = 0
        missing = []
        warnings = []

        for key in required_keys:
            if key not in data:
                missing.append(key)
            elif TemplateValidator.is_empty(data[key]):
                missing.append(key)
            elif isinstance(data[key], str) and TemplateValidator.has_placeholder(data[key]):
                warnings.append(f"{key}: Contains placeholders")
                filled += 0.5  # Partial credit
            else:
                filled += 1

        return filled, len(required_keys), missing, warnings


def validate_session_log(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a Session Log template.

    Required sections:
    - session_info (date, system, evaluator)
    - creative_task
    - generation_attempts (at least 1)
    - real_time_criteria (8 quick ratings)
    - reflective_notes

    Args:
        data: Session log data dictionary

    Returns:
        Validation result with valid, completeness, missing, warnings

    Example:
        >>> data = {
        ...     'session_info': {'date': '2025-10-10', 'system': 'MusicGen'},
        ...     'generation_attempts': [{'prompt': 'funky bass', 'quality': 4}],
        ...     'real_time_criteria': {'usability': 4, 'speed': 5},
        ...     'reflective_notes': {'what_worked': 'Fast generation'}
        ... }
        >>> result = validate_session_log(data)
    """
    required = [
        'session_info',
        'creative_task',
        'generation_attempts',
        'real_time_criteria',
        'reflective_notes'
    ]

    filled, total, missing, warnings = TemplateValidator.count_filled_sections(data, required)

    # Additional validation
    if 'generation_attempts' in data:
        attempts = data['generation_attempts']
        if isinstance(attempts, list) and len(attempts) == 0:
            warnings.append("generation_attempts: No attempts recorded")
            filled -= 0.5
        elif isinstance(attempts, list) and len(attempts) > 0:
            # Check if attempts have required fields
            for i, attempt in enumerate(attempts):
                if not isinstance(attempt, dict) or TemplateValidator.is_empty(attempt.get('prompt', '')):
                    warnings.append(f"generation_attempts[{i}]: Missing prompt")

    if 'real_time_criteria' in data:
        criteria = data['real_time_criteria']
        expected_criteria = 8  # Should have all 8 criteria rated
        if isinstance(criteria, dict):
            actual_count = len([v for v in criteria.values() if v is not None])
            if actual_count < expected_criteria:
                warnings.append(f"real_time_criteria: Only {actual_count}/{expected_criteria} criteria rated")

    completeness = (filled / total * 100) if total > 0 else 0

    return {
        'valid': len(missing) == 0 and completeness >= 60.0,
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings,
        'template_type': 'session_log'
    }


def validate_quantitative(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a Quantitative Assessment template.

    Required sections:
    - system_info (system name, evaluation period)
    - criteria_scores (all 8 criteria with scores 1-5)
    - criteria_evidence (rationale for each score)
    - overall_assessment

    Args:
        data: Quantitative assessment data dictionary

    Returns:
        Validation result with valid, completeness, missing, warnings
    """
    required = [
        'system_info',
        'criteria_scores',
        'criteria_evidence',
        'overall_assessment'
    ]

    filled, total, missing, warnings = TemplateValidator.count_filled_sections(data, required)

    # Validate all 8 criteria are scored
    expected_criteria = [
        'usability',
        'generation_speed',
        'audio_quality',
        'stylistic_accuracy',
        'parameter_control',
        'content_generation_control',
        'daw_integration',
        'creative_workflow'
    ]

    if 'criteria_scores' in data:
        scores = data['criteria_scores']
        if isinstance(scores, dict):
            for criterion in expected_criteria:
                if criterion not in scores or scores[criterion] is None:
                    warnings.append(f"criteria_scores: Missing score for {criterion}")
                elif not isinstance(scores[criterion], (int, float)) or not (1 <= scores[criterion] <= 5):
                    warnings.append(f"criteria_scores: Invalid score for {criterion} (must be 1-5)")

    # Validate evidence provided for scores
    if 'criteria_evidence' in data:
        evidence = data['criteria_evidence']
        if isinstance(evidence, dict):
            for criterion in expected_criteria:
                if criterion not in evidence or TemplateValidator.is_empty(evidence[criterion]):
                    warnings.append(f"criteria_evidence: Missing evidence for {criterion}")

    completeness = (filled / total * 100) if total > 0 else 0

    return {
        'valid': len(missing) == 0 and completeness >= 80.0,  # Higher bar for quantitative
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings,
        'template_type': 'quantitative_assessment'
    }


def validate_critical_incident(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a Critical Incident Report template.

    Required sections:
    - incident_classification (type, severity, date)
    - incident_description (what happened, context)
    - analysis (significance, implications)
    - learnings

    Args:
        data: Critical incident data dictionary

    Returns:
        Validation result with valid, completeness, missing, warnings
    """
    required = [
        'incident_classification',
        'incident_description',
        'analysis',
        'learnings'
    ]

    filled, total, missing, warnings = TemplateValidator.count_filled_sections(data, required)

    # Validate incident type specified
    if 'incident_classification' in data:
        classification = data['incident_classification']
        if isinstance(classification, dict):
            if TemplateValidator.is_empty(classification.get('type', '')):
                warnings.append("incident_classification: Incident type not specified")
            if TemplateValidator.is_empty(classification.get('severity', '')):
                warnings.append("incident_classification: Severity not specified")

    # Validate description has key elements
    if 'incident_description' in data:
        description = data['incident_description']
        if isinstance(description, dict):
            key_elements = ['what_happened', 'what_expected', 'what_actually_happened']
            for element in key_elements:
                if TemplateValidator.is_empty(description.get(element, '')):
                    warnings.append(f"incident_description: Missing '{element}'")

    completeness = (filled / total * 100) if total > 0 else 0

    return {
        'valid': len(missing) == 0 and completeness >= 60.0,
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings,
        'template_type': 'critical_incident'
    }


def validate_comparative(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a Comparative Analysis template.

    Required sections:
    - systems_compared (list of at least 2 systems)
    - comparison_matrix (scores for each system × criterion)
    - criterion_analysis (analysis for each criterion)
    - synthesis (patterns, recommendations)

    Args:
        data: Comparative analysis data dictionary

    Returns:
        Validation result with valid, completeness, missing, warnings
    """
    required = [
        'systems_compared',
        'comparison_matrix',
        'criterion_analysis',
        'synthesis'
    ]

    filled, total, missing, warnings = TemplateValidator.count_filled_sections(data, required)

    # Validate at least 2 systems being compared
    if 'systems_compared' in data:
        systems = data['systems_compared']
        if isinstance(systems, list):
            if len(systems) < 2:
                warnings.append("systems_compared: Need at least 2 systems for comparison")
                filled -= 0.5
        elif TemplateValidator.is_empty(systems):
            warnings.append("systems_compared: No systems specified")

    # Validate comparison matrix completeness
    if 'comparison_matrix' in data:
        matrix = data['comparison_matrix']
        if isinstance(matrix, dict):
            systems = data.get('systems_compared', [])
            if isinstance(systems, list) and len(systems) >= 2:
                expected_entries = len(systems) * 8  # 8 criteria per system
                actual_entries = sum(1 for system_data in matrix.values()
                                   if isinstance(system_data, dict)
                                   for score in system_data.values()
                                   if score is not None)
                if actual_entries < expected_entries:
                    warnings.append(f"comparison_matrix: Only {actual_entries}/{expected_entries} scores provided")

    completeness = (filled / total * 100) if total > 0 else 0

    return {
        'valid': len(missing) == 0 and completeness >= 70.0,
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings,
        'template_type': 'comparative_analysis'
    }


def validate_daily_journal(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a Daily Journal template.

    Required sections:
    - entry_metadata (date, productivity, mood)
    - activities_summary
    - key_observations
    - reflections
    - day_rating

    Args:
        data: Daily journal data dictionary

    Returns:
        Validation result with valid, completeness, missing, warnings
    """
    required = [
        'entry_metadata',
        'activities_summary',
        'key_observations',
        'reflections',
        'day_rating'
    ]

    filled, total, missing, warnings = TemplateValidator.count_filled_sections(data, required)

    # Validate date is present
    if 'entry_metadata' in data:
        metadata = data['entry_metadata']
        if isinstance(metadata, dict):
            if TemplateValidator.is_empty(metadata.get('date', '')):
                warnings.append("entry_metadata: Date not specified")

    # Validate day rating has all dimensions
    if 'day_rating' in data:
        rating = data['day_rating']
        expected_dimensions = ['productivity', 'learning', 'creativity', 'frustration', 'satisfaction']
        if isinstance(rating, dict):
            for dimension in expected_dimensions:
                if dimension not in rating or rating[dimension] is None:
                    warnings.append(f"day_rating: Missing rating for {dimension}")

    completeness = (filled / total * 100) if total > 0 else 0

    return {
        'valid': len(missing) == 0 and completeness >= 50.0,  # Lower bar for daily journals
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings,
        'template_type': 'daily_journal'
    }


def validate_workflow_phase(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a Workflow Phase Documentation template.

    Required sections:
    - phase_overview (phase_name, date, duration, systems, evaluator)
    - pre_phase_state (goals, materials, vision)
    - execution_log (list of activities)
    - workflow_details (observations, patterns)
    - outcome_assessment (achievement, quality)
    - learnings (key takeaways)

    Args:
        data: Workflow phase data dictionary

    Returns:
        Validation result with valid, completeness, missing, warnings
    """
    required = [
        'phase_overview',
        'pre_phase_state',
        'execution_log',
        'workflow_details',
        'outcome_assessment',
        'learnings'
    ]

    filled, total, missing, warnings = TemplateValidator.count_filled_sections(data, required)

    # Validate phase name is specified
    if 'phase_overview' in data:
        overview = data['phase_overview']
        if isinstance(overview, dict):
            valid_phases = ['content_generation', 'curation', 'integration', 'post_production', 'other']
            phase = overview.get('phase_name', '').lower()
            if TemplateValidator.is_empty(phase):
                warnings.append("phase_overview: Phase name not specified")
            elif phase not in valid_phases:
                warnings.append(f"phase_overview: Unknown phase type '{phase}'")

    # Validate execution log has content
    if 'execution_log' in data:
        log = data['execution_log']
        if isinstance(log, list):
            if len(log) == 0:
                warnings.append("execution_log: No activities recorded")
        elif isinstance(log, str):
            if TemplateValidator.is_empty(log):
                warnings.append("execution_log: No activities recorded")

    # Validate phase-specific data exists if applicable
    phase_name = data.get('phase_overview', {}).get('phase_name', '').lower()
    if phase_name == 'content_generation' and 'generation_details' not in data:
        pass  # Optional section
    elif phase_name == 'curation' and 'curation_details' not in data:
        pass  # Optional section
    elif phase_name == 'integration' and 'integration_details' not in data:
        pass  # Optional section
    elif phase_name == 'post_production' and 'postproduction_details' not in data:
        pass  # Optional section

    completeness = (filled / total * 100) if total > 0 else 0

    return {
        'valid': len(missing) == 0 and completeness >= 60.0,
        'completeness': round(completeness, 1),
        'missing': missing,
        'warnings': warnings,
        'template_type': 'workflow_phase'
    }


def validate_template(data: Dict[str, Any], template_type: str) -> Dict[str, Any]:
    """
    Validate any template by type.

    Args:
        data: Template data dictionary
        template_type: One of: session_log, quantitative, critical_incident,
                      comparative, daily_journal, workflow_phase

    Returns:
        Validation result dictionary

    Example:
        >>> data = {'session_info': {...}, 'generation_attempts': [...]}
        >>> result = validate_template(data, 'session_log')
    """
    validators = {
        'session_log': validate_session_log,
        'quantitative': validate_quantitative,
        'quantitative_assessment': validate_quantitative,
        'critical_incident': validate_critical_incident,
        'comparative': validate_comparative,
        'comparative_analysis': validate_comparative,
        'daily_journal': validate_daily_journal,
        'workflow_phase': validate_workflow_phase
    }

    validator = validators.get(template_type.lower())
    if not validator:
        return {
            'valid': False,
            'completeness': 0.0,
            'missing': [],
            'warnings': [f"Unknown template type: {template_type}"],
            'template_type': template_type
        }

    return validator(data)

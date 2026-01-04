"""
Validation Export Synthesis - Validation Module

Validates synthesis journal completeness and quality.
Checks system metadata, criteria scoring, evidence, sessions, and journal entries.
"""

import logging

logger = logging.getLogger(__name__)


def validate_synthesis(synthesis_data):
    """
    Check completeness of synthesis journal.

    Validates:
    - System metadata completeness (system name, evaluator name)
    - All 8 criteria scored
    - Evidence present for criteria
    - Sessions imported (recommended 5+)
    - Journal entries added

    Args:
        synthesis_data (dict): The synthesis journal data structure

    Returns:
        dict: Validation results with keys:
            - status (str): Overall status with emoji indicator
            - completeness (float): Completeness score (0.0-1.0)
            - issues (list): Critical issues that must be resolved
            - warnings (list): Non-critical warnings
            - scored_criteria (int): Number of criteria scored
            - total_criteria (int): Total number of criteria (8)
            - sessions_imported (int): Number of sessions imported
            - journal_entries (int): Number of journal entries

    Example:
        >>> result = validate_synthesis(synthesis_data)
        >>> print(result['status'])
        '🟢 Complete'
        >>> print(result['completeness'])
        1.0
    """
    issues = []
    warnings = []

    # Check system metadata
    if not synthesis_data['system_metadata'].get('system_name'):
        issues.append("Missing system name")
    if not synthesis_data['system_metadata'].get('evaluator_name'):
        warnings.append("Missing evaluator name")

    # Check criteria scored
    scored_criteria = [c for c, data in synthesis_data['quantitative_assessment']['criteria'].items()
                      if data.get('score', 0) > 0]

    if len(scored_criteria) < 8:
        issues.append(f"Only {len(scored_criteria)}/8 criteria scored")

    # Check evidence present
    criteria_with_evidence = [c for c, data in synthesis_data['quantitative_assessment']['criteria'].items()
                             if data.get('evidence', '').strip()]

    if len(criteria_with_evidence) < 5:
        warnings.append(f"Only {len(criteria_with_evidence)} criteria have evidence")

    # Check sessions imported
    if len(synthesis_data['imported_sessions']) < 5:
        warnings.append(f"Only {len(synthesis_data['imported_sessions'])} sessions imported (recommended: 5+)")

    # Check journal entries
    if synthesis_data['reflective_journal']['entry_count'] == 0:
        warnings.append("No journal entries added yet")

    # Determine status
    if len(issues) == 0 and len(warnings) == 0:
        status = "🟢 Complete"
        completeness = 1.0
    elif len(issues) == 0:
        status = "🟡 Good (minor warnings)"
        completeness = 0.8
    else:
        status = "🔴 Incomplete"
        completeness = 0.5

    return {
        'status': status,
        'completeness': completeness,
        'issues': issues,
        'warnings': warnings,
        'scored_criteria': len(scored_criteria),
        'total_criteria': 8,
        'sessions_imported': len(synthesis_data['imported_sessions']),
        'journal_entries': synthesis_data['reflective_journal']['entry_count']
    }


def format_validation_report(validation_result):
    """
    Format validation result as a readable text report.

    Args:
        validation_result (dict): Validation result from validate_synthesis()

    Returns:
        str: Formatted validation report

    Example:
        >>> result = validate_synthesis(synthesis_data)
        >>> print(format_validation_report(result))
    """
    lines = []
    lines.append("=" * 70)
    lines.append("📋 VALIDATION REPORT")
    lines.append("=" * 70)
    lines.append(f"Status: {validation_result['status']}")
    lines.append(f"Completeness: {validation_result['completeness']:.0%}")
    lines.append(f"Criteria Scored: {validation_result['scored_criteria']}/{validation_result['total_criteria']}")
    lines.append(f"Sessions Imported: {validation_result['sessions_imported']}")
    lines.append(f"Journal Entries: {validation_result['journal_entries']}")

    if validation_result['issues']:
        lines.append(f"\n❌ Issues ({len(validation_result['issues'])})")
        for issue in validation_result['issues']:
            lines.append(f"   • {issue}")

    if validation_result['warnings']:
        lines.append(f"\n⚠️  Warnings ({len(validation_result['warnings'])})")
        for warning in validation_result['warnings']:
            lines.append(f"   • {warning}")

    lines.append("=" * 70)
    return "\n".join(lines)

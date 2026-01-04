"""
AI Music Evaluation Framework - Export Functions

Author: Shayan Dadman

This module provides export functionality for evaluation templates:
- Export to Markdown (matching original template format)
- Export to CSV (tabular format for analysis)
- Export to JSON (structured data)
- Parse Markdown back to data (round-trip capability)
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import csv
from datetime import datetime
import re


def export_to_markdown(data: Dict[str, Any], filepath: str, template_type: str) -> bool:
    """
    Export template data to Markdown format matching original templates.

    Args:
        data: Template data dictionary
        filepath: Output file path
        template_type: Template type (session_log, quantitative, etc.)

    Returns:
        True if successful, False otherwise

    Example:
        >>> data = {'session_info': {'date': '2025-10-10', 'system': 'MusicGen'}}
        >>> export_to_markdown(data, 'output.md', 'session_log')
        True
    """
    try:
        exporters = {
            'session_log': _export_session_log_md,
            'quantitative': _export_quantitative_md,
            'quantitative_assessment': _export_quantitative_md,
            'critical_incident': _export_critical_incident_md,
            'comparative': _export_comparative_md,
            'comparative_analysis': _export_comparative_md,
            'daily_journal': _export_daily_journal_md,
            'workflow_phase': _export_workflow_phase_md,
            'synthesis': _export_synthesis_md,
            'synthesis_journal': _export_synthesis_md
        }

        exporter = exporters.get(template_type.lower())
        if not exporter:
            raise ValueError(f"Unknown template type: {template_type}")

        content = exporter(data)
        Path(filepath).write_text(content, encoding='utf-8')
        return True

    except Exception as e:
        print(f"Error exporting to markdown: {e}")
        return False


def _export_session_log_md(data: Dict[str, Any]) -> str:
    """Export session log to markdown."""
    lines = ["# System Evaluation Session Log\n"]

    # Session Information
    lines.append("## Session Information")
    info = data.get('session_info', {})
    lines.append(f"- **Date:** {info.get('date', '')}")
    lines.append(f"- **Session Duration:** {info.get('duration', '')}")
    lines.append(f"- **System Name:** {info.get('system', '')}")
    lines.append(f"- **System Version:** {info.get('version', 'N/A')}")
    lines.append(f"- **Interface Used:** {info.get('interface', '')}")
    lines.append(f"- **Evaluator:** {info.get('evaluator', '')}")
    lines.append(f"- **Session Number:** {info.get('session_number', '')}\n")

    # Creative Task Context
    lines.append("---\n")
    lines.append("## Creative Task Context")
    task = data.get('creative_task', {})
    lines.append(f"- **Musical Element Target:** {task.get('element', '')}")
    lines.append(f"- **Genre/Style:** {task.get('genre', '')}")
    lines.append(f"- **Tempo Target:** {task.get('tempo', '')}")
    lines.append(f"- **Key/Scale:** {task.get('key', 'N/A')}")
    lines.append(f"- **Intended Use:** {task.get('intended_use', '')}\n")

    # Generation Attempts
    lines.append("---\n")
    lines.append("## Generation Attempts Log\n")
    attempts = data.get('generation_attempts', [])
    for i, attempt in enumerate(attempts, 1):
        lines.append(f"### Attempt {i}")
        lines.append(f"- **Time:** {attempt.get('time', '')}")
        lines.append(f"- **Input:** {attempt.get('prompt', '')}")
        lines.append(f"- **Generation Time:** {attempt.get('generation_time', '')} seconds")
        lines.append(f"- **Quality Rating:** {attempt.get('quality', 'N/A')}/5")
        lines.append(f"- **Usable:** {'Yes' if attempt.get('usable') else 'No'}")
        if attempt.get('notes'):
            lines.append(f"- **Notes:** {attempt.get('notes', '')}")
        lines.append("")

    # Real-time Criteria Assessment
    lines.append("---\n")
    lines.append("## Real-Time Criteria Assessment\n")
    criteria = data.get('real_time_criteria', {})
    for criterion, score in criteria.items():
        lines.append(f"### {criterion.replace('_', ' ').title()}")
        lines.append(f"**Score:** {score}/5\n")

    # Reflective Notes
    lines.append("---\n")
    lines.append("## Reflective Notes\n")
    notes = data.get('reflective_notes', {})
    lines.append(f"### What Worked Well\n{notes.get('what_worked', '')}\n")
    lines.append(f"### What Was Frustrating\n{notes.get('what_frustrated', '')}\n")
    lines.append(f"### Unexpected Discoveries\n{notes.get('unexpected', '')}\n")

    # Session Summary
    lines.append("---\n")
    lines.append("## Session Summary Statistics")
    summary = data.get('summary', {})
    lines.append(f"- **Total attempts:** {summary.get('total_attempts', len(attempts))}")
    lines.append(f"- **Usable outputs:** {summary.get('usable_outputs', 0)}")
    lines.append(f"- **Average generation time:** {summary.get('avg_generation_time', 0)} seconds")
    lines.append(f"- **Total session time:** {summary.get('total_time', '')} minutes\n")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def _export_quantitative_md(data: Dict[str, Any]) -> str:
    """Export quantitative assessment to markdown."""
    lines = ["# Quantitative Performance Assessment\n"]

    # System Information
    lines.append("## System Information")
    info = data.get('system_info', {})
    lines.append(f"- **System Name:** {info.get('system', '')}")
    lines.append(f"- **Evaluation Period:** {info.get('period', '')}")
    lines.append(f"- **Total Sessions:** {info.get('total_sessions', '')}")
    lines.append(f"- **Evaluator:** {info.get('evaluator', '')}")
    lines.append(f"- **Assessment Date:** {info.get('date', datetime.now().strftime('%Y-%m-%d'))}\n")

    # Criteria Scores
    lines.append("---\n")
    lines.append("## Performance Criteria Scores\n")

    scores = data.get('criteria_scores', {})
    evidence = data.get('criteria_evidence', {})

    criteria_names = {
        'usability': 'Usability',
        'generation_speed': 'Generation Speed',
        'audio_quality': 'Audio Quality',
        'stylistic_accuracy': 'Stylistic Accuracy',
        'parameter_control': 'Parameter Control',
        'content_generation_control': 'Content Generation Control',
        'daw_integration': 'DAW Integration Capacity',
        'creative_workflow': 'Creative Workflow Support'
    }

    for key, name in criteria_names.items():
        score = scores.get(key, 'N/A')
        lines.append(f"### {name}")
        lines.append(f"**Score:** {score}/5\n")
        lines.append("**Evidence & Rationale:**")
        lines.append(f"{evidence.get(key, 'No evidence provided')}\n")

    # Overall Assessment
    lines.append("---\n")
    lines.append("## Overall Assessment\n")

    # Calculate average
    valid_scores = [s for s in scores.values() if isinstance(s, (int, float))]
    avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0

    lines.append(f"**Average Score:** {avg_score:.2f}/5\n")

    assessment = data.get('overall_assessment', {})
    lines.append(f"### Top 3 Strengths")
    strengths = assessment.get('strengths', [])
    for i, strength in enumerate(strengths[:3], 1):
        lines.append(f"{i}. {strength}")
    lines.append("")

    lines.append(f"### Top 3 Weaknesses")
    weaknesses = assessment.get('weaknesses', [])
    for i, weakness in enumerate(weaknesses[:3], 1):
        lines.append(f"{i}. {weakness}")
    lines.append("")

    lines.append(f"### Use Case Recommendations")
    lines.append(f"{assessment.get('recommendations', 'No recommendations provided')}\n")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def _export_critical_incident_md(data: Dict[str, Any]) -> str:
    """Export critical incident to markdown."""
    lines = ["# Critical Incident Report\n"]

    # Classification
    lines.append("## Incident Classification")
    classification = data.get('incident_classification', {})
    lines.append(f"- **Date & Time:** {classification.get('datetime', '')}")
    lines.append(f"- **System:** {classification.get('system', '')}")
    lines.append(f"- **Type:** {classification.get('type', '')}")
    lines.append(f"- **Severity:** {classification.get('severity', '')}\n")

    # Description
    lines.append("---\n")
    lines.append("## Incident Description\n")
    description = data.get('incident_description', {})
    lines.append(f"### What Happened\n{description.get('what_happened', '')}\n")
    lines.append(f"### What Was Expected\n{description.get('what_expected', '')}\n")
    lines.append(f"### What Actually Happened\n{description.get('what_actually_happened', '')}\n")

    # Analysis
    lines.append("---\n")
    lines.append("## Analysis & Significance\n")
    analysis = data.get('analysis', {})
    lines.append(f"### Why This Matters\n{analysis.get('significance', '')}\n")
    lines.append(f"### Criterion Implications\n{analysis.get('criterion_implications', '')}\n")

    # Learnings
    lines.append("---\n")
    lines.append("## Learnings & Adaptations\n")
    learnings = data.get('learnings', {})
    lines.append(f"### What I Learned\n{learnings.get('learned', '')}\n")
    lines.append(f"### How This Changed My Approach\n{learnings.get('approach_change', '')}\n")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def _export_comparative_md(data: Dict[str, Any]) -> str:
    """Export comparative analysis to markdown."""
    lines = ["# Comparative System Analysis\n"]

    # Systems Compared
    lines.append("## Systems Compared")
    systems = data.get('systems_compared', [])
    for system in systems:
        lines.append(f"- **{system}**")
    lines.append("")

    # Comparison Matrix
    lines.append("---\n")
    lines.append("## Quantitative Comparison Matrix\n")

    matrix = data.get('comparison_matrix', {})
    if matrix:
        # Header row
        lines.append("| Criterion | " + " | ".join(systems) + " |")
        lines.append("|-----------|" + "|".join(["-------"] * len(systems)) + "|")

        # Data rows
        criteria = ['usability', 'generation_speed', 'audio_quality', 'stylistic_accuracy',
                   'parameter_control', 'content_generation_control', 'daw_integration', 'creative_workflow']
        for criterion in criteria:
            row = [criterion.replace('_', ' ').title()]
            for system in systems:
                score = matrix.get(system, {}).get(criterion, 'N/A')
                row.append(str(score))
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    # Synthesis
    lines.append("---\n")
    lines.append("## Synthesis\n")
    synthesis = data.get('synthesis', {})
    lines.append(f"### Universal Patterns\n{synthesis.get('patterns', '')}\n")
    lines.append(f"### Distinctive Capabilities\n{synthesis.get('distinctive', '')}\n")
    lines.append(f"### Recommendations\n{synthesis.get('recommendations', '')}\n")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def _export_daily_journal_md(data: Dict[str, Any]) -> str:
    """Export daily journal to markdown."""
    lines = ["# Daily Evaluation Journal\n"]

    # Metadata
    lines.append("## Entry Metadata")
    metadata = data.get('entry_metadata', {})
    lines.append(f"- **Date:** {metadata.get('date', '')}")
    lines.append(f"- **Day of Week:** {metadata.get('day_of_week', '')}")
    lines.append(f"- **Overall Productivity:** {metadata.get('productivity', '')}")
    lines.append(f"- **Overall Mood:** {metadata.get('mood', '')}\n")

    # Activities
    lines.append("---\n")
    lines.append("## Today's Activities\n")
    activities = data.get('activities_summary', {})
    lines.append(f"### Systems Worked With\n{activities.get('systems', '')}\n")
    lines.append(f"### Time Invested\n{activities.get('time_invested', '')}\n")

    # Observations
    lines.append("---\n")
    lines.append("## Key Observations & Insights\n")
    observations = data.get('key_observations', {})
    lines.append(f"{observations.get('observations', '')}\n")

    # Reflections
    lines.append("---\n")
    lines.append("## Reflections\n")
    reflections = data.get('reflections', {})
    lines.append(f"### Emotional Journey\n{reflections.get('emotional', '')}\n")
    lines.append(f"### Learnings\n{reflections.get('learnings', '')}\n")

    # Day Rating
    lines.append("---\n")
    lines.append("## Day Rating\n")
    rating = data.get('day_rating', {})
    for dimension in ['productivity', 'learning', 'creativity', 'frustration', 'satisfaction']:
        score = rating.get(dimension, 'N/A')
        lines.append(f"- **{dimension.title()}:** {score}/10")
    lines.append("")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def _export_workflow_phase_md(data: Dict[str, Any]) -> str:
    """Export workflow phase to markdown."""
    lines = ["# Workflow Phase Documentation\n"]

    # Overview
    lines.append("## Phase Overview")
    overview = data.get('phase_overview', {})
    lines.append(f"- **Phase Name:** {overview.get('phase_name', '')}")
    lines.append(f"- **Date:** {overview.get('date', '')}")
    lines.append(f"- **Duration:** {overview.get('duration', '')}")
    lines.append(f"- **Systems Involved:** {overview.get('systems', '')}\n")

    # Pre-Phase State
    lines.append("---\n")
    lines.append("## Pre-Phase State\n")
    pre_phase = data.get('pre_phase_state', {})
    lines.append(f"### Goals\n{pre_phase.get('goals', '')}\n")
    lines.append(f"### Resources\n{pre_phase.get('resources', '')}\n")

    # Execution Log
    lines.append("---\n")
    lines.append("## Execution Log\n")
    log = data.get('execution_log', [])
    for i, entry in enumerate(log, 1):
        lines.append(f"### Activity {i}")
        lines.append(f"- **Time:** {entry.get('time', '')}")
        lines.append(f"- **Action:** {entry.get('action', '')}")
        lines.append(f"- **Result:** {entry.get('result', '')}\n")

    # Outcome Assessment
    lines.append("---\n")
    lines.append("## Outcome Assessment\n")
    outcome = data.get('outcome_assessment', {})
    lines.append(f"### Goal Achievement\n{outcome.get('achievement', '')}\n")
    lines.append(f"### Quality\n{outcome.get('quality', '')}\n")

    # Learnings
    lines.append("---\n")
    lines.append("## Learnings\n")
    learnings = data.get('learnings', {})
    lines.append(f"{learnings.get('key_learnings', '')}\n")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def _export_synthesis_md(data: Dict[str, Any]) -> str:
    """Export synthesis journal to markdown."""
    lines = ["# Synthesis Journal\n"]

    # System Metadata
    lines.append("## System Information")
    metadata = data.get('system_metadata', {})
    lines.append(f"- **System Name:** {metadata.get('system_name', '')}")
    lines.append(f"- **System Version:** {metadata.get('system_version', 'N/A')}")
    lines.append(f"- **Evaluator:** {metadata.get('evaluator_name', '')}")
    lines.append(f"- **Evaluation Period:** {metadata.get('evaluation_start_date', '')} to {metadata.get('evaluation_end_date', '')}")
    lines.append(f"- **Assessment Date:** {metadata.get('assessment_date', '')}")
    lines.append(f"- **Overall Confidence:** {metadata.get('confidence_level', '')}\n")

    # Quantitative Assessment
    lines.append("---\n")
    lines.append("## Quantitative Assessment\n")

    assessment = data.get('quantitative_assessment', {})
    avg_score = assessment.get('average_score', 0)
    lines.append(f"**Average Score:** {avg_score:.2f}/5\n")

    # Criteria Scores
    lines.append("### Performance Criteria\n")

    criteria_names = {
        'usability': 'Usability',
        'generation_speed': 'Generation Speed',
        'audio_quality': 'Audio Quality',
        'stylistic_accuracy': 'Stylistic Accuracy',
        'parameter_control': 'Parameter Control',
        'content_generation_control': 'Content Generation Control',
        'daw_integration': 'DAW Integration Capacity',
        'creative_workflow': 'Creative Workflow Support'
    }

    criteria = assessment.get('criteria', {})
    for criterion_id, criterion_name in criteria_names.items():
        criterion_data = criteria.get(criterion_id, {})
        score = criterion_data.get('score', 'N/A')
        confidence = criterion_data.get('confidence', 'N/A')
        evidence = criterion_data.get('evidence', 'No evidence provided')

        lines.append(f"#### {criterion_name}")
        lines.append(f"**Score:** {score}/5 (Confidence: {confidence}/5)\n")
        lines.append("**Evidence & Rationale:**")
        lines.append(f"{evidence}\n")

    # Overall Synthesis
    lines.append("---\n")
    lines.append("## Overall Synthesis\n")

    synthesis = assessment.get('synthesis', {})

    lines.append("### Top 3 Strengths")
    lines.append(f"{synthesis.get('top_strengths', 'Not provided')}\n")

    lines.append("### Top 3 Weaknesses")
    lines.append(f"{synthesis.get('top_weaknesses', 'Not provided')}\n")

    lines.append("### Standout Feature")
    lines.append(f"{synthesis.get('standout_feature', 'Not provided')}\n")

    lines.append("### Best Suited For")
    lines.append(f"{synthesis.get('best_suited_for', 'Not provided')}\n")

    lines.append("### Not Recommended For")
    lines.append(f"{synthesis.get('not_recommended_for', 'Not provided')}\n")

    lines.append("### Ideal User Profile")
    lines.append(f"{synthesis.get('ideal_user_profile', 'Not provided')}\n")

    # Imported Sessions
    lines.append("---\n")
    lines.append("## Imported Sessions\n")
    imported_sessions = data.get('imported_sessions', [])
    lines.append(f"**Total Sessions Imported:** {len(imported_sessions)}\n")

    for i, session in enumerate(imported_sessions[:5], 1):
        session_id = session.get('session_id', f'Session {i}')
        session_date = session.get('date', 'N/A')
        lines.append(f"{i}. {session_id} (Date: {session_date})")

    if len(imported_sessions) > 5:
        lines.append(f"\n... and {len(imported_sessions) - 5} more sessions\n")
    else:
        lines.append("")

    # Reflective Journal
    lines.append("---\n")
    lines.append("## Reflective Journal\n")
    journal = data.get('reflective_journal', {})
    entry_count = journal.get('entry_count', 0)
    lines.append(f"**Total Journal Entries:** {entry_count}\n")

    entries = journal.get('entries', [])
    for i, entry in enumerate(entries[:3], 1):
        entry_date = entry.get('date', 'N/A')
        entry_type = entry.get('type', 'General')
        entry_content = entry.get('content', '')

        lines.append(f"### Entry {i} - {entry_type} ({entry_date})")
        lines.append(f"{entry_content[:200]}{'...' if len(entry_content) > 200 else ''}\n")

    if len(entries) > 3:
        lines.append(f"... and {len(entries) - 3} more entries\n")

    # Footer
    lines.append("---\n")
    lines.append(f"*Generated with AI Music Evaluation Framework on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    return "\n".join(lines)


def export_to_csv(data: Dict[str, Any], filepath: str, template_type: str) -> bool:
    """
    Export template data to CSV format for analysis.

    CSV format focuses on quantitative data and metadata.
    Best for: quantitative assessments, comparative analysis

    Args:
        data: Template data dictionary
        filepath: Output file path
        template_type: Template type

    Returns:
        True if successful, False otherwise
    """
    try:
        rows = []

        if template_type in ('quantitative', 'quantitative_assessment'):
            # Export as: evaluator, system, date, criterion, score, evidence_snippet
            info = data.get('system_info', {})
            scores = data.get('criteria_scores', {})
            evidence = data.get('criteria_evidence', {})

            for criterion, score in scores.items():
                rows.append({
                    'evaluator': info.get('evaluator', ''),
                    'system': info.get('system', ''),
                    'date': info.get('date', ''),
                    'criterion': criterion,
                    'score': score,
                    'evidence': evidence.get(criterion, '')[:100] + '...' if evidence.get(criterion) else ''
                })

        elif template_type == 'comparative':
            # Export comparison matrix
            systems = data.get('systems_compared', [])
            matrix = data.get('comparison_matrix', {})

            for system in systems:
                system_scores = matrix.get(system, {})
                for criterion, score in system_scores.items():
                    rows.append({
                        'system': system,
                        'criterion': criterion,
                        'score': score
                    })

        elif template_type == 'session_log':
            # Export attempts
            info = data.get('session_info', {})
            attempts = data.get('generation_attempts', [])

            for i, attempt in enumerate(attempts, 1):
                rows.append({
                    'system': info.get('system', ''),
                    'date': info.get('date', ''),
                    'session_number': info.get('session_number', ''),
                    'attempt_number': i,
                    'prompt': attempt.get('prompt', ''),
                    'generation_time': attempt.get('generation_time', ''),
                    'quality': attempt.get('quality', ''),
                    'usable': attempt.get('usable', False)
                })

        elif template_type in ('synthesis', 'synthesis_journal'):
            # Export synthesis scores
            metadata = data.get('system_metadata', {})
            assessment = data.get('quantitative_assessment', {})
            criteria = assessment.get('criteria', {})

            for criterion_id, criterion_data in criteria.items():
                rows.append({
                    'evaluator': metadata.get('evaluator_name', ''),
                    'system': metadata.get('system_name', ''),
                    'system_version': metadata.get('system_version', ''),
                    'assessment_date': metadata.get('assessment_date', ''),
                    'criterion': criterion_id,
                    'score': criterion_data.get('score', ''),
                    'confidence': criterion_data.get('confidence', ''),
                    'evidence': criterion_data.get('evidence', '')[:100] + '...' if criterion_data.get('evidence') else ''
                })

        if rows:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            return True

        return False

    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False


def export_to_json(data: Dict[str, Any], filepath: str) -> bool:
    """
    Export template data to JSON format.

    Preserves complete data structure with metadata.

    Args:
        data: Template data dictionary
        filepath: Output file path

    Returns:
        True if successful, False otherwise

    Example:
        >>> data = {'system_info': {...}, 'scores': {...}}
        >>> export_to_json(data, 'output.json')
        True
    """
    try:
        # Add metadata
        export_data = {
            'export_date': datetime.now().isoformat(),
            'framework_version': '0.1.0',
            'data': data
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"Error exporting to JSON: {e}")
        return False


def parse_markdown_to_data(filepath: str) -> Optional[Dict[str, Any]]:
    """
    Parse exported Markdown back to data dictionary.

    Limited functionality - works best with consistently formatted exports.

    Args:
        filepath: Path to markdown file

    Returns:
        Parsed data dictionary or None if parsing fails
    """
    try:
        content = Path(filepath).read_text(encoding='utf-8')

        # Basic parsing - extract key-value pairs
        data = {}
        current_section = None

        for line in content.split('\n'):
            # Detect sections
            if line.startswith('## '):
                current_section = line[3:].strip().lower().replace(' ', '_')
                data[current_section] = {}

            # Extract key-value pairs
            elif line.startswith('- **') and current_section:
                match = re.match(r'- \*\*(.+?):\*\* (.+)', line)
                if match:
                    key = match.group(1).lower().replace(' ', '_')
                    value = match.group(2).strip()
                    data[current_section][key] = value

        return data if data else None

    except Exception as e:
        print(f"Error parsing markdown: {e}")
        return None

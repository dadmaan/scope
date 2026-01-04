"""
Evidence Extraction Engine

Searches loaded session logs for observations relevant to specific assessment criteria.
Keyword-based search across reflections, generation attempts, and critical incidents.

PRESERVED: Original logic, keywords, and formatting - NO MODIFICATIONS
"""


def extract_relevant_evidence(criterion_name, sessions):
    """
    Searches loaded sessions for observations relevant to a specific criterion.

    Args:
        criterion_name (str): Criterion identifier (e.g., 'usability', 'generation_speed')
        sessions (list): List of loaded session JSON objects

    Returns:
        list: Evidence items with session_id, date, source, and excerpt
    """
    # PRESERVED: Original keyword mappings - DO NOT MODIFY
    keyword_map = {
        'usability': ['interface', 'UI', 'ease', 'learning', 'documentation', 'intuitive', 'confusing', 'error'],
        'generation_speed': ['speed', 'fast', 'slow', 'latency', 'time', 'wait', 'generation time', 'quick'],
        'audio_quality': ['quality', 'artifact', 'noise', 'clarity', 'fidelity', 'compression', 'glitch'],
        'stylistic_accuracy': ['style', 'genre', 'accuracy', 'resemblance', 'faithful', 'consistent'],
        'parameter_control': ['parameter', 'control', 'predictable', 'responsive', 'precision', 'setting'],
        'content_control': ['stem', 'separation', 'modify', 'edit', 'flexibility', 'arrangement'],
        'daw_integration': ['DAW', 'integration', 'plugin', 'workflow', 'session', 'compatibility', 'export'],
        'creative_workflow': ['workflow', 'flow', 'creative', 'interruption', 'focus', 'frustration', 'momentum']
    }

    keywords = keyword_map.get(criterion_name, [])
    evidence = []

    for session in sessions:
        session_id = session.get('session_id', 'unknown')
        session_date = session.get('core_session', {}).get('metadata', {}).get('date', '')

        # Search in reflections
        reflections = session.get('core_session', {}).get('reflections', {})
        for field, text in reflections.items():
            if isinstance(text, str) and any(kw.lower() in text.lower() for kw in keywords):
                evidence.append({
                    'session_id': session_id,
                    'date': session_date,
                    'source': f'reflections.{field}',
                    'excerpt': text[:200] + '...' if len(text) > 200 else text
                })

        # Search in generation attempts
        attempts = session.get('core_session', {}).get('generation_attempts', [])
        for i, attempt in enumerate(attempts):
            for field in ['notable_observations', 'issues', 'artifacts']:
                text = attempt.get(field, '')
                if isinstance(text, str) and any(kw.lower() in text.lower() for kw in keywords):
                    evidence.append({
                        'session_id': session_id,
                        'date': session_date,
                        'source': f'attempt_{i+1}.{field}',
                        'excerpt': text[:200] + '...' if len(text) > 200 else text
                    })

        # Search in critical incident (if present)
        incident = session.get('optional_incident', {})
        if incident:
            incident_desc = incident.get('description', {})
            for field, text in incident_desc.items():
                if isinstance(text, str) and any(kw.lower() in text.lower() for kw in keywords):
                    evidence.append({
                        'session_id': session_id,
                        'date': session_date,
                        'source': f'incident.{field}',
                        'excerpt': text[:200] + '...' if len(text) > 200 else text
                    })

    return evidence


def format_evidence_display(evidence_list):
    """
    Formats evidence list for display in widget.

    Args:
        evidence_list (list): List of evidence items from extract_relevant_evidence()

    Returns:
        str: Formatted markdown string for display
    """
    if not evidence_list:
        return "No relevant evidence found in imported sessions."

    output = []
    for ev in evidence_list[:10]:  # Limit to 10 most relevant
        output.append(f"**{ev['session_id']}** ({ev['date']}) - {ev['source']}:")
        output.append(f"> {ev['excerpt']}")
        output.append("")  # blank line

    if len(evidence_list) > 10:
        output.append(f"... and {len(evidence_list) - 10} more evidence items")

    return "\n".join(output)

"""
Validation Export Synthesis - Export Builder Module

Collects all data from widgets into synthesis_data structure ready for export.
Preserves the complete schema structure for JSON, Markdown, and CSV export.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def collect_synthesis_data(
    synthesis_data,
    system_widgets,
    criterion_widgets,
    synthesis_widgets,
    loaded_sessions,
    calculate_scores_func
):
    """
    Gather all data from widgets into synthesis_data structure.

    Collects:
    - System metadata (system name, version, evaluator, dates, confidence)
    - Quantitative assessment (criteria scores, evidence, session references)
    - Overall synthesis (strengths, weaknesses, recommendations)
    - Updates modified timestamp

    Args:
        synthesis_data (dict): The synthesis journal data structure to update
        system_widgets (dict): Dictionary of system metadata widgets
        criterion_widgets (dict): Dictionary of criterion widgets (nested by criterion_id)
        synthesis_widgets (dict): Dictionary of synthesis widgets
        loaded_sessions (list): List of loaded session data
        calculate_scores_func (callable): Function that calculates scores and returns (scores, confidences, avg)

    Returns:
        dict: Updated synthesis_data ready for export

    Example:
        >>> data = collect_synthesis_data(
        ...     synthesis_data,
        ...     system_widgets,
        ...     criterion_widgets,
        ...     synthesis_widgets,
        ...     loaded_sessions,
        ...     calculate_scores
        ... )
        >>> print(f"Collected {len(data['quantitative_assessment']['criteria'])} criteria")
    """
    try:
        # Update system metadata
        synthesis_data['system_metadata'] = {
            'system_name': system_widgets.get('system_name').value if 'system_name' in system_widgets else '',
            'system_version': system_widgets.get('system_version').value if 'system_version' in system_widgets else '',
            'evaluator_name': system_widgets.get('evaluator_name').value if 'evaluator_name' in system_widgets else '',
            'evaluation_start_date': str(system_widgets.get('evaluation_start_date').value) if 'evaluation_start_date' in system_widgets and system_widgets.get('evaluation_start_date').value else '',
            'evaluation_end_date': str(system_widgets.get('evaluation_end_date').value) if 'evaluation_end_date' in system_widgets and system_widgets.get('evaluation_end_date').value else '',
            'assessment_date': str(system_widgets.get('assessment_date').value) if 'assessment_date' in system_widgets and system_widgets.get('assessment_date').value else '',
            'confidence_level': system_widgets.get('confidence_level').value if 'confidence_level' in system_widgets else ''
        }

        # Collect criterion data
        scores, confidences, avg = calculate_scores_func()

        for criterion_id, widgets_dict in criterion_widgets.items():
            criterion_data = {
                'score': scores.get(criterion_id, 0),
                'confidence': confidences.get(criterion_id, 3)
            }

            # Collect all widget values
            for field_name, widget in widgets_dict.items():
                if field_name not in ['score', 'confidence']:
                    if hasattr(widget, 'value'):
                        if isinstance(widget.value, (list, tuple)):
                            criterion_data[field_name] = list(widget.value)
                        else:
                            criterion_data[field_name] = widget.value

            # Add session references
            criterion_data['session_references'] = [
                s.get('session_id', '') for s in loaded_sessions[:5]
            ]

            synthesis_data['quantitative_assessment']['criteria'][criterion_id] = criterion_data

        # Update average score
        synthesis_data['quantitative_assessment']['average_score'] = avg

        # Collect synthesis
        synthesis_data['quantitative_assessment']['synthesis'] = {
            'top_strengths': synthesis_widgets.get('top_strengths').value if 'top_strengths' in synthesis_widgets else '',
            'top_weaknesses': synthesis_widgets.get('top_weaknesses').value if 'top_weaknesses' in synthesis_widgets else '',
            'standout_feature': synthesis_widgets.get('standout_feature').value if 'standout_feature' in synthesis_widgets else '',
            'best_suited_for': synthesis_widgets.get('best_suited_for').value if 'best_suited_for' in synthesis_widgets else '',
            'not_recommended_for': synthesis_widgets.get('not_recommended_for').value if 'not_recommended_for' in synthesis_widgets else '',
            'ideal_user_profile': synthesis_widgets.get('ideal_user_profile').value if 'ideal_user_profile' in synthesis_widgets else ''
        }

        # Update modified timestamp
        synthesis_data['modified_at'] = datetime.now().isoformat()

        logger.info(f"Data collected: {len(synthesis_data['quantitative_assessment']['criteria'])} criteria, "
                   f"{len(synthesis_data['imported_sessions'])} sessions")

        return synthesis_data

    except Exception as e:
        logger.error(f"Error collecting synthesis data: {e}")
        raise


def get_collection_summary(synthesis_data):
    """
    Generate a summary of collected data.

    Args:
        synthesis_data (dict): The synthesis journal data structure

    Returns:
        dict: Summary statistics

    Example:
        >>> summary = get_collection_summary(synthesis_data)
        >>> print(f"Criteria captured: {summary['criteria_count']}")
    """
    return {
        'criteria_count': len(synthesis_data['quantitative_assessment']['criteria']),
        'sessions_imported': len(synthesis_data['imported_sessions']),
        'journal_entries': synthesis_data['reflective_journal']['entry_count'],
        'average_score': synthesis_data['quantitative_assessment']['average_score'],
        'modified_at': synthesis_data.get('modified_at', '')
    }

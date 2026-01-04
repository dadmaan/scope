"""
Criterion 7: DAW Integration & Compatibility

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_7_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 7: DAW Integration & Compatibility tab.

    Args:
        loaded_sessions_ref (list): Reference to global loaded_sessions
        criterion_widgets_ref (dict): Reference to global criterion_widgets

    Returns:
        dict: {
            'container': VBox with criterion widgets,
            'widgets': {criterion widgets dict}
        }
    """

    # Indicators
    daw_indicators = [
        'Seamless DAW integration',
        'Plugin compatibility',
        'Stable workflow integration',
        'Easy export/import',
        'Session compatibility',
        'Minimal workflow disruption'
    ]

    # Create criterion widget set
    daw = create_criterion_widget_set(
        criterion_num=7,
        criterion_name='DAW Integration Capacity',
        criterion_key='daw_integration',
        indicators=daw_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #FF9800; border-bottom: 2px solid #FF9800; padding-bottom: 10px;">Criterion 7: DAW Integration Capacity</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Score DAW compatibility, file format support, metadata handling, and integration ease.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How well does the system integrate into DAW workflows?</p>'),
        widgets.HTML('<p><em>Consider: Plugin support, export/import, session compatibility</em></p>'),
        daw['score'],
        daw['confidence'],
        daw['indicators'],
        daw['view_btn'],
        daw['output'],
        daw['evidence'],
        daw['rationale']
    ])

    return {
        'container': container,
        'widgets': daw
    }

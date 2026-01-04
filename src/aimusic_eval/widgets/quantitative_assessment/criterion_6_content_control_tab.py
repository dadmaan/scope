"""
Criterion 6: Content Control & Flexibility

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_6_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 6: Content Control & Flexibility tab.

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
    content_indicators = [
        'Flexible content modification',
        'Stem separation capability',
        'Arrangement control',
        'Fine-grained editing options',
        'Selective regeneration',
        'Multi-track control'
    ]

    # Create criterion widget set
    content = create_criterion_widget_set(
        criterion_num=6,
        criterion_name='Content Generation Control',
        criterion_key='content_control',
        indicators=content_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">Criterion 6: Content Generation Control</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Rate control over melody, harmony, rhythm, texture, and specific musical elements.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How much control over generated content structure?</p>'),
        widgets.HTML('<p><em>Consider: Stems, arrangement, editing, selective modification</em></p>'),
        content['score'],
        content['confidence'],
        content['indicators'],
        content['view_btn'],
        content['output'],
        content['evidence'],
        content['rationale']
    ])

    return {
        'container': container,
        'widgets': content
    }

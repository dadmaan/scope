"""
Criterion 5: Parameter Control & Predictability

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_5_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 5: Parameter Control & Predictability tab.

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
    parameter_indicators = [
        'Predictable parameter behavior',
        'Responsive controls',
        'Precise adjustments possible',
        'Intuitive parameter mappings',
        'Granular control options',
        'Stable parameter response'
    ]

    # Create criterion widget set
    parameter = create_criterion_widget_set(
        criterion_num=5,
        criterion_name='Parameter Control',
        criterion_key='parameter_control',
        indicators=parameter_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">Criterion 5: Parameter Control</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Judge control over duration, tempo, key, dynamics, and other musical parameters.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How much control do parameters provide over output?</p>'),
        widgets.HTML('<p><em>Consider: Predictability, precision, responsiveness, granularity</em></p>'),
        parameter['score'],
        parameter['confidence'],
        parameter['indicators'],
        parameter['view_btn'],
        parameter['output'],
        parameter['evidence'],
        parameter['rationale']
    ])

    return {
        'container': container,
        'widgets': parameter
    }

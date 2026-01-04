"""
Criterion 2: Generation Speed & Latency

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_2_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 2: Generation Speed & Latency tab.

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
    speed_indicators = [
        'Fast generation times',
        'Minimal latency',
        'Real-time feedback',
        'Efficient iteration workflow',
        'Batch processing capability',
        'Responsive UI during generation'
    ]

    # Create criterion widget set
    speed = create_criterion_widget_set(
        criterion_num=2,
        criterion_name='Generation Speed',
        criterion_key='generation_speed',
        indicators=speed_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">Criterion 2: Generation Speed</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Rate generation time relative to output duration and assess wait time impact on workflow.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How quickly does the system generate content?</p>'),
        widgets.HTML('<p><em>Consider: Latency, iteration speed, real-time capabilities</em></p>'),
        speed['score'],
        speed['confidence'],
        speed['indicators'],
        speed['view_btn'],
        speed['output'],
        speed['evidence'],
        speed['rationale']
    ])

    return {
        'container': container,
        'widgets': speed
    }

"""
Criterion 1: Usability & Interface Design

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_1_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 1: Usability & Interface Design tab.

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
    usability_indicators = [
        'Interface clarity and intuitiveness',
        'Feature discoverability',
        'Documentation quality',
        'Helpful error messages',
        'Accessibility features',
        'Short learning curve'
    ]

    # Create criterion widget set
    usability = create_criterion_widget_set(
        criterion_num=1,
        criterion_name='Usability',
        criterion_key='usability',
        indicators=usability_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">Criterion 1: Usability</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Score ease of learning, interface clarity, documentation, and error handling.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How easy is the system to learn and use?</p>'),
        widgets.HTML('<p><em>Consider: UI clarity, documentation, error handling, learning curve</em></p>'),
        usability['score'],
        usability['confidence'],
        usability['indicators'],
        usability['view_btn'],
        usability['output'],
        usability['evidence'],
        usability['rationale']
    ])

    return {
        'container': container,
        'widgets': usability
    }

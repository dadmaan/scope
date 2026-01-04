"""
Criterion 8: Creative Workflow Integration

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_8_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 8: Creative Workflow Integration tab.

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
    workflow_indicators = [
        'Supports creative flow state',
        'Minimal interruptions',
        'Intuitive creative process',
        'Quick iteration cycles',
        'Maintains creative momentum',
        'Low cognitive overhead'
    ]

    # Create criterion widget set
    workflow = create_criterion_widget_set(
        criterion_num=8,
        criterion_name='Creative Workflow Support',
        criterion_key='creative_workflow',
        indicators=workflow_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #FF9800; border-bottom: 2px solid #FF9800; padding-bottom: 10px;">Criterion 8: Creative Workflow Support</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Evaluate impact on creative process, iteration speed, and workflow enhancement.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How well does the system support creative workflow?</p>'),
        widgets.HTML('<p><em>Consider: Flow state, interruptions, creative momentum, iteration</em></p>'),
        workflow['score'],
        workflow['confidence'],
        workflow['indicators'],
        workflow['view_btn'],
        workflow['output'],
        workflow['evidence'],
        workflow['rationale']
    ])

    return {
        'container': container,
        'widgets': workflow
    }

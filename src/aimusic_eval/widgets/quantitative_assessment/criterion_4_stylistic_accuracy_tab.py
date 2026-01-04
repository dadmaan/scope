"""
Criterion 4: Stylistic Range & Accuracy

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_4_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 4: Stylistic Range & Accuracy tab.

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
    stylistic_indicators = [
        'Faithful genre representation',
        'Accurate style adherence',
        'Consistent aesthetic',
        'Recognizable musical characteristics',
        'Appropriate instrumentation choices',
        'Stylistically coherent outputs'
    ]

    # Create criterion widget set
    stylistic = create_criterion_widget_set(
        criterion_num=4,
        criterion_name='Stylistic Accuracy',
        criterion_key='stylistic_accuracy',
        indicators=stylistic_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">Criterion 4: Stylistic Accuracy</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Assess genre consistency, timbral authenticity, and stylistic coherence of outputs.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> How accurately does the system match requested styles?</p>'),
        widgets.HTML('<p><em>Consider: Genre fidelity, style adherence, aesthetic consistency</em></p>'),
        stylistic['score'],
        stylistic['confidence'],
        stylistic['indicators'],
        stylistic['view_btn'],
        stylistic['output'],
        stylistic['evidence'],
        stylistic['rationale']
    ])

    return {
        'container': container,
        'widgets': stylistic
    }

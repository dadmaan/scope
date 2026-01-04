"""
Criterion 3: Audio Quality & Fidelity

PRESERVED: All widget content, labels, indicators - NO MODIFICATIONS
"""

import ipywidgets as widgets
from .criterion_builder import create_criterion_widget_set


def create_criterion_3_tab(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Criterion 3: Audio Quality & Fidelity tab.

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
    audio_indicators = [
        'High fidelity output',
        'Minimal artifacts',
        'Clean audio reproduction',
        'Professional sound quality',
        'Consistent quality across generations',
        'Absence of compression artifacts'
    ]

    # Create criterion widget set
    audio = create_criterion_widget_set(
        criterion_num=3,
        criterion_name='Audio Quality',
        criterion_key='audio_quality',
        indicators=audio_indicators,
        loaded_sessions_ref=loaded_sessions_ref,
        criterion_widgets_ref=criterion_widgets_ref
    )

    # Container layout
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">Criterion 3: Audio Quality</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Evaluate technical audio quality: fidelity, artifacts, frequency response, and dynamics.</p>'),
        widgets.HTML('<p><strong>Definition:</strong> What is the quality of generated audio?</p>'),
        widgets.HTML('<p><em>Consider: Fidelity, artifacts, clarity, professional sound</em></p>'),
        audio['score'],
        audio['confidence'],
        audio['indicators'],
        audio['view_btn'],
        audio['output'],
        audio['evidence'],
        audio['rationale']
    ])

    return {
        'container': container,
        'widgets': audio
    }

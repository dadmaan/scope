"""
Criterion Builder - DRY Pattern for Assessment Criteria

Factory function for creating criterion widget sets.
Reduces duplication across 8 identical criterion structures.

PRESERVED: All widget labels, options, placeholders - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import clear_output, Markdown
from ..session_import.evidence_extraction import extract_relevant_evidence, format_evidence_display


def create_criterion_widget_set(
    criterion_num,
    criterion_name,
    criterion_key,
    indicators,
    loaded_sessions_ref,
    criterion_widgets_ref
):
    """
    Create standard widget set for a single assessment criterion.

    Args:
        criterion_num (int): Criterion number (1-8)
        criterion_name (str): Display name (e.g., "Usability", "Generation Speed")
        criterion_key (str): Evidence extraction key (e.g., "usability", "generation_speed")
        indicators (list): List of strength indicator strings
        loaded_sessions_ref (list): Reference to global loaded_sessions
        criterion_widgets_ref (dict): Reference to global criterion_widgets dict

    Returns:
        dict: {
            'score': RadioButtons,
            'confidence': IntSlider,
            'indicators': SelectMultiple,
            'evidence': Textarea,
            'rationale': Textarea,
            'view_btn': Button,
            'output': Output
        }
    """

    # Score widget (1-5 scale) - PRESERVED OPTIONS
    score = widgets.RadioButtons(
        options=[
            ('1 - Fails to meet basic expectations', 1),
            ('2 - Meets minimum requirements with limitations', 2),
            ('3 - Satisfies acceptable standards', 3),
            ('4 - Exceeds expectations in most areas', 4),
            ('5 - Fully meets/surpasses all expectations', 5)
        ],
        description='Score:',
        style={'description_width': 'initial'}
    )

    # Confidence slider (1-5)
    confidence = widgets.IntSlider(
        value=3,
        min=1,
        max=5,
        description='Confidence:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='400px')
    )

    # Strength indicators (multi-select) - PRESERVED OPTIONS
    indicators_widget = widgets.SelectMultiple(
        options=indicators,
        description='Strengths:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(height='120px', width='500px')
    )

    # Evidence textarea
    evidence = widgets.Textarea(
        description='Evidence:',
        placeholder='Provide specific examples from your sessions...',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='150px')
    )

    # Rationale textarea
    rationale = widgets.Textarea(
        description='Rationale:',
        placeholder='Explain your score based on the evidence above',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    # Evidence output area
    evidence_output = widgets.Output()

    # View evidence button with callback
    def view_evidence(b):
        """Extract and display evidence from loaded sessions"""
        with evidence_output:
            clear_output()
            evidence_items = extract_relevant_evidence(criterion_key, loaded_sessions_ref)
            formatted = format_evidence_display(evidence_items)
            display(Markdown(formatted))

            # Auto-populate textarea with evidence
            if evidence_items:
                evidence.value = formatted[:1000]  # Limit to 1000 chars

    view_btn = widgets.Button(
        description='🔍 View Evidence from Sessions',
        button_style='info',
        layout=widgets.Layout(width='250px')
    )
    view_btn.on_click(view_evidence)

    # Store in criterion_widgets dict
    widget_key = f"{criterion_num}_{criterion_key}"
    criterion_widgets_ref[widget_key] = {
        'score': score,
        'confidence': confidence,
        'indicators': indicators_widget,
        'evidence': evidence,
        'rationale': rationale
    }

    # Return widget set
    return {
        'score': score,
        'confidence': confidence,
        'indicators': indicators_widget,
        'evidence': evidence,
        'rationale': rationale,
        'view_btn': view_btn,
        'output': evidence_output
    }

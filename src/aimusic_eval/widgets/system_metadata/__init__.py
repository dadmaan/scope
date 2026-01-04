"""
System Metadata Module

Provides widgets for capturing system information and evaluator metadata.
Part of the modularized Synthesis Journal architecture.

Returns:
    dict: {
        'container': VBox widget with all system metadata widgets,
        'widgets': dict of individual widget references
    }
"""

import ipywidgets as widgets
from IPython.display import display, HTML, Markdown
from datetime import date


def create_system_metadata_section():
    """
    Create system and evaluator metadata widgets.

    Returns:
        dict: {
            'container': VBox containing all metadata widgets,
            'widgets': {
                'system_name': Text widget,
                'system_version': Text widget,
                'evaluator_name': Text widget,
                'evaluation_start_date': DatePicker,
                'evaluation_end_date': DatePicker,
                'assessment_date': DatePicker,
                'confidence_level': Dropdown
            }
        }
    """

    # System metadata widgets
    system_name = widgets.Text(
        description='System Name:',
        placeholder='e.g., MusicGen, Riffusion, Magenta Studio',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    system_version = widgets.Text(
        description='Version:',
        placeholder='e.g., v1.2.0, Large model',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    evaluator_name = widgets.Text(
        description='Evaluator:',
        placeholder='Your name or ID',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    evaluation_start_date = widgets.DatePicker(
        description='Eval Start Date:',
        style={'description_width': 'initial'}
    )

    evaluation_end_date = widgets.DatePicker(
        description='Eval End Date:',
        value=date.today(),
        style={'description_width': 'initial'}
    )

    assessment_date = widgets.DatePicker(
        description='Assessment Date:',
        value=date.today(),
        style={'description_width': 'initial'}
    )

    confidence_level = widgets.Dropdown(
        options=[
            'Very confident (10+ sessions, extensive testing)',
            'Confident (5-9 sessions, good coverage)',
            'Moderate confidence (3-4 sessions, basic coverage)',
            'Low confidence (<3 sessions, limited testing)'
        ],
        description='Overall Confidence:',
        value='Confident (5-9 sessions, good coverage)',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )

    # Create container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #555;">System & Evaluator Information</h3><p style="color: #777; font-size: 14px;">Record system details, evaluator identity, and evaluation timeline for this assessment.</p>'),
        system_name,
        system_version,
        evaluator_name,
        evaluation_start_date,
        evaluation_end_date,
        assessment_date,
        confidence_level
    ])

    # Return structured data
    return {
        'container': container,
        'widgets': {
            'system_name': system_name,
            'system_version': system_version,
            'evaluator_name': evaluator_name,
            'evaluation_start_date': evaluation_start_date,
            'evaluation_end_date': evaluation_end_date,
            'assessment_date': assessment_date,
            'confidence_level': confidence_level
        }
    }

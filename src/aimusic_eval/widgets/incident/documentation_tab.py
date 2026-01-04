"""
Documentation Tab Module

Creates the Reproducibility & Documentation tab for incident
reproducibility tracking and documentation.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_incident_documentation_tab():
    """Create the Reproducibility & Documentation sub-tab."""
    # Reproducibility Widgets
    reproducibility_level = widgets.RadioButtons(
        options=[
            'Consistently reproducible',
            'Sometimes reproducible',
            'Difficult to reproduce',
            'Not reproducible',
            'Have not attempted'
        ],
        description='Reproducibility:',
        value='Have not attempted',
        style={'description_width': 'initial'}
    )

    reproduction_steps = widgets.Textarea(
        description='Steps:',
        placeholder='Detailed steps to reproduce this incident',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    reproduction_conditions = widgets.Textarea(
        description='Conditions:',
        placeholder='Specific conditions or context needed for reproduction',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    reproduction_attempts = widgets.IntText(
        value=0,
        description='Attempts made:',
        style={'description_width': 'initial'}
    )

    success_rate = widgets.Text(
        description='Success rate:',
        placeholder='e.g., "3 out of 5 attempts"',
        style={'description_width': 'initial'}
    )

    # Documentation Widgets
    evidence_types = widgets.SelectMultiple(
        options=[
            'Screenshots',
            'Audio recordings',
            'Video screen capture',
            'System logs',
            'Prompt history',
            'Generated output files',
            'Error messages',
            'None'
        ],
        description='Evidence types:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(height='160px')
    )

    evidence_location = widgets.Text(
        description='Location:',
        placeholder='Path or reference to evidence files',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px')
    )

    related_incidents = widgets.Textarea(
        description='Related incidents:',
        placeholder='References to similar incidents or patterns',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    follow_up = widgets.Textarea(
        description='Follow-up:',
        placeholder='What additional investigation or testing is needed?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #555; border-bottom: 2px solid #555; padding-bottom: 10px;">📋 Reproducibility & Documentation</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Document evidence:</strong> logs, screenshots, audio files, and supporting materials.</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Distill the insights from this event. Document what you learned about the system or your own process, and note any recommendations or follow-up actions you plan to take to test your new understanding.</p>"),
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Reproducibility</h4>'),
        reproducibility_level,
        reproduction_steps,
        reproduction_conditions,
        widgets.HBox([reproduction_attempts, success_rate]),
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Documentation</h4>'),
        evidence_types,
        evidence_location,
        related_incidents,
        follow_up
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'reproducibility_level': reproducibility_level,
        'reproduction_steps': reproduction_steps,
        'reproduction_conditions': reproduction_conditions,
        'reproduction_attempts': reproduction_attempts,
        'success_rate': success_rate,
        'evidence_types': evidence_types,
        'evidence_location': evidence_location,
        'related_incidents': related_incidents,
        'follow_up': follow_up
    }

    return {'container': container, 'widgets': widgets_dict}

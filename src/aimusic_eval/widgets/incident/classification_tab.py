"""
Classification Tab Module

Creates the Classification & Description tab for incident metadata
and detailed description.
"""

import logging
import ipywidgets as widgets
from datetime import date

# Configure module logger
logger = logging.getLogger(__name__)


def create_incident_classification_tab():
    """Create the Classification & Description sub-tab."""
    # Classification Widgets
    incident_logged = widgets.Checkbox(
        value=False,
        description='Log a critical incident',
        style={'description_width': 'initial'}
    )

    incident_date = widgets.DatePicker(
        description='Date:',
        value=date.today(),
        style={'description_width': 'initial'}
    )

    incident_time = widgets.Text(
        description='Time:',
        value='',  # Will be set in notebook
        placeholder='HH:MM',
        style={'description_width': 'initial'}
    )

    incident_type = widgets.Dropdown(
        options=[
            'Breakthrough/Success',
            'Failure/Error',
            'Unexpected Behavior',
            'Workflow Discovery',
            'Creative Insight',
            'Technical Issue',
            'Prompt Engineering Discovery',
            'Integration Challenge',
            'Quality Issue'
        ],
        description='Type:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='400px')
    )

    incident_severity = widgets.RadioButtons(
        options=['Minor', 'Moderate', 'Major', 'Critical'],
        description='Severity:',
        value='Moderate',
        style={'description_width': 'initial'}
    )

    # Description Widgets
    what_happened = widgets.Textarea(
        description='What happened:',
        placeholder='Detailed chronological description of the incident',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='120px')
    )

    incident_goal = widgets.Textarea(
        description='Your goal:',
        placeholder='What you were trying to accomplish',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    expected_outcome = widgets.Textarea(
        description='Expected:',
        placeholder='What you expected to happen',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    actual_outcome = widgets.Textarea(
        description='Actual:',
        placeholder='What actually occurred',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    why_notable = widgets.Textarea(
        description='Why notable:',
        placeholder='What made this incident significant or surprising',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #E91E63; border-bottom: 2px solid #E91E63; padding-bottom: 10px;">🚨 Critical Incident Logging</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Document observations:</strong> record incident type, timestamp, severity, and detailed description of what occurred.</div>'),
        
        widgets.HTML('<p style="margin: 0; font-size: 16px;">📌 When logging a new incident, start here to categorize the event and assess its impact. Classifying its type and severity helps to contextualize its importance within the broader evaluation.</p>'),
        
        
        incident_logged,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Classification</h4>'),
        widgets.HBox([incident_date, incident_time]),
        incident_type,
        incident_severity,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Description</h4>'),
        what_happened,
        incident_goal,
        expected_outcome,
        actual_outcome,
        why_notable
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'incident_logged': incident_logged,
        'incident_date': incident_date,
        'incident_time': incident_time,
        'incident_type': incident_type,
        'incident_severity': incident_severity,
        'what_happened': what_happened,
        'incident_goal': incident_goal,
        'expected_outcome': expected_outcome,
        'actual_outcome': actual_outcome,
        'why_notable': why_notable
    }

    return {'container': container, 'widgets': widgets_dict}

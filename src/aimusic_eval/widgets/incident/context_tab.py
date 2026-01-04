"""
Context Tab Module

Creates the Context & Analysis tab for incident context, autoethnography,
and analysis.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_incident_context_tab():
    """Create the Context & Analysis sub-tab."""
    # Context Widgets
    prior_actions = widgets.Textarea(
        description='Prior actions:',
        placeholder='What steps led to this incident (chronological)',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    system_state = widgets.Textarea(
        description='System state:',
        placeholder='System behavior, settings, environmental factors',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # Autoethnographic context (CRITICAL for T03)
    time_of_day = widgets.Dropdown(
        options=['Morning (6am-12pm)', 'Afternoon (12pm-6pm)', 'Evening (6pm-12am)', 'Night (12am-6am)'],
        description='Time of day:',
        style={'description_width': 'initial'}
    )

    fatigue_level = widgets.RadioButtons(
        options=['Fresh/Alert', 'Normal', 'Somewhat Tired', 'Very Fatigued'],
        description='Fatigue level:',
        value='Normal',
        style={'description_width': 'initial'}
    )

    incident_emotional_state = widgets.Dropdown(
        options=['Curious/Exploratory', 'Focused/Determined', 'Frustrated', 'Excited', 'Neutral', 'Confused', 'Other'],
        description='Emotional state:',
        style={'description_width': 'initial'}
    )

    external_pressures = widgets.Textarea(
        description='External pressures:',
        placeholder='Deadlines, distractions, other contextual factors',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # Analysis Widgets
    significance = widgets.Textarea(
        description='Significance:',
        placeholder='Why this incident matters to your evaluation',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    affected_criteria = widgets.SelectMultiple(
        options=[
            '1. Usability',
            '2. Generation Speed',
            '3. Audio Quality',
            '4. Stylistic Accuracy',
            '5. Parameter Control',
            '6. Content Generation Control',
            '7. DAW Integration',
            '8. Creative Workflow Fit'
        ],
        description='Affected criteria:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(height='180px')
    )

    theoretical_insights = widgets.Textarea(
        description='Theoretical insights:',
        placeholder='What does this reveal about AI music generation, creativity, or evaluation?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    workflow_impact = widgets.Textarea(
        description='Workflow impact:',
        placeholder='How did this change your approach or understanding?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #E91E63; border-bottom: 2px solid #E91E63; padding-bottom: 10px;">🔍 Incident Context & Analysis</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Capture surrounding conditions:</strong> system state, user actions, and environmental factors.</div>'),
        
        widgets.HTML('<p style="margin: 0; font-size: 16px;">📌 Provide a narrative of what occurred. Explain what you were trying to accomplish, what you expected to happen versus what actually happened, and why you believe this event is significant or noteworthy.</p>'),
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Context</h4>'),
        prior_actions,
        system_state,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Autoethnography (Your State)</h4>'),
        time_of_day,
        fatigue_level,
        incident_emotional_state,
        external_pressures,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Analysis</h4>'),
        significance,
        affected_criteria,
        theoretical_insights,
        workflow_impact
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'prior_actions': prior_actions,
        'system_state': system_state,
        'time_of_day': time_of_day,
        'fatigue_level': fatigue_level,
        'incident_emotional_state': incident_emotional_state,
        'external_pressures': external_pressures,
        'significance': significance,
        'affected_criteria': affected_criteria,
        'theoretical_insights': theoretical_insights,
        'workflow_impact': workflow_impact
    }

    return {'container': container, 'widgets': widgets_dict}

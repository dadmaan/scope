"""
Experience Tab Module

Creates the Creative Experience tab for documenting flow state
and creative satisfaction.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_workflow_experience_tab():
    """Create the Creative Experience sub-tab."""
    # Creative Experience Widgets
    exp_flow_state = widgets.RadioButtons(
        options=['Deep flow', 'Good focus', 'Moderate', 'Distracted', 'Frustrated'],
        description='Flow state:',
        style={'description_width': 'initial'}
    )
    
    exp_satisfaction = widgets.IntSlider(
        value=3,
        min=1,
        max=5,
        description='Satisfaction:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='400px')
    )
    
    exp_reflection = widgets.Textarea(
        description='Reflection:',
        placeholder='How did this phase affect your creative process?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    exp_would_repeat = widgets.RadioButtons(
        options=['Definitely', 'Probably', 'Maybe', 'Probably not', 'Definitely not'],
        description='Would repeat?',
        style={'description_width': 'initial'}
    )
    
    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">✨ Creative Experience</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;">Evaluate system effectiveness, tool performance, collaboration, and overall experience.</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Conclude your workflow documentation by analyzing the phase's outcome and reflecting on the experience. Assess your efficiency, whether you achieved your goals, and your overall creative satisfaction with the process.</p>"),
                
        exp_flow_state,
        exp_satisfaction,
        exp_reflection,
        exp_would_repeat
    ])
    
    # Create widget reference dictionary
    widgets_dict = {
        'exp_flow_state': exp_flow_state,
        'exp_satisfaction': exp_satisfaction,
        'exp_reflection': exp_reflection,
        'exp_would_repeat': exp_would_repeat
    }
    
    return {'container': container, 'widgets': widgets_dict}

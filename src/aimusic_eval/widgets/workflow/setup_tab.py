"""
Setup Tab Module

Creates the Phase Setup tab for workflow phase metadata
and pre-phase planning.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_workflow_setup_tab():
    """Create the Phase Setup sub-tab."""
    # Phase Metadata Widgets
    phase_type = widgets.Dropdown(
        options=['Content Generation', 'Curation', 'Integration', 'Post-Production'],
        value='Content Generation',
        description='Phase Type:',
        style={'description_width': 'initial'}
    )
    
    phase_start_time = widgets.Text(
        description='Start Time:',
        placeholder='HH:MM',
        style={'description_width': 'initial'}
    )
    
    phase_end_time = widgets.Text(
        description='End Time:',
        placeholder='HH:MM',
        style={'description_width': 'initial'}
    )
    
    systems_used = widgets.Textarea(
        description='Systems Used:',
        placeholder='List AI systems used (one per line)',
        layout=widgets.Layout(width='500px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    # Pre-Phase Planning Widgets
    phase_goal = widgets.Textarea(
        description='Goal:',
        placeholder='What do you want to achieve in this phase?',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    phase_materials = widgets.Textarea(
        description='Materials:',
        placeholder='Existing tracks, loops, ideas, prompts prepared, etc.',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    phase_vision = widgets.Textarea(
        description='Vision:',
        placeholder='Describe the intended outcome for this phase',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    phase_expected_challenges = widgets.Textarea(
        description='Expected challenges:',
        placeholder='What do you anticipate being difficult?',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    time_estimate = widgets.FloatText(
        description='Time estimate (min):',
        value=30.0,
        step=5.0,
        style={'description_width': 'initial'}
    )
    
    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">⚙️ Workflow Documentation</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Document details:</strong> define phase type, time bounds, systems used, goals, and expected deliverables.</div>'),
        
        widgets.HTML('<p style="margin: 0; font-size: 16px;">📌 Begin here to define the specific phase you are about to undertake, such as "Curation" or "Integration." This selection will tailor the subsequent tabs to capture the most relevant information for that particular stage of the creative process.</p>'),
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Phase Metadata</h4>'),
        phase_type,
        widgets.HBox([phase_start_time, phase_end_time]),
        systems_used,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Pre-Phase State</h4>'),
        phase_goal,
        phase_materials,
        phase_vision,
        phase_expected_challenges,
        time_estimate
    ])
    
    # Create widget reference dictionary
    widgets_dict = {
        'phase_type': phase_type,
        'phase_start_time': phase_start_time,
        'phase_end_time': phase_end_time,
        'systems_used': systems_used,
        'phase_goal': phase_goal,
        'phase_materials': phase_materials,
        'phase_vision': phase_vision,
        'phase_expected_challenges': phase_expected_challenges,
        'time_estimate': time_estimate
    }
    
    return {'container': container, 'widgets': widgets_dict}

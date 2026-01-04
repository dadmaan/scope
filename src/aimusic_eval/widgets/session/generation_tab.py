"""
Generation Tab Module

Creates the Generation Attempts tab for documenting re-runnable generation attempts.
Note: Global variables (generation_attempts, attempt_counter) must be maintained
in notebook scope for re-runnable cells.
"""

import logging
import ipywidgets as widgets
from datetime import datetime

# Configure module logger
logger = logging.getLogger(__name__)


def create_generation_attempts_tab():
    """
    Create the Generation sub-tab with re-runnable attempt logging.
    
    Note: This function creates the UI for ONE attempt. The notebook cell that calls this
    should be re-runnable to add multiple attempts. Global variables generation_attempts
    and attempt_counter must be maintained in the notebook scope.
    
    Returns:
        dict: {
            'container': VBox widget with generation attempt UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating Generation Attempts tab")
    
    # Get attempt counter from globals (will be set in notebook)
    # This is a placeholder - actual counter comes from notebook globals
    import builtins
    if hasattr(builtins, 'attempt_counter'):
        attempt_counter = builtins.attempt_counter
    else:
        attempt_counter = 1
    
    # Create widgets for this attempt
    attempt_time = widgets.Text(
        description='Time:',
        value=datetime.now().strftime('%H:%M'),
        style={'description_width': '100px'}
    )

    input_type = widgets.Dropdown(
        options=['Text prompt', 'MIDI file', 'Audio file', 'Melody condition', 'Attribute tags', 'Other'],
        description='Input Type:',
        style={'description_width': '100px'}
    )

    input_content = widgets.Textarea(
        description='Input:',
        placeholder='Exact prompt or input specification',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='600px', height='80px')
    )

    parameters = widgets.Textarea(
        description='Parameters:',
        placeholder='e.g., duration=30s, temperature=0.9, model=large',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    generation_time = widgets.Text(
        description='Gen Time:',
        placeholder='e.g., 45 seconds for 30s output',
        style={'description_width': '100px'}
    )

    output_description = widgets.Textarea(
        description='Output:',
        placeholder='Detailed description of what was generated',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='600px', height='80px')
    )

    match_to_intent = widgets.RadioButtons(
        options=['Perfect', 'Close', 'Partial', 'Poor', 'Completely different'],
        description='Match:',
        style={'description_width': '100px'}
    )

    quality_rating = widgets.IntSlider(
        value=3,
        min=1,
        max=5,
        description='Quality:',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='400px')
    )

    usability = widgets.RadioButtons(
        options=['Usable as-is', 'Usable with processing', 'Not usable', 'Uncertain'],
        description='Usability:',
        style={'description_width': '100px'}
    )

    issues = widgets.SelectMultiple(
        options=[
            'Prompt interpretation failure',
            'Wrong instrument/element',
            'Multiple instruments blended',
            'Poor audio quality',
            'Structural incoherence',
            'Wrong tempo/key/style',
            'Too short/long',
            'Technical error/crash',
            'None'
        ],
        description='Issues:',
        style={'description_width': '100px'},
        layout=widgets.Layout(height='150px')
    )

    artifacts = widgets.SelectMultiple(
        options=[
            'Compression artifacts',
            'Frequency issues',
            'Timing/rhythm inconsistencies',
            'Pitch/tuning problems',
            'Glitches or noise',
            'None'
        ],
        description='Artifacts:',
        style={'description_width': '100px'},
        layout=widgets.Layout(height='120px')
    )

    notable_observations = widgets.Textarea(
        description='Notes:',
        placeholder='Anything unexpected, interesting, or significant',
        style={'description_width': '100px'},
        layout=widgets.Layout(width='600px', height='80px')
    )

    # Save button callback - will be set up in notebook with access to globals
    def save_attempt(b):
        # This will be properly implemented in the notebook where globals are accessible
        pass
    
    save_button = widgets.Button(
        description=f'💾 Save Attempt',
        button_style='success',
        layout=widgets.Layout(width='200px')
    )
    save_button.on_click(save_attempt)

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">🎲 Generation Attempts</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Document each generation attempt:</strong> inputs, outputs, quality, issues, and artifacts</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Document each attempt to generate audio in this section. This is where you'll log your specific prompts, the system's parameters, and your immediate impressions of the output's quality and usability, along with any technical issues or audio artifacts you observe.</p>"),
        
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Attempt Details</h4>'),
        widgets.HBox([attempt_time, input_type]),
        input_content,
        parameters,
        generation_time,
        output_description,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Quality Assessment</h4>'),
        match_to_intent,
        quality_rating,
        usability,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Issues & Artifacts</h4>'),
        issues,
        artifacts,
        notable_observations,
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Save Your Attempt: </strong>Save your attempts incrementally as performing the evaluation</div>'),
        save_button
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'attempt_time': attempt_time,
        'input_type': input_type,
        'input_content': input_content,
        'parameters': parameters,
        'generation_time': generation_time,
        'output_description': output_description,
        'match_to_intent': match_to_intent,
        'quality_rating': quality_rating,
        'usability': usability,
        'issues': issues,
        'artifacts': artifacts,
        'notable_observations': notable_observations,
        'save_button': save_button
    }

    logger.debug("✅ Generation Attempts tab created")
    return {'container': container, 'widgets': widgets_dict}

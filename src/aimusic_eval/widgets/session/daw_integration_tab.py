"""
DAW Integration Tab Module

Creates the DAW Integration tab for documenting how generated content
integrates with digital audio workstations.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_daw_integration_tab():
    """
    Create the DAW Integration sub-tab (converted from accordion).
    
    Returns:
        dict: {
            'container': VBox widget with DAW integration UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating DAW Integration tab")
    
    # DAW Integration Widgets
    daw = widgets.Dropdown(
        options=['Ableton Live', 'Logic Pro', 'FL Studio', 'Pro Tools', 'Cubase', 'Studio One', 'Reaper', 'Other', 'None tested'],
        description='DAW:',
        style={'description_width': 'initial'}
    )

    file_format = widgets.Dropdown(
        options=['WAV', 'MP3', 'AIFF', 'FLAC', 'MIDI', 'Other'],
        description='File format:',
        style={'description_width': 'initial'}
    )

    sample_rate = widgets.Text(
        description='Sample rate:',
        placeholder='e.g., 44.1kHz/16-bit',
        style={'description_width': 'initial'}
    )

    daw_context = widgets.Textarea(
        description='Context:',
        placeholder='What you integrated with (e.g., existing drum loop at 90 BPM)',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    daw_issues = widgets.SelectMultiple(
        options=[
            'Tempo sync problems',
            'Cannot start on specific beat',
            'Timing/rhythm drift',
            'Key/pitch incompatibility',
            'File format issues',
            'Metadata loss',
            'Plugin compatibility',
            'None'
        ],
        description='Issues:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(height='150px')
    )

    workarounds = widgets.Textarea(
        description='Workarounds:',
        placeholder='Any adaptations or manual adjustments needed',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='80px')
    )

    integration_ease = widgets.RadioButtons(
        options=['Seamless', 'Minor adjustments', 'Significant work', 'Failed'],
        description='Ease:',
        style={'description_width': 'initial'}
    )

    integration_time = widgets.Text(
        description='Time to integrate:',
        placeholder='e.g., 5 minutes',
        style={'description_width': 'initial'}
    )

    integration_result = widgets.RadioButtons(
        options=['Fully integrated', 'Partially integrated', 'Could not integrate'],
        description='Final result:',
        style={'description_width': 'initial'}
    )

    # Organize into container (no accordion - direct display)
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #FF9800; border-bottom: 2px solid #FF9800; padding-bottom: 10px;">🎹 DAW Integration Testing</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Record DAW workflow:</strong> import process, editing, mixing, and integration challenges</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 If you test the generated audio in a Digital Audio Workstation (DAW), describe that process here. This section is for logging compatibility, synchronization issues, and the general ease or difficulty of making the system's output function within a standard production environment.</p>"),
                
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Integration Details</h4>'),
        daw,
        file_format,
        sample_rate,
        daw_context,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Challenges & Workarounds</h4>'),
        daw_issues,
        workarounds,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Integration Results</h4>'),
        integration_ease,
        integration_time,
        integration_result
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'daw': daw,
        'file_format': file_format,
        'sample_rate': sample_rate,
        'daw_context': daw_context,
        'daw_issues': daw_issues,
        'workarounds': workarounds,
        'integration_ease': integration_ease,
        'integration_time': integration_time,
        'integration_result': integration_result
    }

    logger.debug("✅ DAW Integration tab created")
    return {'container': container, 'widgets': widgets_dict}

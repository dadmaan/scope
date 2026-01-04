"""
System Selector Tab Module

Creates the system selection and management interface for Phase 0.
Allows creating new systems and loading existing assessments.
"""

import logging
import ipywidgets as widgets
from datetime import date

logger = logging.getLogger(__name__)


def create_system_selector_tab(state_manager=None):
    """
    Create the System Selector tab for Phase 0.
    
    This tab provides:
    - New system creation form
    - Existing system dropdown selector
    - Save/Load buttons
    - Current system status display
    
    Args:
        state_manager: Phase 0 StateManager instance (optional)
    
    Returns:
        dict: {
            'container': VBox widget with system selector UI,
            'widgets': {
                'system_name': Text widget,
                'category': Dropdown widget,
                'notes': Textarea widget,
                'existing_selector': Dropdown widget,
                'save_button': Button widget,
                'load_button': Button widget,
                'new_button': Button widget,
                'status_output': Output widget
            }
        }
    """
    logger.debug("Creating System Selector tab")
    
    # Header
    header = widgets.HTML(
        value="<h3>🎵 System Selection & Management</h3>"
              "<p>Create a new system assessment or load an existing one.</p>"
    )
    
    # NEW SYSTEM SECTION
    new_system_header = widgets.HTML(
        value="<h4>New System</h4>"
    )
    
    system_name = widgets.Text(
        description='System Name:',
        placeholder='e.g., MusicGen, Riffusion, Stable Audio',
        style={'description_width': '120px'},
        layout=widgets.Layout(width='500px')
    )
    
    category = widgets.Dropdown(
        options=[
            'Text-to-Music',
            'Audio-to-Audio',
            'MIDI-based',
            'Hybrid/Multimodal',
            'Stem Separation/Editing',
            'Voice Synthesis',
            'Sound Effect Generation',
            'Other'
        ],
        description='Category:',
        style={'description_width': '120px'},
        layout=widgets.Layout(width='400px')
    )
    
    notes = widgets.Textarea(
        description='Initial Notes:',
        placeholder='Optional: Brief description, version info, access method, etc.',
        style={'description_width': '120px'},
        layout=widgets.Layout(width='600px', height='80px')
    )
    
    new_system_box = widgets.VBox([
        new_system_header,
        system_name,
        category,
        notes
    ])
    
    # EXISTING SYSTEMS SECTION
    existing_header = widgets.HTML(
        value="<h4>Load Existing System</h4>"
    )
    
    # Populate with existing systems if state_manager provided
    existing_options = ['-- Select System --']
    if state_manager:
        existing_options.extend(state_manager.list_all())
    
    existing_selector = widgets.Dropdown(
        options=existing_options,
        description='Existing System:',
        style={'description_width': '120px'},
        layout=widgets.Layout(width='500px')
    )
    
    existing_box = widgets.VBox([
        existing_header,
        existing_selector
    ])
    
    # ACTION BUTTONS
    button_box = widgets.HBox([
        widgets.Button(
            description='💾 Save Current',
            button_style='success',
            tooltip='Save current system assessment',
            layout=widgets.Layout(width='150px', margin='5px')
        ),
        widgets.Button(
            description='📂 Load Selected',
            button_style='primary',
            tooltip='Load selected system from dropdown',
            layout=widgets.Layout(width='150px', margin='5px')
        ),
        widgets.Button(
            description='🆕 New System',
            button_style='info',
            tooltip='Clear form to start new system',
            layout=widgets.Layout(width='150px', margin='5px')
        )
    ])
    
    save_button = button_box.children[0]
    load_button = button_box.children[1]
    new_button = button_box.children[2]
    
    # STATUS OUTPUT
    status_output = widgets.Output(
        layout=widgets.Layout(
            border='1px solid #ddd',
            padding='10px',
            margin='10px 0'
        )
    )
    
    # Assemble container
    container = widgets.VBox([
        header,
        widgets.HTML("<hr>"),
        new_system_box,
        widgets.HTML("<hr>"),
        existing_box,
        button_box,
        status_output
    ])
    
    # Return standard structure
    return {
        'container': container,
        'widgets': {
            'system_name': system_name,
            'category': category,
            'notes': notes,
            'existing_selector': existing_selector,
            'save_button': save_button,
            'load_button': load_button,
            'new_button': new_button,
            'status_output': status_output,
            'state_manager': state_manager  # Pass through for callbacks
        }
    }

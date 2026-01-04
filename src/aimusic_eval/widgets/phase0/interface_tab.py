"""
Interface & Interaction Tab Module

Creates the Interface & Interaction (Criterion 2) assessment interface for Phase 0.
Evaluates usability, setup complexity, and interaction patterns.
"""

import logging
import ipywidgets as widgets
from ..constants import INTERACTION_MODES, SETUP_COMPLEXITY, INTERFACE_TYPES

logger = logging.getLogger(__name__)


def create_interface_tab(state_manager=None):
    """
    Create the Interface & Interaction tab for Phase 0.
    
    This tab assesses:
    - Interaction modes available
    - Primary interface type
    - Setup complexity
    - GPU/hardware requirements for setup
    - Estimated setup time
    - Confidence rating (1-5)
    - Supporting evidence
    
    Args:
        state_manager: Phase 0 StateManager instance (optional)
    
    Returns:
        dict: {
            'container': VBox widget with interface assessment UI,
            'widgets': {
                'interaction_modes': SelectMultiple widget,
                'interface_type': Dropdown widget,
                'setup_complexity': Dropdown widget,
                'gpu_required': Checkbox widget,
                'setup_time_minutes': IntText widget,
                'confidence': IntSlider widget,
                'evidence': Textarea widget
            }
        }
    """
    logger.debug("Creating Interface & Interaction tab")
    
    # Header
    header = widgets.HTML(
        value="<h3>🖥️ Criterion 2: Interface & Interaction</h3>"
              "<p>Assess the user interface, interaction patterns, and setup experience.</p>"
    )
    
    # Interaction modes (multiple selection)
    interaction_modes = widgets.SelectMultiple(
        options=INTERACTION_MODES,
        description='Interaction Modes:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px', height='150px')
    )
    
    interaction_help = widgets.HTML(
        value="<small><i>Hold Ctrl/Cmd to select multiple modes</i></small>"
    )
    
    # Primary interface type
    interface_type = widgets.Dropdown(
        options=INTERFACE_TYPES,
        description='Interface Type:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    # Setup complexity
    setup_complexity = widgets.Dropdown(
        options=SETUP_COMPLEXITY,
        description='Setup Complexity:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    # GPU required for setup
    gpu_required = widgets.Checkbox(
        value=False,
        description='GPU Required for Setup',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='300px')
    )
    
    # Estimated setup time
    setup_time_minutes = widgets.IntText(
        value=0,
        description='Setup Time (min):',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='300px')
    )
    
    setup_time_help = widgets.HTML(
        value="<small><i>Approximate time from download to first generation</i></small>"
    )
    
    # Confidence rating
    confidence_label = widgets.HTML(
        value="<hr><b>Confidence Rating</b><br>"
              "<small>How confident are you in this assessment?</small>"
    )
    
    confidence = widgets.IntSlider(
        value=3,
        min=1,
        max=5,
        step=1,
        description='Confidence:',
        readout_format='d',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    confidence_scale = widgets.HTML(
        value="<small>1 = Uncertain | 2 = Low | 3 = Moderate | 4 = High | 5 = Very High</small>"
    )
    
    # Supporting evidence
    evidence = widgets.Textarea(
        description='Evidence:',
        placeholder='Setup guides, user reviews, personal experience, video tutorials, etc.',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='700px', height='100px')
    )
    
    # Assemble container
    container = widgets.VBox([
        header,
        widgets.HTML("<hr>"),
        interaction_modes,
        interaction_help,
        interface_type,
        setup_complexity,
        gpu_required,
        setup_time_minutes,
        setup_time_help,
        confidence_label,
        confidence,
        confidence_scale,
        evidence
    ])
    
    # Return standard structure
    return {
        'container': container,
        'widgets': {
            'interaction_modes': interaction_modes,
            'interface_type': interface_type,
            'setup_complexity': setup_complexity,
            'gpu_required': gpu_required,
            'setup_time_minutes': setup_time_minutes,
            'confidence': confidence,
            'evidence': evidence
        }
    }

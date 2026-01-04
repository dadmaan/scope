"""
Architecture & Design Tab Module

Creates the Architecture & Design (Criterion 1) assessment interface for Phase 0.
Evaluates the AI/ML architecture and generation approach.
"""

import logging
import ipywidgets as widgets
from ..constants import FRAMEWORKS, GENERATION_MODES, MODALITIES

logger = logging.getLogger(__name__)


def create_architecture_tab(state_manager=None):
    """
    Create the Architecture & Design tab for Phase 0.
    
    This tab assesses:
    - Underlying AI/ML framework
    - Generation mode/approach
    - Modalities supported
    - Conditioning mechanisms
    - Confidence rating (1-5)
    - Supporting evidence
    
    Args:
        state_manager: Phase 0 StateManager instance (optional)
    
    Returns:
        dict: {
            'container': VBox widget with architecture assessment UI,
            'widgets': {
                'framework': Dropdown widget,
                'generation_mode': Dropdown widget,
                'modalities': SelectMultiple widget,
                'conditioning': Text widget,
                'confidence': IntSlider widget,
                'evidence': Textarea widget
            }
        }
    """
    logger.debug("Creating Architecture & Design tab")
    
    # Header
    header = widgets.HTML(
        value="<h3>🏗️ Criterion 1: Architecture & Design</h3>"
              "<p>Assess the underlying AI/ML architecture and generation approach.</p>"
    )
    
    # Framework selection
    framework = widgets.Dropdown(
        options=FRAMEWORKS,
        description='Framework:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    # Generation mode
    generation_mode = widgets.Dropdown(
        options=GENERATION_MODES,
        description='Generation Mode:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    # Modalities (multiple selection)
    modalities = widgets.SelectMultiple(
        options=MODALITIES,
        description='Modalities:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px', height='120px')
    )
    
    modalities_help = widgets.HTML(
        value="<small><i>Hold Ctrl/Cmd to select multiple</i></small>"
    )
    
    # Conditioning mechanisms
    conditioning = widgets.Text(
        description='Conditioning:',
        placeholder='e.g., Text prompts, Audio references, Parameter controls',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='600px')
    )
    
    # Confidence rating
    confidence_label = widgets.HTML(
        value="<b>Confidence Rating</b><br>"
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
        placeholder='Documentation links, blog posts, papers, observed behavior, etc.',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='700px', height='100px')
    )
    
    # Assemble container
    container = widgets.VBox([
        header,
        widgets.HTML("<hr>"),
        framework,
        generation_mode,
        modalities,
        modalities_help,
        conditioning,
        widgets.HTML("<hr>"),
        confidence_label,
        confidence,
        confidence_scale,
        evidence
    ])
    
    # Return standard structure
    return {
        'container': container,
        'widgets': {
            'framework': framework,
            'generation_mode': generation_mode,
            'modalities': modalities,
            'conditioning': conditioning,
            'confidence': confidence,
            'evidence': evidence
        }
    }

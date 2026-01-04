"""
Hardware & Accessibility Tab Module

Creates the Hardware & Accessibility (Criterion 3) assessment interface for Phase 0.
Evaluates hardware requirements and accessibility for different user types.
"""

import logging
import ipywidgets as widgets
from ..constants import GPU_TYPES, ACCESSIBILITY_LEVELS

logger = logging.getLogger(__name__)


def create_hardware_tab(state_manager=None):
    """
    Create the Hardware & Accessibility tab for Phase 0.
    
    This tab assesses:
    - GPU type required
    - VRAM requirements (min/recommended)
    - RAM requirements (min/recommended)
    - CPU-only option availability
    - Accessibility levels for different user types
    - Confidence rating (1-5)
    - Supporting evidence
    
    Args:
        state_manager: Phase 0 StateManager instance (optional)
    
    Returns:
        dict: {
            'container': VBox widget with hardware assessment UI,
            'widgets': {
                'gpu_type': Dropdown widget,
                'min_vram_gb': FloatText widget,
                'rec_vram_gb': FloatText widget,
                'min_ram_gb': FloatText widget,
                'rec_ram_gb': FloatText widget,
                'cpu_only_available': Checkbox widget,
                'accessibility_small_studio': Dropdown widget,
                'accessibility_independent': Dropdown widget,
                'accessibility_high_end': Dropdown widget,
                'confidence': IntSlider widget,
                'evidence': Textarea widget
            }
        }
    """
    logger.debug("Creating Hardware & Accessibility tab")
    
    # Header
    header = widgets.HTML(
        value="<h3>💻 Criterion 3: Hardware & Accessibility</h3>"
              "<p>Assess hardware requirements and accessibility for different user types.</p>"
    )
    
    # GPU type
    gpu_type = widgets.Dropdown(
        options=GPU_TYPES,
        description='GPU Type:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    # VRAM requirements
    vram_header = widgets.HTML(value="<b>VRAM Requirements (GB)</b>")
    
    vram_box = widgets.HBox([
        widgets.FloatText(
            value=0,
            description='Minimum:',
            step=0.5,
            style={'description_width': '80px'},
            layout=widgets.Layout(width='200px')
        ),
        widgets.FloatText(
            value=0,
            description='Recommended:',
            step=0.5,
            style={'description_width': '100px'},
            layout=widgets.Layout(width='250px')
        )
    ])
    
    min_vram_gb = vram_box.children[0]
    rec_vram_gb = vram_box.children[1]
    
    # RAM requirements
    ram_header = widgets.HTML(value="<b>RAM Requirements (GB)</b>")
    
    ram_box = widgets.HBox([
        widgets.FloatText(
            value=0,
            description='Minimum:',
            step=1,
            style={'description_width': '80px'},
            layout=widgets.Layout(width='200px')
        ),
        widgets.FloatText(
            value=0,
            description='Recommended:',
            step=1,
            style={'description_width': '100px'},
            layout=widgets.Layout(width='250px')
        )
    ])
    
    min_ram_gb = ram_box.children[0]
    rec_ram_gb = ram_box.children[1]
    
    # CPU-only option
    cpu_only_available = widgets.Checkbox(
        value=False,
        description='CPU-Only Mode Available',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='300px')
    )
    
    # Accessibility assessment
    accessibility_header = widgets.HTML(
        value="<hr><b>Accessibility Assessment</b><br>"
              "<small>How accessible is this system for different user types?</small>"
    )
    
    accessibility_small_studio = widgets.Dropdown(
        options=ACCESSIBILITY_LEVELS,
        value='Accessible (Consumer Hardware)',
        description='Small Studio:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    accessibility_independent = widgets.Dropdown(
        options=ACCESSIBILITY_LEVELS,
        value='Accessible (Consumer Hardware)',
        description='Independent Researcher:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
    )
    
    accessibility_high_end = widgets.Dropdown(
        options=ACCESSIBILITY_LEVELS,
        value='Accessible (Consumer Hardware)',
        description='High-End User:',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='500px')
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
        placeholder='Official specs, benchmarks, user reports, testing results, etc.',
        style={'description_width': '150px'},
        layout=widgets.Layout(width='700px', height='100px')
    )
    
    # Assemble container
    container = widgets.VBox([
        header,
        widgets.HTML("<hr>"),
        gpu_type,
        vram_header,
        vram_box,
        ram_header,
        ram_box,
        cpu_only_available,
        accessibility_header,
        accessibility_small_studio,
        accessibility_independent,
        accessibility_high_end,
        confidence_label,
        confidence,
        confidence_scale,
        evidence
    ])
    
    # Return standard structure
    return {
        'container': container,
        'widgets': {
            'gpu_type': gpu_type,
            'min_vram_gb': min_vram_gb,
            'rec_vram_gb': rec_vram_gb,
            'min_ram_gb': min_ram_gb,
            'rec_ram_gb': rec_ram_gb,
            'cpu_only_available': cpu_only_available,
            'accessibility_small_studio': accessibility_small_studio,
            'accessibility_independent': accessibility_independent,
            'accessibility_high_end': accessibility_high_end,
            'confidence': confidence,
            'evidence': evidence
        }
    }

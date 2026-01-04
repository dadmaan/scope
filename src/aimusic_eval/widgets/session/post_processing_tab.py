"""
Post-Processing Tab Module

Creates the Post-Processing tab for documenting audio processing steps
applied to generated content.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_post_processing_tab():
    """
    Create the Post-Processing sub-tab (converted from accordion).
    
    Returns:
        dict: {
            'container': VBox widget with post-processing UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating Post-Processing tab")
    
    # Post-Processing Widgets
    separation_needed = widgets.RadioButtons(
        options=['Yes', 'No', 'N/A (single instrument)'],
        description='Separation needed:',
        style={'description_width': 'initial'}
    )

    separation_tool = widgets.Text(
        description='Tool used:',
        placeholder='e.g., Demucs, Spleeter, RipX',
        style={'description_width': 'initial'}
    )

    separation_quality = widgets.Textarea(
        description='Separation quality:',
        placeholder='Describe isolation quality and any bleed/crosstalk',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    eq_applied = widgets.Checkbox(
        value=False,
        description='Equalization applied',
        style={'description_width': 'initial'}
    )

    eq_details = widgets.Textarea(
        description='EQ details:',
        placeholder='Purpose, frequency cuts/boosts, tool used',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    compression_applied = widgets.Checkbox(
        value=False,
        description='Compression applied',
        style={'description_width': 'initial'}
    )

    compression_details = widgets.Textarea(
        description='Compression:',
        placeholder='Purpose, ratio, threshold, tool used',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    reverb_applied = widgets.Checkbox(
        value=False,
        description='Reverb/Delay applied',
        style={'description_width': 'initial'}
    )

    reverb_details = widgets.Textarea(
        description='Reverb/Delay:',
        placeholder='Purpose, type, amount, tool used',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    trimming_applied = widgets.Checkbox(
        value=False,
        description='Trimming/Editing applied',
        style={'description_width': 'initial'}
    )

    trimming_details = widgets.Textarea(
        description='Trimming:',
        placeholder='What was trimmed/edited and why',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    other_processing = widgets.Textarea(
        description='Other processing:',
        placeholder='Pitch correction, time stretch, saturation, etc.',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    processing_total_time = widgets.Text(
        description='Total time:',
        placeholder='e.g., 20 minutes',
        style={'description_width': 'initial'}
    )

    # Organize into container (no accordion - direct display)
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #FF9800; border-bottom: 2px solid #FF9800; padding-bottom: 10px;">🎚️ Post-Processing Requirements</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Track audio processing applied:</strong> separation, EQ, compression, reverb, editing</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Note any steps you take to make the system's output usable, such as EQ, compression, or trimming. Documenting the type and extent of this work helps measure the raw quality of the generation and the effort required to integrate it into a musical piece.</p>"),
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Source Separation</h4>'),
        separation_needed,
        separation_tool,
        separation_quality,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Processing Steps</h4>'),
        eq_applied,
        eq_details,
        compression_applied,
        compression_details,
        reverb_applied,
        reverb_details,
        trimming_applied,
        trimming_details,
        other_processing,
        processing_total_time
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'separation_needed': separation_needed,
        'separation_tool': separation_tool,
        'separation_quality': separation_quality,
        'eq_applied': eq_applied,
        'eq_details': eq_details,
        'compression_applied': compression_applied,
        'compression_details': compression_details,
        'reverb_applied': reverb_applied,
        'reverb_details': reverb_details,
        'trimming_applied': trimming_applied,
        'trimming_details': trimming_details,
        'other_processing': other_processing,
        'processing_total_time': processing_total_time
    }

    logger.debug("✅ Post-Processing tab created")
    return {'container': container, 'widgets': widgets_dict}

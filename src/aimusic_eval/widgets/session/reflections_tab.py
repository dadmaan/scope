"""
Reflections Tab Module

Creates the Reflections tab for qualitative session feedback and observations.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_reflections_tab():
    """
    Create the Reflections sub-tab with qualitative session feedback.
    
    Returns:
        dict: {
            'container': VBox widget with reflections UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating Reflections tab")
    
    # Reflection Widgets
    what_worked = widgets.Textarea(
        description='What worked:',
        placeholder='Positive aspects, successes, pleasant surprises',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    frustrations = widgets.Textarea(
        description='Frustrations:',
        placeholder='Challenges, roadblocks, disappointments',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    discoveries = widgets.Textarea(
        description='Discoveries:',
        placeholder='Surprising behaviors, capabilities, limitations, creative insights',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    comparisons = widgets.Textarea(
        description='Comparisons:',
        placeholder='How this compares to previous sessions or other systems',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    emotional_state = widgets.Textarea(
        description='Emotional state:',
        placeholder='How did you feel? (Fatigue, excitement, flow state, frustration)',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">💭 Session Reflections</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Document reflections:</strong> reflect on what worked, what didn\'t, surprises, and key learnings from session</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 This is your space for subjective, personal insights. Use this section to reflect on your creative experience, noting any frustrations, discoveries, or emotional responses you had during the session. Your personal perspective provides qualitative context to the technical data.</p>"),
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Qualitative Insights</h4>'),
        what_worked,
        frustrations,
        discoveries,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Comparative Analysis</h4>'),
        comparisons,
        emotional_state
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'what_worked': what_worked,
        'frustrations': frustrations,
        'discoveries': discoveries,
        'comparisons': comparisons,
        'emotional_state': emotional_state
    }

    logger.debug("✅ Reflections tab created")
    return {'container': container, 'widgets': widgets_dict}

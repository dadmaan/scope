"""
Refinement Tab Module

Creates the Prompt Refinement tab for documenting prompt iteration
and system interpretation learnings.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_refinement_tab():
    """
    Create the Refinement sub-tab (converted from accordion).
    
    Returns:
        dict: {
            'container': VBox widget with refinement UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating Refinement tab")
    
    # Prompt Refinement Widgets
    initial_prompt = widgets.Textarea(
        description='Initial Prompt:',
        placeholder='Your first attempt prompt',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    final_prompt = widgets.Textarea(
        description='Final Prompt:',
        placeholder='The prompt that yielded best results',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    iterations = widgets.Textarea(
        description='Iterations:',
        placeholder='Describe changes made between attempts and why',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    responds_well = widgets.Textarea(
        description='Responds well to:',
        placeholder='e.g., Specific instrument names, BPM, rhythmic descriptors',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    struggles_with = widgets.Textarea(
        description='Struggles with:',
        placeholder='e.g., Harmonic complexity, negative constraints',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    unexpected = widgets.Textarea(
        description='Unexpected:',
        placeholder='Any surprising interpretations or patterns',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    effective_keywords = widgets.Text(
        description='Effective keywords:',
        placeholder='Comma-separated list',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px')
    )

    ineffective_keywords = widgets.Text(
        description='Ineffective keywords:',
        placeholder='Comma-separated list',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px')
    )

    # Organize into container (no accordion - direct display)
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #4CAF50; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">🔄 Prompt Refinement Process</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Log iterative refinements:</strong> regeneration strategy, prompt adjustments, and results</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 This section is for analyzing your prompt engineering process. Detail your journey from the initial prompt to the final, most effective version to shed light on the system's interpretive capabilities and uncover patterns in how it responds to different keywords and phrasing.</p>"),
                
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Prompt Evolution</h4>'),
        initial_prompt,
        final_prompt,
        iterations,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">System Interpretation Learnings</h4>'),
        responds_well,
        struggles_with,
        unexpected,
        effective_keywords,
        ineffective_keywords
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'initial_prompt': initial_prompt,
        'final_prompt': final_prompt,
        'iterations': iterations,
        'responds_well': responds_well,
        'struggles_with': struggles_with,
        'unexpected': unexpected,
        'effective_keywords': effective_keywords,
        'ineffective_keywords': ineffective_keywords
    }

    logger.debug("✅ Refinement tab created")
    return {'container': container, 'widgets': widgets_dict}

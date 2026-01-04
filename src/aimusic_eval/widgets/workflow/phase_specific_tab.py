"""
Phase-Specific Tab Module

Creates the Phase-Specific Details tab with conditional content
that switches based on selected phase type (Generation, Curation,
Integration, Post-Production).

Note: Content switching is handled by observer in notebook.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_workflow_phase_specific_tab():
    """
    Create the Phase-Specific Details sub-tab with conditional content.
    
    This tab displays different widgets based on the selected phase_type.
    The observer will be set up in the notebook to switch content dynamically.
    """
    # Content Generation Widgets
    gen_approach = widgets.Dropdown(
        options=['Prompt-based', 'Parameter-driven', 'Hybrid', 'Iterative refinement', 'Other'],
        description='Approach:',
        style={'description_width': 'initial'}
    )
    
    gen_prompts = widgets.Textarea(
        description='Prompts:',
        placeholder='Document prompts/parameters used',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )
    
    gen_iterations = widgets.IntText(
        value=1,
        description='Iterations:',
        style={'description_width': 'initial'}
    )
    
    gen_output = widgets.Textarea(
        description='Output:',
        placeholder='Describe what was generated and initial quality',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    # Curation Phase Widgets
    cur_candidates_reviewed = widgets.IntText(
        value=0,
        description='Reviewed:',
        style={'description_width': 'initial'}
    )
    
    cur_candidates_selected = widgets.IntText(
        value=0,
        description='Selected:',
        style={'description_width': 'initial'}
    )
    
    cur_criteria = widgets.Textarea(
        description='Criteria:',
        placeholder='What criteria guided your selection?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    cur_notes = widgets.Textarea(
        description='Notes:',
        placeholder='Document curation decisions and reasoning',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )
    
    # Integration Phase Widgets
    int_activities = widgets.SelectMultiple(
        options=['Import audio', 'Import MIDI', 'Arrangement', 'Mixing', 'Effects processing', 'Other'],
        description='Activities:',
        layout=widgets.Layout(width='400px', height='100px'),
        style={'description_width': 'initial'}
    )
    
    int_challenges = widgets.Textarea(
        description='Challenges:',
        placeholder='Technical issues, format problems, workflow friction?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    int_success = widgets.Textarea(
        description='Success:',
        placeholder='What integrated smoothly? Any pleasant surprises?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    # Post-Production Phase Widgets
    pp_activities = widgets.SelectMultiple(
        options=['Mixing', 'Mastering', 'Effects', 'EQ', 'Compression', 'Reverb/Delay', 'Automation', 'Other'],
        description='Activities:',
        layout=widgets.Layout(width='400px', height='120px'),
        style={'description_width': 'initial'}
    )
    
    pp_ai_percentage = widgets.IntSlider(
        value=50,
        min=0,
        max=100,
        step=5,
        description='AI Content %:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )
    
    pp_modifications = widgets.Textarea(
        description='Modifications:',
        placeholder='How did you modify/enhance the AI-generated content?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    pp_quality = widgets.RadioButtons(
        options=['Excellent', 'Good', 'Acceptable', 'Needs work', 'Failed'],
        description='Final quality:',
        style={'description_width': 'initial'}
    )
    
    # Create conditional container (will be populated by observer in notebook)
    phase_specific_container = widgets.VBox([
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">⚡ Phase-Specific Details</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Document each generation attempt:</strong> generation approach, curation criteria, or integration steps.</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Keep a running, timestamped log of your activities here. This chronological record provides a granular view of your process, allowing for a detailed analysis of how you spent your time and the outcomes of each step.</p>"),
                
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><em>Content will update based on Phase Type selection in Setup tab</em></div>'),
    ])
    
    # Create widget reference dictionary with all phase-specific widgets
    widgets_dict = {
        'phase_specific_container': phase_specific_container,
        'generation': {
            'gen_approach': gen_approach,
            'gen_prompts': gen_prompts,
            'gen_iterations': gen_iterations,
            'gen_output': gen_output
        },
        'curation': {
            'cur_candidates_reviewed': cur_candidates_reviewed,
            'cur_candidates_selected': cur_candidates_selected,
            'cur_criteria': cur_criteria,
            'cur_notes': cur_notes
        },
        'integration': {
            'int_activities': int_activities,
            'int_challenges': int_challenges,
            'int_success': int_success
        },
        'post_production': {
            'pp_activities': pp_activities,
            'pp_ai_percentage': pp_ai_percentage,
            'pp_modifications': pp_modifications,
            'pp_quality': pp_quality
        }
    }
    
    return {'container': phase_specific_container, 'widgets': widgets_dict}

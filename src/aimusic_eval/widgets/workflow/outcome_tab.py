"""
Outcome Tab Module

Creates the Efficiency & Outcome tab for efficiency analysis,
outcome assessment, and criterion bridge (connecting to 8 performance criteria).
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_workflow_outcome_tab():
    """Create the Efficiency & Outcome sub-tab."""
    # Efficiency Analysis Widgets (CRITICAL from T06)
    eff_time_planned = widgets.IntText(
        value=0,
        description='Planned (min):',
        style={'description_width': 'initial'}
    )
    
    eff_time_actual = widgets.IntText(
        value=0,
        description='Actual (min):',
        style={'description_width': 'initial'}
    )
    
    eff_breakdown = widgets.Textarea(
        description='Breakdown:',
        placeholder='How was time distributed? (e.g., 30% prompting, 50% reviewing)',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    eff_bottlenecks = widgets.Textarea(
        description='Bottlenecks:',
        placeholder='What slowed you down?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )
    
    eff_rating = widgets.RadioButtons(
        options=['Very efficient', 'Efficient', 'Moderate', 'Inefficient', 'Very inefficient'],
        description='Rating:',
        style={'description_width': 'initial'}
    )
    
    # Outcome Assessment Widgets
    outcome_goals = widgets.RadioButtons(
        options=['Completely', 'Mostly', 'Partially', 'Minimally', 'Not at all'],
        description='Goals met:',
        style={'description_width': 'initial'}
    )
    
    outcome_quality = widgets.RadioButtons(
        options=['Excellent', 'Good', 'Acceptable', 'Poor', 'Failed'],
        description='Quality:',
        style={'description_width': 'initial'}
    )
    
    outcome_usable = widgets.Textarea(
        description='Usable outputs:',
        placeholder='What outputs are usable for next phases or final product?',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    outcome_surprises = widgets.Textarea(
        description='Surprises:',
        placeholder='Unexpected outcomes (positive or negative)',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    outcome_next_phase = widgets.Textarea(
        description='Next phase impact:',
        placeholder='How will this affect subsequent work?',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )
    
    # Criterion Bridge (CRITICAL from T06)
    criterion_connections = widgets.Textarea(
        description='Criterion connections:',
        placeholder='Map workflow observations to 8 performance criteria',
        layout=widgets.Layout(width='700px', height='120px'),
        style={'description_width': 'initial'}
    )
    
    criterion_evidence = widgets.Textarea(
        description='Evidence:',
        placeholder='What specific evidence can inform quantitative scores?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )
    
    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #9C27B0; border-bottom: 2px solid #9C27B0; padding-bottom: 10px;">🎯 Efficiency & Outcome</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;">Assess completion status, output satisfaction, technical quality, and goal achievement.</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 This section provides fields tailored to the phase you selected in the setup tab. Whether you are generating content, curating candidates, or integrating assets, this is where you'll log the core details of that specific activity.</p>"),
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Efficiency Analysis</h4>'),
        
        widgets.HBox([eff_time_planned, eff_time_actual]),
        eff_breakdown,
        eff_bottlenecks,
        eff_rating,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Outcome Assessment</h4>'),
        outcome_goals,
        outcome_quality,
        outcome_usable,
        outcome_surprises,
        outcome_next_phase,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Criterion Bridge (Connect to 8 Performance Criteria)</h4>'),
        criterion_connections,
        criterion_evidence
    ])
    
    # Create widget reference dictionary
    widgets_dict = {
        'eff_time_planned': eff_time_planned,
        'eff_time_actual': eff_time_actual,
        'eff_breakdown': eff_breakdown,
        'eff_bottlenecks': eff_bottlenecks,
        'eff_rating': eff_rating,
        'outcome_goals': outcome_goals,
        'outcome_quality': outcome_quality,
        'outcome_usable': outcome_usable,
        'outcome_surprises': outcome_surprises,
        'outcome_next_phase': outcome_next_phase,
        'criterion_connections': criterion_connections,
        'criterion_evidence': criterion_evidence
    }
    
    return {'container': container, 'widgets': widgets_dict}

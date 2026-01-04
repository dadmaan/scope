"""
Learnings Tab Module

Creates the Root Cause & Learnings tab for root cause analysis
and 3D learnings documentation.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_incident_learnings_tab():
    """Create the Root Cause & Learnings sub-tab."""
    # Root Cause Analysis (CRITICAL for T03)
    probable_causes = widgets.SelectMultiple(
        options=[
            'User error/misunderstanding',
            'System bug/glitch',
            'Model limitation',
            'Inadequate documentation',
            'Ambiguous prompt',
            'Environmental factors',
            'Integration issue',
            'Resource constraints',
            'Unexpected feature interaction',
            'Training data bias',
            'Random/stochastic behavior',
            'Other'
        ],
        description='Probable causes:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(height='200px')
    )

    evidence = widgets.Textarea(
        description='Evidence:',
        placeholder='What evidence supports your root cause hypothesis?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    alternatives = widgets.Textarea(
        description='Alternatives:',
        placeholder='What other explanations did you consider?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # 3D Learnings (CRITICAL for T03)
    learning_system = widgets.Textarea(
        description='System learning:',
        placeholder='What did you learn about this AI music system?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    learning_evaluation = widgets.Textarea(
        description='Evaluation learning:',
        placeholder='What did you learn about evaluating AI music systems?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    learning_practice = widgets.Textarea(
        description='Practice learning:',
        placeholder='What did you learn about your own creative/technical practice?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    approach_changes = widgets.Textarea(
        description='Approach changes:',
        placeholder='How will you change your approach based on this incident?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    recommendations = widgets.Textarea(
        description='Recommendations:',
        placeholder='What would you recommend to other evaluators?',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='60px')
    )

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">💡 Root Cause & Learnings</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Root causes and Lerning outcomes:</strong> analyze immediate impact, workarounds applied, and implications for evaluation.</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Analyze the incident's root cause and impact. This is where you explore why the event matters, which evaluation criteria it affects, and your hypothesis on what caused it, while also noting your own disposition at the time.</p>"),
                
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Root Cause Analysis</h4>'),
        probable_causes,
        evidence,
        alternatives,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Learning Outcomes</h4>'),
        learning_system,
        learning_evaluation,
        learning_practice,
        approach_changes,
        recommendations
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'probable_causes': probable_causes,
        'evidence': evidence,
        'alternatives': alternatives,
        'learning_system': learning_system,
        'learning_evaluation': learning_evaluation,
        'learning_practice': learning_practice,
        'approach_changes': approach_changes,
        'recommendations': recommendations
    }

    return {'container': container, 'widgets': widgets_dict}

"""
Overall Synthesis Tab

Provides holistic assessment capturing:
- Top strengths and weaknesses
- Standout features
- Use case recommendations
- Ideal user profile

PRESERVED: All widget content, labels, placeholders - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML


def create_synthesis_tab():
    """
    Create Overall Synthesis sub-tab.

    Returns:
        dict: {
            'container': VBox with synthesis widgets,
            'widgets': {
                'top_strengths': Textarea,
                'top_weaknesses': Textarea,
                'standout_feature': Textarea,
                'best_suited_for': Textarea,
                'not_recommended_for': Textarea,
                'ideal_user_profile': Textarea
            }
        }
    """

    # Synthesis widgets - PRESERVED PLACEHOLDERS
    top_strengths = widgets.Textarea(
        description='Top 3 Strengths:',
        placeholder='1. [Criterion]: Specific strength with example\n2. [Criterion]: Specific strength with example\n3. [Criterion]: Specific strength with example',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    top_weaknesses = widgets.Textarea(
        description='Top 3 Weaknesses:',
        placeholder='1. [Criterion]: Specific weakness with example\n2. [Criterion]: Specific weakness with example\n3. [Criterion]: Specific weakness with example',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    standout_feature = widgets.Textarea(
        description='Standout Feature:',
        placeholder="What single aspect most defines this system's character?",
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    best_suited_for = widgets.Textarea(
        description='Best Suited For:',
        placeholder='List 2-3 use cases with rationale',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    not_recommended_for = widgets.Textarea(
        description='Not Recommended:',
        placeholder='List 2-3 use cases with rationale',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='100px')
    )

    ideal_user_profile = widgets.Textarea(
        description='Ideal User:',
        placeholder='Describe who would benefit most from this system',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='80px')
    )

    # Container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #9C27B0; border-bottom: 2px solid #9C27B0; padding-bottom: 10px;">Overall Synthesis</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Summarize overall assessment, calculate average scores, and identify key patterns.</p>'),
        widgets.HTML('<p>Provide a holistic assessment of the system across all criteria.</p>'),
        widgets.HTML('<h4 style="color: #555;">Summary Analysis</h4>'),
        top_strengths,
        top_weaknesses,
        standout_feature,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Use Case Recommendations</h4>'),
        best_suited_for,
        not_recommended_for,
        ideal_user_profile
    ])

    return {
        'container': container,
        'widgets': {
            'top_strengths': top_strengths,
            'top_weaknesses': top_weaknesses,
            'standout_feature': standout_feature,
            'best_suited_for': best_suited_for,
            'not_recommended_for': not_recommended_for,
            'ideal_user_profile': ideal_user_profile
        }
    }

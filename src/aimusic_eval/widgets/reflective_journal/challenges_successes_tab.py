"""
Challenges & Successes Tab

Groups journal sections for challenges and successes:
- Challenges: technical issues, conceptual difficulties, frustrations
- What worked: things that went well
- Output metrics: usable outputs count and quality level
- Satisfaction: slider for satisfaction level
- Small wins: victories to celebrate

PRESERVED: All widget content, labels, options - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML


def create_challenges_successes_tab():
    """
    Create Challenges & Successes sub-tab with mixed widget types.

    Returns:
        dict: {
            'container': VBox with all challenges/successes widgets,
            'widgets': {
                'challenges': Textarea,
                'what_worked': Textarea,
                'outputs': IntText,
                'output_quality': Dropdown,
                'satisfaction': IntSlider,
                'wins': Textarea
            }
        }
    """

    # ========================================================================
    # CHALLENGES
    # ========================================================================

    journal_challenges = widgets.Textarea(
        description='Challenges:',
        placeholder='Technical issues, conceptual difficulties, practical frustrations...',
        layout=widgets.Layout(width='700px', height='120px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # SUCCESSES
    # ========================================================================

    journal_what_worked = widgets.Textarea(
        description='What Worked:',
        placeholder='List 3-5 things that went well today...',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_outputs = widgets.IntText(
        description='Usable outputs:',
        value=0,
        min=0,
        style={'description_width': 'initial'}
    )

    journal_output_quality = widgets.Dropdown(
        options=['Excellent', 'Good', 'Acceptable', 'Poor'],
        description='Quality level:',
        value='Good',
        style={'description_width': 'initial'}
    )

    journal_satisfaction = widgets.IntSlider(
        description='Satisfaction:',
        value=5,
        min=1,
        max=10,
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='400px')
    )

    journal_wins = widgets.Textarea(
        description='Small Wins:',
        placeholder='Even small victories - what felt good today?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">Challenges & Successes</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Document problems encountered, successes achieved, and outputs created.</p>'),
        widgets.HTML('<p>Record obstacles encountered and victories achieved.</p>'),
        widgets.HTML('<h4 style="color: #555;">Challenges</h4>'),
        journal_challenges,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Successes</h4>'),
        journal_what_worked,
        journal_outputs,
        journal_output_quality,
        journal_satisfaction,
        journal_wins
    ])

    return {
        'container': container,
        'widgets': {
            'challenges': journal_challenges,
            'what_worked': journal_what_worked,
            'outputs': journal_outputs,
            'output_quality': journal_output_quality,
            'satisfaction': journal_satisfaction,
            'wins': journal_wins
        }
    }

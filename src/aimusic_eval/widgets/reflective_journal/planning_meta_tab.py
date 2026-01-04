"""
Planning & Meta-Learning Tab

Groups journal sections for planning and meta-learning:
- Tomorrow's goals: 3-5 priorities for tomorrow
- Systems focus: which systems to work with and specific goals
- Questions: questions or issues needing investigation
- Meta-learning insights: learnings about AI music generation, research, or production
- Random notes: miscellaneous thoughts, quotes, unexpected moments, tangential ideas

PRESERVED: All widget content, labels, options - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML


def create_planning_meta_tab():
    """
    Create Planning & Meta-Learning sub-tab combining planning and meta-learning sections.

    Returns:
        dict: {
            'container': VBox with all planning/meta-learning widgets,
            'widgets': {
                'tomorrow': Textarea,
                'systems_focus': Textarea,
                'questions': Textarea,
                'meta_insights': Textarea,
                'random': Textarea
            }
        }
    """

    # ========================================================================
    # PLANNING
    # ========================================================================

    journal_tomorrow = widgets.Textarea(
        description="Tomorrow's Goals:",
        placeholder='List 3-5 priorities for tomorrow...',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_systems_focus = widgets.Textarea(
        description='Systems Focus:',
        placeholder='Which systems to work with and what specific goals?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )

    journal_questions = widgets.Textarea(
        description='Questions:',
        placeholder='What questions or issues need investigation?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # META-LEARNING
    # ========================================================================

    journal_meta_insights = widgets.Textarea(
        description='Meta-Learning:',
        placeholder='What did today teach you about AI music generation, research, or music production?',
        layout=widgets.Layout(width='700px', height='120px'),
        style={'description_width': 'initial'}
    )

    journal_random = widgets.Textarea(
        description='Random Notes:',
        placeholder='Miscellaneous thoughts, quotes, unexpected moments, tangential ideas...',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">Planning & Meta-Learning</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Plan tomorrow\'s activities, note meta-learning, and record general observations.</p>'),
        widgets.HTML('<p>Plan ahead and capture meta-level insights.</p>'),
        widgets.HTML('<h4 style="color: #555;">Planning</h4>'),
        journal_tomorrow,
        journal_systems_focus,
        journal_questions,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Meta-Learning</h4>'),
        journal_meta_insights,
        journal_random
    ])

    return {
        'container': container,
        'widgets': {
            'tomorrow': journal_tomorrow,
            'systems_focus': journal_systems_focus,
            'questions': journal_questions,
            'meta_insights': journal_meta_insights,
            'random': journal_random
        }
    }

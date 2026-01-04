"""
Insights & Learning Tab

Groups journal sections for observations and insights:
- Technical discoveries about system capabilities, parameters, behaviors
- Creative insights: breakthroughs, artistic discoveries, compositional revelations
- Workflow learnings: what worked well or poorly in process
- Comparative observations: insights about how systems compare

PRESERVED: All widget content, labels, options - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML


def create_insights_learning_tab():
    """
    Create Insights & Learning sub-tab with observation textareas.

    Returns:
        dict: {
            'container': VBox with all insights/learning widgets,
            'widgets': {
                'technical': Textarea,
                'creative': Textarea,
                'workflow': Textarea,
                'comparative': Textarea
            }
        }
    """

    # ========================================================================
    # OBSERVATIONS
    # ========================================================================

    journal_technical = widgets.Textarea(
        description='Technical:',
        placeholder='What did you learn about system capabilities, parameters, behaviors?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_creative = widgets.Textarea(
        description='Creative:',
        placeholder='Any breakthroughs, artistic discoveries, or compositional revelations?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_workflow = widgets.Textarea(
        description='Workflow:',
        placeholder='What worked well or poorly in your process today?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_comparative = widgets.Textarea(
        description='Comparative:',
        placeholder='New insights about how systems compare to each other?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">Insights & Learning</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Capture technical, creative, workflow, and comparative discoveries from today\'s work.</p>'),
        widgets.HTML('<p>Record observations and discoveries from today\'s work.</p>'),
        widgets.HTML('<h4 style="color: #555;">Observations</h4>'),
        journal_technical,
        journal_creative,
        journal_workflow,
        journal_comparative
    ])

    return {
        'container': container,
        'widgets': {
            'technical': journal_technical,
            'creative': journal_creative,
            'workflow': journal_workflow,
            'comparative': journal_comparative
        }
    }

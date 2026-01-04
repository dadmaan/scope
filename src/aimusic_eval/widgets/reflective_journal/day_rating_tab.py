"""
Day Rating & Summary Tab

Groups journal sections for day ratings and summary:
- 5D Ratings: Productivity, Learning, Creativity, Frustration, Satisfaction (1-10 sliders)
- One sentence summary: capture essence of today
- Key takeaway: single most important thing learned or experienced
- Gratitude: what you're grateful for, what went better than expected

PRESERVED: All widget content, labels, options - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML


def create_day_rating_tab():
    """
    Create Day Rating & Summary sub-tab combining ratings and summary sections.

    Returns:
        dict: {
            'container': VBox with all rating/summary widgets,
            'widgets': {
                'rating_productivity': IntSlider,
                'rating_learning': IntSlider,
                'rating_creativity': IntSlider,
                'rating_frustration': IntSlider,
                'rating_satisfaction': IntSlider,
                'one_sentence': Textarea,
                'key_takeaway': Textarea,
                'gratitude': Textarea
            }
        }
    """

    # ========================================================================
    # DAY RATINGS (5 DIMENSIONS)
    # ========================================================================

    journal_rating_productivity = widgets.IntSlider(
        description='Productivity:',
        value=5,
        min=1,
        max=10,
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    journal_rating_learning = widgets.IntSlider(
        description='Learning:',
        value=5,
        min=1,
        max=10,
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    journal_rating_creativity = widgets.IntSlider(
        description='Creativity:',
        value=5,
        min=1,
        max=10,
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    journal_rating_frustration = widgets.IntSlider(
        description='Frustration:',
        value=5,
        min=1,
        max=10,
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    journal_rating_satisfaction = widgets.IntSlider(
        description='Satisfaction:',
        value=5,
        min=1,
        max=10,
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    # ========================================================================
    # SUMMARY
    # ========================================================================

    journal_one_sentence = widgets.Textarea(
        description='One Sentence:',
        placeholder='Capture the essence of today in one sentence...',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )

    journal_key_takeaway = widgets.Textarea(
        description='Key Takeaway:',
        placeholder='The single most important thing learned or experienced today...',
        layout=widgets.Layout(width='700px', height='60px'),
        style={'description_width': 'initial'}
    )

    journal_gratitude = widgets.Textarea(
        description='Gratitude:',
        placeholder='What are you grateful for today? What went better than expected?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">Day Rating & Summary</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Rate today across 5 dimensions: progress, quality, learning, enjoyment, challenge.</p>'),
        widgets.HTML('<p>Rate today across 5 dimensions and summarize your experience.</p>'),
        widgets.HTML('<h4 style="color: #555;">5D Ratings</h4>'),
        journal_rating_productivity,
        journal_rating_learning,
        journal_rating_creativity,
        journal_rating_frustration,
        journal_rating_satisfaction,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Summary</h4>'),
        journal_one_sentence,
        journal_key_takeaway,
        journal_gratitude
    ])

    return {
        'container': container,
        'widgets': {
            'rating_productivity': journal_rating_productivity,
            'rating_learning': journal_rating_learning,
            'rating_creativity': journal_rating_creativity,
            'rating_frustration': journal_rating_frustration,
            'rating_satisfaction': journal_rating_satisfaction,
            'one_sentence': journal_one_sentence,
            'key_takeaway': journal_key_takeaway,
            'gratitude': journal_gratitude
        }
    }

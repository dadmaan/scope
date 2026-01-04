"""
Daily Entry Tab

Groups journal sections for basic entry metadata and daily activities:
- Entry Metadata (Date, Day #, Productivity, Mood)
- Activities (Systems worked, Tasks, Time investment)

PRESERVED: All widget content, labels, options - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML
from datetime import date


def create_daily_entry_tab():
    """
    Create Daily Entry sub-tab combining metadata and activities.

    Returns:
        dict: {
            'container': VBox with all daily entry widgets,
            'widgets': {
                'entry_date': DatePicker,
                'day_number': IntText,
                'productivity': Dropdown,
                'mood': Dropdown,
                'systems_worked': Textarea,
                'tasks': SelectMultiple,
                'time_hands_on': FloatText,
                'time_processing': FloatText,
                'time_docs': FloatText
            }
        }
    """

    # ========================================================================
    # ENTRY METADATA
    # ========================================================================

    journal_entry_date = widgets.DatePicker(
        description='Date:',
        value=date.today(),
        style={'description_width': 'initial'}
    )

    journal_day_number = widgets.IntText(
        description='Day # of eval:',
        value=1,
        min=1,
        style={'description_width': 'initial'}
    )

    journal_productivity = widgets.Dropdown(
        options=['High', 'Medium', 'Low'],
        description='Productivity:',
        value='Medium',
        style={'description_width': 'initial'}
    )

    journal_mood = widgets.Dropdown(
        options=['Energized', 'Focused', 'Neutral', 'Tired', 'Frustrated'],
        description='Mood:',
        value='Neutral',
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # ACTIVITIES & TIME
    # ========================================================================

    journal_systems_worked = widgets.Textarea(
        description='Systems:',
        placeholder='List systems worked with today (one per line)',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )

    journal_tasks = widgets.SelectMultiple(
        options=[
            'Content generation sessions',
            'Post-processing work',
            'DAW integration testing',
            'Documentation/logging',
            'Technical troubleshooting',
            'Comparative analysis',
            'Reading/research',
            'Other'
        ],
        description='Tasks Done:',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='400px', height='150px')
    )

    journal_time_hands_on = widgets.FloatText(
        description='Hands-on (hrs):',
        value=0.0,
        step=0.5,
        style={'description_width': 'initial'}
    )

    journal_time_processing = widgets.FloatText(
        description='Processing (hrs):',
        value=0.0,
        step=0.5,
        style={'description_width': 'initial'}
    )

    journal_time_docs = widgets.FloatText(
        description='Documentation (hrs):',
        value=0.0,
        step=0.5,
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">Daily Entry</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Log date, mood, productivity, systems used, tasks completed, and time investment.</p>'),
        widgets.HTML('<p>Record today\'s basic metadata and activities.</p>'),
        widgets.HTML('<h4 style="color: #555;">Entry Metadata</h4>'),
        journal_entry_date,
        journal_day_number,
        journal_productivity,
        journal_mood,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Systems & Tasks</h4>'),
        journal_systems_worked,
        journal_tasks,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Time Investment</h4>'),
        journal_time_hands_on,
        journal_time_processing,
        journal_time_docs
    ])

    return {
        'container': container,
        'widgets': {
            'entry_date': journal_entry_date,
            'day_number': journal_day_number,
            'productivity': journal_productivity,
            'mood': journal_mood,
            'systems_worked': journal_systems_worked,
            'tasks': journal_tasks,
            'time_hands_on': journal_time_hands_on,
            'time_processing': journal_time_processing,
            'time_docs': journal_time_docs
        }
    }

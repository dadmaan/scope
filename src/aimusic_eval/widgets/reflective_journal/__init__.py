"""
Reflective Journal Module - Orchestrator

Creates nested tab structure for reflective journaling with 7 sub-tabs:
1. Daily Entry (Metadata + Activities)
2. Insights & Learning (Technical, Creative, Workflow, Comparative)
3. Challenges & Successes (Problems, Wins, Outputs)
4. Reflection & Growth (Evolution, Autoethnographic, Flow)
5. Planning & Meta (Tomorrow, Meta-learning, Notes)
6. Day Rating (5D Ratings + Summary)
7. History & Trends (Historical entries + Longitudinal analysis)

Returns nested Tab widget with all journal widgets organized hierarchically.
"""

import ipywidgets as widgets
from .journal_state import JournalStateManager


def create_journal_tabs(synthesis_data_ref):
    """
    Create Reflective Journal nested tab structure.

    Args:
        synthesis_data_ref (dict): Reference to global synthesis_data

    Returns:
        dict: {
            'container': Tab widget with 7 nested sub-tabs,
            'widgets': {
                'daily_entry': {...},
                'insights_learning': {...},
                'challenges_successes': {...},
                'reflection_growth': {...},
                'planning_meta': {...},
                'day_rating': {...},
                'history_trends': {...}
            },
            'state_manager': JournalStateManager instance
        }
    """

    # Create state manager
    state_manager = JournalStateManager(synthesis_data_ref)

    # Import sub-tab creators
    from .daily_entry_tab import create_daily_entry_tab
    from .insights_learning_tab import create_insights_learning_tab
    from .challenges_successes_tab import create_challenges_successes_tab
    from .reflection_growth_tab import create_reflection_growth_tab
    from .planning_meta_tab import create_planning_meta_tab
    from .day_rating_tab import create_day_rating_tab
    from .history_trends_tab import create_history_trends_tab

    # Create sub-tabs (no dependencies)
    daily_entry = create_daily_entry_tab()
    insights_learning = create_insights_learning_tab()
    challenges_successes = create_challenges_successes_tab()
    reflection_growth = create_reflection_growth_tab()
    planning_meta = create_planning_meta_tab()
    day_rating = create_day_rating_tab()

    # Create widget references dict for history tab
    all_journal_widgets = {
        'daily_entry': daily_entry['widgets'],
        'insights_learning': insights_learning['widgets'],
        'challenges_successes': challenges_successes['widgets'],
        'reflection_growth': reflection_growth['widgets'],
        'planning_meta': planning_meta['widgets'],
        'day_rating': day_rating['widgets']
    }

    # Create history/trends tab (requires synthesis_data and widget refs)
    history_trends = create_history_trends_tab(
        synthesis_data=synthesis_data_ref,
        widget_refs=all_journal_widgets
    )

    # Create nested Tab widget
    nested_tabs = widgets.Tab()
    nested_tabs.children = [
        daily_entry['container'],
        insights_learning['container'],
        challenges_successes['container'],
        reflection_growth['container'],
        planning_meta['container'],
        day_rating['container'],
        history_trends['container']
    ]

    # Set tab titles
    nested_tabs.set_title(0, '📅 Daily Entry')
    nested_tabs.set_title(1, '💡 Insights & Learning')
    nested_tabs.set_title(2, '🎯 Challenges & Successes')
    nested_tabs.set_title(3, '🌱 Reflection & Growth')
    nested_tabs.set_title(4, '📝 Planning & Meta')
    nested_tabs.set_title(5, '⭐ Day Rating')
    nested_tabs.set_title(6, '📊 History & Trends')

    # Return container + widget references + state manager
    return {
        'container': nested_tabs,
        'widgets': {
            'daily_entry': daily_entry['widgets'],
            'insights_learning': insights_learning['widgets'],
            'challenges_successes': challenges_successes['widgets'],
            'reflection_growth': reflection_growth['widgets'],
            'planning_meta': planning_meta['widgets'],
            'day_rating': day_rating['widgets'],
            'history_trends': history_trends['widgets']
        },
        'state_manager': state_manager
    }

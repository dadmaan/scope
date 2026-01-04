"""
Session Statistics Tab Module

Creates the Session Statistics tab for quantitative metrics and
session-wide observations.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_session_statistics_tab():
    """
    Create the Session Statistics sub-tab with quantitative metrics and export.
    
    Returns:
        dict: {
            'container': VBox widget with session statistics UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating Session Statistics tab")
    
    # Session Stats Widgets
    usable_outputs = widgets.IntText(
        description='Usable outputs:',
        value=0,
        style={'description_width': 'initial'}
    )

    total_generation_time = widgets.Text(
        description='Generation time:',
        placeholder='e.g., 15 minutes total',
        style={'description_width': 'initial'}
    )

    total_processing_time = widgets.Text(
        description='Processing time:',
        placeholder='e.g., 30 minutes total',
        style={'description_width': 'initial'}
    )

    total_integration_time = widgets.Text(
        description='Integration time:',
        placeholder='e.g., 10 minutes',
        style={'description_width': 'initial'}
    )

    total_session_time = widgets.Text(
        description='Total session time:',
        placeholder='e.g., 55 minutes',
        style={'description_width': 'initial'}
    )

    productivity = widgets.RadioButtons(
        options=['High', 'Medium', 'Low'],
        description='Productivity:',
        style={'description_width': 'initial'}
    )

    efficiency = widgets.RadioButtons(
        options=['Faster than traditional', 'Comparable', 'Slower than traditional'],
        description='vs Traditional:',
        style={'description_width': 'initial'}
    )

    # Auto-calculate total attempts (placeholder - will be updated from notebook)
    total_attempts_display = widgets.HTML(
        value='<p><strong>Total attempts:</strong> Will be calculated from generation attempts</p>'
    )

    # Export button
    export_stats_button = widgets.Button(
        description='📊 Export Stats',
        button_style='info',
        tooltip='Export session statistics as CSV',
        layout=widgets.Layout(width='200px')
    )

    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #9C27B0; border-bottom: 2px solid #9C27B0; padding-bottom: 10px;">📊 Session Statistics</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Review session summary:</strong> generation counts, success rates, time investment, and outputs</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Briefly summarize the session's key metrics here. This provides a high-level overview of your productivity and efficiency, including the number of attempts versus usable outputs and the total time invested across different activities.</p>"),
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Basic Metrics</h4>'),
        total_attempts_display,
        usable_outputs,

        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Timing Metrics</h4>'),
        total_generation_time,
        total_processing_time,
        total_integration_time,
        total_session_time,

        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Quality Metrics</h4>'),
        productivity,
        efficiency,
        
        export_stats_button
    ])

    # Create widget reference dictionary
    widgets_dict = {
        'total_attempts_display': total_attempts_display,
        'usable_outputs': usable_outputs,
        'total_generation_time': total_generation_time,
        'total_processing_time': total_processing_time,
        'total_integration_time': total_integration_time,
        'total_session_time': total_session_time,
        'productivity': productivity,
        'efficiency': efficiency,
        'export_stats_button': export_stats_button
    }

    logger.debug("✅ Session Statistics tab created")
    return {'container': container, 'widgets': widgets_dict}

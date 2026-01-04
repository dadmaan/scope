"""
Execution Tab Module

Creates the Execution & Performance tab for activity logging
and system performance documentation.
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def create_workflow_execution_tab():
    """Create the Execution & Performance sub-tab."""
    # Execution Log Widget
    execution_log = widgets.Textarea(
        description='Activity Log:',
        placeholder='Document activities chronologically:\n\n[HH:MM] Activity - What you did, system used, outcome\n[HH:MM] ...',
        layout=widgets.Layout(width='700px', height='180px'),
        style={'description_width': 'initial'}
    )
    
    # System Performance Widget
    system_performance = widgets.Textarea(
        description='System performance:',
        placeholder='How did each system perform in this phase?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )
    
    # Organize into container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #FF9800; border-bottom: 2px solid #FF9800; padding-bottom: 10px;">📊 Execution & Performance</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;"></p>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;">Log activities performed, human/AI contributions, and time allocation during phase.</div>'),
        
        widgets.HTML("<p style=\"margin: 0; font-size: 16px;\">📌 Before you begin, outline your goals and expectations for this phase. Defining your creative vision, the assets you're starting with, and your estimated time commitment helps to frame the subsequent activities and measure success.</p>"),
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">Execution Log</h4>'),
        execution_log,
        
        widgets.HTML('<h4 style="color: #555; margin-top: 20px; border-bottom: 1px solid #ddd;">System Performance</h4>'),
        system_performance
    ])
    
    # Create widget reference dictionary
    widgets_dict = {
        'execution_log': execution_log,
        'system_performance': system_performance
    }
    
    return {'container': container, 'widgets': widgets_dict}

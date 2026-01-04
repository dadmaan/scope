"""
Quantitative Assessment Module - Orchestrator

Creates nested tab structure with 9 individual tabs:
- 8 assessment criteria (C1-C8), each in its own tab
- 1 overall synthesis tab

Returns nested Tab widget with all criterion widgets organized hierarchically.
"""

import ipywidgets as widgets


def create_assessment_tabs(loaded_sessions_ref, criterion_widgets_ref):
    """
    Create Quantitative Assessment nested tab structure.

    Args:
        loaded_sessions_ref (list): Reference to global loaded_sessions
        criterion_widgets_ref (dict): Reference to global criterion_widgets

    Returns:
        dict: {
            'container': Tab widget with 9 nested sub-tabs (8 criteria + synthesis),
            'widgets': {
                'C1': {...},
                'C2': {...},
                'C3': {...},
                'C4': {...},
                'C5': {...},
                'C6': {...},
                'C7': {...},
                'C8': {...},
                'synthesis': {...}
            }
        }
    """

    # Import individual criterion tab creators
    from .criterion_1_usability_tab import create_criterion_1_tab
    from .criterion_2_generation_speed_tab import create_criterion_2_tab
    from .criterion_3_audio_quality_tab import create_criterion_3_tab
    from .criterion_4_stylistic_accuracy_tab import create_criterion_4_tab
    from .criterion_5_parameter_control_tab import create_criterion_5_tab
    from .criterion_6_content_control_tab import create_criterion_6_tab
    from .criterion_7_daw_integration_tab import create_criterion_7_tab
    from .criterion_8_creative_workflow_tab import create_criterion_8_tab
    from .overall_synthesis_tab import create_synthesis_tab

    # Create individual criterion tabs
    c1 = create_criterion_1_tab(loaded_sessions_ref, criterion_widgets_ref)
    c2 = create_criterion_2_tab(loaded_sessions_ref, criterion_widgets_ref)
    c3 = create_criterion_3_tab(loaded_sessions_ref, criterion_widgets_ref)
    c4 = create_criterion_4_tab(loaded_sessions_ref, criterion_widgets_ref)
    c5 = create_criterion_5_tab(loaded_sessions_ref, criterion_widgets_ref)
    c6 = create_criterion_6_tab(loaded_sessions_ref, criterion_widgets_ref)
    c7 = create_criterion_7_tab(loaded_sessions_ref, criterion_widgets_ref)
    c8 = create_criterion_8_tab(loaded_sessions_ref, criterion_widgets_ref)
    synthesis = create_synthesis_tab()

    # Create nested Tab widget
    nested_tabs = widgets.Tab()
    nested_tabs.children = [
        c1['container'],
        c2['container'],
        c3['container'],
        c4['container'],
        c5['container'],
        c6['container'],
        c7['container'],
        c8['container'],
        synthesis['container']
    ]

    # Set tab titles
    nested_tabs.set_title(0, '1️⃣ Usability')
    nested_tabs.set_title(1, '2️⃣ Generation Speed')
    nested_tabs.set_title(2, '3️⃣ Audio Quality')
    nested_tabs.set_title(3, '4️⃣ Stylistic Accuracy')
    nested_tabs.set_title(4, '5️⃣ Parameter Control')
    nested_tabs.set_title(5, '6️⃣ Content Control')
    nested_tabs.set_title(6, '7️⃣ DAW Integration')
    nested_tabs.set_title(7, '8️⃣ Creative Workflow')
    nested_tabs.set_title(8, '📊 Overall Synthesis')

    # Return container + widget references
    return {
        'container': nested_tabs,
        'widgets': {
            'C1': c1['widgets'],
            'C2': c2['widgets'],
            'C3': c3['widgets'],
            'C4': c4['widgets'],
            'C5': c5['widgets'],
            'C6': c6['widgets'],
            'C7': c7['widgets'],
            'C8': c8['widgets'],
            'synthesis': synthesis['widgets']
        }
    }

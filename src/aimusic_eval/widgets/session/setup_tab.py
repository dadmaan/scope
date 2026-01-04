"""
Setup Tab Module

Creates the Session Setup & Metadata tab with session management,
metadata collection, and creative context definition.
"""

import logging
import ipywidgets as widgets
from datetime import datetime, date
from pathlib import Path

# Configure module logger
logger = logging.getLogger(__name__)


def create_session_setup_tab():
    """
    Create the Setup sub-tab with metadata, creative context, and goals.
    
    Returns:
        dict: {
            'container': VBox widget with setup UI,
            'widgets': Dictionary of widget references
        }
    """
    logger.debug("Creating enhanced Session Setup tab")
    
    # Session Metadata Widgets
    # session_type = widgets.Dropdown(
    #     options=['Standard Session', 'Full Workflow Cycle'],
    #     value='Standard Session',
    #     description='Session Type:',
    #     style={'description_width': 'initial'},
    #     layout=widgets.Layout(width='500px')
    # )
    evaluator_name = widgets.Text(
        description='Evaluator:',
        placeholder='Your name or ID',
        style={'description_width': 'initial'}
    )

    session_number = widgets.IntText(
        description='Session #:',
        value=1,
        min=1,
        style={'description_width': 'initial'}
    )

    session_name = widgets.Text(
        description='Session Name:',
        placeholder='e.g., Jazz Improv Study, Pop Melody Test',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='300px')
    )

    session_date = widgets.DatePicker(
        description='Date:',
        value=date.today(),
        style={'description_width': 'initial'}
    )

    session_start_time = widgets.Text(
        description='Start Time:',
        value=datetime.now().strftime('%H:%M'),
        placeholder='HH:MM (e.g., 14:30)',
        style={'description_width': 'initial'}
    )

    session_end_time = widgets.Text(
        description='End Time:',
        placeholder='HH:MM (e.g., 16:15)',
        style={'description_width': 'initial'}
    )

    system_name = widgets.Text(
        description='System Name:',
        placeholder='e.g., MusicGen, Riffusion, Magenta Studio',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    system_version = widgets.Text(
        description='Version:',
        placeholder='e.g., v1.2.0, Large model',
        style={'description_width': 'initial'}
    )

    interface_type = widgets.Dropdown(
        options=['Web Interface', 'Local GUI', 'Command Line', 'VST Plugin', 'AU Plugin', 'Standalone App', 'Other'],
        description='Interface:',
        style={'description_width': 'initial'}
    )

    hardware = widgets.Textarea(
        description='Hardware:',
        placeholder='e.g., NVIDIA RTX 3080, 32GB RAM, Intel i7',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    # Creative Context Widgets
    musical_element = widgets.Dropdown(
        options=['Bassline', 'Melody', 'Harmony', 'Drum Pattern', 'Percussion', 'Riffs', 'Texture', 'Effects', 'Full Mix', 'Other'],
        description='Musical Element:',
        style={'description_width': 'initial'}
    )

    genre = widgets.Text(
        description='Genre/Style:',
        placeholder='e.g., Funk, Electronic, Jazz, Rock',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='500px')
    )

    tempo = widgets.Text(
        description='Tempo:',
        placeholder='e.g., 90-130 BPM or 120 BPM',
        style={'description_width': 'initial'}
    )

    key = widgets.Text(
        description='Key/Scale:',
        placeholder='e.g., C minor, A major pentatonic',
        style={'description_width': 'initial'}
    )

    intended_use = widgets.Dropdown(
        options=['Foundation', 'Layer', 'Accent', 'Background', 'Transition', 'Feature Element', 'Experimental'],
        description='Intended Use:',
        style={'description_width': 'initial'}
    )

    references = widgets.Textarea(
        description='References:',
        placeholder='Any reference tracks or inspiration sources',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='600px', height='60px')
    )

    # Session Management Buttons
    new_session_button = widgets.Button(
        description='🆕 New Session',
        button_style='primary',
        tooltip='Clear all data and start fresh session',
        layout=widgets.Layout(width='150px', margin='10px')
    )

    save_session_button = widgets.Button(
        description='💾 Save State',
        button_style='success',
        tooltip='Save current session state for later resumption',
        layout=widgets.Layout(width='150px', margin='10px')
    )

    # Session status indicator
    session_status = widgets.HTML(
        value='<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Complete Session Setup First:</strong> Fill in the metadata below before proceeding to other tabs.</div>'
    )
    
    # Session status indicator
    session_save_status = widgets.HTML(
        value='<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;"><strong>Save First: </strong>It is recommended to save the current state before starting a new session.</div>'
    )

    # Session list display
    session_list_textbox = widgets.Textarea(
        description='Saved Sessions:',
        placeholder='No saved sessions found...',
        value='Loading saved sessions...',
        style={'description_width': 'initial'},
        layout=widgets.Layout(width='700px', height='120px'),
        disabled=True
    )

    # Refresh button for session list
    refresh_sessions_button = widgets.Button(
        description='🔄 Refresh List',
        button_style='info',
        tooltip='Refresh the list of saved sessions',
        layout=widgets.Layout(width='150px', margin='5px')
    )

    # Function to update session list
    def update_session_list():
        """Update the session list textbox with current saved sessions."""
        try:
            sessions_dir = Path.cwd().parent / 'outputs' / 'sessions'
            if not sessions_dir.exists():
                session_list_textbox.value = "No saved sessions directory found."
                return
            
            session_files = list(sessions_dir.glob('*.json'))
            if not session_files:
                session_list_textbox.value = "No saved sessions found.\nUse '💾 Save State' to create your first session checkpoint."
                return
            
            # Sort by modification time (newest first)
            session_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            session_list = []
            for session_file in session_files[:10]:  # Show last 10 sessions
                try:
                    # Get file info
                    mtime = session_file.stat().st_mtime
                    modified_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Try to extract session info from filename
                    filename = session_file.name
                    if 'session_state_' in filename:
                        session_type = "Auto-saved State"
                    elif 'session_checkpoint_' in filename:
                        session_type = "Manual Checkpoint"
                    else:
                        session_type = "Session File"
                    
                    session_list.append(f"📁 {session_type}")
                    session_list.append(f"   File: {filename}")
                    session_list.append(f"   Path: ../outputs/sessions/{filename}")
                    session_list.append(f"   Modified: {modified_time}")
                    session_list.append("")
                    
                except Exception as e:
                    session_list.append(f"📁 {session_file.name} (error reading file)")
                    session_list.append("")
            
            if len(session_files) > 10:
                session_list.append(f"... and {len(session_files) - 10} more sessions")
            
            session_list_textbox.value = "\n".join(session_list)
            
        except Exception as e:
            session_list_textbox.value = f"Error loading session list: {e}"

    # Initial update of session list
    update_session_list()

    # Connect refresh button
    def on_refresh_click(b):
        update_session_list()
        logger.info("🔄 Session list refreshed")
    
    refresh_sessions_button.on_click(on_refresh_click)

    # Organize into container with enhanced visibility
    container = widgets.VBox([
        # Enhanced header with visual prominence
        widgets.HTML('''
        <div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <h2 style="margin: 0; font-size: 24px;">🚀 Session Setup & Metadata</h2>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">Record session metadata, creative goals, and anticipated challenges before starting.</p>
        </div>
        '''),
        
        # Status indicator
        session_status,
        
        widgets.HTML('<p style="margin: 0; font-size: 16px;">📌 Use this section to record the context of your session. Capturing the AI system details, your hardware, and your creative intent (such as genre and tempo) provides a baseline for your evaluation and ensures your work is reproducible.</p>'),
        
        # Session Metadata section
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">📋 Session Metadata</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;">Record evaluator, session ID, system details, and technical environment</div>'),
        
        # session_type,
        evaluator_name,
        widgets.HBox([session_number, session_name]),
        widgets.HBox([session_date, session_start_time, session_end_time]),
        widgets.HBox([system_name, system_version]),
        interface_type,
        hardware,
    
        
        # Creative Context section
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">🎵 Creative Context</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;">Define the musical goals and constraints for this session</div>'),
        
        widgets.HBox([musical_element, genre]),
        widgets.HBox([tempo, key]),
        intended_use,
        references,
        
        # Saved Sessions section
        widgets.HTML('<h3 style="color: #2196F3; border-bottom: 2px solid #2196F3; padding-bottom: 10px;">💾 Session Management</h3>'),
        widgets.HTML('<div style="background: #FFF3CD; border: 2px solid #FFC107; border-radius: 5px; padding: 10px; margin: 10px 0;">View and manage your saved session states</div>'),
        
        session_list_textbox,
        refresh_sessions_button,
        
        session_save_status,
        # Session management buttons
        widgets.HBox([new_session_button, save_session_button], layout=widgets.Layout(justify_content='center')),
        
    ])

    # Create widget reference dictionary
    widgets_dict = {
        # 'session_type': session_type,
        'evaluator_name': evaluator_name,
        'session_number': session_number,
        'session_name': session_name,
        'session_date': session_date,
        'session_start_time': session_start_time,
        'session_end_time': session_end_time,
        'system_name': system_name,
        'system_version': system_version,
        'interface_type': interface_type,
        'hardware': hardware,
        'musical_element': musical_element,
        'genre': genre,
        'tempo': tempo,
        'key': key,
        'intended_use': intended_use,
        'references': references,
        'new_session_button': new_session_button,
        'save_session_button': save_session_button,
        'session_status': session_status,
        'session_list_textbox': session_list_textbox,
        'refresh_sessions_button': refresh_sessions_button
    }

    logger.debug("✅ Enhanced Session Setup tab created")
    return {'container': container, 'widgets': widgets_dict}

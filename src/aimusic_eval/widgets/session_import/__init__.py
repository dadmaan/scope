"""
Session Import Module

Handles loading Phase 1 session logs and makes them available for evidence extraction.
Provides UI for file path input and session loading with validation and statistics.

Returns:
    dict: {
        'container': VBox widget with session import UI,
        'widgets': dict of widget references
    }
"""

import ipywidgets as widgets
from IPython.display import clear_output, HTML, Markdown
import json
from pathlib import Path


def create_session_import_section(loaded_sessions_ref):
    """
    Create session import UI with file loading and validation.

    Args:
        loaded_sessions_ref (list): Reference to global loaded_sessions list (will be populated)

    Returns:
        dict: {
            'container': VBox containing session import widgets,
            'widgets': {
                'session_file_paths': Textarea,
                'load_button': Button,
                'import_output': Output
            },
            'load_sessions': function reference for programmatic access
        }
    """

    # Session file paths input
    session_file_paths = widgets.Textarea(
        description='Session Files:',
        placeholder='Paste file paths (one per line):\n../outputs/sessions/session_musicgen_20251020.json\n../outputs/sessions/session_musicgen_20251021.json',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    import_output = widgets.Output()

    def load_sessions(b):
        """
        Load session JSON files and populate loaded_sessions_ref.
        Displays statistics and validation results.
        """
        with import_output:
            clear_output()

            # Parse file paths
            paths = [p.strip() for p in session_file_paths.value.split('\n') if p.strip()]

            if not paths:
                print("❌ No file paths provided")
                return

            loaded_sessions_ref.clear()
            synthesis_data_sessions = []

            print(f"📥 Loading {len(paths)} session file(s)...\n")

            for path in paths:
                try:
                    file_path = Path(path)
                    if not file_path.exists():
                        print(f"⚠️ File not found: {path}")
                        continue

                    with open(file_path, 'r', encoding='utf-8') as f:
                        session = json.load(f)

                    # Extract key metadata
                    session_id = session.get('session_id', file_path.stem)
                    session_date = session.get('core_session', {}).get('metadata', {}).get('date', '')
                    session_system = session.get('core_session', {}).get('metadata', {}).get('system_name', '')

                    loaded_sessions_ref.append(session)
                    synthesis_data_sessions.append({
                        'session_id': session_id,
                        'date': session_date,
                        'file_path': str(file_path),
                        'system_name': session_system
                    })

                    print(f"✅ {session_id} ({session_date})")

                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {path}")
                except Exception as e:
                    print(f"❌ Error loading {path}: {e}")

            if loaded_sessions_ref:
                print(f"\n✅ Successfully loaded {len(loaded_sessions_ref)} session(s)")

                # Calculate statistics
                total_attempts = sum(
                    len(s.get('core_session', {}).get('generation_attempts', []))
                    for s in loaded_sessions_ref
                )
                print(f"📊 Total generation attempts: {total_attempts}")

                print("\n💡 Evidence from these sessions will populate criterion fields below.")
            else:
                print("\n❌ No sessions loaded. Check file paths and try again.")

    # Load button
    load_button = widgets.Button(
        description='📥 Load Sessions',
        button_style='success',
        layout=widgets.Layout(width='150px')
    )
    load_button.on_click(load_sessions)

    # Create container
    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #555;">Import Phase 1 Session Logs</h3>'),
        session_file_paths,
        load_button,
        import_output
    ])

    # Return structured data
    return {
        'container': container,
        'widgets': {
            'session_file_paths': session_file_paths,
            'load_button': load_button,
            'import_output': import_output
        },
        'load_sessions': load_sessions
    }

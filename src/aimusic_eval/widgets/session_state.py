"""
Session State Management Module

Provides functionality for saving, loading, and clearing session state across
all widget sections. This module is shared across the entire widgets package
to enable consistent state management.

Functions:
    - save_session_state: Save current widget values to JSON
    - load_session_state: Restore widget values from JSON
    - clear_session_state: Reset all widgets to defaults
    - setup_session_management_observers: Wire up session management buttons
"""

import logging
import ipywidgets as widgets

# Configure module logger
logger = logging.getLogger(__name__)


def save_session_state(all_widgets, session_file=None):
    """
    Save the current state of all session widgets to a JSON file.
    
    Args:
        all_widgets: Dictionary containing all widget sections
        session_file: Optional custom filename, defaults to timestamped file
        
    Returns:
        str: Path to saved session file, or None if failed
    """
    import json
    from pathlib import Path
    from datetime import datetime
    
    try:
        # Create sessions directory if it doesn't exist
        sessions_dir = Path.cwd().parent / 'outputs' / 'sessions'
        sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename if not provided
        if session_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            session_file = f"session_state_{timestamp}.json"
        
        session_path = sessions_dir / session_file
        
        # Collect all widget values
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'session_file': session_file
        }
        
        # Extract values from all widget sections
        for section_name, section_widgets in all_widgets.items():
            if section_name == 'container':
                continue
            session_data[section_name] = {}
            
            for widget_name, widget in section_widgets.items():
                if hasattr(widget, 'value'):
                    # Handle different widget types
                    if hasattr(widget, 'options'):  # Dropdown, RadioButtons
                        session_data[section_name][widget_name] = widget.value
                    elif widget_name.endswith('_date'):  # DatePicker
                        session_data[section_name][widget_name] = widget.value.isoformat() if widget.value else None
                    else:  # Text, Textarea, IntText
                        session_data[section_name][widget_name] = widget.value
        
        # Save to file
        with open(session_path, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        logger.info(f"✅ Session state saved to: {session_path}")
        return str(session_path)
        
    except Exception as e:
        logger.error(f"❌ Failed to save session state: {e}")
        return None


def load_session_state(all_widgets, session_file):
    """
    Load session state from a JSON file and restore widget values.
    
    Args:
        all_widgets: Dictionary containing all widget sections
        session_file: Path to the session file to load
        
    Returns:
        bool: True if successful, False otherwise
    """
    import json
    from pathlib import Path
    from datetime import date
    
    try:
        session_path = Path(session_file)
        if not session_path.exists():
            logger.error(f"❌ Session file not found: {session_file}")
            return False
        
        # Load session data
        with open(session_path, 'r') as f:
            session_data = json.load(f)
        
        logger.info(f"📂 Loading session state from: {session_file}")
        
        # Restore widget values
        for section_name, section_data in session_data.items():
            if section_name in ['timestamp', 'session_file'] or section_name not in all_widgets:
                continue
                
            section_widgets = all_widgets[section_name]
            
            for widget_name, value in section_data.items():
                if widget_name in section_widgets and hasattr(section_widgets[widget_name], 'value'):
                    widget = section_widgets[widget_name]
                    
                    # Handle different widget types
                    if widget_name.endswith('_date') and value:  # DatePicker
                        try:
                            widget.value = date.fromisoformat(value)
                        except:
                            widget.value = date.today()
                    else:
                        widget.value = value
        
        logger.info("✅ Session state loaded successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to load session state: {e}")
        return False


def clear_session_state(all_widgets):
    """
    Clear all widget values to start a fresh session.
    
    Args:
        all_widgets: Dictionary containing all widget sections
        
    Returns:
        bool: True if successful, False otherwise
    """
    from datetime import date, datetime
    
    try:
        logger.info("🆕 Starting new session - clearing all data...")
        
        # Clear each section
        for section_name, section_widgets in all_widgets.items():
            if section_name == 'container':
                continue
                
            # section_widgets could be a dict of sub-sections (like 'setup', 'generation') 
            # or directly widgets (for simpler sections)
            if isinstance(section_widgets, dict):
                for subsection_name, subsection_widgets in section_widgets.items():
                    if isinstance(subsection_widgets, dict):
                        # This is a sub-section with widgets
                        for widget_name, widget in subsection_widgets.items():
                            if hasattr(widget, 'value'):
                                # Reset to appropriate default values based on widget type
                                if widget_name == 'session_number':
                                    widget.value = 1
                                elif widget_name == 'session_name':
                                    widget.value = ''
                                elif widget_name.endswith('_date'):
                                    widget.value = date.today()
                                elif widget_name == 'session_start_time':
                                    widget.value = datetime.now().strftime('%H:%M')
                                elif widget_name == 'session_end_time':
                                    widget.value = ''
                                elif widget_name == 'usable_outputs':
                                    widget.value = 0
                                elif isinstance(widget, widgets.IntText) or isinstance(widget, widgets.IntSlider):
                                    widget.value = 0 if widget.min is None or widget.min < 0 else widget.min
                                elif isinstance(widget, widgets.FloatText) or isinstance(widget, widgets.FloatSlider):
                                    widget.value = 0.0 if widget.min is None or widget.min < 0 else float(widget.min)
                                elif isinstance(widget, widgets.SelectMultiple):
                                    widget.value = ()  # Empty tuple for SelectMultiple
                                elif isinstance(widget, widgets.Checkbox):
                                    widget.value = False  # Unchecked for Checkbox
                                elif hasattr(widget, 'options') and widget.options:
                                    widget.value = widget.options[0]  # First option
                                else:
                                    widget.value = ''  # Empty for text fields
                    else:
                        # subsection_widgets is actually a widget
                        widget = subsection_widgets
                        if hasattr(widget, 'value'):
                            if isinstance(widget, widgets.IntText) or isinstance(widget, widgets.IntSlider):
                                widget.value = 0 if widget.min is None or widget.min < 0 else widget.min
                            elif isinstance(widget, widgets.FloatText) or isinstance(widget, widgets.FloatSlider):
                                widget.value = 0.0 if widget.min is None or widget.min < 0 else float(widget.min)
                            elif isinstance(widget, widgets.SelectMultiple):
                                widget.value = ()  # Empty tuple for SelectMultiple
                            elif isinstance(widget, widgets.Checkbox):
                                widget.value = False  # Unchecked for Checkbox
                            elif hasattr(widget, 'options') and widget.options:
                                widget.value = widget.options[0]  # First option
                            else:
                                widget.value = ''  # Default clear
            else:
                # section_widgets is directly a widget
                widget = section_widgets
                if hasattr(widget, 'value'):
                    if isinstance(widget, widgets.IntText) or isinstance(widget, widgets.IntSlider):
                        widget.value = 0 if widget.min is None or widget.min < 0 else widget.min
                    elif isinstance(widget, widgets.FloatText) or isinstance(widget, widgets.FloatSlider):
                        widget.value = 0.0 if widget.min is None or widget.min < 0 else float(widget.min)
                    elif isinstance(widget, widgets.SelectMultiple):
                        widget.value = ()  # Empty tuple for SelectMultiple
                    elif isinstance(widget, widgets.Checkbox):
                        widget.value = False  # Unchecked for Checkbox
                    elif hasattr(widget, 'options') and widget.options:
                        widget.value = widget.options[0]  # First option
                    else:
                        widget.value = ''  # Default clear
        
        logger.info("✅ All session data cleared - ready for new session")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to clear session state: {e}")
        return False


def setup_session_management_observers(all_widgets, main_tabs):
    """
    Set up observers for automatic session saving and button handlers.
    
    Args:
        all_widgets: Dictionary containing all widget sections
        main_tabs: Main tab widget for observing tab changes
    """
    from datetime import datetime
    
    # Get setup widgets for button handlers
    setup_widgets = all_widgets.get('core_session', {}).get('setup', {})
    new_session_btn = setup_widgets.get('new_session_button')
    save_session_btn = setup_widgets.get('save_session_button')
    
    # Button click handlers
    def on_new_session_click(b):
        """Handle new session button click."""
        clear_session_state(all_widgets)
        # Reset to setup tab
        if hasattr(main_tabs, 'selected_index'):
            main_tabs.selected_index = 0
        logger.info("🆕 New session initiated")
    
    def on_save_session_click(b):
        """Handle save session button click."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"session_checkpoint_{timestamp}.json"
        save_session_state(all_widgets, filename)
    
    # Attach button handlers
    if new_session_btn:
        new_session_btn.on_click(on_new_session_click)
    if save_session_btn:
        save_session_btn.on_click(on_save_session_click)
    
    # Auto-save on tab changes (optional - could be too frequent)
    def on_tab_change(change):
        """Optional: Auto-save when switching tabs."""
        # Uncomment to enable auto-saving on tab changes
        # if change['new'] != change['old']:
        #     save_session_state(all_widgets, f"auto_save_{datetime.now().strftime('%H%M%S')}.json")
        pass
    
    # Attach tab change observer (currently disabled to avoid too frequent saves)
    # main_tabs.observe(on_tab_change, names='selected_index')
    
    logger.debug("✅ Session management observers configured")

"""
Export Package - Validation and Export Functionality

This package provides validation and JSON export capabilities for session data.

Main components:
- __init__: Main UI creation function
- validation: Session validation logic
- export_builder: Session data structure builder
- (utils.py is at root widgets/ level for shared use)

Main entry point: create_export_section(all_widgets, generation_attempts)
"""

import logging
import ipywidgets as widgets
import json
from datetime import datetime
from pathlib import Path
from IPython.display import HTML
import sys

try:
    # When imported as a package (from widgets.export)
    from .validation import validate_session_completeness
    from .export_builder import build_session_data
except ImportError:
    # When imported from widgets directory level - add current dir to path
    sys.path.insert(0, str(Path(__file__).parent))
    from validation import validate_session_completeness
    from export_builder import build_session_data

# Configure module logger
logger = logging.getLogger(__name__)


def create_export_section(all_widgets, generation_attempts):
    """
    Create the validation and export section.
    
    Args:
        all_widgets (dict): Dictionary containing all widget references organized by section
        generation_attempts (list): Global list of generation attempts
    
    Returns:
        dict: {
            'container': VBox with validation display and export button,
            'widgets': {
                'validation_output': Output widget,
                'validate_btn': Button widget,
                'export_btn': Button widget
            }
        }
    """
    logger.debug("Creating Validation & Export section")
    
    # Validation output area
    validation_output = widgets.Output()
    
    def validate_session():
        """Validate session data and display completeness."""
        with validation_output:
            validation_output.clear_output()
            validate_session_completeness(all_widgets, generation_attempts)
    
    def export_session(b):
        """Export session data to JSON file."""
        with validation_output:
            validation_output.clear_output()
            
            try:
                # Build session_data from all_widgets
                session_data = build_session_data(all_widgets, generation_attempts)
                
                # Update export timestamp
                session_data["template_metadata"]["exported_at"] = datetime.now().isoformat()
                
                # Generate filename
                session_id = session_data["core_session"]["metadata"]["session_id"]
                filename = f"{session_id}.json"
                
                # Create output directory
                output_dir = Path.cwd().parent / 'outputs' / 'sessions'
                output_dir.mkdir(parents=True, exist_ok=True)
                
                # Export JSON
                json_path = output_dir / filename
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)
                
                logger.info("=" * 60)
                logger.info("✅ SESSION EXPORTED SUCCESS")
                logger.info("=" * 60)
                logger.info(f"📄 Session ID: {session_id}")
                logger.info(f"📂 Location: {json_path}")
                logger.info("💡 Use this file in Phase 2 (Synthesis Journal) for:")
                logger.info("   - Formal 1-5 scoring of 8 performance criteria")
                logger.info("   - Evidence-based assessment")
                logger.info("   - Longitudinal analysis")
                logger.info("=" * 60)
                
            except Exception as e:
                logger.error(f"❌ Export failed: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
    
    # Create buttons
    validate_btn = widgets.Button(
        description='🔍 Validate Session',
        button_style='info',
        layout=widgets.Layout(width='180px', height='40px')
    )
    validate_btn.on_click(lambda b: validate_session())
    
    export_btn = widgets.Button(
        description='📦 Export Session',
        button_style='success',
        layout=widgets.Layout(width='180px', height='40px')
    )
    export_btn.on_click(export_session)
    
    # Create button container
    button_container = widgets.HBox([validate_btn, export_btn])
    
    # Create container
    container = widgets.VBox([
        widgets.HTML('<hr style="border: 1px solid #ddd; margin: 30px 0;">'),
        widgets.HTML('<h3 style="color: #555; border-bottom: 2px solid #555; padding-bottom: 10px;">✅ Validation & Export</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Check completeness and export your session data for Phase 2 (Synthesis Journal).</p>'),
        button_container,
        widgets.HTML('<hr style="border: 1px solid #ddd; margin: 30px 0;">'),
        validation_output
    ])
    
    # Create widget reference dictionary
    widgets_dict = {
        'validation_output': validation_output,
        'validate_btn': validate_btn,
        'export_btn': export_btn
    }
    
    logger.debug("✅ Validation & Export section created")
    return {'container': container, 'widgets': widgets_dict}


# Public API
__all__ = ['create_export_section']

"""
Validation Export Synthesis - Orchestrator Module

Creates the validation and export UI section for the synthesis journal.
Provides:
- Validation button with report display
- Export buttons (JSON, Markdown, CSV)
- Integration with shared exporters

Usage:
    >>> from widgets.validation_export_synthesis import create_validation_export_section
    >>> result = create_validation_export_section(
    ...     synthesis_data=synthesis_data,
    ...     system_widgets=system_widgets,
    ...     criterion_widgets=criterion_widgets,
    ...     synthesis_widgets=synthesis_widgets,
    ...     loaded_sessions=loaded_sessions,
    ...     calculate_scores=calculate_scores
    ... )
    >>> container = result['container']
    >>> widgets_dict = result['widgets']
"""

import ipywidgets as widgets
from IPython.display import display, Markdown, clear_output
from pathlib import Path
from datetime import datetime
import json
import logging

from .validation import validate_synthesis, format_validation_report
from .export_builder import collect_synthesis_data, get_collection_summary

# Import from core utilities package
from aimusic_eval.core.exporters import export_to_markdown, export_to_csv, export_to_json

logger = logging.getLogger(__name__)


def create_synthesis_export_section(all_widgets, synthesis_data, loaded_sessions):
    """
    Create validation and export UI section (Simplified Interface).

    Creates:
    - Validation button that runs validation and displays report
    - Export buttons (JSON, Markdown, CSV) with smart versioning
    - Output areas for validation reports and export status

    Args:
        all_widgets (dict): Dictionary containing all widget sections:
            - 'system_metadata': System metadata widgets
            - 'assessment': Assessment widgets
            - 'journal': Journal widgets
        synthesis_data (dict): The synthesis journal data structure
        loaded_sessions (list): List of loaded session data

    Returns:
        dict: Contains 'container' (VBox) and 'widgets' (dict) with all widgets

    Example:
        >>> result = create_synthesis_export_section(all_widgets, synthesis_data, loaded_sessions)
        >>> display(result['container'])
    """
    # Extract widget sections from all_widgets
    system_widgets = all_widgets.get('system_metadata', {})
    criterion_widgets = {}  # Will be populated from assessment widgets
    synthesis_widgets = {}  # Will be populated from assessment widgets

    # Extract criterion and synthesis widgets from assessment structure
    if 'assessment' in all_widgets:
        assessment = all_widgets['assessment']
        # Assessment contains sub-tabs, extract widgets from each
        for key, value in assessment.items():
            if isinstance(value, dict) and 'widgets' in value:
                criterion_widgets.update(value['widgets'])
                synthesis_widgets.update(value['widgets'])

    # Simple score calculation function
    def calculate_scores():
        """Calculate average score from criterion widgets."""
        scores = []
        for crit_id in [f'C{i}' for i in range(1, 9)]:
            if crit_id in criterion_widgets and 'score' in criterion_widgets[crit_id]:
                score_widget = criterion_widgets[crit_id]['score']
                if hasattr(score_widget, 'value') and score_widget.value:
                    try:
                        scores.append(int(score_widget.value))
                    except (ValueError, TypeError):
                        pass
        return sum(scores) / len(scores) if scores else 0
    # Output areas
    validation_output = widgets.Output()
    export_output = widgets.Output()

    # Create output directory
    output_dir = Path('../outputs/synthesis')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Validation button handler
    def run_validation(b):
        """Run validation and display report."""
        with validation_output:
            clear_output()
            try:
                # Collect latest data first
                collect_synthesis_data(
                    synthesis_data,
                    system_widgets,
                    criterion_widgets,
                    synthesis_widgets,
                    loaded_sessions,
                    calculate_scores
                )

                # Run validation
                validation_result = validate_synthesis(synthesis_data)

                # Display formatted report
                report = format_validation_report(validation_result)
                print(report)

            except Exception as e:
                logger.error(f"Validation error: {e}")
                print(f"❌ Validation failed: {e}")

    # Export JSON handler
    def export_synthesis_json(b):
        """Export synthesis journal to JSON with smart versioning."""
        with export_output:
            clear_output()
            try:
                # Collect latest data
                data = collect_synthesis_data(
                    synthesis_data,
                    system_widgets,
                    criterion_widgets,
                    synthesis_widgets,
                    loaded_sessions,
                    calculate_scores
                )

                # Generate filename
                system_slug = system_widgets.get('system_name').value.lower().replace(' ', '_') if 'system_name' in system_widgets and system_widgets.get('system_name').value else 'unnamed'
                base_filename = f"synthesis_{system_slug}.json"
                filepath = output_dir / base_filename

                # Smart versioning logic
                if filepath.exists():
                    print(f"File {base_filename} exists.")
                    print("To update, delete the old file and re-export, or export will create a new timestamped version.")
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    filepath = output_dir / f"synthesis_{system_slug}_{timestamp}.json"

                # Export using shared exporter
                if export_to_json(data, str(filepath)):
                    print(f"✅ JSON exported: {filepath}")
                    summary = get_collection_summary(data)
                    print(f"📊 {summary['criteria_count']} criteria captured")
                    print(f"📥 {summary['sessions_imported']} sessions referenced")
                else:
                    print(f"❌ Export failed")

            except Exception as e:
                logger.error(f"JSON export error: {e}")
                print(f"❌ Export failed: {e}")

    # Export Markdown handler
    def export_synthesis_markdown(b):
        """Export synthesis journal to Markdown."""
        with export_output:
            clear_output()
            try:
                # Collect latest data
                data = collect_synthesis_data(
                    synthesis_data,
                    system_widgets,
                    criterion_widgets,
                    synthesis_widgets,
                    loaded_sessions,
                    calculate_scores
                )

                # Generate filename
                system_slug = system_widgets.get('system_name').value.lower().replace(' ', '_') if 'system_name' in system_widgets and system_widgets.get('system_name').value else 'unnamed'
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filepath = output_dir / f"synthesis_{system_slug}_{timestamp}.md"

                # Export using shared exporter
                if export_to_markdown(data, str(filepath), 'synthesis'):
                    print(f"✅ Markdown exported: {filepath}")
                else:
                    print(f"❌ Export failed")

            except Exception as e:
                logger.error(f"Markdown export error: {e}")
                print(f"❌ Export failed: {e}")

    # Export CSV handler
    def export_synthesis_csv(b):
        """Export scores to CSV."""
        with export_output:
            clear_output()
            try:
                # Collect latest data
                data = collect_synthesis_data(
                    synthesis_data,
                    system_widgets,
                    criterion_widgets,
                    synthesis_widgets,
                    loaded_sessions,
                    calculate_scores
                )

                # Generate filename
                system_slug = system_widgets.get('system_name').value.lower().replace(' ', '_') if 'system_name' in system_widgets and system_widgets.get('system_name').value else 'unnamed'
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filepath = output_dir / f"synthesis_scores_{system_slug}_{timestamp}.csv"

                # Export using shared exporter
                if export_to_csv(data, str(filepath), 'synthesis'):
                    print(f"✅ CSV exported: {filepath}")
                else:
                    print(f"❌ Export failed")

            except Exception as e:
                logger.error(f"CSV export error: {e}")
                print(f"❌ Export failed: {e}")

    # Create validation button
    btn_validate = widgets.Button(
        description='🔍 Validate',
        button_style='warning',
        layout=widgets.Layout(width='150px')
    )
    btn_validate.on_click(run_validation)

    # Create export buttons
    btn_export_json = widgets.Button(
        description='💾 Export JSON',
        button_style='success',
        layout=widgets.Layout(width='150px')
    )
    btn_export_json.on_click(export_synthesis_json)

    btn_export_md = widgets.Button(
        description='📄 Export Markdown',
        button_style='info',
        layout=widgets.Layout(width='150px')
    )
    btn_export_md.on_click(export_synthesis_markdown)

    btn_export_csv = widgets.Button(
        description='📊 Export CSV',
        button_style='info',
        layout=widgets.Layout(width='150px')
    )
    btn_export_csv.on_click(export_synthesis_csv)

    # Create layout
    validation_section = widgets.VBox([
        widgets.HTML("<h3>Validation</h3>"),
        btn_validate,
        validation_output
    ])

    export_section = widgets.VBox([
        widgets.HTML("<h3>Export Your Synthesis Journal</h3>"),
        widgets.HBox([btn_export_json, btn_export_md, btn_export_csv]),
        export_output
    ])

    container = widgets.VBox([
        validation_section,
        export_section
    ])

    # Widget dictionary for external access
    widgets_dict = {
        'btn_validate': btn_validate,
        'btn_export_json': btn_export_json,
        'btn_export_md': btn_export_md,
        'btn_export_csv': btn_export_csv,
        'validation_output': validation_output,
        'export_output': export_output
    }

    return {
        'container': container,
        'widgets': widgets_dict
    }


# Create alias for backward compatibility
create_validation_export_section = create_synthesis_export_section

# Module exports
__all__ = [
    'create_synthesis_export_section',
    'create_validation_export_section',  # Alias for compatibility
    'validate_synthesis',
    'format_validation_report',
    'collect_synthesis_data',
    'get_collection_summary'
]

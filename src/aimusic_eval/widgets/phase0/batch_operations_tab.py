"""
Batch Operations Tab Module

Creates the batch operations interface for Phase 0.
Provides viewing, exporting, and importing functionality for all systems.
"""

import logging
import ipywidgets as widgets
from IPython.display import display, HTML
import json

logger = logging.getLogger(__name__)


def create_batch_operations_tab(state_manager=None):
    """
    Create the Batch Operations tab for Phase 0.
    
    This tab provides:
    - View all systems table
    - Export all systems to JSON
    - Export summary to CSV
    - Import systems from previous exports
    - Generate completion report
    - Status display
    
    Args:
        state_manager: Phase 0 StateManager instance (optional)
    
    Returns:
        dict: {
            'container': VBox widget with batch operations UI,
            'widgets': {
                'systems_table': HTML widget,
                'export_json_button': Button widget,
                'export_csv_button': Button widget,
                'import_button': Button widget,
                'report_button': Button widget,
                'refresh_button': Button widget,
                'status_output': Output widget,
                'file_upload': FileUpload widget
            }
        }
    """
    logger.debug("Creating Batch Operations tab")
    
    # Header
    header = widgets.HTML(
        value="<h3>📊 Batch Operations</h3>"
              "<p>View, export, and import Phase 0 system assessments.</p>"
    )
    
    # Systems table (populated dynamically)
    systems_table = widgets.HTML(
        value="<p><i>Loading systems...</i></p>",
        layout=widgets.Layout(
            border='1px solid #ddd',
            padding='10px',
            max_height='300px',
            overflow_y='auto'
        )
    )
    
    # Refresh button
    refresh_button = widgets.Button(
        description='🔄 Refresh Table',
        button_style='',
        tooltip='Reload systems list',
        layout=widgets.Layout(width='150px', margin='5px')
    )
    
    # Export buttons
    export_header = widgets.HTML(
        value="<hr><h4>Export Operations</h4>"
    )
    
    export_json_button = widgets.Button(
        description='📥 Export JSON',
        button_style='success',
        tooltip='Export all systems to single JSON file',
        layout=widgets.Layout(width='150px', margin='5px')
    )
    
    export_csv_button = widgets.Button(
        description='📊 Export CSV',
        button_style='success',
        tooltip='Export summary table to CSV',
        layout=widgets.Layout(width='150px', margin='5px')
    )
    
    report_button = widgets.Button(
        description='📝 Generate Report',
        button_style='info',
        tooltip='Create completion report',
        layout=widgets.Layout(width='150px', margin='5px')
    )
    
    export_box = widgets.HBox([
        export_json_button,
        export_csv_button,
        report_button
    ])
    
    # Import section
    import_header = widgets.HTML(
        value="<hr><h4>Import Operations</h4>"
    )
    
    file_upload = widgets.FileUpload(
        accept='.json',
        multiple=False,
        description='Choose JSON File',
        layout=widgets.Layout(width='300px')
    )
    
    import_button = widgets.Button(
        description='📤 Import Systems',
        button_style='primary',
        tooltip='Import systems from uploaded JSON file',
        layout=widgets.Layout(width='150px', margin='5px')
    )
    
    import_box = widgets.VBox([
        import_header,
        widgets.HTML("<small>Upload a Phase 0 export JSON file to import systems.</small>"),
        file_upload,
        import_button
    ])
    
    # Status output
    status_output = widgets.Output(
        layout=widgets.Layout(
            border='1px solid #ddd',
            padding='10px',
            margin='10px 0'
        )
    )
    
    # Assemble container
    container = widgets.VBox([
        header,
        widgets.HTML("<hr>"),
        widgets.HTML("<h4>Systems Overview</h4>"),
        systems_table,
        refresh_button,
        export_header,
        export_box,
        import_box,
        status_output
    ])
    
    # Return standard structure
    return {
        'container': container,
        'widgets': {
            'systems_table': systems_table,
            'export_json_button': export_json_button,
            'export_csv_button': export_csv_button,
            'import_button': import_button,
            'report_button': report_button,
            'refresh_button': refresh_button,
            'status_output': status_output,
            'file_upload': file_upload,
            'state_manager': state_manager  # Pass through for callbacks
        }
    }


def _generate_systems_table_html(systems):
    """
    Helper function to generate HTML table of systems.
    
    Args:
        systems (dict): Dictionary of system assessments
        
    Returns:
        str: HTML table markup
    """
    if not systems:
        return "<p><i>No systems assessed yet.</i></p>"
    
    html = """
    <table style='width:100%; border-collapse: collapse;'>
        <thead>
            <tr style='background-color: #f0f0f0;'>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>System</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Framework</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>GPU Type</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: center;'>Confidence</th>
                <th style='border: 1px solid #ddd; padding: 8px; text-align: left;'>Date</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for system_name, data in sorted(systems.items()):
        arch = data.get('architecture', {})
        hardware = data.get('hardware', {})
        
        # Calculate average confidence
        confidences = []
        for section in ['architecture', 'interface', 'hardware']:
            if section in data and 'confidence_rating' in data[section]:
                confidences.append(data[section]['confidence_rating'])
        avg_conf = sum(confidences) / len(confidences) if confidences else 0
        
        html += f"""
            <tr>
                <td style='border: 1px solid #ddd; padding: 8px;'><b>{system_name}</b></td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{arch.get('framework', 'N/A')}</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{hardware.get('gpu_type', 'N/A')}</td>
                <td style='border: 1px solid #ddd; padding: 8px; text-align: center;'>{avg_conf:.1f}/5</td>
                <td style='border: 1px solid #ddd; padding: 8px;'>{data.get('assessment_date', 'N/A')}</td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    """
    
    return html

"""
Phase 0 Package - System Overview

This package provides widgets for Phase 0 system-level assessments.
Includes system selection, architecture analysis, interface evaluation,
hardware requirements, and batch operations.

Main entry point: create_phase0_section()
"""

import logging
import ipywidgets as widgets
from datetime import datetime

# Import all tab creators
from .system_selector_tab import create_system_selector_tab
from .architecture_tab import create_architecture_tab
from .interface_tab import create_interface_tab
from .hardware_tab import create_hardware_tab
from .batch_operations_tab import create_batch_operations_tab, _generate_systems_table_html
from .state_manager import StateManager

# Configure module logger
logger = logging.getLogger(__name__)


def create_phase0_section(state_manager=None):
    """
    Create the complete Phase 0: System Overview section with all tabs.
    
    This function assembles all 5 Phase 0 tabs:
    - System Selector: Create/load systems
    - Architecture & Design: Criterion 1 assessment
    - Interface & Interaction: Criterion 2 assessment
    - Hardware & Accessibility: Criterion 3 assessment
    - Batch Operations: Export, import, view all
    
    Args:
        state_manager (StateManager): Optional StateManager instance.
                                     If None, creates new instance.
    
    Returns:
        dict: {
            'container': Tab widget with 5 sub-tabs,
            'widgets': {
                'system_selector': {...},
                'architecture': {...},
                'interface': {...},
                'hardware': {...},
                'batch_operations': {...},
                'state_manager': StateManager instance
            }
        }
    """
    logger.debug("Assembling Phase 0 section")
    
    # Create or use provided StateManager
    if state_manager is None:
        state_manager = StateManager()
    
    # Create all tabs
    system_selector = create_system_selector_tab(state_manager)
    architecture = create_architecture_tab(state_manager)
    interface = create_interface_tab(state_manager)
    hardware = create_hardware_tab(state_manager)
    batch_operations = create_batch_operations_tab(state_manager)
    
    # Wire up callbacks for system selector
    _setup_system_selector_callbacks(system_selector, architecture, interface, hardware, batch_operations, state_manager)
    
    # Wire up callbacks for batch operations
    _setup_batch_operations_callbacks(batch_operations, state_manager)
    
    # Create tab container
    tabs = widgets.Tab()
    tabs.children = [
        system_selector['container'],
        architecture['container'],
        interface['container'],
        hardware['container'],
        batch_operations['container']
    ]
    
    # Set tab titles
    tabs.set_title(0, '🎵 System')
    tabs.set_title(1, '🏗️ Architecture')
    tabs.set_title(2, '🖥️ Interface')
    tabs.set_title(3, '💻 Hardware')
    tabs.set_title(4, '📊 Batch Ops')
    
    # Return standard structure
    return {
        'container': tabs,
        'widgets': {
            'system_selector': system_selector['widgets'],
            'architecture': architecture['widgets'],
            'interface': interface['widgets'],
            'hardware': hardware['widgets'],
            'batch_operations': batch_operations['widgets'],
            'state_manager': state_manager
        }
    }


def _setup_system_selector_callbacks(selector, architecture, interface, hardware, batch_ops, state_manager):
    """
    Wire up callbacks for system selector tab.
    
    Args:
        selector (dict): System selector widgets
        architecture (dict): Architecture widgets
        interface (dict): Interface widgets
        hardware (dict): Hardware widgets
        batch_ops (dict): Batch operations widgets
        state_manager (StateManager): State manager instance
    """
    widgets_dict = selector['widgets']
    
    def on_save_clicked(b):
        """Handle save button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            
            system_name = widgets_dict['system_name'].value.strip()
            if not system_name:
                print("❌ Error: System name is required")
                return
            
            # Gather data from all tabs
            assessment = {
                'system_name': system_name,
                'category': widgets_dict['category'].value,
                'notes': widgets_dict['notes'].value,
                'assessment_date': datetime.now().strftime('%Y-%m-%d'),
                'architecture': {
                    'framework': architecture['widgets']['framework'].value,
                    'generation_mode': architecture['widgets']['generation_mode'].value,
                    'modalities': list(architecture['widgets']['modalities'].value),
                    'conditioning': architecture['widgets']['conditioning'].value,
                    'confidence_rating': architecture['widgets']['confidence'].value,
                    'evidence': architecture['widgets']['evidence'].value
                },
                'interface': {
                    'interaction_modes': list(interface['widgets']['interaction_modes'].value),
                    'interface_type': interface['widgets']['interface_type'].value,
                    'setup_complexity': interface['widgets']['setup_complexity'].value,
                    'gpu_required': interface['widgets']['gpu_required'].value,
                    'setup_time_minutes': interface['widgets']['setup_time_minutes'].value,
                    'confidence_rating': interface['widgets']['confidence'].value,
                    'evidence': interface['widgets']['evidence'].value
                },
                'hardware': {
                    'gpu_type': hardware['widgets']['gpu_type'].value,
                    'min_vram_gb': hardware['widgets']['min_vram_gb'].value,
                    'rec_vram_gb': hardware['widgets']['rec_vram_gb'].value,
                    'min_ram_gb': hardware['widgets']['min_ram_gb'].value,
                    'rec_ram_gb': hardware['widgets']['rec_ram_gb'].value,
                    'cpu_only_available': hardware['widgets']['cpu_only_available'].value,
                    'accessibility': {
                        'small_studio': hardware['widgets']['accessibility_small_studio'].value,
                        'independent': hardware['widgets']['accessibility_independent'].value,
                        'high_end': hardware['widgets']['accessibility_high_end'].value
                    },
                    'confidence_rating': hardware['widgets']['confidence'].value,
                    'evidence': hardware['widgets']['evidence'].value
                }
            }
            
            # Save via state manager
            success, result = state_manager.save_current(system_name, assessment)
            
            if success:
                print(f"✅ Saved: {system_name}")
                print(f"📁 File: {result}")
                
                # Update existing systems dropdown
                systems_list = ['-- Select System --'] + state_manager.list_all()
                widgets_dict['existing_selector'].options = systems_list
                widgets_dict['existing_selector'].value = '-- Select System --'
            else:
                print(f"❌ Error saving: {result}")
    
    def on_load_clicked(b):
        """Handle load button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            
            selected = widgets_dict['existing_selector'].value
            if selected == '-- Select System --':
                print("❌ Please select a system to load")
                return
            
            # Load from state manager
            data = state_manager.get_system(selected)
            
            if data:
                # Populate all widgets
                widgets_dict['system_name'].value = data.get('system_name', '')
                widgets_dict['category'].value = data.get('category', 'Other')
                widgets_dict['notes'].value = data.get('notes', '')
                
                arch = data.get('architecture', {})
                architecture['widgets']['framework'].value = arch.get('framework', 'Transformer')
                architecture['widgets']['generation_mode'].value = arch.get('generation_mode', 'Sequential (token-by-token)')
                architecture['widgets']['modalities'].value = arch.get('modalities', [])
                architecture['widgets']['conditioning'].value = arch.get('conditioning', '')
                architecture['widgets']['confidence'].value = arch.get('confidence_rating', 3)
                architecture['widgets']['evidence'].value = arch.get('evidence', '')
                
                iface = data.get('interface', {})
                interface['widgets']['interaction_modes'].value = iface.get('interaction_modes', [])
                interface['widgets']['interface_type'].value = iface.get('interface_type', 'Web Interface')
                interface['widgets']['setup_complexity'].value = iface.get('setup_complexity', 'Instant (Web/No Setup)')
                interface['widgets']['gpu_required'].value = iface.get('gpu_required', False)
                interface['widgets']['setup_time_minutes'].value = iface.get('setup_time_minutes', 0)
                interface['widgets']['confidence'].value = iface.get('confidence_rating', 3)
                interface['widgets']['evidence'].value = iface.get('evidence', '')
                
                hw = data.get('hardware', {})
                hardware['widgets']['gpu_type'].value = hw.get('gpu_type', 'NVIDIA (CUDA)')
                hardware['widgets']['min_vram_gb'].value = hw.get('min_vram_gb', 0)
                hardware['widgets']['rec_vram_gb'].value = hw.get('rec_vram_gb', 0)
                hardware['widgets']['min_ram_gb'].value = hw.get('min_ram_gb', 0)
                hardware['widgets']['rec_ram_gb'].value = hw.get('rec_ram_gb', 0)
                hardware['widgets']['cpu_only_available'].value = hw.get('cpu_only_available', False)
                
                acc = hw.get('accessibility', {})
                hardware['widgets']['accessibility_small_studio'].value = acc.get('small_studio', 'Accessible (Consumer Hardware)')
                hardware['widgets']['accessibility_independent'].value = acc.get('independent', 'Accessible (Consumer Hardware)')
                hardware['widgets']['accessibility_high_end'].value = acc.get('high_end', 'Accessible (Consumer Hardware)')
                hardware['widgets']['confidence'].value = hw.get('confidence_rating', 3)
                hardware['widgets']['evidence'].value = hw.get('evidence', '')
                
                print(f"✅ Loaded: {selected}")
            else:
                print(f"❌ System not found: {selected}")
    
    def on_new_clicked(b):
        """Handle new system button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            
            # Clear all widgets
            widgets_dict['system_name'].value = ''
            widgets_dict['notes'].value = ''
            widgets_dict['existing_selector'].value = '-- Select System --'
            
            # Reset architecture
            architecture['widgets']['conditioning'].value = ''
            architecture['widgets']['confidence'].value = 3
            architecture['widgets']['evidence'].value = ''
            
            # Reset interface
            interface['widgets']['gpu_required'].value = False
            interface['widgets']['setup_time_minutes'].value = 0
            interface['widgets']['confidence'].value = 3
            interface['widgets']['evidence'].value = ''
            
            # Reset hardware
            hardware['widgets']['min_vram_gb'].value = 0
            hardware['widgets']['rec_vram_gb'].value = 0
            hardware['widgets']['min_ram_gb'].value = 0
            hardware['widgets']['rec_ram_gb'].value = 0
            hardware['widgets']['cpu_only_available'].value = False
            hardware['widgets']['confidence'].value = 3
            hardware['widgets']['evidence'].value = ''
            
            print("✅ Form cleared for new system")
    
    # Attach callbacks
    widgets_dict['save_button'].on_click(on_save_clicked)
    widgets_dict['load_button'].on_click(on_load_clicked)
    widgets_dict['new_button'].on_click(on_new_clicked)


def _setup_batch_operations_callbacks(batch_ops, state_manager):
    """
    Wire up callbacks for batch operations tab.
    
    Args:
        batch_ops (dict): Batch operations widgets
        state_manager (StateManager): State manager instance
    """
    widgets_dict = batch_ops['widgets']
    
    def refresh_table():
        """Refresh the systems table."""
        html = _generate_systems_table_html(state_manager.systems)
        widgets_dict['systems_table'].value = html
    
    def on_refresh_clicked(b):
        """Handle refresh button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            state_manager.load_existing()
            refresh_table()
            print(f"✅ Refreshed: {len(state_manager.systems)} systems loaded")
    
    def on_export_json_clicked(b):
        """Handle export JSON button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            success, result = state_manager.export_all_json()
            if success:
                print(f"✅ Exported JSON: {result}")
            else:
                print(f"❌ Export failed: {result}")
    
    def on_export_csv_clicked(b):
        """Handle export CSV button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            success, result = state_manager.export_all_csv()
            if success:
                print(f"✅ Exported CSV: {result}")
            else:
                print(f"❌ Export failed: {result}")
    
    def on_report_clicked(b):
        """Handle generate report button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            success, result = state_manager.generate_completion_report()
            if success:
                print(f"✅ Report generated: {result}")
            else:
                print(f"❌ Report failed: {result}")
    
    def on_import_clicked(b):
        """Handle import button click."""
        with widgets_dict['status_output']:
            widgets_dict['status_output'].clear_output()
            
            uploaded = widgets_dict['file_upload'].value
            if not uploaded:
                print("❌ No file uploaded")
                return
            
            # Save uploaded file temporarily
            import tempfile
            from pathlib import Path
            
            try:
                # Get file content
                file_info = list(uploaded.values())[0]
                content = file_info['content']
                
                # Write to temp file
                with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.json') as f:
                    f.write(content)
                    temp_path = f.name
                
                # Import via state manager
                success, result = state_manager.import_from_previous(temp_path)
                
                # Clean up temp file
                Path(temp_path).unlink()
                
                if success:
                    print(f"✅ Imported {result} systems")
                    refresh_table()
                else:
                    print(f"❌ Import failed: {result}")
            except Exception as e:
                print(f"❌ Import error: {str(e)}")
    
    # Attach callbacks
    widgets_dict['refresh_button'].on_click(on_refresh_clicked)
    widgets_dict['export_json_button'].on_click(on_export_json_clicked)
    widgets_dict['export_csv_button'].on_click(on_export_csv_clicked)
    widgets_dict['report_button'].on_click(on_report_clicked)
    widgets_dict['import_button'].on_click(on_import_clicked)
    
    # Initialize table
    refresh_table()

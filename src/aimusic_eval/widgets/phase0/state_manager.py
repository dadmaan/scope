"""
Phase 0 State Manager

Manages persistence and retrieval of Phase 0 system assessments.
Handles loading, saving, exporting, and importing system overview data.
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class StateManager:
    """
    Manages Phase 0 system assessment data persistence.
    
    Unlike session_state.py (which handles Phase 1 archive-based versioning),
    this StateManager handles simple registry-style storage for system assessments.
    """
    
    def __init__(self, output_dir=None):
        """
        Initialize StateManager.
        
        Args:
            output_dir (str or Path): Directory for Phase 0 results.
                                     Defaults to '../outputs/phase0_results'
        """
        if output_dir is None:
            # Default to standard outputs location
            self.output_dir = Path(__file__).parent.parent.parent.parent.parent / 'outputs' / 'phase0_results'
        else:
            self.output_dir = Path(output_dir)
        
        # Create directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory registry of systems
        self.systems = {}
        
        # Load existing systems on initialization
        self.load_existing()
        
        logger.info(f"StateManager initialized with output_dir: {self.output_dir}")
    
    def load_existing(self):
        """
        Load all existing Phase 0 system assessments from disk.
        
        Scans output_dir for *_phase0.json files and loads them into memory.
        """
        self.systems = {}
        
        if not self.output_dir.exists():
            logger.warning(f"Output directory does not exist: {self.output_dir}")
            return
        
        # Find all phase0 JSON files
        json_files = list(self.output_dir.glob('*_phase0.json'))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    system_name = data.get('system_name', json_file.stem.replace('_phase0', ''))
                    self.systems[system_name] = data
                    logger.debug(f"Loaded system: {system_name}")
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")
        
        logger.info(f"Loaded {len(self.systems)} existing systems")
    
    def save_current(self, system_name, assessment):
        """
        Save current system assessment to disk and memory.
        
        Args:
            system_name (str): Name of the system
            assessment (dict): Complete Phase 0 assessment data
        """
        # Update in-memory registry
        self.systems[system_name] = assessment
        
        # Save to individual JSON file
        safe_name = system_name.replace(' ', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_name}_phase0.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(assessment, f, indent=2)
            logger.info(f"Saved system assessment: {system_name} -> {output_file}")
            return True, str(output_file)
        except Exception as e:
            logger.error(f"Error saving system {system_name}: {e}")
            return False, str(e)
    
    def get_system(self, system_name):
        """
        Retrieve system assessment from memory.
        
        Args:
            system_name (str): Name of the system
            
        Returns:
            dict or None: System assessment data or None if not found
        """
        return self.systems.get(system_name)
    
    def list_all(self):
        """
        Get list of all system names.
        
        Returns:
            list: List of system names
        """
        return list(self.systems.keys())
    
    def delete_system(self, system_name):
        """
        Delete system assessment from disk and memory.
        
        Args:
            system_name (str): Name of the system to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Remove from memory
        if system_name in self.systems:
            del self.systems[system_name]
        
        # Remove from disk
        safe_name = system_name.replace(' ', '_').replace('/', '_')
        output_file = self.output_dir / f"{safe_name}_phase0.json"
        
        try:
            if output_file.exists():
                output_file.unlink()
            logger.info(f"Deleted system: {system_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting system {system_name}: {e}")
            return False
    
    def export_all_json(self, output_file=None):
        """
        Export all systems to a single consolidated JSON file.
        
        Args:
            output_file (str or Path): Output file path. 
                                      Defaults to 'phase0_all_systems.json'
        
        Returns:
            tuple: (success: bool, filepath: str or error_message: str)
        """
        if output_file is None:
            output_file = self.output_dir / 'phase0_all_systems.json'
        else:
            output_file = Path(output_file)
        
        try:
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_systems': len(self.systems),
                'systems': self.systems
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"Exported {len(self.systems)} systems to {output_file}")
            return True, str(output_file)
        except Exception as e:
            logger.error(f"Error exporting all systems: {e}")
            return False, str(e)
    
    def export_all_csv(self, output_file=None):
        """
        Export systems summary to CSV file.
        
        Args:
            output_file (str or Path): Output file path.
                                      Defaults to 'phase0_summary.csv'
        
        Returns:
            tuple: (success: bool, filepath: str or error_message: str)
        """
        if output_file is None:
            output_file = self.output_dir / 'phase0_summary.csv'
        else:
            output_file = Path(output_file)
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header row
                writer.writerow([
                    'System Name',
                    'Assessment Date',
                    'Framework',
                    'Generation Mode',
                    'Architecture Confidence',
                    'Interaction Modes',
                    'Setup Complexity',
                    'Interface Confidence',
                    'GPU Type',
                    'Min VRAM (GB)',
                    'Hardware Confidence',
                    'Overall Notes'
                ])
                
                # Data rows
                for system_name, data in self.systems.items():
                    arch = data.get('architecture', {})
                    interface = data.get('interface', {})
                    hardware = data.get('hardware', {})
                    
                    writer.writerow([
                        system_name,
                        data.get('assessment_date', ''),
                        arch.get('framework', ''),
                        arch.get('generation_mode', ''),
                        arch.get('confidence_rating', ''),
                        ', '.join(interface.get('interaction_modes', [])),
                        interface.get('setup_complexity', ''),
                        interface.get('confidence_rating', ''),
                        hardware.get('gpu_type', ''),
                        hardware.get('min_vram_gb', ''),
                        hardware.get('confidence_rating', ''),
                        data.get('notes', '')[:100]  # Truncate notes
                    ])
            
            logger.info(f"Exported {len(self.systems)} systems to CSV: {output_file}")
            return True, str(output_file)
        except Exception as e:
            logger.error(f"Error exporting CSV: {e}")
            return False, str(e)
    
    def import_from_previous(self, import_file):
        """
        Import systems from a previous export JSON file.
        
        Args:
            import_file (str or Path): Path to JSON file to import
            
        Returns:
            tuple: (success: bool, count: int or error_message: str)
        """
        import_file = Path(import_file)
        
        if not import_file.exists():
            return False, f"File not found: {import_file}"
        
        try:
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both single system and multi-system formats
            if 'systems' in data:
                # Multi-system export format
                imported_systems = data['systems']
            else:
                # Single system format
                imported_systems = {data.get('system_name', 'imported_system'): data}
            
            # Save each system
            count = 0
            for system_name, assessment in imported_systems.items():
                success, _ = self.save_current(system_name, assessment)
                if success:
                    count += 1
            
            logger.info(f"Imported {count} systems from {import_file}")
            return True, count
        except Exception as e:
            logger.error(f"Error importing from {import_file}: {e}")
            return False, str(e)
    
    def generate_completion_report(self, output_file=None):
        """
        Generate a text report summarizing Phase 0 completion status.
        
        Args:
            output_file (str or Path): Output file path.
                                      Defaults to 'phase0_completion_report.txt'
        
        Returns:
            tuple: (success: bool, filepath: str or error_message: str)
        """
        if output_file is None:
            output_file = self.output_dir / 'phase0_completion_report.txt'
        else:
            output_file = Path(output_file)
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("=" * 70 + "\n")
                f.write("PHASE 0: SYSTEM OVERVIEW - COMPLETION REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Systems Assessed: {len(self.systems)}\n\n")
                
                if not self.systems:
                    f.write("No systems assessed yet.\n")
                else:
                    f.write("-" * 70 + "\n")
                    f.write("SYSTEMS OVERVIEW\n")
                    f.write("-" * 70 + "\n\n")
                    
                    for system_name, data in sorted(self.systems.items()):
                        f.write(f"System: {system_name}\n")
                        f.write(f"  Assessment Date: {data.get('assessment_date', 'N/A')}\n")
                        
                        arch = data.get('architecture', {})
                        f.write(f"  Framework: {arch.get('framework', 'N/A')}\n")
                        f.write(f"  Architecture Confidence: {arch.get('confidence_rating', 'N/A')}/5\n")
                        
                        interface = data.get('interface', {})
                        f.write(f"  Setup Complexity: {interface.get('setup_complexity', 'N/A')}\n")
                        f.write(f"  Interface Confidence: {interface.get('confidence_rating', 'N/A')}/5\n")
                        
                        hardware = data.get('hardware', {})
                        f.write(f"  GPU Type: {hardware.get('gpu_type', 'N/A')}\n")
                        f.write(f"  Hardware Confidence: {hardware.get('confidence_rating', 'N/A')}/5\n")
                        f.write("\n")
                
                f.write("-" * 70 + "\n")
                f.write("END OF REPORT\n")
                f.write("-" * 70 + "\n")
            
            logger.info(f"Generated completion report: {output_file}")
            return True, str(output_file)
        except Exception as e:
            logger.error(f"Error generating completion report: {e}")
            return False, str(e)

"""
Unit Tests for Phase 0 State Manager

Tests the StateManager class for loading, saving, exporting, and importing
Phase 0 system assessments.
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime

# Import the StateManager
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from aimusic_eval.widgets.phase0.state_manager import StateManager


class TestStateManager(unittest.TestCase):
    """Test cases for Phase 0 StateManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for tests
        self.temp_dir = tempfile.mkdtemp()
        self.state_manager = StateManager(output_dir=self.temp_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test StateManager initialization."""
        self.assertIsInstance(self.state_manager, StateManager)
        self.assertEqual(self.state_manager.systems, {})
        self.assertTrue(Path(self.temp_dir).exists())
    
    def test_save_and_load_system(self):
        """Test saving and loading a system assessment."""
        # Create sample assessment
        assessment = {
            'system_name': 'TestSystem',
            'assessment_date': '2025-10-31',
            'architecture': {
                'framework': 'Transformer',
                'generation_mode': 'Sequential (token-by-token)',
                'confidence_rating': 4
            },
            'interface': {
                'setup_complexity': 'Simple (One-Click Install)',
                'confidence_rating': 5
            },
            'hardware': {
                'gpu_type': 'NVIDIA (CUDA)',
                'confidence_rating': 3
            }
        }
        
        # Save system
        success, filepath = self.state_manager.save_current('TestSystem', assessment)
        self.assertTrue(success)
        self.assertTrue(Path(filepath).exists())
        
        # Verify in-memory storage
        self.assertIn('TestSystem', self.state_manager.systems)
        self.assertEqual(self.state_manager.systems['TestSystem'], assessment)
        
        # Load from disk (simulate fresh StateManager)
        new_manager = StateManager(output_dir=self.temp_dir)
        self.assertIn('TestSystem', new_manager.systems)
        self.assertEqual(new_manager.systems['TestSystem'], assessment)
    
    def test_list_all_systems(self):
        """Test listing all systems."""
        # Initially empty
        self.assertEqual(self.state_manager.list_all(), [])
        
        # Add systems
        for i in range(3):
            assessment = {
                'system_name': f'System{i}',
                'assessment_date': '2025-10-31',
                'architecture': {'confidence_rating': 3},
                'interface': {'confidence_rating': 3},
                'hardware': {'confidence_rating': 3}
            }
            self.state_manager.save_current(f'System{i}', assessment)
        
        # Verify list
        systems = self.state_manager.list_all()
        self.assertEqual(len(systems), 3)
        self.assertIn('System0', systems)
        self.assertIn('System1', systems)
        self.assertIn('System2', systems)
    
    def test_delete_system(self):
        """Test deleting a system."""
        # Create and save system
        assessment = {
            'system_name': 'DeleteMe',
            'assessment_date': '2025-10-31',
            'architecture': {'confidence_rating': 3},
            'interface': {'confidence_rating': 3},
            'hardware': {'confidence_rating': 3}
        }
        self.state_manager.save_current('DeleteMe', assessment)
        self.assertIn('DeleteMe', self.state_manager.systems)
        
        # Delete system
        success = self.state_manager.delete_system('DeleteMe')
        self.assertTrue(success)
        self.assertNotIn('DeleteMe', self.state_manager.systems)
        
        # Verify file deleted
        filepath = Path(self.temp_dir) / 'DeleteMe_phase0.json'
        self.assertFalse(filepath.exists())
    
    def test_export_json(self):
        """Test exporting all systems to JSON."""
        # Add systems
        for i in range(2):
            assessment = {
                'system_name': f'ExportSystem{i}',
                'assessment_date': '2025-10-31',
                'architecture': {'confidence_rating': 3},
                'interface': {'confidence_rating': 3},
                'hardware': {'confidence_rating': 3}
            }
            self.state_manager.save_current(f'ExportSystem{i}', assessment)
        
        # Export to JSON
        success, filepath = self.state_manager.export_all_json()
        self.assertTrue(success)
        self.assertTrue(Path(filepath).exists())
        
        # Verify JSON content
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.assertIn('export_date', data)
        self.assertEqual(data['total_systems'], 2)
        self.assertIn('systems', data)
        self.assertIn('ExportSystem0', data['systems'])
        self.assertIn('ExportSystem1', data['systems'])
    
    def test_export_csv(self):
        """Test exporting summary to CSV."""
        # Add system
        assessment = {
            'system_name': 'CSVSystem',
            'assessment_date': '2025-10-31',
            'architecture': {
                'framework': 'Diffusion Model',
                'generation_mode': 'Iterative Refinement',
                'confidence_rating': 4
            },
            'interface': {
                'interaction_modes': ['Text Prompts', 'Audio Input'],
                'setup_complexity': 'Moderate (Some Configuration)',
                'confidence_rating': 3
            },
            'hardware': {
                'gpu_type': 'NVIDIA (CUDA)',
                'min_vram_gb': 8,
                'confidence_rating': 5
            }
        }
        self.state_manager.save_current('CSVSystem', assessment)
        
        # Export to CSV
        success, filepath = self.state_manager.export_all_csv()
        self.assertTrue(success)
        self.assertTrue(Path(filepath).exists())
        
        # Verify CSV has content
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        self.assertGreater(len(lines), 1)  # Header + at least 1 data row
        self.assertIn('System Name', lines[0])
        self.assertIn('CSVSystem', lines[1])
    
    def test_import_from_previous(self):
        """Test importing systems from previous export."""
        # Create export file
        export_data = {
            'export_date': '2025-10-31',
            'total_systems': 1,
            'systems': {
                'ImportedSystem': {
                    'system_name': 'ImportedSystem',
                    'assessment_date': '2025-10-31',
                    'architecture': {'confidence_rating': 3},
                    'interface': {'confidence_rating': 3},
                    'hardware': {'confidence_rating': 3}
                }
            }
        }
        
        import_file = Path(self.temp_dir) / 'import_test.json'
        with open(import_file, 'w') as f:
            json.dump(export_data, f)
        
        # Import
        success, count = self.state_manager.import_from_previous(import_file)
        self.assertTrue(success)
        self.assertEqual(count, 1)
        self.assertIn('ImportedSystem', self.state_manager.systems)
    
    def test_generate_completion_report(self):
        """Test generating completion report."""
        # Add system
        assessment = {
            'system_name': 'ReportSystem',
            'assessment_date': '2025-10-31',
            'architecture': {
                'framework': 'Transformer',
                'confidence_rating': 4
            },
            'interface': {
                'setup_complexity': 'Simple (One-Click Install)',
                'confidence_rating': 5
            },
            'hardware': {
                'gpu_type': 'NVIDIA (CUDA)',
                'confidence_rating': 3
            }
        }
        self.state_manager.save_current('ReportSystem', assessment)
        
        # Generate report
        success, filepath = self.state_manager.generate_completion_report()
        self.assertTrue(success)
        self.assertTrue(Path(filepath).exists())
        
        # Verify report content
        with open(filepath, 'r') as f:
            content = f.read()
        
        self.assertIn('PHASE 0: SYSTEM OVERVIEW', content)
        self.assertIn('ReportSystem', content)
        self.assertIn('Total Systems Assessed: 1', content)


if __name__ == '__main__':
    unittest.main()

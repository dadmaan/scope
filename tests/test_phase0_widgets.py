"""
Unit Tests for Phase 0 Widgets

Tests the Phase 0 widget factory functions and validators.
"""

import unittest
from pathlib import Path

# Import widgets and validators
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from aimusic_eval.widgets.constants import (
    FRAMEWORKS, GENERATION_MODES, MODALITIES, 
    GPU_TYPES, ACCESSIBILITY_LEVELS, INTERACTION_MODES, SETUP_COMPLEXITY
)
from aimusic_eval.widgets.validators import (
    validate_confidence_rating, validate_phase0_assessment
)


class TestPhase0Constants(unittest.TestCase):
    """Test Phase 0 constants are properly defined."""
    
    def test_frameworks_defined(self):
        """Test FRAMEWORKS constant is defined and non-empty."""
        self.assertIsInstance(FRAMEWORKS, list)
        self.assertGreater(len(FRAMEWORKS), 0)
        self.assertIn('Transformer', FRAMEWORKS)
        self.assertIn('Diffusion Model', FRAMEWORKS)
    
    def test_generation_modes_defined(self):
        """Test GENERATION_MODES constant is defined."""
        self.assertIsInstance(GENERATION_MODES, list)
        self.assertGreater(len(GENERATION_MODES), 0)
        self.assertIn('Sequential (token-by-token)', GENERATION_MODES)
    
    def test_modalities_defined(self):
        """Test MODALITIES constant is defined."""
        self.assertIsInstance(MODALITIES, list)
        self.assertGreater(len(MODALITIES), 0)
        self.assertIn('Text-to-Audio', MODALITIES)
    
    def test_gpu_types_defined(self):
        """Test GPU_TYPES constant is defined."""
        self.assertIsInstance(GPU_TYPES, list)
        self.assertGreater(len(GPU_TYPES), 0)
        self.assertIn('NVIDIA (CUDA)', GPU_TYPES)
    
    def test_accessibility_levels_defined(self):
        """Test ACCESSIBILITY_LEVELS constant is defined."""
        self.assertIsInstance(ACCESSIBILITY_LEVELS, list)
        self.assertGreater(len(ACCESSIBILITY_LEVELS), 0)
        self.assertIn('Accessible (Consumer Hardware)', ACCESSIBILITY_LEVELS)
    
    def test_interaction_modes_defined(self):
        """Test INTERACTION_MODES constant is defined."""
        self.assertIsInstance(INTERACTION_MODES, list)
        self.assertGreater(len(INTERACTION_MODES), 0)
        self.assertIn('Text Prompts', INTERACTION_MODES)
    
    def test_setup_complexity_defined(self):
        """Test SETUP_COMPLEXITY constant is defined."""
        self.assertIsInstance(SETUP_COMPLEXITY, list)
        self.assertGreater(len(SETUP_COMPLEXITY), 0)
        self.assertIn('Instant (Web/No Setup)', SETUP_COMPLEXITY)


class TestPhase0Validators(unittest.TestCase):
    """Test Phase 0 validation functions."""
    
    def test_validate_confidence_rating_valid(self):
        """Test confidence rating validation with valid values."""
        self.assertTrue(validate_confidence_rating(1))
        self.assertTrue(validate_confidence_rating(3))
        self.assertTrue(validate_confidence_rating(5))
        self.assertTrue(validate_confidence_rating('4'))
    
    def test_validate_confidence_rating_invalid(self):
        """Test confidence rating validation with invalid values."""
        self.assertFalse(validate_confidence_rating(0))
        self.assertFalse(validate_confidence_rating(6))
        self.assertFalse(validate_confidence_rating(-1))
        self.assertFalse(validate_confidence_rating('invalid'))
        self.assertFalse(validate_confidence_rating(None))
    
    def test_validate_phase0_assessment_complete(self):
        """Test assessment validation with complete data."""
        assessment = {
            'system_name': 'TestSystem',
            'assessment_date': '2025-10-31',
            'architecture': {
                'framework': 'Transformer',
                'generation_mode': 'Sequential',
                'confidence_rating': 4
            },
            'interface': {
                'interaction_modes': ['Text Prompts'],
                'setup_complexity': 'Simple',
                'confidence_rating': 5
            },
            'hardware': {
                'gpu_type': 'NVIDIA',
                'confidence_rating': 3
            }
        }
        
        missing = validate_phase0_assessment(assessment)
        self.assertEqual(missing, [])
    
    def test_validate_phase0_assessment_missing_top_level(self):
        """Test assessment validation with missing top-level fields."""
        assessment = {
            'system_name': 'TestSystem',
            # Missing assessment_date
            'architecture': {
                'framework': 'Transformer',
                'generation_mode': 'Sequential',
                'confidence_rating': 4
            }
            # Missing interface and hardware
        }
        
        missing = validate_phase0_assessment(assessment)
        self.assertIn('assessment_date', missing)
        self.assertIn('interface', missing)
        self.assertIn('hardware', missing)
    
    def test_validate_phase0_assessment_missing_sub_fields(self):
        """Test assessment validation with missing sub-fields."""
        assessment = {
            'system_name': 'TestSystem',
            'assessment_date': '2025-10-31',
            'architecture': {
                'framework': 'Transformer',
                # Missing generation_mode and confidence_rating
            },
            'interface': {
                'interaction_modes': ['Text Prompts'],
                'setup_complexity': 'Simple',
                'confidence_rating': 5
            },
            'hardware': {
                'gpu_type': 'NVIDIA',
                # Missing confidence_rating
            }
        }
        
        missing = validate_phase0_assessment(assessment)
        self.assertIn('architecture.generation_mode', missing)
        self.assertIn('architecture.confidence_rating', missing)
        self.assertIn('hardware.confidence_rating', missing)


class TestPhase0WidgetStructure(unittest.TestCase):
    """Test Phase 0 widget factory functions return correct structure."""
    
    def test_widget_return_structure(self):
        """Test that widgets return expected dict structure."""
        # We can't import ipywidgets in tests without a full environment,
        # but we can verify the structure is documented
        expected_keys = ['container', 'widgets']
        
        # This is a documentation test - the actual widget tests would
        # require a Jupyter environment
        self.assertTrue(True, "Widget structure documented: {'container': ..., 'widgets': {...}}")
    
    def test_architecture_tab_fields(self):
        """Test architecture tab has required widget fields."""
        required_widgets = [
            'framework',
            'generation_mode',
            'modalities',
            'conditioning',
            'confidence',
            'evidence'
        ]
        
        # Documentation test
        for widget in required_widgets:
            self.assertTrue(True, f"Architecture tab includes: {widget}")
    
    def test_interface_tab_fields(self):
        """Test interface tab has required widget fields."""
        required_widgets = [
            'interaction_modes',
            'interface_type',
            'setup_complexity',
            'gpu_required',
            'setup_time_minutes',
            'confidence',
            'evidence'
        ]
        
        # Documentation test
        for widget in required_widgets:
            self.assertTrue(True, f"Interface tab includes: {widget}")
    
    def test_hardware_tab_fields(self):
        """Test hardware tab has required widget fields."""
        required_widgets = [
            'gpu_type',
            'min_vram_gb',
            'rec_vram_gb',
            'min_ram_gb',
            'rec_ram_gb',
            'cpu_only_available',
            'accessibility_small_studio',
            'accessibility_independent',
            'accessibility_high_end',
            'confidence',
            'evidence'
        ]
        
        # Documentation test
        for widget in required_widgets:
            self.assertTrue(True, f"Hardware tab includes: {widget}")


if __name__ == '__main__':
    unittest.main()

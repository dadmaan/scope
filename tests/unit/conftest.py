"""
Pytest configuration and fixtures for AI Music Evaluation Framework tests.

Author: Shayan Dadman
"""

import pytest
from pathlib import Path
import json


@pytest.fixture
def sample_session_log():
    """Sample session log data for testing."""
    return {
        'session_info': {
            'date': '2025-10-10',
            'duration': '1.5 hours',
            'system': 'MusicGen',
            'version': '1.0',
            'interface': 'Web',
            'evaluator': 'Test Evaluator',
            'session_number': '1'
        },
        'creative_task': {
            'element': 'Bassline',
            'genre': 'Funk',
            'tempo': '90 BPM',
            'key': 'C minor',
            'intended_use': 'Foundation layer'
        },
        'generation_attempts': [
            {
                'time': '10:00',
                'prompt': 'Funky bassline at 90 BPM',
                'generation_time': 45.2,
                'quality': 4,
                'usable': True,
                'notes': 'Good groove'
            },
            {
                'time': '10:05',
                'prompt': 'Deep funk bass with syncopation',
                'generation_time': 43.8,
                'quality': 5,
                'usable': True,
                'notes': 'Excellent result'
            },
            {
                'time': '10:10',
                'prompt': 'Slap bass funk style',
                'generation_time': 47.1,
                'quality': 3,
                'usable': False,
                'notes': 'Too aggressive'
            }
        ],
        'real_time_criteria': {
            'usability': 4,
            'generation_speed': 5,
            'audio_quality': 4,
            'stylistic_accuracy': 4,
            'parameter_control': 3,
            'content_generation_control': 3,
            'daw_integration': 2,
            'creative_workflow': 4
        },
        'reflective_notes': {
            'what_worked': 'Fast generation times enabled rapid iteration',
            'what_frustrated': 'Limited control over bass timbre',
            'unexpected': 'System understood syncopation well'
        },
        'summary': {
            'total_attempts': 3,
            'usable_outputs': 2,
            'avg_generation_time': 45.4,
            'total_time': '90'
        },
        '_required_sections': ['session_info', 'creative_task', 'generation_attempts', 'real_time_criteria', 'reflective_notes']
    }


@pytest.fixture
def sample_quantitative_assessment():
    """Sample quantitative assessment data for testing."""
    return {
        'system_info': {
            'system': 'MusicGen',
            'period': '2025-10-01 to 2025-10-10',
            'total_sessions': 5,
            'evaluator': 'Test Evaluator',
            'date': '2025-10-10'
        },
        'criteria_scores': {
            'usability': 4,
            'generation_speed': 5,
            'audio_quality': 4,
            'stylistic_accuracy': 4,
            'parameter_control': 3,
            'content_generation_control': 3,
            'daw_integration': 2,
            'creative_workflow': 4
        },
        'criteria_evidence': {
            'usability': 'Interface is intuitive with clear prompting system',
            'generation_speed': 'Generates 15s output in ~45 seconds consistently',
            'audio_quality': 'Professional quality with minor compression artifacts',
            'stylistic_accuracy': 'Captures genre characteristics well',
            'parameter_control': 'Limited control over timbre and instrument specifics',
            'content_generation_control': 'Generates full mixes, requires separation',
            'daw_integration': 'File export only, no plugin version',
            'creative_workflow': 'Fast iteration supports creative flow'
        },
        'overall_assessment': {
            'strengths': [
                'Exceptional generation speed',
                'Good stylistic accuracy',
                'Intuitive interface'
            ],
            'weaknesses': [
                'Limited DAW integration',
                'Generates full mixes rather than stems',
                'Parameter control could be more granular'
            ],
            'recommendations': 'Best for rapid ideation and inspiration gathering'
        },
        '_required_sections': ['system_info', 'criteria_scores', 'criteria_evidence', 'overall_assessment']
    }


@pytest.fixture
def sample_critical_incident():
    """Sample critical incident data for testing."""
    return {
        'incident_classification': {
            'datetime': '2025-10-10 14:30',
            'system': 'MusicGen',
            'type': 'Unexpected Behavior',
            'severity': 'Moderate'
        },
        'incident_description': {
            'what_happened': 'System generated drums instead of requested bassline',
            'what_expected': 'Funk bassline at 90 BPM',
            'what_actually_happened': 'Drum pattern with some bass elements mixed in'
        },
        'analysis': {
            'significance': 'Reveals limitations in prompt interpretation for specific instruments',
            'criterion_implications': 'Affects stylistic accuracy and content generation control'
        },
        'learnings': {
            'learned': 'Need to be more specific with instrument names and add negative constraints',
            'approach_change': 'Now include "bass only, no drums" in all bass prompts'
        },
        '_required_sections': ['incident_classification', 'incident_description', 'analysis', 'learnings']
    }


@pytest.fixture
def sample_comparative_analysis():
    """Sample comparative analysis data for testing."""
    return {
        'systems_compared': ['MusicGen', 'Riffusion', 'Magenta Studio'],
        'comparison_matrix': {
            'MusicGen': {
                'usability': 4,
                'generation_speed': 5,
                'audio_quality': 4,
                'stylistic_accuracy': 4,
                'parameter_control': 3,
                'content_generation_control': 3,
                'daw_integration': 2,
                'creative_workflow': 4
            },
            'Riffusion': {
                'usability': 3,
                'generation_speed': 4,
                'audio_quality': 3,
                'stylistic_accuracy': 3,
                'parameter_control': 2,
                'content_generation_control': 2,
                'daw_integration': 1,
                'creative_workflow': 3
            },
            'Magenta Studio': {
                'usability': 3,
                'generation_speed': 4,
                'audio_quality': 5,
                'stylistic_accuracy': 4,
                'parameter_control': 4,
                'content_generation_control': 5,
                'daw_integration': 5,
                'creative_workflow': 4
            }
        },
        'criterion_analysis': {
            'usability': 'MusicGen leads with intuitive interface',
            'generation_speed': 'MusicGen is fastest',
            'audio_quality': 'Magenta Studio produces highest quality',
            'stylistic_accuracy': 'MusicGen and Magenta both strong',
            'parameter_control': 'Magenta offers most control',
            'content_generation_control': 'Magenta excels in content control',
            'daw_integration': 'Magenta is only true plugin',
            'creative_workflow': 'MusicGen and Magenta support flow best'
        },
        'synthesis': {
            'patterns': 'All systems struggle with precise instrument control',
            'distinctive': 'MusicGen fastest, Magenta best integration, Riffusion most experimental',
            'recommendations': 'Use MusicGen for ideation, Magenta for production'
        },
        '_required_sections': ['systems_compared', 'comparison_matrix', 'criterion_analysis', 'synthesis']
    }


@pytest.fixture
def sample_daily_journal():
    """Sample daily journal data for testing."""
    return {
        'entry_metadata': {
            'date': '2025-10-10',
            'day_of_week': 'Thursday',
            'productivity': 'High',
            'mood': 'Focused'
        },
        'activities_summary': {
            'systems': 'MusicGen (3 hours), Riffusion (1 hour)',
            'time_invested': 'Hands-on: 4 hours, Documentation: 1 hour'
        },
        'key_observations': {
            'observations': 'MusicGen much faster than Riffusion. Quality comparable but different character.'
        },
        'reflections': {
            'emotional': 'Started excited, became slightly frustrated with Riffusion limitations',
            'learnings': 'Speed matters more than I expected for maintaining creative flow'
        },
        'day_rating': {
            'productivity': 8,
            'learning': 9,
            'creativity': 7,
            'frustration': 4,
            'satisfaction': 8
        },
        '_required_sections': ['entry_metadata', 'activities_summary', 'key_observations', 'reflections', 'day_rating']
    }


@pytest.fixture
def sample_workflow_phase():
    """Sample workflow phase data for testing."""
    return {
        'phase_overview': {
            'phase_name': 'content_generation',
            'date': '2025-10-10',
            'duration': '2 hours',
            'systems': 'MusicGen'
        },
        'pre_phase_state': {
            'goals': 'Generate 5 usable basslines for funk track',
            'resources': 'Reference tracks, prompt templates'
        },
        'execution_log': [
            {
                'time': '10:00',
                'action': 'Generated first bassline with prompt "funky bass 90bpm"',
                'result': 'Good quality, usable'
            },
            {
                'time': '10:05',
                'action': 'Refined prompt to "deep funk bass with syncopation"',
                'result': 'Excellent result, exactly what needed'
            }
        ],
        'workflow_details': {
            'technical_observations': 'System responds well to specific tempo and style descriptors',
            'workflow_patterns': 'Iterative refinement of prompts yields better results'
        },
        'outcome_assessment': {
            'achievement': 'Generated 7 basslines, 5 usable (71% success rate)',
            'quality': 'High quality, met professional standards'
        },
        'learnings': {
            'key_learnings': 'Specific rhythmic descriptors (syncopation, groove) work well'
        },
        '_required_sections': ['phase_overview', 'pre_phase_state', 'execution_log', 'workflow_details', 'outcome_assessment', 'learnings']
    }


@pytest.fixture
def incomplete_session_log():
    """Incomplete session log for validation testing."""
    return {
        'session_info': {
            'date': '2025-10-10',
            'system': 'MusicGen',
            'evaluator': '___',  # Placeholder
        },
        'creative_task': {},  # Empty
        'generation_attempts': [],  # No attempts
        'real_time_criteria': {
            'usability': 4,
            'generation_speed': None  # Missing score
        },
        'reflective_notes': {
            'what_worked': 'YYYY-MM-DD'  # Placeholder
        },
        '_required_sections': ['session_info', 'creative_task', 'generation_attempts', 'real_time_criteria', 'reflective_notes']
    }


@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary directory for test outputs."""
    output_dir = tmp_path / "outputs"
    output_dir.mkdir()
    return output_dir

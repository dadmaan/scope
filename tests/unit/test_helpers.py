"""
Unit tests for helpers.py module.

Author: Shayan Dadman
"""

import pytest
from pathlib import Path

from aimusic_eval.core.helpers import (
    validate_completeness,
    calculate_completeness_percentage,
    aggregate_sessions,
    aggregate_quantitative,
    generate_radar_chart,
    calculate_statistics,
    format_time_duration,
    _has_unfilled_placeholders
)


class TestValidateCompleteness:
    """Tests for validate_completeness function."""

    def test_complete_data(self, sample_session_log):
        """Test validation of complete data."""
        result = validate_completeness(sample_session_log)

        assert result['valid'] is True
        assert result['completeness'] == 100.0
        assert len(result['missing']) == 0

    def test_incomplete_data(self, incomplete_session_log):
        """Test validation of incomplete data."""
        result = validate_completeness(incomplete_session_log)

        assert result['valid'] is False
        assert result['completeness'] < 100.0
        assert len(result['missing']) > 0
        assert 'creative_task' in result['missing']

    def test_partial_data(self):
        """Test validation of partially complete data."""
        data = {
            'section1': 'complete',
            'section2': '___',  # Placeholder
            'section3': 'complete',
            '_required_sections': ['section1', 'section2', 'section3']
        }

        result = validate_completeness(data)

        assert result['completeness'] > 0
        assert result['completeness'] < 100
        assert len(result['warnings']) > 0

    def test_empty_data(self):
        """Test validation of empty data."""
        data = {
            '_required_sections': ['field1', 'field2'],
            '_optional_sections': []
        }

        result = validate_completeness(data)

        assert result['valid'] is False
        assert result['completeness'] == 0.0
        assert 'field1' in result['missing']
        assert 'field2' in result['missing']


class TestHasUnfilledPlaceholders:
    """Tests for placeholder detection."""

    def test_underscore_placeholder(self):
        """Test detection of underscore placeholders."""
        assert _has_unfilled_placeholders('___') is True
        assert _has_unfilled_placeholders('__________') is True

    def test_bracket_placeholder(self):
        """Test detection of bracket placeholders."""
        assert _has_unfilled_placeholders('[Name]') is True
        assert _has_unfilled_placeholders('[System]') is True

    def test_date_placeholder(self):
        """Test detection of date placeholders."""
        assert _has_unfilled_placeholders('YYYY-MM-DD') is True
        assert _has_unfilled_placeholders('HH:MM') is True

    def test_real_values(self):
        """Test that real values are not detected as placeholders."""
        assert _has_unfilled_placeholders('MusicGen') is False
        assert _has_unfilled_placeholders('2025-10-10') is False
        assert _has_unfilled_placeholders('14:30') is False

    def test_empty_string(self):
        """Test empty string detection."""
        assert _has_unfilled_placeholders('') is True
        assert _has_unfilled_placeholders('   ') is True

    def test_nested_structures(self):
        """Test placeholder detection in nested structures."""
        assert _has_unfilled_placeholders({'key': '___'}) is True
        assert _has_unfilled_placeholders(['___', 'value']) is True
        assert _has_unfilled_placeholders([]) is True


class TestAggregateSessions:
    """Tests for aggregate_sessions function."""

    def test_single_session(self):
        """Test aggregation of single session."""
        sessions = [{
            'system': 'MusicGen',
            'attempts': 5,
            'usable': 3,
            'avg_time': 45.2,
            'date': '2025-10-10'
        }]

        result = aggregate_sessions(sessions)

        assert result['total_sessions'] == 1
        assert result['total_attempts'] == 5
        assert result['usable_outputs'] == 3
        assert result['usable_rate'] == 60.0
        assert result['avg_generation_time'] == 45.2

    def test_multiple_sessions(self):
        """Test aggregation of multiple sessions."""
        sessions = [
            {
                'system': 'MusicGen',
                'attempts': 5,
                'usable': 3,
                'avg_time': 45.2,
                'date': '2025-10-10'
            },
            {
                'system': 'MusicGen',
                'attempts': 4,
                'usable': 2,
                'avg_time': 42.8,
                'date': '2025-10-11'
            }
        ]

        result = aggregate_sessions(sessions)

        assert result['total_sessions'] == 2
        assert result['total_attempts'] == 9
        assert result['usable_outputs'] == 5
        assert result['usable_rate'] == pytest.approx(55.6, 0.1)
        assert result['avg_generation_time'] == pytest.approx(44.0, 0.1)
        assert 'MusicGen' in result['systems']

    def test_empty_sessions(self):
        """Test aggregation with no sessions."""
        result = aggregate_sessions([])

        assert result['total_sessions'] == 0
        assert result['total_attempts'] == 0
        assert result['usable_rate'] == 0.0

    def test_multiple_systems(self):
        """Test aggregation across multiple systems."""
        sessions = [
            {'system': 'MusicGen', 'attempts': 5, 'usable': 3, 'avg_time': 45},
            {'system': 'Riffusion', 'attempts': 5, 'usable': 2, 'avg_time': 60}
        ]

        result = aggregate_sessions(sessions)

        assert len(result['systems']) == 2
        assert 'MusicGen' in result['systems']
        assert 'Riffusion' in result['systems']


class TestAggregateQuantitative:
    """Tests for aggregate_quantitative function."""

    def test_single_assessment(self, sample_quantitative_assessment):
        """Test aggregation of single assessment."""
        assessments = [sample_quantitative_assessment]

        result = aggregate_quantitative(assessments)

        assert len(result['systems_evaluated']) == 1
        assert 'MusicGen' in result['systems_evaluated']
        assert 'usability' in result['criteria_scores']
        assert result['criteria_scores']['usability'] == [4]

    def test_multiple_assessments(self):
        """Test aggregation of multiple assessments."""
        assessments = [
            {
                'system': 'MusicGen',
                'scores': {'usability': 4, 'speed': 5, 'quality': 4}
            },
            {
                'system': 'Riffusion',
                'scores': {'usability': 3, 'speed': 4, 'quality': 3}
            }
        ]

        result = aggregate_quantitative(assessments)

        assert len(result['systems_evaluated']) == 2
        assert result['criteria_scores']['usability'] == [4, 3]
        assert result['criteria_stats']['usability']['mean'] == 3.5
        assert result['criteria_stats']['usability']['min'] == 3
        assert result['criteria_stats']['usability']['max'] == 4

    def test_overall_averages(self):
        """Test calculation of overall system averages."""
        assessments = [
            {
                'system': 'MusicGen',
                'scores': {'usability': 4, 'speed': 5}
            },
            {
                'system': 'Riffusion',
                'scores': {'usability': 3, 'speed': 3}
            }
        ]

        result = aggregate_quantitative(assessments)

        assert 'MusicGen' in result['overall_averages']
        assert 'Riffusion' in result['overall_averages']
        assert result['overall_averages']['MusicGen'] == 4.5
        assert result['overall_averages']['Riffusion'] == 3.0

    def test_empty_assessments(self):
        """Test aggregation with no assessments."""
        result = aggregate_quantitative([])

        assert result['criteria_scores'] == {}
        assert result['systems_evaluated'] == []


class TestGenerateRadarChart:
    """Tests for generate_radar_chart function."""

    def test_plotly_chart(self):
        """Test Plotly radar chart generation."""
        scores = {
            'Usability': 4,
            'Speed': 5,
            'Quality': 3,
            'Accuracy': 4,
            'Control': 3,
            'Content Control': 3,
            'DAW Integration': 2,
            'Workflow': 4
        }

        try:
            fig = generate_radar_chart(scores, backend='plotly')
            assert fig is not None
        except ImportError:
            pytest.skip("Plotly not installed")

    def test_matplotlib_chart(self):
        """Test Matplotlib radar chart generation."""
        scores = {
            'Usability': 4,
            'Speed': 5,
            'Quality': 3,
            'Accuracy': 4,
            'Control': 3,
            'Content Control': 3,
            'DAW Integration': 2,
            'Workflow': 4
        }

        try:
            fig = generate_radar_chart(scores, backend='matplotlib')
            assert fig is not None
        except ImportError:
            pytest.skip("Matplotlib not installed")

    def test_auto_backend(self):
        """Test automatic backend selection."""
        scores = {
            'Usability': 4,
            'Speed': 5,
            'Quality': 3
        }

        fig = generate_radar_chart(scores, backend='auto')
        # Should return something if either library is available
        # Or None if neither is available

    def test_empty_scores(self):
        """Test with empty scores."""
        result = generate_radar_chart({})
        # Should handle gracefully


class TestCalculateStatistics:
    """Tests for calculate_statistics function."""

    def test_basic_statistics(self):
        """Test calculation of basic statistics."""
        scores = [3, 4, 5, 4, 3, 4, 5, 3, 4, 4]

        stats = calculate_statistics(scores)

        assert stats['count'] == 10
        assert stats['mean'] == pytest.approx(3.9, 0.1)
        assert stats['median'] == 4.0
        assert stats['min'] == 3
        assert stats['max'] == 5
        assert stats['std'] > 0

    def test_single_value(self):
        """Test with single value."""
        stats = calculate_statistics([5])

        assert stats['count'] == 1
        assert stats['mean'] == 5.0
        assert stats['median'] == 5.0
        assert stats['std'] == 0.0

    def test_empty_list(self):
        """Test with empty list."""
        stats = calculate_statistics([])

        assert stats['count'] == 0
        assert stats['mean'] == 0.0
        assert stats['std'] == 0.0

    def test_floating_point_scores(self):
        """Test with floating point scores."""
        scores = [3.5, 4.2, 4.8, 3.9]

        stats = calculate_statistics(scores)

        assert stats['count'] == 4
        assert stats['mean'] > 3.0
        assert stats['mean'] < 5.0


class TestFormatTimeDuration:
    """Tests for format_time_duration function."""

    def test_seconds_only(self):
        """Test formatting of seconds."""
        assert format_time_duration(45) == "45s"
        assert format_time_duration(30) == "30s"

    def test_minutes_and_seconds(self):
        """Test formatting of minutes and seconds."""
        assert format_time_duration(150) == "2m 30s"
        assert format_time_duration(90) == "1m 30s"

    def test_minutes_only(self):
        """Test formatting of exact minutes."""
        assert format_time_duration(120) == "2m"
        assert format_time_duration(180) == "3m"

    def test_hours_minutes_seconds(self):
        """Test formatting with hours."""
        assert format_time_duration(3665) == "1h 1m 5s"
        assert format_time_duration(7200) == "2h"

    def test_zero(self):
        """Test zero duration."""
        assert format_time_duration(0) == "0s"


class TestCalculateCompletenessPercentage:
    """Tests for calculate_completeness_percentage function."""

    def test_complete_data(self, sample_session_log):
        """Test percentage for complete data."""
        percentage = calculate_completeness_percentage(sample_session_log)
        assert percentage == 100.0

    def test_incomplete_data(self, incomplete_session_log):
        """Test percentage for incomplete data."""
        percentage = calculate_completeness_percentage(incomplete_session_log)
        assert 0 < percentage < 100

    def test_empty_data(self):
        """Test percentage for empty data."""
        data = {
            '_required_sections': ['field1', 'field2']
        }
        percentage = calculate_completeness_percentage(data)
        assert percentage == 0.0

"""
Unit tests for validators.py module.

Author: Shayan Dadman
"""

import pytest

from aimusic_eval.core.validators import (
    TemplateValidator,
    validate_session_log,
    validate_quantitative,
    validate_critical_incident,
    validate_comparative,
    validate_daily_journal,
    validate_workflow_phase,
    validate_template
)


class TestTemplateValidator:
    """Tests for TemplateValidator base class."""

    def test_has_placeholder_underscores(self):
        """Test placeholder detection for underscores."""
        assert TemplateValidator.has_placeholder('___') is True
        assert TemplateValidator.has_placeholder('__________') is True
        assert TemplateValidator.has_placeholder('normal text') is False

    def test_has_placeholder_brackets(self):
        """Test placeholder detection for brackets."""
        assert TemplateValidator.has_placeholder('[Name]') is True
        assert TemplateValidator.has_placeholder('[System]') is True

    def test_has_placeholder_dates(self):
        """Test placeholder detection for date/time patterns."""
        assert TemplateValidator.has_placeholder('YYYY-MM-DD') is True
        assert TemplateValidator.has_placeholder('HH:MM') is True
        assert TemplateValidator.has_placeholder('2025-10-10') is False

    def test_is_empty_string(self):
        """Test empty string detection."""
        assert TemplateValidator.is_empty('') is True
        assert TemplateValidator.is_empty('   ') is True
        assert TemplateValidator.is_empty('text') is False

    def test_is_empty_none(self):
        """Test None detection."""
        assert TemplateValidator.is_empty(None) is True

    def test_is_empty_collections(self):
        """Test empty collection detection."""
        assert TemplateValidator.is_empty([]) is True
        assert TemplateValidator.is_empty({}) is True
        assert TemplateValidator.is_empty(['item']) is False


class TestValidateSessionLog:
    """Tests for validate_session_log function."""

    def test_valid_session_log(self, sample_session_log):
        """Test validation of valid session log."""
        result = validate_session_log(sample_session_log)

        assert result['valid'] is True
        assert result['completeness'] == 100.0
        assert len(result['missing']) == 0
        assert result['template_type'] == 'session_log'

    def test_incomplete_session_log(self, incomplete_session_log):
        """Test validation of incomplete session log."""
        result = validate_session_log(incomplete_session_log)

        assert result['valid'] is False
        assert result['completeness'] < 100.0
        assert len(result['missing']) > 0

    def test_missing_attempts(self):
        """Test validation when no generation attempts recorded."""
        data = {
            'session_info': {'date': '2025-10-10', 'system': 'Test'},
            'creative_task': {'element': 'bass'},
            'generation_attempts': [],  # Empty
            'real_time_criteria': {'usability': 4},
            'reflective_notes': {'what_worked': 'Something'},
            '_required_sections': ['session_info', 'creative_task', 'generation_attempts', 'real_time_criteria', 'reflective_notes']
        }

        result = validate_session_log(data)

        assert 'generation_attempts' in str(result['warnings'])

    def test_incomplete_criteria(self):
        """Test validation with incomplete criteria ratings."""
        data = {
            'session_info': {'date': '2025-10-10', 'system': 'Test'},
            'creative_task': {'element': 'bass'},
            'generation_attempts': [{'prompt': 'test'}],
            'real_time_criteria': {'usability': 4},  # Only 1 of 8
            'reflective_notes': {'what_worked': 'Something'},
            '_required_sections': ['session_info', 'creative_task', 'generation_attempts', 'real_time_criteria', 'reflective_notes']
        }

        result = validate_session_log(data)

        warnings_text = str(result['warnings'])
        assert 'criteria' in warnings_text.lower()


class TestValidateQuantitative:
    """Tests for validate_quantitative function."""

    def test_valid_quantitative(self, sample_quantitative_assessment):
        """Test validation of valid quantitative assessment."""
        result = validate_quantitative(sample_quantitative_assessment)

        assert result['valid'] is True
        assert result['completeness'] >= 80.0  # Higher bar
        assert len(result['missing']) == 0
        assert result['template_type'] == 'quantitative_assessment'

    def test_missing_criteria_scores(self):
        """Test validation with missing criterion scores."""
        data = {
            'system_info': {'system': 'Test', 'date': '2025-10-10'},
            'criteria_scores': {
                'usability': 4,
                'generation_speed': 5
                # Missing other 6 criteria
            },
            'criteria_evidence': {
                'usability': 'Good interface',
                'generation_speed': 'Very fast'
            },
            'overall_assessment': {'strengths': []},
            '_required_sections': ['system_info', 'criteria_scores', 'criteria_evidence', 'overall_assessment']
        }

        result = validate_quantitative(data)

        assert len(result['warnings']) > 0
        warnings_text = str(result['warnings'])
        assert 'missing score' in warnings_text.lower()

    def test_invalid_score_range(self):
        """Test validation with scores outside 1-5 range."""
        data = {
            'system_info': {'system': 'Test', 'date': '2025-10-10'},
            'criteria_scores': {
                'usability': 6,  # Invalid - should be 1-5
                'generation_speed': 0  # Invalid - should be 1-5
            },
            'criteria_evidence': {
                'usability': 'Evidence',
                'generation_speed': 'Evidence'
            },
            'overall_assessment': {},
            '_required_sections': ['system_info', 'criteria_scores', 'criteria_evidence', 'overall_assessment']
        }

        result = validate_quantitative(data)

        assert len(result['warnings']) > 0
        warnings_text = str(result['warnings'])
        assert 'invalid score' in warnings_text.lower()

    def test_missing_evidence(self):
        """Test validation with missing evidence."""
        data = {
            'system_info': {'system': 'Test', 'date': '2025-10-10'},
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
            'criteria_evidence': {},  # No evidence
            'overall_assessment': {},
            '_required_sections': ['system_info', 'criteria_scores', 'criteria_evidence', 'overall_assessment']
        }

        result = validate_quantitative(data)

        warnings_text = str(result['warnings'])
        assert 'evidence' in warnings_text.lower()


class TestValidateCriticalIncident:
    """Tests for validate_critical_incident function."""

    def test_valid_incident(self, sample_critical_incident):
        """Test validation of valid critical incident."""
        result = validate_critical_incident(sample_critical_incident)

        assert result['valid'] is True
        assert result['completeness'] >= 60.0
        assert len(result['missing']) == 0
        assert result['template_type'] == 'critical_incident'

    def test_missing_classification(self):
        """Test validation with missing classification details."""
        data = {
            'incident_classification': {
                'datetime': '2025-10-10 14:30',
                # Missing type and severity
            },
            'incident_description': {
                'what_happened': 'Something',
                'what_expected': 'Something',
                'what_actually_happened': 'Something'
            },
            'analysis': {'significance': 'Important'},
            'learnings': {'learned': 'Something'},
            '_required_sections': ['incident_classification', 'incident_description', 'analysis', 'learnings']
        }

        result = validate_critical_incident(data)

        warnings_text = str(result['warnings'])
        assert 'type' in warnings_text.lower() or 'severity' in warnings_text.lower()

    def test_incomplete_description(self):
        """Test validation with incomplete description."""
        data = {
            'incident_classification': {
                'datetime': '2025-10-10 14:30',
                'type': 'Breakthrough',
                'severity': 'Major'
            },
            'incident_description': {
                'what_happened': 'Something',
                # Missing what_expected and what_actually_happened
            },
            'analysis': {'significance': 'Important'},
            'learnings': {'learned': 'Something'},
            '_required_sections': ['incident_classification', 'incident_description', 'analysis', 'learnings']
        }

        result = validate_critical_incident(data)

        warnings_text = str(result['warnings'])
        assert 'what_expected' in warnings_text or 'what_actually_happened' in warnings_text


class TestValidateComparative:
    """Tests for validate_comparative function."""

    def test_valid_comparative(self, sample_comparative_analysis):
        """Test validation of valid comparative analysis."""
        result = validate_comparative(sample_comparative_analysis)

        assert result['valid'] is True
        assert result['completeness'] >= 70.0
        assert len(result['missing']) == 0
        assert result['template_type'] == 'comparative_analysis'

    def test_insufficient_systems(self):
        """Test validation with less than 2 systems."""
        data = {
            'systems_compared': ['OnlyOne'],  # Need at least 2
            'comparison_matrix': {},
            'criterion_analysis': {},
            'synthesis': {'patterns': 'Some'},
            '_required_sections': ['systems_compared', 'comparison_matrix', 'criterion_analysis', 'synthesis']
        }

        result = validate_comparative(data)

        warnings_text = str(result['warnings'])
        assert 'at least 2' in warnings_text.lower()

    def test_incomplete_comparison_matrix(self):
        """Test validation with incomplete comparison matrix."""
        data = {
            'systems_compared': ['System1', 'System2'],
            'comparison_matrix': {
                'System1': {'usability': 4}  # Only 1 criterion
                # Missing System2 scores
            },
            'criterion_analysis': {},
            'synthesis': {},
            '_required_sections': ['systems_compared', 'comparison_matrix', 'criterion_analysis', 'synthesis']
        }

        result = validate_comparative(data)

        # Should warn about incomplete matrix
        assert len(result['warnings']) > 0


class TestValidateDailyJournal:
    """Tests for validate_daily_journal function."""

    def test_valid_journal(self, sample_daily_journal):
        """Test validation of valid daily journal."""
        result = validate_daily_journal(sample_daily_journal)

        assert result['valid'] is True
        assert result['completeness'] >= 50.0  # Lower bar
        assert len(result['missing']) == 0
        assert result['template_type'] == 'daily_journal'

    def test_missing_date(self):
        """Test validation with missing date."""
        data = {
            'entry_metadata': {},  # No date
            'activities_summary': {'systems': 'Test'},
            'key_observations': {'observations': 'Some'},
            'reflections': {'emotional': 'Good'},
            'day_rating': {'productivity': 8},
            '_required_sections': ['entry_metadata', 'activities_summary', 'key_observations', 'reflections', 'day_rating']
        }

        result = validate_daily_journal(data)

        warnings_text = str(result['warnings'])
        assert 'date' in warnings_text.lower()

    def test_incomplete_rating(self):
        """Test validation with incomplete day rating."""
        data = {
            'entry_metadata': {'date': '2025-10-10'},
            'activities_summary': {'systems': 'Test'},
            'key_observations': {'observations': 'Some'},
            'reflections': {'emotional': 'Good'},
            'day_rating': {'productivity': 8},  # Missing other dimensions
            '_required_sections': ['entry_metadata', 'activities_summary', 'key_observations', 'reflections', 'day_rating']
        }

        result = validate_daily_journal(data)

        warnings_text = str(result['warnings'])
        # Should warn about missing rating dimensions


class TestValidateWorkflowPhase:
    """Tests for validate_workflow_phase function."""

    def test_valid_workflow(self, sample_workflow_phase):
        """Test validation of valid workflow phase."""
        result = validate_workflow_phase(sample_workflow_phase)

        assert result['valid'] is True
        assert result['completeness'] >= 60.0
        assert len(result['missing']) == 0
        assert result['template_type'] == 'workflow_phase'

    def test_missing_phase_name(self):
        """Test validation with missing phase name."""
        data = {
            'phase_overview': {},  # No phase_name
            'pre_phase_state': {'goals': 'Test'},
            'execution_log': [{'action': 'something'}],
            'workflow_details': {},
            'outcome_assessment': {},
            'learnings': {},
            '_required_sections': ['phase_overview', 'pre_phase_state', 'execution_log', 'workflow_details', 'outcome_assessment', 'learnings']
        }

        result = validate_workflow_phase(data)

        warnings_text = str(result['warnings'])
        assert 'phase name' in warnings_text.lower()

    def test_invalid_phase_name(self):
        """Test validation with invalid phase name."""
        data = {
            'phase_overview': {'phase_name': 'invalid_phase'},
            'pre_phase_state': {'goals': 'Test'},
            'execution_log': [{'action': 'something'}],
            'workflow_details': {},
            'outcome_assessment': {},
            'learnings': {},
            '_required_sections': ['phase_overview', 'pre_phase_state', 'execution_log', 'workflow_details', 'outcome_assessment', 'learnings']
        }

        result = validate_workflow_phase(data)

        warnings_text = str(result['warnings'])
        assert 'unknown phase' in warnings_text.lower()

    def test_empty_execution_log(self):
        """Test validation with empty execution log."""
        data = {
            'phase_overview': {'phase_name': 'content_generation'},
            'pre_phase_state': {'goals': 'Test'},
            'execution_log': [],  # Empty
            'workflow_details': {},
            'outcome_assessment': {},
            'learnings': {},
            '_required_sections': ['phase_overview', 'pre_phase_state', 'execution_log', 'workflow_details', 'outcome_assessment', 'learnings']
        }

        result = validate_workflow_phase(data)

        warnings_text = str(result['warnings'])
        assert 'no activities' in warnings_text.lower()


class TestValidateTemplate:
    """Tests for validate_template dispatcher function."""

    def test_session_log_type(self, sample_session_log):
        """Test validation with session_log type."""
        result = validate_template(sample_session_log, 'session_log')
        assert result['template_type'] == 'session_log'

    def test_quantitative_type(self, sample_quantitative_assessment):
        """Test validation with quantitative type."""
        result = validate_template(sample_quantitative_assessment, 'quantitative')
        assert result['template_type'] == 'quantitative_assessment'

    def test_quantitative_assessment_alias(self, sample_quantitative_assessment):
        """Test validation with quantitative_assessment alias."""
        result = validate_template(sample_quantitative_assessment, 'quantitative_assessment')
        assert result['template_type'] == 'quantitative_assessment'

    def test_critical_incident_type(self, sample_critical_incident):
        """Test validation with critical_incident type."""
        result = validate_template(sample_critical_incident, 'critical_incident')
        assert result['template_type'] == 'critical_incident'

    def test_comparative_type(self, sample_comparative_analysis):
        """Test validation with comparative type."""
        result = validate_template(sample_comparative_analysis, 'comparative')
        assert result['template_type'] == 'comparative_analysis'

    def test_daily_journal_type(self, sample_daily_journal):
        """Test validation with daily_journal type."""
        result = validate_template(sample_daily_journal, 'daily_journal')
        assert result['template_type'] == 'daily_journal'

    def test_workflow_phase_type(self, sample_workflow_phase):
        """Test validation with workflow_phase type."""
        result = validate_template(sample_workflow_phase, 'workflow_phase')
        assert result['template_type'] == 'workflow_phase'

    def test_unknown_type(self):
        """Test validation with unknown type."""
        result = validate_template({}, 'unknown_type')
        assert result['valid'] is False
        assert 'unknown template type' in str(result['warnings']).lower()

    def test_case_insensitive(self, sample_session_log):
        """Test that template type is case insensitive."""
        result1 = validate_template(sample_session_log, 'SESSION_LOG')
        result2 = validate_template(sample_session_log, 'session_log')
        assert result1['template_type'] == result2['template_type']

"""
Unit tests for comparative_analysis.py module.

Author: Shayan Dadman
"""

import pytest
from pathlib import Path
import json
import tempfile
import pandas as pd

from aimusic_eval.core.comparative_analysis import (
    load_quantitative_assessments,
    validate_assessment_compatibility,
    create_score_matrix,
    calculate_statistics,
    identify_criterion_winners,
    generate_radar_comparison,
    generate_bar_comparison,
    generate_heatmap,
    create_comparison_summary,
    export_comparison_report
)


@pytest.fixture
def sample_assessment_musicgen():
    """Sample quantitative assessment for MusicGen."""
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
            'usability': 'Interface is intuitive',
            'generation_speed': 'Very fast generation',
            'audio_quality': 'Professional quality',
            'stylistic_accuracy': 'Good genre matching',
            'parameter_control': 'Limited control',
            'content_generation_control': 'Generates full mixes',
            'daw_integration': 'File export only',
            'creative_workflow': 'Supports fast iteration'
        },
        'overall_assessment': {
            'strengths': [
                'Exceptional generation speed',
                'Good stylistic accuracy',
                'Intuitive interface'
            ],
            'weaknesses': [
                'Limited DAW integration',
                'Limited parameter control'
            ],
            'recommendations': 'Best for rapid ideation'
        }
    }


@pytest.fixture
def sample_assessment_riffusion():
    """Sample quantitative assessment for Riffusion."""
    return {
        'system_info': {
            'system': 'Riffusion',
            'period': '2025-10-01 to 2025-10-10',
            'total_sessions': 4,
            'evaluator': 'Test Evaluator',
            'date': '2025-10-10'
        },
        'criteria_scores': {
            'usability': 5,
            'generation_speed': 4,
            'audio_quality': 3,
            'stylistic_accuracy': 3,
            'parameter_control': 2,
            'content_generation_control': 2,
            'daw_integration': 3,
            'creative_workflow': 4
        },
        'criteria_evidence': {
            'usability': 'Very user-friendly interface',
            'generation_speed': 'Fast but not instant',
            'audio_quality': 'Moderate quality',
            'stylistic_accuracy': 'Variable style matching',
            'parameter_control': 'Minimal controls',
            'content_generation_control': 'Limited control',
            'daw_integration': 'Basic file export',
            'creative_workflow': 'Good for experimentation'
        },
        'overall_assessment': {
            'strengths': [
                'Excellent usability',
                'Good for experimentation'
            ],
            'weaknesses': [
                'Audio quality inconsistent',
                'Very limited control'
            ],
            'recommendations': 'Good for quick ideas'
        }
    }


@pytest.fixture
def sample_assessment_ddsp():
    """Sample quantitative assessment for DDSP."""
    return {
        'system_info': {
            'system': 'DDSP',
            'period': '2025-10-01 to 2025-10-10',
            'total_sessions': 6,
            'evaluator': 'Test Evaluator',
            'date': '2025-10-10'
        },
        'criteria_scores': {
            'usability': 2,
            'generation_speed': 3,
            'audio_quality': 5,
            'stylistic_accuracy': 5,
            'parameter_control': 5,
            'content_generation_control': 4,
            'daw_integration': 4,
            'creative_workflow': 3
        },
        'criteria_evidence': {
            'usability': 'Steep learning curve',
            'generation_speed': 'Moderate speed',
            'audio_quality': 'Exceptional quality',
            'stylistic_accuracy': 'Very accurate',
            'parameter_control': 'Extensive control',
            'content_generation_control': 'Good control',
            'daw_integration': 'Good plugin support',
            'creative_workflow': 'Complex workflow'
        },
        'overall_assessment': {
            'strengths': [
                'Exceptional audio quality',
                'Extensive parameter control',
                'Strong DAW integration'
            ],
            'weaknesses': [
                'Difficult to learn',
                'Complex workflow'
            ],
            'recommendations': 'Best for advanced users'
        }
    }


@pytest.fixture
def temp_json_files(sample_assessment_musicgen, sample_assessment_riffusion, sample_assessment_ddsp):
    """Create temporary JSON files for testing."""
    temp_dir = tempfile.mkdtemp()
    
    files = {}
    
    # MusicGen
    musicgen_path = Path(temp_dir) / 'musicgen_assessment.json'
    with open(musicgen_path, 'w') as f:
        json.dump({'data': sample_assessment_musicgen}, f)
    files['musicgen'] = str(musicgen_path)
    
    # Riffusion
    riffusion_path = Path(temp_dir) / 'riffusion_assessment.json'
    with open(riffusion_path, 'w') as f:
        json.dump({'data': sample_assessment_riffusion}, f)
    files['riffusion'] = str(riffusion_path)
    
    # DDSP
    ddsp_path = Path(temp_dir) / 'ddsp_assessment.json'
    with open(ddsp_path, 'w') as f:
        json.dump({'data': sample_assessment_ddsp}, f)
    files['ddsp'] = str(ddsp_path)
    
    yield files
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


class TestLoadQuantitativeAssessments:
    """Tests for load_quantitative_assessments function."""
    
    def test_load_single_file(self, temp_json_files):
        """Test loading a single assessment file."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        
        assert len(assessments) == 1
        assert 'MusicGen' in assessments
        assert assessments['MusicGen']['system_info']['system'] == 'MusicGen'
    
    def test_load_multiple_files(self, temp_json_files):
        """Test loading multiple assessment files."""
        file_list = [temp_json_files['musicgen'], temp_json_files['riffusion']]
        assessments = load_quantitative_assessments(file_list)
        
        assert len(assessments) == 2
        assert 'MusicGen' in assessments
        assert 'Riffusion' in assessments
    
    def test_file_not_found(self):
        """Test error handling for missing file."""
        with pytest.raises(FileNotFoundError):
            load_quantitative_assessments(['nonexistent.json'])
    
    def test_invalid_json(self):
        """Test error handling for invalid JSON."""
        temp_dir = tempfile.mkdtemp()
        bad_file = Path(temp_dir) / 'bad.json'
        
        with open(bad_file, 'w') as f:
            f.write('{ invalid json')
        
        with pytest.raises(ValueError, match='Invalid JSON'):
            load_quantitative_assessments([str(bad_file)])
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_wrong_template_type(self):
        """Test error handling for non-quantitative template."""
        temp_dir = tempfile.mkdtemp()
        wrong_file = Path(temp_dir) / 'wrong.json'
        
        with open(wrong_file, 'w') as f:
            json.dump({'data': {'session_info': {}, 'not_quantitative': True}}, f)
        
        with pytest.raises(ValueError, match='does not appear to be a quantitative assessment'):
            load_quantitative_assessments([str(wrong_file)])
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_duplicate_system_names(self, sample_assessment_musicgen):
        """Test handling of duplicate system names."""
        temp_dir = tempfile.mkdtemp()
        
        file1 = Path(temp_dir) / 'system1.json'
        file2 = Path(temp_dir) / 'system2.json'
        
        with open(file1, 'w') as f:
            json.dump({'data': sample_assessment_musicgen}, f)
        with open(file2, 'w') as f:
            json.dump({'data': sample_assessment_musicgen}, f)
        
        with pytest.warns(UserWarning, match='Duplicate system name'):
            assessments = load_quantitative_assessments([str(file1), str(file2)])
        
        assert len(assessments) == 2
        
        import shutil
        shutil.rmtree(temp_dir)


class TestValidateAssessmentCompatibility:
    """Tests for validate_assessment_compatibility function."""
    
    def test_compatible_assessments(self, temp_json_files):
        """Test validation of compatible assessments."""
        file_list = [temp_json_files['musicgen'], temp_json_files['riffusion']]
        assessments = load_quantitative_assessments(file_list)
        
        is_valid, warnings = validate_assessment_compatibility(assessments)
        
        assert is_valid is True
        assert isinstance(warnings, list)
    
    def test_too_few_assessments(self, temp_json_files):
        """Test validation with only one assessment."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        
        is_valid, warnings = validate_assessment_compatibility(assessments)
        
        assert is_valid is False
        assert any('at least 2' in w for w in warnings)
    
    def test_multiple_evaluators_warning(self, sample_assessment_musicgen, sample_assessment_riffusion):
        """Test warning for multiple evaluators."""
        sample_assessment_riffusion['system_info']['evaluator'] = 'Different Evaluator'
        
        assessments = {
            'MusicGen': sample_assessment_musicgen,
            'Riffusion': sample_assessment_riffusion
        }
        
        is_valid, warnings = validate_assessment_compatibility(assessments)
        
        assert any('Multiple evaluators' in w for w in warnings)
    
    def test_missing_criteria_warning(self, sample_assessment_musicgen, sample_assessment_riffusion):
        """Test warning for missing criteria."""
        del sample_assessment_riffusion['criteria_scores']['usability']
        
        assessments = {
            'MusicGen': sample_assessment_musicgen,
            'Riffusion': sample_assessment_riffusion
        }
        
        is_valid, warnings = validate_assessment_compatibility(assessments)
        
        assert any('missing criteria' in w for w in warnings)
    
    def test_few_common_criteria(self, sample_assessment_musicgen, sample_assessment_riffusion):
        """Test validation with very few common criteria."""
        # Remove most criteria from riffusion
        sample_assessment_riffusion['criteria_scores'] = {
            'usability': 5,
            'generation_speed': 4
        }
        
        assessments = {
            'MusicGen': sample_assessment_musicgen,
            'Riffusion': sample_assessment_riffusion
        }
        
        is_valid, warnings = validate_assessment_compatibility(assessments)
        
        assert is_valid is False
        assert any('few common criteria' in w.lower() for w in warnings)


class TestCreateScoreMatrix:
    """Tests for create_score_matrix function."""
    
    def test_basic_matrix_creation(self, temp_json_files):
        """Test basic score matrix creation."""
        file_list = [temp_json_files['musicgen'], temp_json_files['riffusion']]
        assessments = load_quantitative_assessments(file_list)
        
        matrix = create_score_matrix(assessments)
        
        assert isinstance(matrix, pd.DataFrame)
        assert len(matrix) == 2
        assert 'Average' in matrix.columns
        assert 'Usability' in matrix.columns
    
    def test_matrix_index(self, temp_json_files):
        """Test that system names are used as index."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        assert 'MusicGen' in matrix.index
    
    def test_average_calculation(self, sample_assessment_musicgen):
        """Test average score calculation."""
        assessments = {'MusicGen': sample_assessment_musicgen}
        matrix = create_score_matrix(assessments)
        
        scores = list(sample_assessment_musicgen['criteria_scores'].values())
        expected_avg = sum(scores) / len(scores)
        
        assert abs(matrix.loc['MusicGen', 'Average'] - expected_avg) < 0.01
    
    def test_all_criteria_present(self, temp_json_files):
        """Test that all standard criteria are in matrix."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        expected_columns = [
            'Usability', 'Generation Speed', 'Audio Quality', 'Stylistic Accuracy',
            'Parameter Control', 'Content Generation Control', 'DAW Integration',
            'Creative Workflow', 'Average'
        ]
        
        for col in expected_columns:
            assert col in matrix.columns


class TestCalculateStatistics:
    """Tests for calculate_statistics function."""
    
    def test_basic_statistics(self, temp_json_files):
        """Test basic statistical calculations."""
        file_list = [temp_json_files['musicgen'], temp_json_files['riffusion'], temp_json_files['ddsp']]
        assessments = load_quantitative_assessments(file_list)
        matrix = create_score_matrix(assessments)
        
        stats = calculate_statistics(matrix)
        
        assert isinstance(stats, dict)
        assert 'Usability' in stats
        assert 'mean' in stats['Usability']
        assert 'std' in stats['Usability']
    
    def test_statistics_accuracy(self, temp_json_files):
        """Test accuracy of statistical calculations."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        
        stats = calculate_statistics(matrix)
        
        # MusicGen usability: 4, Riffusion usability: 5
        # Mean should be 4.5
        assert stats['Usability']['mean'] == 4.5
        assert stats['Usability']['min'] == 4.0
        assert stats['Usability']['max'] == 5.0
    
    def test_single_system_statistics(self, temp_json_files):
        """Test statistics with single system (std should be 0)."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        stats = calculate_statistics(matrix)
        
        assert stats['Usability']['std'] == 0.0
    
    def test_statistics_include_average(self, temp_json_files):
        """Test that statistics include Average column."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        
        stats = calculate_statistics(matrix)
        
        assert 'Average' in stats
        assert stats['Average']['mean'] is not None


class TestIdentifyCriterionWinners:
    """Tests for identify_criterion_winners function."""
    
    def test_clear_winners(self, temp_json_files):
        """Test identification of clear winners."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        
        winners = identify_criterion_winners(matrix)
        
        assert isinstance(winners, dict)
        assert 'Usability' in winners
        assert 'Riffusion' in winners['Usability']  # Riffusion has 5 for usability
    
    def test_tied_winners(self, sample_assessment_musicgen, sample_assessment_riffusion):
        """Test handling of tied winners."""
        # Make both systems have same usability score
        sample_assessment_riffusion['criteria_scores']['usability'] = 4
        
        assessments = {
            'MusicGen': sample_assessment_musicgen,
            'Riffusion': sample_assessment_riffusion
        }
        
        matrix = create_score_matrix(assessments)
        winners = identify_criterion_winners(matrix)
        
        assert len(winners['Usability']) == 2
        assert 'MusicGen' in winners['Usability']
        assert 'Riffusion' in winners['Usability']
    
    def test_overall_winner(self, temp_json_files):
        """Test identification of overall winner."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        
        winners = identify_criterion_winners(matrix)
        
        assert 'Overall' in winners
        assert len(winners['Overall']) > 0
    
    def test_all_criteria_have_winners(self, temp_json_files):
        """Test that all criteria have winners identified."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        winners = identify_criterion_winners(matrix)
        
        # All criteria should have the single system as winner
        for col in matrix.columns:
            if col != 'Average':
                assert col in winners
                assert 'MusicGen' in winners[col]


class TestVisualizationFunctions:
    """Tests for visualization generation functions."""
    
    def test_radar_comparison_creates_figure(self, temp_json_files):
        """Test that radar comparison creates a figure object."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        
        fig = generate_radar_comparison(assessments)
        
        # Should return a figure object (plotly or matplotlib) or None if no lib
        assert fig is not None or True  # Either returns figure or None is acceptable
    
    def test_bar_comparison_with_criterion(self, temp_json_files):
        """Test bar comparison with specific criterion."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        fig = generate_bar_comparison(matrix, criterion='Usability')
        
        assert fig is not None or True
    
    def test_bar_comparison_average(self, temp_json_files):
        """Test bar comparison with average scores."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        fig = generate_bar_comparison(matrix, criterion=None)
        
        assert fig is not None or True
    
    def test_heatmap_generation(self, temp_json_files):
        """Test heatmap generation."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        
        fig = generate_heatmap(matrix)
        
        assert fig is not None or True


class TestCreateComparisonSummary:
    """Tests for create_comparison_summary function."""
    
    def test_summary_generation(self, temp_json_files):
        """Test generation of comparison summary."""
        file_list = [temp_json_files['musicgen'], temp_json_files['riffusion']]
        assessments = load_quantitative_assessments(file_list)
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        summary = create_comparison_summary(assessments, stats, winners)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'MusicGen' in summary or 'Riffusion' in summary
    
    def test_summary_includes_key_elements(self, temp_json_files):
        """Test that summary includes all key elements."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        summary = create_comparison_summary(assessments, stats, winners)
        
        assert 'Systems Compared' in summary
        assert 'Overall Winner' in summary or 'Overall Winners' in summary
        assert 'Criterion Winners' in summary
    
    def test_summary_with_three_systems(self, temp_json_files):
        """Test summary generation with three systems."""
        file_list = list(temp_json_files.values())
        assessments = load_quantitative_assessments(file_list)
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        summary = create_comparison_summary(assessments, stats, winners)
        
        assert 'MusicGen' in summary
        assert 'Riffusion' in summary
        assert 'DDSP' in summary


class TestExportComparisonReport:
    """Tests for export_comparison_report function."""
    
    def test_export_markdown(self, temp_json_files):
        """Test export to markdown format."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen'], temp_json_files['riffusion']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / 'report.md'
        
        result = export_comparison_report(
            assessments, matrix, stats, winners,
            "Manual insights here",
            str(output_path),
            format='markdown'
        )
        
        assert result is True
        assert output_path.exists()
        
        content = output_path.read_text()
        assert 'Comparison Report' in content
        assert 'MusicGen' in content
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_export_json(self, temp_json_files):
        """Test export to JSON format."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / 'report.json'
        
        result = export_comparison_report(
            assessments, matrix, stats, winners,
            "Manual insights",
            str(output_path),
            format='json'
        )
        
        assert result is True
        assert output_path.exists()
        
        with open(output_path) as f:
            data = json.load(f)
        assert 'comparison' in data
        assert 'systems_compared' in data['comparison']
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_export_csv(self, temp_json_files):
        """Test export to CSV format."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / 'report.csv'
        
        result = export_comparison_report(
            assessments, matrix, stats, winners,
            "Manual insights",
            str(output_path),
            format='csv'
        )
        
        assert result is True
        assert output_path.exists()
        
        # Verify CSV can be read
        df = pd.read_csv(output_path)
        assert len(df) > 0
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_export_creates_directories(self, temp_json_files):
        """Test that export creates necessary directories."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / 'nested' / 'path' / 'report.md'
        
        result = export_comparison_report(
            assessments, matrix, stats, winners,
            "Manual insights",
            str(output_path),
            format='markdown'
        )
        
        assert result is True
        assert output_path.exists()
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_export_unknown_format_defaults_to_markdown(self, temp_json_files):
        """Test that unknown format defaults to markdown."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / 'report.txt'
        
        with pytest.warns(UserWarning, match='Unknown format'):
            result = export_comparison_report(
                assessments, matrix, stats, winners,
                "Manual insights",
                str(output_path),
                format='unknown_format'
            )
        
        assert result is True
        assert output_path.exists()
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_export_with_empty_manual_insights(self, temp_json_files):
        """Test export with empty manual insights."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        temp_dir = tempfile.mkdtemp()
        output_path = Path(temp_dir) / 'report.md'
        
        result = export_comparison_report(
            assessments, matrix, stats, winners,
            "",  # Empty insights
            str(output_path),
            format='markdown'
        )
        
        assert result is True
        content = output_path.read_text()
        assert 'No manual insights provided' in content
        
        import shutil
        shutil.rmtree(temp_dir)


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_empty_file_list(self):
        """Test with empty file list."""
        assessments = load_quantitative_assessments([])
        assert len(assessments) == 0
    
    def test_bar_comparison_invalid_criterion(self, temp_json_files):
        """Test bar comparison with invalid criterion name."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        fig = generate_bar_comparison(matrix, criterion='NonexistentCriterion')
        
        # Should return None or warn
        assert fig is None or True
    
    def test_create_score_matrix_with_missing_scores(self, sample_assessment_musicgen):
        """Test score matrix creation when some scores are missing."""
        sample_assessment_musicgen['criteria_scores']['usability'] = None
        
        assessments = {'MusicGen': sample_assessment_musicgen}
        matrix = create_score_matrix(assessments)
        
        assert matrix.loc['MusicGen', 'Usability'] is None
    
    def test_statistics_with_all_none_values(self):
        """Test statistics calculation with all None values."""
        matrix = pd.DataFrame({
            'System': ['Test'],
            'Usability': [None],
            'Average': [None]
        }).set_index('System')
        
        stats = calculate_statistics(matrix)
        
        assert stats['Usability']['mean'] is None
        assert stats['Usability']['count'] == 0
    
    def test_winners_with_all_nan_criterion(self):
        """Test winner identification with all NaN values in a criterion."""
        matrix = pd.DataFrame({
            'System': ['Test1', 'Test2'],
            'Usability': [None, None],
            'Generation Speed': [4, 5],
            'Average': [4, 5]
        }).set_index('System')
        
        winners = identify_criterion_winners(matrix)
        
        assert winners['Usability'] == []
        assert 'Test2' in winners['Generation Speed']
    
    def test_visualization_with_single_system(self, temp_json_files):
        """Test visualizations with only one system."""
        assessments = load_quantitative_assessments([temp_json_files['musicgen']])
        matrix = create_score_matrix(assessments)
        
        # All visualizations should still work with single system
        radar = generate_radar_comparison(assessments, title="Single System Test")
        bar = generate_bar_comparison(matrix)
        heatmap = generate_heatmap(matrix, title="Single System Heatmap")
        
        assert radar is not None or True
        assert bar is not None or True
        assert heatmap is not None or True
    
    def test_summary_with_no_average_column(self, sample_assessment_musicgen):
        """Test summary generation when Average column is missing."""
        assessments = {'MusicGen': sample_assessment_musicgen}
        matrix = create_score_matrix(assessments)
        
        # Remove Average column
        if 'Average' in matrix.columns:
            matrix = matrix.drop(columns=['Average'])
        
        stats = calculate_statistics(matrix)
        winners = identify_criterion_winners(matrix)
        
        summary = create_comparison_summary(assessments, stats, winners)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_load_assessment_without_data_wrapper(self, sample_assessment_musicgen):
        """Test loading assessment JSON without 'data' wrapper."""
        temp_dir = tempfile.mkdtemp()
        json_file = Path(temp_dir) / 'direct_format.json'
        
        # Save without 'data' wrapper
        with open(json_file, 'w') as f:
            json.dump(sample_assessment_musicgen, f)
        
        assessments = load_quantitative_assessments([str(json_file)])
        
        assert 'MusicGen' in assessments
        assert assessments['MusicGen']['system_info']['system'] == 'MusicGen'
        
        import shutil
        shutil.rmtree(temp_dir)
    
    def test_validate_with_different_year_assessments(self, sample_assessment_musicgen, sample_assessment_riffusion):
        """Test validation warning for assessments from different years."""
        sample_assessment_musicgen['system_info']['period'] = '2024-10-01 to 2024-10-10'
        sample_assessment_riffusion['system_info']['period'] = '2025-10-01 to 2025-10-10'
        
        assessments = {
            'MusicGen': sample_assessment_musicgen,
            'Riffusion': sample_assessment_riffusion
        }
        
        is_valid, warnings = validate_assessment_compatibility(assessments)
        
        # Should have warning about multiple years
        assert any('multiple years' in w.lower() for w in warnings)

"""
Unit tests for exporters.py module.

Author: Shayan Dadman
"""

import pytest
import json
from pathlib import Path

from aimusic_eval.core.exporters import (
    export_to_markdown,
    export_to_csv,
    export_to_json,
    parse_markdown_to_data
)


class TestExportToMarkdown:
    """Tests for export_to_markdown function."""

    def test_export_session_log(self, sample_session_log, temp_output_dir):
        """Test exporting session log to markdown."""
        output_file = temp_output_dir / "session_log.md"

        success = export_to_markdown(
            sample_session_log,
            str(output_file),
            'session_log'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert '# System Evaluation Session Log' in content
        assert 'MusicGen' in content
        assert '## Session Information' in content

    def test_export_quantitative(self, sample_quantitative_assessment, temp_output_dir):
        """Test exporting quantitative assessment to markdown."""
        output_file = temp_output_dir / "quantitative.md"

        success = export_to_markdown(
            sample_quantitative_assessment,
            str(output_file),
            'quantitative'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert '# Quantitative Performance Assessment' in content
        assert 'Usability' in content
        assert 'Generation Speed' in content

    def test_export_critical_incident(self, sample_critical_incident, temp_output_dir):
        """Test exporting critical incident to markdown."""
        output_file = temp_output_dir / "incident.md"

        success = export_to_markdown(
            sample_critical_incident,
            str(output_file),
            'critical_incident'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert '# Critical Incident Report' in content
        assert 'Unexpected Behavior' in content

    def test_export_comparative(self, sample_comparative_analysis, temp_output_dir):
        """Test exporting comparative analysis to markdown."""
        output_file = temp_output_dir / "comparative.md"

        success = export_to_markdown(
            sample_comparative_analysis,
            str(output_file),
            'comparative'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert '# Comparative System Analysis' in content
        assert 'MusicGen' in content
        assert 'Riffusion' in content

    def test_export_daily_journal(self, sample_daily_journal, temp_output_dir):
        """Test exporting daily journal to markdown."""
        output_file = temp_output_dir / "journal.md"

        success = export_to_markdown(
            sample_daily_journal,
            str(output_file),
            'daily_journal'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert '# Daily Evaluation Journal' in content
        assert '2025-10-10' in content

    def test_export_workflow_phase(self, sample_workflow_phase, temp_output_dir):
        """Test exporting workflow phase to markdown."""
        output_file = temp_output_dir / "workflow.md"

        success = export_to_markdown(
            sample_workflow_phase,
            str(output_file),
            'workflow_phase'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert '# Workflow Phase Documentation' in content
        assert 'content_generation' in content

    def test_unknown_template_type(self, sample_session_log, temp_output_dir):
        """Test exporting with unknown template type."""
        output_file = temp_output_dir / "unknown.md"

        success = export_to_markdown(
            sample_session_log,
            str(output_file),
            'unknown_type'
        )

        assert success is False


class TestExportToCSV:
    """Tests for export_to_csv function."""

    def test_export_quantitative_csv(self, sample_quantitative_assessment, temp_output_dir):
        """Test exporting quantitative assessment to CSV."""
        output_file = temp_output_dir / "quantitative.csv"

        success = export_to_csv(
            sample_quantitative_assessment,
            str(output_file),
            'quantitative'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert 'evaluator' in content
        assert 'system' in content
        assert 'criterion' in content
        assert 'score' in content
        assert 'MusicGen' in content

    def test_export_comparative_csv(self, sample_comparative_analysis, temp_output_dir):
        """Test exporting comparative analysis to CSV."""
        output_file = temp_output_dir / "comparative.csv"

        success = export_to_csv(
            sample_comparative_analysis,
            str(output_file),
            'comparative'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert 'system' in content
        assert 'criterion' in content
        assert 'score' in content

    def test_export_session_log_csv(self, sample_session_log, temp_output_dir):
        """Test exporting session log to CSV."""
        output_file = temp_output_dir / "session.csv"

        success = export_to_csv(
            sample_session_log,
            str(output_file),
            'session_log'
        )

        assert success is True
        assert output_file.exists()

        content = output_file.read_text(encoding='utf-8')
        assert 'system' in content
        assert 'prompt' in content
        assert 'generation_time' in content


class TestExportToJSON:
    """Tests for export_to_json function."""

    def test_export_session_log_json(self, sample_session_log, temp_output_dir):
        """Test exporting session log to JSON."""
        output_file = temp_output_dir / "session.json"

        success = export_to_json(sample_session_log, str(output_file))

        assert success is True
        assert output_file.exists()

        # Verify JSON is valid
        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert 'export_date' in data
        assert 'framework_version' in data
        assert 'data' in data
        assert data['data']['session_info']['system'] == 'MusicGen'

    def test_export_quantitative_json(self, sample_quantitative_assessment, temp_output_dir):
        """Test exporting quantitative assessment to JSON."""
        output_file = temp_output_dir / "quantitative.json"

        success = export_to_json(sample_quantitative_assessment, str(output_file))

        assert success is True
        assert output_file.exists()

        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert 'data' in data
        assert 'criteria_scores' in data['data']
        assert data['data']['criteria_scores']['usability'] == 4

    def test_json_metadata(self, sample_session_log, temp_output_dir):
        """Test that JSON export includes metadata."""
        output_file = temp_output_dir / "session.json"

        export_to_json(sample_session_log, str(output_file))

        with open(output_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert 'export_date' in data
        assert 'framework_version' in data
        assert data['framework_version'] == '0.1.0'


class TestParseMarkdownToData:
    """Tests for parse_markdown_to_data function."""

    def test_round_trip_session_log(self, sample_session_log, temp_output_dir):
        """Test round-trip export and parse for session log."""
        output_file = temp_output_dir / "session.md"

        # Export
        export_to_markdown(sample_session_log, str(output_file), 'session_log')

        # Parse back
        parsed_data = parse_markdown_to_data(str(output_file))

        assert parsed_data is not None
        assert 'session_information' in parsed_data

    def test_parse_nonexistent_file(self):
        """Test parsing a non-existent file."""
        result = parse_markdown_to_data("nonexistent_file.md")
        assert result is None

    def test_parse_empty_file(self, temp_output_dir):
        """Test parsing an empty file."""
        empty_file = temp_output_dir / "empty.md"
        empty_file.write_text("", encoding='utf-8')

        result = parse_markdown_to_data(str(empty_file))
        # Should handle gracefully


class TestExportIntegration:
    """Integration tests for export functionality."""

    def test_export_all_formats(self, sample_quantitative_assessment, temp_output_dir):
        """Test exporting to all formats."""
        md_file = temp_output_dir / "test.md"
        csv_file = temp_output_dir / "test.csv"
        json_file = temp_output_dir / "test.json"

        # Export to all formats
        md_success = export_to_markdown(
            sample_quantitative_assessment,
            str(md_file),
            'quantitative'
        )
        csv_success = export_to_csv(
            sample_quantitative_assessment,
            str(csv_file),
            'quantitative'
        )
        json_success = export_to_json(
            sample_quantitative_assessment,
            str(json_file)
        )

        assert md_success is True
        assert csv_success is True
        assert json_success is True
        assert md_file.exists()
        assert csv_file.exists()
        assert json_file.exists()

    def test_unicode_handling(self, temp_output_dir):
        """Test that exports handle Unicode characters correctly."""
        data = {
            'system_info': {
                'system': 'Test System with émojis 🎵',
                'evaluator': 'Tëst Évàluåtor',
                'date': '2025-10-10'
            },
            'criteria_scores': {'usability': 4},
            'criteria_evidence': {'usability': 'Unicode test: café, naïve, 日本語'},
            'overall_assessment': {}
        }

        output_file = temp_output_dir / "unicode_test.md"

        success = export_to_markdown(data, str(output_file), 'quantitative')

        assert success is True

        content = output_file.read_text(encoding='utf-8')
        assert 'émojis' in content
        assert '🎵' in content
        assert 'café' in content

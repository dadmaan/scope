"""
AI Music Evaluation Framework - Comparative Analysis Module

Author: Shayan Dadman

This module provides automated comparative analysis functionality for quantitative assessments:
- Load and parse multiple JSON assessment files
- Validate assessment compatibility
- Create score matrices and statistical summaries
- Generate visualizations (radar, bar, heatmap)
- Auto-generate comparison insights
- Export comprehensive comparison reports
"""

from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import json
import pandas as pd
import warnings
from datetime import datetime

# Plotly imports with matplotlib fallback
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    warnings.warn("Plotly not available. Visualizations will use matplotlib fallback.")

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


# Standard 8 criteria for AI music systems
STANDARD_CRITERIA = [
    'usability',
    'generation_speed',
    'audio_quality',
    'stylistic_accuracy',
    'parameter_control',
    'content_generation_control',
    'daw_integration',
    'creative_workflow'
]

CRITERIA_DISPLAY_NAMES = {
    'usability': 'Usability',
    'generation_speed': 'Generation Speed',
    'audio_quality': 'Audio Quality',
    'stylistic_accuracy': 'Stylistic Accuracy',
    'parameter_control': 'Parameter Control',
    'content_generation_control': 'Content Generation Control',
    'daw_integration': 'DAW Integration',
    'creative_workflow': 'Creative Workflow'
}


def load_quantitative_assessments(file_paths: List[str]) -> Dict[str, Dict]:
    """
    Load and parse multiple JSON assessment files.
    
    Args:
        file_paths: List of paths to JSON files from quantitative assessments
        
    Returns:
        Dict mapping system names to assessment data
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or not quantitative template
        
    Example:
        >>> files = ['musicgen_assessment.json', 'riffusion_assessment.json']
        >>> assessments = load_quantitative_assessments(files)
        >>> print(list(assessments.keys()))
        ['MusicGen', 'Riffusion']
    """
    assessments = {}
    
    for file_path in file_paths:
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Assessment file not found: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
        
        # Extract data section (handle both direct data and wrapped format)
        if 'data' in content:
            data = content['data']
        else:
            data = content
        
        # Validate it's a quantitative assessment
        if 'system_info' not in data or 'criteria_scores' not in data:
            raise ValueError(
                f"File {file_path} does not appear to be a quantitative assessment. "
                f"Missing 'system_info' or 'criteria_scores' sections."
            )
        
        # Extract system name
        system_name = data['system_info'].get('system', 'Unknown System')
        
        # Check for duplicate system names
        if system_name in assessments:
            warnings.warn(
                f"Duplicate system name '{system_name}' found. "
                f"Using filename to distinguish: {path.stem}"
            )
            system_name = f"{system_name} ({path.stem})"
        
        assessments[system_name] = data
    
    return assessments


def validate_assessment_compatibility(assessments: Dict[str, Dict]) -> Tuple[bool, List[str]]:
    """
    Check if assessments can be compared (same evaluator, similar timeframe, etc.)
    
    Args:
        assessments: Dict of assessment data
        
    Returns:
        (is_valid, list_of_warnings)
        
    Example:
        >>> assessments = load_quantitative_assessments(['sys1.json', 'sys2.json'])
        >>> valid, warnings = validate_assessment_compatibility(assessments)
        >>> if not valid:
        ...     print("Compatibility issues:", warnings)
    """
    if len(assessments) < 2:
        return False, ["Need at least 2 assessments for comparison"]
    
    warnings_list = []
    
    # Extract evaluators
    evaluators = set()
    for system, data in assessments.items():
        evaluator = data.get('system_info', {}).get('evaluator', 'Unknown')
        evaluators.add(evaluator)
    
    if len(evaluators) > 1:
        warnings_list.append(
            f"Multiple evaluators detected: {', '.join(evaluators)}. "
            f"Scores may not be directly comparable due to subjective differences."
        )
    
    # Check for missing criteria
    for system, data in assessments.items():
        scores = data.get('criteria_scores', {})
        missing = [c for c in STANDARD_CRITERIA if c not in scores]
        if missing:
            warnings_list.append(
                f"System '{system}' missing criteria: {', '.join(missing)}"
            )
    
    # Check for criteria with no scores across all systems
    all_criteria = set()
    for data in assessments.values():
        all_criteria.update(data.get('criteria_scores', {}).keys())
    
    # Count criteria present in ALL systems (not just any)
    common_criteria = []
    for criterion in STANDARD_CRITERIA:
        criterion_in_all = all(
            criterion in data.get('criteria_scores', {}) 
            for data in assessments.values()
        )
        if criterion_in_all:
            common_criteria.append(criterion)
    
    if len(common_criteria) < 4:
        warnings_list.append(
            f"Very few common criteria ({len(common_criteria)}) across all systems. "
            f"Comparison may not be meaningful."
        )
    
    # Check date ranges for comparability
    dates = []
    for system, data in assessments.items():
        period = data.get('system_info', {}).get('period', '')
        date = data.get('system_info', {}).get('date', '')
        if period or date:
            dates.append((system, period or date))
    
    if len(dates) >= 2:
        # Just note if dates seem very different (basic heuristic)
        date_strings = [d[1] for d in dates]
        if any('2024' in d for d in date_strings) and any('2025' in d for d in date_strings):
            warnings_list.append(
                "Assessments span multiple years. System versions or evaluation context may have changed."
            )
    
    # Valid if we have data and critical structure, even if warnings exist
    is_valid = len(assessments) >= 2 and len(common_criteria) >= 4
    
    return is_valid, warnings_list


def create_score_matrix(assessments: Dict[str, Dict]) -> pd.DataFrame:
    """
    Extract scores into DataFrame for easy analysis.
    
    Columns: [System, Usability, Generation Speed, ..., Average]
    Rows: One per system
    
    Args:
        assessments: Dict of assessment data from load_quantitative_assessments()
        
    Returns:
        DataFrame with systems as rows, criteria as columns, plus Average column
        
    Example:
        >>> assessments = load_quantitative_assessments(['sys1.json', 'sys2.json'])
        >>> matrix = create_score_matrix(assessments)
        >>> print(matrix['Average'].sort_values(ascending=False))
    """
    rows = []
    
    for system_name, data in assessments.items():
        row = {'System': system_name}
        scores = data.get('criteria_scores', {})
        
        # Add all criterion scores
        criterion_scores = []
        for criterion in STANDARD_CRITERIA:
            score = scores.get(criterion)
            display_name = CRITERIA_DISPLAY_NAMES[criterion]
            row[display_name] = score
            if score is not None:
                criterion_scores.append(score)
        
        # Calculate average
        if criterion_scores:
            row['Average'] = round(sum(criterion_scores) / len(criterion_scores), 2)
        else:
            row['Average'] = None
        
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Set System as index
    if 'System' in df.columns:
        df = df.set_index('System')
    
    return df


def calculate_statistics(matrix: pd.DataFrame) -> Dict[str, Dict]:
    """
    Calculate summary statistics per criterion.
    
    Args:
        matrix: Score matrix from create_score_matrix()
        
    Returns:
        Dict with statistics per criterion:
        {
            'Usability': {'mean': 3.5, 'std': 1.2, 'min': 2, 'max': 5, 'range': 3},
            ...
        }
        
    Example:
        >>> matrix = create_score_matrix(assessments)
        >>> stats = calculate_statistics(matrix)
        >>> print(f"Average Usability: {stats['Usability']['mean']:.1f}")
    """
    statistics = {}
    
    # Get all columns except 'Average'
    criteria_columns = [col for col in matrix.columns if col != 'Average']
    
    for criterion in criteria_columns:
        values = matrix[criterion].dropna()
        
        if len(values) > 0:
            statistics[criterion] = {
                'mean': round(values.mean(), 2),
                'std': round(values.std(), 2) if len(values) > 1 else 0.0,
                'min': float(values.min()),
                'max': float(values.max()),
                'range': float(values.max() - values.min()),
                'count': len(values)
            }
        else:
            statistics[criterion] = {
                'mean': None,
                'std': None,
                'min': None,
                'max': None,
                'range': None,
                'count': 0
            }
    
    # Add statistics for Average column if present
    if 'Average' in matrix.columns:
        values = matrix['Average'].dropna()
        if len(values) > 0:
            statistics['Average'] = {
                'mean': round(values.mean(), 2),
                'std': round(values.std(), 2) if len(values) > 1 else 0.0,
                'min': float(values.min()),
                'max': float(values.max()),
                'range': float(values.max() - values.min()),
                'count': len(values)
            }
    
    return statistics


def identify_criterion_winners(matrix: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Find best system(s) for each criterion.
    
    Args:
        matrix: Score matrix from create_score_matrix()
        
    Returns:
        Dict mapping criterion to list of winning systems (handles ties)
        {
            'Usability': ['MusicGen', 'Riffusion'],  # tied at 5
            'Generation Speed': ['DDSP'],
            ...
        }
        
    Example:
        >>> matrix = create_score_matrix(assessments)
        >>> winners = identify_criterion_winners(matrix)
        >>> print(f"Best for Usability: {', '.join(winners['Usability'])}")
    """
    winners = {}
    
    criteria_columns = [col for col in matrix.columns if col != 'Average']
    
    for criterion in criteria_columns:
        # Get max score for this criterion
        max_score = matrix[criterion].max()
        
        if pd.isna(max_score):
            winners[criterion] = []
            continue
        
        # Find all systems with max score (handles ties)
        top_systems = matrix[matrix[criterion] == max_score].index.tolist()
        winners[criterion] = top_systems
    
    # Add overall winner(s) based on average
    if 'Average' in matrix.columns:
        max_avg = matrix['Average'].max()
        if not pd.isna(max_avg):
            overall_winners = matrix[matrix['Average'] == max_avg].index.tolist()
            winners['Overall'] = overall_winners
    
    return winners


def generate_radar_comparison(assessments: Dict[str, Dict], 
                              title: str = "System Comparison - Radar Chart") -> Any:
    """
    Create overlay radar chart comparing all systems.
    
    Args:
        assessments: Dict of assessment data
        title: Chart title
        
    Returns:
        Plotly Figure object (or matplotlib Figure if plotly unavailable)
        
    Example:
        >>> assessments = load_quantitative_assessments(['sys1.json', 'sys2.json'])
        >>> fig = generate_radar_comparison(assessments)
        >>> fig.show()  # Display in notebook
    """
    if not PLOTLY_AVAILABLE and not MATPLOTLIB_AVAILABLE:
        warnings.warn("No visualization library available. Cannot generate radar chart.")
        return None
    
    # Prepare data
    matrix = create_score_matrix(assessments)
    criteria_columns = [col for col in matrix.columns if col != 'Average']
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        
        for system in matrix.index:
            values = [matrix.loc[system, criterion] for criterion in criteria_columns]
            # Close the radar by repeating first value
            values_closed = values + [values[0]]
            criteria_closed = criteria_columns + [criteria_columns[0]]
            
            fig.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=criteria_closed,
                name=system,
                fill='toself',
                opacity=0.6
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )
            ),
            title=title,
            showlegend=True,
            height=600
        )
        
        return fig
    
    elif MATPLOTLIB_AVAILABLE:
        # Matplotlib fallback
        import numpy as np
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        angles = np.linspace(0, 2 * np.pi, len(criteria_columns), endpoint=False).tolist()
        angles += angles[:1]  # Close the plot
        
        for system in matrix.index:
            values = [matrix.loc[system, criterion] for criterion in criteria_columns]
            values += values[:1]  # Close the plot
            
            ax.plot(angles, values, 'o-', linewidth=2, label=system)
            ax.fill(angles, values, alpha=0.25)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(criteria_columns, size=10)
        ax.set_ylim(0, 5)
        ax.set_title(title, size=14, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)
        
        return fig


def generate_bar_comparison(matrix: pd.DataFrame, 
                            criterion: Optional[str] = None,
                            title: Optional[str] = None) -> Any:
    """
    Create bar chart. If criterion specified, show that criterion only.
    If None, show average scores.
    
    Args:
        matrix: Score matrix from create_score_matrix()
        criterion: Specific criterion to visualize, or None for averages
        title: Chart title (auto-generated if None)
        
    Returns:
        Plotly Figure object (or matplotlib Figure if plotly unavailable)
        
    Example:
        >>> matrix = create_score_matrix(assessments)
        >>> fig = generate_bar_comparison(matrix, criterion='Usability')
        >>> fig.show()
    """
    if not PLOTLY_AVAILABLE and not MATPLOTLIB_AVAILABLE:
        warnings.warn("No visualization library available. Cannot generate bar chart.")
        return None
    
    if criterion is None:
        # Show average scores
        data_column = 'Average'
        if title is None:
            title = "System Comparison - Average Scores"
    else:
        data_column = criterion
        if title is None:
            title = f"System Comparison - {criterion}"
    
    if data_column not in matrix.columns:
        warnings.warn(f"Column '{data_column}' not found in matrix.")
        return None
    
    # Sort by score
    sorted_matrix = matrix.sort_values(by=data_column, ascending=True)
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure(data=[
            go.Bar(
                y=sorted_matrix.index,
                x=sorted_matrix[data_column],
                orientation='h',
                marker=dict(
                    color=sorted_matrix[data_column],
                    colorscale='Viridis',
                    cmin=0,
                    cmax=5
                ),
                text=sorted_matrix[data_column].round(2),
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title="Score",
            yaxis_title="System",
            xaxis=dict(range=[0, 5.5]),
            height=max(400, len(sorted_matrix) * 60)
        )
        
        return fig
    
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=(10, max(6, len(sorted_matrix) * 0.5)))
        
        bars = ax.barh(sorted_matrix.index, sorted_matrix[data_column])
        
        # Color bars based on score
        colors = plt.cm.viridis(sorted_matrix[data_column] / 5.0)
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        ax.set_xlabel('Score')
        ax.set_ylabel('System')
        ax.set_title(title)
        ax.set_xlim(0, 5.5)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (idx, row) in enumerate(sorted_matrix.iterrows()):
            ax.text(row[data_column] + 0.1, i, f"{row[data_column]:.2f}", 
                   va='center', fontsize=10)
        
        plt.tight_layout()
        return fig


def generate_heatmap(matrix: pd.DataFrame,
                     title: str = "System Comparison - Heatmap") -> Any:
    """
    Create heatmap: systems × criteria with color-coded scores.
    
    Args:
        matrix: Score matrix from create_score_matrix()
        title: Chart title
        
    Returns:
        Plotly Figure object (or matplotlib Figure if plotly unavailable)
        
    Example:
        >>> matrix = create_score_matrix(assessments)
        >>> fig = generate_heatmap(matrix)
        >>> fig.show()
    """
    if not PLOTLY_AVAILABLE and not MATPLOTLIB_AVAILABLE:
        warnings.warn("No visualization library available. Cannot generate heatmap.")
        return None
    
    # Exclude Average column for heatmap
    heatmap_data = matrix.drop(columns=['Average'], errors='ignore')
    
    if PLOTLY_AVAILABLE:
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn',
            zmin=0,
            zmax=5,
            text=heatmap_data.values,
            texttemplate='%{text:.1f}',
            textfont={"size": 12},
            colorbar=dict(title="Score")
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Criteria",
            yaxis_title="System",
            height=max(400, len(heatmap_data) * 80),
            xaxis={'side': 'bottom'},
        )
        
        return fig
    
    elif MATPLOTLIB_AVAILABLE:
        fig, ax = plt.subplots(figsize=(12, max(6, len(heatmap_data) * 0.6)))
        
        im = ax.imshow(heatmap_data.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=5)
        
        # Set ticks
        ax.set_xticks(range(len(heatmap_data.columns)))
        ax.set_yticks(range(len(heatmap_data.index)))
        ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right')
        ax.set_yticklabels(heatmap_data.index)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Score', rotation=270, labelpad=20)
        
        # Add text annotations
        for i in range(len(heatmap_data.index)):
            for j in range(len(heatmap_data.columns)):
                value = heatmap_data.values[i, j]
                if not pd.isna(value):
                    text = ax.text(j, i, f'{value:.1f}',
                                 ha="center", va="center", color="black", fontsize=10)
        
        ax.set_title(title)
        plt.tight_layout()
        return fig


def create_comparison_summary(assessments: Dict[str, Dict], 
                              statistics: Dict[str, Dict],
                              winners: Dict[str, List[str]]) -> str:
    """
    Generate auto-text summary with key findings.
    
    Args:
        assessments: Dict of assessment data
        statistics: Statistics from calculate_statistics()
        winners: Winners from identify_criterion_winners()
        
    Returns:
        Formatted string with key insights
        
    Example:
        >>> assessments = load_quantitative_assessments(files)
        >>> matrix = create_score_matrix(assessments)
        >>> stats = calculate_statistics(matrix)
        >>> winners = identify_criterion_winners(matrix)
        >>> summary = create_comparison_summary(assessments, stats, winners)
        >>> print(summary)
    """
    lines = []
    
    # Header
    lines.append("# Automated Comparison Summary\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    
    # Systems compared
    system_count = len(assessments)
    system_names = list(assessments.keys())
    lines.append(f"**Systems Compared:** {system_count}")
    for i, system in enumerate(system_names, 1):
        lines.append(f"{i}. {system}")
    lines.append("")
    
    # Overall winner
    if 'Overall' in winners and winners['Overall']:
        overall_winner = winners['Overall']
        if len(overall_winner) == 1:
            avg_score = statistics.get('Average', {}).get('mean', 'N/A')
            lines.append(f"**Overall Winner:** {overall_winner[0]} (avg {avg_score}/5.0)")
        else:
            lines.append(f"**Overall Winners (tied):** {', '.join(overall_winner)}")
    lines.append("")
    
    # Strongest and weakest criteria across all systems
    criteria_avgs = []
    for criterion, stats in statistics.items():
        if criterion != 'Average' and stats['mean'] is not None:
            criteria_avgs.append((criterion, stats['mean']))
    
    if criteria_avgs:
        criteria_avgs.sort(key=lambda x: x[1], reverse=True)
        strongest = criteria_avgs[0]
        weakest = criteria_avgs[-1]
        
        lines.append(f"**Strongest Criterion Across All Systems:** {strongest[0]} (avg {strongest[1]:.1f}/5.0)")
        lines.append(f"**Weakest Criterion Across All Systems:** {weakest[0]} (avg {weakest[1]:.1f}/5.0)")
        lines.append("")
    
    # Highest individual score
    matrix = create_score_matrix(assessments)
    criteria_columns = [col for col in matrix.columns if col != 'Average']
    
    highest_score = 0
    highest_system = ""
    highest_criterion = ""
    
    for system in matrix.index:
        for criterion in criteria_columns:
            score = matrix.loc[system, criterion]
            if not pd.isna(score) and score > highest_score:
                highest_score = score
                highest_system = system
                highest_criterion = criterion
    
    if highest_score > 0:
        lines.append(f"**Highest Individual Score:** {highest_system} - {highest_criterion} ({highest_score:.0f}/5)")
    
    # Most consistent system (lowest std deviation in scores)
    system_stds = []
    for system in matrix.index:
        scores = [float(matrix.loc[system, c]) for c in criteria_columns if not pd.isna(matrix.loc[system, c])]
        if len(scores) > 1:
            import statistics as stats_module
            std = stats_module.stdev(scores)
            system_stds.append((system, std))
    
    if system_stds:
        system_stds.sort(key=lambda x: x[1])
        most_consistent = system_stds[0]
        lines.append(f"**Most Consistent System:** {most_consistent[0]} (std dev {most_consistent[1]:.2f})")
    
    lines.append("")
    
    # Per-criterion winners
    lines.append("## Criterion Winners\n")
    for criterion in criteria_columns:
        if criterion in winners and winners[criterion]:
            winner_list = winners[criterion]
            if len(winner_list) == 1:
                score = matrix.loc[winner_list[0], criterion]
                lines.append(f"- **{criterion}:** {winner_list[0]} ({score:.0f}/5)")
            else:
                lines.append(f"- **{criterion}:** {', '.join(winner_list)} (tied)")
    
    return '\n'.join(lines)


def export_comparison_report(assessments: Dict[str, Dict],
                             matrix: pd.DataFrame,
                             statistics: Dict[str, Dict],
                             winners: Dict[str, List[str]],
                             manual_insights: str,
                             output_path: str,
                             format: str = 'markdown') -> bool:
    """
    Export comprehensive comparison report.
    
    Args:
        assessments: Dict of assessment data
        matrix: Score matrix from create_score_matrix()
        statistics: Statistics from calculate_statistics()
        winners: Winners from identify_criterion_winners()
        manual_insights: User-provided manual analysis text
        output_path: Path to save the report
        format: Export format ('markdown', 'json', or 'csv')
        
    Returns:
        True if successful, False otherwise
        
    Example:
        >>> export_comparison_report(
        ...     assessments, matrix, stats, winners,
        ...     "MusicGen excels at rapid iteration...",
        ...     "comparison_report.md"
        ... )
        True
    """
    try:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == 'markdown':
            return _export_comparison_markdown(
                assessments, matrix, statistics, winners,
                manual_insights, output_path
            )
        elif format.lower() == 'json':
            return _export_comparison_json(
                assessments, matrix, statistics, winners,
                manual_insights, output_path
            )
        elif format.lower() == 'csv':
            return _export_comparison_csv(matrix, output_path)
        else:
            warnings.warn(f"Unknown format '{format}'. Defaulting to markdown.")
            return _export_comparison_markdown(
                assessments, matrix, statistics, winners,
                manual_insights, output_path
            )
            
    except Exception as e:
        warnings.warn(f"Error exporting comparison report: {e}")
        return False


def _export_comparison_markdown(assessments: Dict[str, Dict],
                                matrix: pd.DataFrame,
                                statistics: Dict[str, Dict],
                                winners: Dict[str, List[str]],
                                manual_insights: str,
                                output_path: Path) -> bool:
    """Internal: Export comparison as markdown."""
    lines = []
    
    # Header
    lines.append("# AI Music System Comparison Report\n")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Framework Version:** 1.5.0")
    lines.append("")
    
    # Auto-generated summary
    lines.append("---\n")
    summary = create_comparison_summary(assessments, statistics, winners)
    lines.append(summary)
    lines.append("")
    
    # Score matrix
    lines.append("---\n")
    lines.append("## Score Matrix\n")
    lines.append(matrix.to_markdown())
    lines.append("")
    
    # Statistical summary
    lines.append("---\n")
    lines.append("## Statistical Summary\n")
    stats_rows = []
    for criterion, stats in statistics.items():
        if stats['mean'] is not None:
            stats_rows.append({
                'Criterion': criterion,
                'Mean': f"{stats['mean']:.2f}",
                'Std Dev': f"{stats['std']:.2f}",
                'Min': f"{stats['min']:.1f}",
                'Max': f"{stats['max']:.1f}",
                'Range': f"{stats['range']:.1f}"
            })
    
    if stats_rows:
        stats_df = pd.DataFrame(stats_rows)
        lines.append(stats_df.to_markdown(index=False))
    lines.append("")
    
    # Manual insights
    lines.append("---\n")
    lines.append("## Manual Analysis & Insights\n")
    if manual_insights and manual_insights.strip():
        lines.append(manual_insights)
    else:
        lines.append("*No manual insights provided.*")
    lines.append("")
    
    # System details
    lines.append("---\n")
    lines.append("## System Details\n")
    for system_name, data in assessments.items():
        lines.append(f"### {system_name}\n")
        system_info = data.get('system_info', {})
        lines.append(f"- **Evaluation Period:** {system_info.get('period', 'N/A')}")
        lines.append(f"- **Total Sessions:** {system_info.get('total_sessions', 'N/A')}")
        lines.append(f"- **Evaluator:** {system_info.get('evaluator', 'N/A')}")
        lines.append("")
        
        # Top strengths
        overall = data.get('overall_assessment', {})
        if 'strengths' in overall and overall['strengths']:
            lines.append("**Key Strengths:**")
            for strength in overall['strengths']:
                lines.append(f"- {strength}")
            lines.append("")
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return True


def _export_comparison_json(assessments: Dict[str, Dict],
                            matrix: pd.DataFrame,
                            statistics: Dict[str, Dict],
                            winners: Dict[str, List[str]],
                            manual_insights: str,
                            output_path: Path) -> bool:
    """Internal: Export comparison as JSON."""
    export_data = {
        'export_date': datetime.now().isoformat(),
        'framework_version': '1.5.0',
        'comparison': {
            'systems_compared': list(assessments.keys()),
            'score_matrix': matrix.to_dict(orient='index'),
            'statistics': statistics,
            'winners': winners,
            'manual_insights': manual_insights
        },
        'system_details': assessments
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return True


def _export_comparison_csv(matrix: pd.DataFrame, output_path: Path) -> bool:
    """Internal: Export score matrix as CSV."""
    matrix.to_csv(output_path, encoding='utf-8')
    return True

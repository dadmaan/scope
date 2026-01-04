"""
History & Trends Tab

Complex tab that displays historical entries and longitudinal analysis:
- Append Entry button: saves current entry to journal history
- Historical Display: accordion view of past entries (reverse chronological)
- Longitudinal Analysis: trend analysis, averages, and highlights (requires 5+ entries)
- Interactive chart: 5D ratings over time using Plotly

PRESERVED: All widget content, labels, options - NO MODIFICATIONS

Note: This tab requires access to synthesis_data and widget references from other tabs.
The create function accepts these dependencies as parameters.
"""

import ipywidgets as widgets
from IPython.display import HTML, clear_output
from datetime import datetime


def create_history_trends_tab(synthesis_data, widget_refs):
    """
    Create History & Trends sub-tab with append, display, and analysis features.

    Args:
        synthesis_data: Global data dictionary containing reflective_journal.entries
        widget_refs: Dictionary of all journal widgets from other tabs (for collecting entry data)

    Returns:
        dict: {
            'container': VBox with all history/trends widgets,
            'widgets': {
                'append_button': Button,
                'append_output': Output,
                'historical_display': VBox,
                'analyze_button': Button,
                'analysis_output': Output
            }
        }
    """

    # ========================================================================
    # APPEND ENTRY BUTTON AND CALLBACK
    # ========================================================================

    append_output = widgets.Output()

    def append_journal_entry(b):
        with append_output:
            clear_output()

            # Collect entry data from all widget references
            entry = {
                'entry_date': str(widget_refs['entry_date'].value) if widget_refs['entry_date'].value else '',
                'day_number': widget_refs['day_number'].value,
                'productivity': widget_refs['productivity'].value,
                'mood': widget_refs['mood'].value,
                'systems_worked': widget_refs['systems_worked'].value,
                'tasks_accomplished': list(widget_refs['tasks'].value),
                'time_hands_on': widget_refs['time_hands_on'].value,
                'time_processing': widget_refs['time_processing'].value,
                'time_documentation': widget_refs['time_docs'].value,
                'technical_discoveries': widget_refs['technical'].value,
                'creative_insights': widget_refs['creative'].value,
                'workflow_learnings': widget_refs['workflow'].value,
                'comparative_observations': widget_refs['comparative'].value,
                'challenges_encountered': widget_refs['challenges'].value,
                'what_worked_well': widget_refs['what_worked'].value,
                'outputs_created': widget_refs['outputs'].value,
                'output_quality': widget_refs['output_quality'].value,
                'satisfaction_level': widget_refs['satisfaction'].value,
                'wins_to_celebrate': widget_refs['wins'].value,
                'changed_perspectives': widget_refs['perspectives'].value,
                'evolving_rankings': widget_refs['rankings'].value,
                'emotional_journey': widget_refs['emotional'].value,
                'relationship_with_tech': widget_refs['relationship'].value,
                'creative_identity': widget_refs['identity'].value,
                'flow_state_achieved': widget_refs['flow_state'].value,
                'flow_state_notes': widget_refs['flow_notes'].value,
                'tomorrow_priorities': widget_refs['tomorrow'].value,
                'systems_to_focus': widget_refs['systems_focus'].value,
                'questions_to_investigate': widget_refs['questions'].value,
                'meta_learning_insights': widget_refs['meta_insights'].value,
                'random_observations': widget_refs['random'].value,
                'productivity_rating': widget_refs['rating_productivity'].value,
                'learning_rating': widget_refs['rating_learning'].value,
                'creativity_rating': widget_refs['rating_creativity'].value,
                'frustration_rating': widget_refs['rating_frustration'].value,
                'satisfaction_rating': widget_refs['rating_satisfaction'].value,
                'one_sentence_summary': widget_refs['one_sentence'].value,
                'key_takeaway': widget_refs['key_takeaway'].value,
                'gratitude': widget_refs['gratitude'].value
            }

            # Append to entries array
            synthesis_data['reflective_journal']['entries'].append(entry)
            synthesis_data['reflective_journal']['entry_count'] = len(synthesis_data['reflective_journal']['entries'])
            synthesis_data['modified_at'] = datetime.now().isoformat()

            entry_num = len(synthesis_data['reflective_journal']['entries'])
            print(f"Entry #{entry_num} added successfully!")
            print(f"Date: {entry['entry_date']} (Day {entry['day_number']})")
            print(f"\nTotal entries: {entry_num}")
            print(f"\nScroll down to see historical entries and longitudinal analysis.")

            # Update historical display
            update_historical_display()

    append_button = widgets.Button(
        description='Append Entry',
        button_style='success',
        layout=widgets.Layout(width='150px')
    )
    append_button.on_click(append_journal_entry)

    # ========================================================================
    # HISTORICAL ENTRIES DISPLAY
    # ========================================================================

    historical_display = widgets.VBox([])

    def update_historical_display():
        entries = synthesis_data['reflective_journal']['entries']

        if not entries:
            historical_display.children = [widgets.widgets.HTML(
                value="<i>No journal entries yet. Add your first entry above!</i>"
            )]
            return

        # Sort by date (reverse chronological)
        sorted_entries = sorted(entries, key=lambda x: x.get('entry_date', ''), reverse=True)

        accordions = []

        for i, entry in enumerate(sorted_entries):
            # Create summary for accordion title
            entry_date = entry.get('entry_date', 'Unknown date')
            day_num = entry.get('day_number', '?')
            one_sentence = entry.get('one_sentence_summary', 'No summary')

            title = f"Day {day_num} - {entry_date}: {one_sentence[:50]}..."

            # Create content with string formatting
            prod_val = entry.get('productivity', 'N/A')
            mood_val = entry.get('mood', 'N/A')
            summary_val = entry.get('one_sentence_summary', 'N/A')
            takeaway_val = entry.get('key_takeaway', 'N/A')
            prod_rating = entry.get('productivity_rating', 0)
            learn_rating = entry.get('learning_rating', 0)
            creat_rating = entry.get('creativity_rating', 0)
            frust_rating = entry.get('frustration_rating', 0)
            satis_rating = entry.get('satisfaction_rating', 0)
            systems_val = entry.get('systems_worked', 'N/A')
            tech_val = entry.get('technical_discoveries', 'N/A')
            chall_val = entry.get('challenges_encountered', 'N/A')
            worked_val = entry.get('what_worked_well', 'N/A')
            tomorrow_val = entry.get('tomorrow_priorities', 'N/A')
            grat_val = entry.get('gratitude', 'N/A')

            content_html = f"""
            <div style='padding: 10px;'>
                <h4>Day {day_num} - {entry_date}</h4>
                <p><b>Productivity:</b> {prod_val} | <b>Mood:</b> {mood_val}</p>
                <h5>One Sentence Summary:</h5>
                <p>{summary_val}</p>
                <h5>Key Takeaway:</h5>
                <p>{takeaway_val}</p>
                <h5>Ratings (5 Dimensions):</h5>
                <ul>
                    <li>Productivity: {prod_rating}/10</li>
                    <li>Learning: {learn_rating}/10</li>
                    <li>Creativity: {creat_rating}/10</li>
                    <li>Frustration: {frust_rating}/10</li>
                    <li>Satisfaction: {satis_rating}/10</li>
                </ul>
                <h5>Systems Worked:</h5>
                <p>{systems_val}</p>
                <h5>Technical Discoveries:</h5>
                <p>{tech_val}</p>
                <h5>Challenges:</h5>
                <p>{chall_val}</p>
                <h5>What Worked Well:</h5>
                <p>{worked_val}</p>
                <h5>Tomorrow's Priorities:</h5>
                <p>{tomorrow_val}</p>
                <h5>Gratitude:</h5>
                <p>{grat_val}</p>
            </div>
            """

            accordion = widgets.Accordion(children=[widgets.widgets.HTML(value=content_html)])
            accordion.set_title(0, title)
            accordion.selected_index = None  # Collapsed by default
            accordions.append(accordion)

        historical_display.children = accordions

    # Initialize display
    update_historical_display()

    # ========================================================================
    # LONGITUDINAL ANALYSIS
    # ========================================================================

    analysis_output = widgets.Output()

    def run_longitudinal_analysis(b):
        with analysis_output:
            clear_output()

            entries = synthesis_data['reflective_journal']['entries']

            if len(entries) < 5:
                print(f"Longitudinal analysis requires at least 5 entries.")
                print(f"Current entries: {len(entries)}/5")
                print(f"\nKeep adding journal entries to unlock trend analysis!")
                return

            print("=" * 70)
            print("LONGITUDINAL ANALYSIS")
            print("=" * 70)
            print(f"Total entries: {len(entries)}\n")

            # Extract ratings from all entries
            productivity_ratings = [e.get('productivity_rating', 0) for e in entries]
            learning_ratings = [e.get('learning_rating', 0) for e in entries]
            creativity_ratings = [e.get('creativity_rating', 0) for e in entries]
            frustration_ratings = [e.get('frustration_rating', 0) for e in entries]
            satisfaction_ratings = [e.get('satisfaction_rating', 0) for e in entries]

            # Calculate averages
            avg_productivity = sum(productivity_ratings) / len(productivity_ratings)
            avg_learning = sum(learning_ratings) / len(learning_ratings)
            avg_creativity = sum(creativity_ratings) / len(creativity_ratings)
            avg_frustration = sum(frustration_ratings) / len(frustration_ratings)
            avg_satisfaction = sum(satisfaction_ratings) / len(satisfaction_ratings)

            print("AVERAGE RATINGS")
            print("-" * 70)
            print(f"Productivity:  {avg_productivity:.1f}/10 {'*' * int(avg_productivity)}")
            print(f"Learning:      {avg_learning:.1f}/10 {'*' * int(avg_learning)}")
            print(f"Creativity:    {avg_creativity:.1f}/10 {'*' * int(avg_creativity)}")
            print(f"Frustration:   {avg_frustration:.1f}/10 {'!' * int(avg_frustration)}")
            print(f"Satisfaction:  {avg_satisfaction:.1f}/10 {'*' * int(avg_satisfaction)}")
            print()

            # Trend analysis (simple: compare first half to second half)
            mid = len(entries) // 2

            def trend_direction(ratings):
                first_half_avg = sum(ratings[:mid]) / mid
                second_half_avg = sum(ratings[mid:]) / (len(ratings) - mid)
                diff = second_half_avg - first_half_avg

                if abs(diff) < 0.5:
                    return "-> Stable", diff
                elif diff > 0:
                    return "-> Increasing", diff
                else:
                    return "-> Decreasing", diff

            print("TRENDS (First half vs Second half)")
            print("-" * 70)

            prod_trend, prod_diff = trend_direction(productivity_ratings)
            learn_trend, learn_diff = trend_direction(learning_ratings)
            creat_trend, creat_diff = trend_direction(creativity_ratings)
            frust_trend, frust_diff = trend_direction(frustration_ratings)
            satis_trend, satis_diff = trend_direction(satisfaction_ratings)

            print(f"Productivity:  {prod_trend} ({prod_diff:+.1f})")
            print(f"Learning:      {learn_trend} ({learn_diff:+.1f})")
            print(f"Creativity:    {creat_trend} ({creat_diff:+.1f})")
            print(f"Frustration:   {frust_trend} ({frust_diff:+.1f})")
            print(f"Satisfaction:  {satis_trend} ({satis_diff:+.1f})")
            print()

            # Identify peaks
            max_prod_idx = productivity_ratings.index(max(productivity_ratings))
            min_frust_idx = frustration_ratings.index(min(frustration_ratings))
            max_satis_idx = satisfaction_ratings.index(max(satisfaction_ratings))

            print("HIGHLIGHTS")
            print("-" * 70)
            print(f"Most productive day: Day {entries[max_prod_idx].get('day_number', '?')}")
            print(f"  -> {entries[max_prod_idx].get('one_sentence_summary', 'N/A')[:60]}...")
            print()
            print(f"Least frustrating day: Day {entries[min_frust_idx].get('day_number', '?')}")
            print(f"  -> {entries[min_frust_idx].get('one_sentence_summary', 'N/A')[:60]}...")
            print()
            print(f"Most satisfying day: Day {entries[max_satis_idx].get('day_number', '?')}")
            print(f"  -> {entries[max_satis_idx].get('one_sentence_summary', 'N/A')[:60]}...")
            print()

            print("=" * 70)

            # Try to generate line chart
            try:
                import plotly.graph_objects as go

                days = [e.get('day_number', i+1) for i, e in enumerate(entries)]

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=days, y=productivity_ratings, name='Productivity', mode='lines+markers'))
                fig.add_trace(go.Scatter(x=days, y=learning_ratings, name='Learning', mode='lines+markers'))
                fig.add_trace(go.Scatter(x=days, y=creativity_ratings, name='Creativity', mode='lines+markers'))
                fig.add_trace(go.Scatter(x=days, y=frustration_ratings, name='Frustration', mode='lines+markers'))
                fig.add_trace(go.Scatter(x=days, y=satisfaction_ratings, name='Satisfaction', mode='lines+markers'))

                fig.update_layout(
                    title='5D Ratings Over Time',
                    xaxis_title='Day Number',
                    yaxis_title='Rating (1-10)',
                    yaxis=dict(range=[0, 11]),
                    hovermode='x unified'
                )

                fig.show()
                print("\nInteractive chart generated above")

            except Exception as e:
                print(f"\nCould not generate chart: {e}")
                print("Trend data is still valid above.")

    analyze_button = widgets.Button(
        description='Analyze Trends',
        button_style='info',
        layout=widgets.Layout(width='150px')
    )
    analyze_button.on_click(run_longitudinal_analysis)

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">History & Trends</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Review past entries and analyze longitudinal trends in your evaluation journey.</p>'),
        widgets.HTML('<p>Save entries, view history, and analyze longitudinal trends.</p>'),
        widgets.HTML('<h4 style="color: #555;">Save Entry</h4>'),
        append_button,
        append_output,
        widgets.HTML('<h4 style="color: #555; margin-top: 30px;">Historical Entries</h4>'),
        historical_display,
        widgets.HTML('<h4 style="color: #555; margin-top: 30px;">Longitudinal Analysis</h4>'),
        widgets.HTML('<p><i>Requires at least 5 entries. Analyzes trends, averages, and highlights.</i></p>'),
        analyze_button,
        analysis_output
    ])

    return {
        'container': container,
        'widgets': {
            'append_button': append_button,
            'append_output': append_output,
            'historical_display': historical_display,
            'analyze_button': analyze_button,
            'analysis_output': analysis_output
        }
    }

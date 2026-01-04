import plotly.graph_objects as go

categories = ['Usability', 'Generation\nSpeed', 'Audio\nQuality', 'Semantic\nAlignment',
              'Parameter\nControl', 'Content\nControl', 'Production\nEnvironment\nIntegration', 'Creative\nWorkflow\nFit']

musicgen = [3, 2, 3, 3, 3, 2, 1, 2]
riffusion = [3, 4, 3, 3, 3, 3, 1, 3]
magenta_studio = [3, 4, 0, 2, 2, 1, 3, 1]  # 0 for N/A Audio Quality
ddsp_vst = [4, 5, 4, 4, 4, 4, 3, 4]

systems = [
    ('MusicGen', musicgen, 'blue'),
    ('Riffusion', riffusion, 'orange'),
    ('Magenta Studio 2.0', magenta_studio, 'green'),
    ('DDSP-VST', ddsp_vst, 'red')
]

fig = go.Figure()

for name, scores, color in systems:
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        name=name,
        line=dict(color=color, width=3, dash='dash' if name == 'Magenta Studio 2.0' else 'solid'),
        marker=dict(size=8),
        fill='toself',
        opacity=0.3 if name == 'Magenta Studio 2.0' else 0.5
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5],
            tickvals=[1, 2, 3, 4, 5],
            tickfont=dict(size=18)
        ),
        angularaxis=dict(
            tickfont=dict(size=24)
        )
    ),
    showlegend=True,
    legend=dict(font=dict(size=24), x=0.5, y=-0.15, xanchor='center', yanchor='top', orientation="h"),
    # title=dict(text='System Performance Comparison Across Evaluation Criteria', x=0.5, y=1.0, xanchor='center', yanchor='top'),
    margin=dict(l=40, r=40, t=80, b=100),
    # width=900,
    # height=900
)

# any comments, leave it down there
# fig.add_annotation(
#     text="Note: Magenta Studio 2.0 Audio Quality not applicable (MIDI output)",
#     xref="paper", yref="paper",
#     x=0.5, y=0, showarrow=False,
#     font=dict(size=11, color="gray", style="italic")
# )

fig.write_html("performance_radar_chart_plotly.html")
print("Radar chart saved as 'performance_radar_chart_plotly.html'")

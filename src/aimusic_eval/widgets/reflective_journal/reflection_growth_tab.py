"""
Reflection & Growth Tab

Groups journal sections for evolution and autoethnographic reflection:
- Perspective shifts: changes in thinking throughout the day
- System rankings: evolving opinions about systems
- Emotional journey: emotional arc throughout the day
- Relationship with tech: feelings about AI systems (trust, frustration, partnership)
- Creative identity: effects on self-perception as producer/creator
- Flow state: whether flow was achieved and details

PRESERVED: All widget content, labels, options - NO MODIFICATIONS
"""

import ipywidgets as widgets
from IPython.display import HTML


def create_reflection_growth_tab():
    """
    Create Reflection & Growth sub-tab combining evolution and autoethnographic sections.

    Returns:
        dict: {
            'container': VBox with all reflection/growth widgets,
            'widgets': {
                'perspectives': Textarea,
                'rankings': Textarea,
                'emotional': Textarea,
                'relationship': Textarea,
                'identity': Textarea,
                'flow_state': Dropdown,
                'flow_notes': Textarea
            }
        }
    """

    # ========================================================================
    # EVOLUTION
    # ========================================================================

    journal_perspectives = widgets.Textarea(
        description='Perspective Shift:',
        placeholder='What did you think at start of day vs. now? What caused this shift?',
        layout=widgets.Layout(width='700px', height='120px'),
        style={'description_width': 'initial'}
    )

    journal_rankings = widgets.Textarea(
        description='System Rankings:',
        placeholder='Are your opinions about any systems changing? Why?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # AUTOETHNOGRAPHIC
    # ========================================================================

    journal_emotional = widgets.Textarea(
        description='Emotional Arc:',
        placeholder='Describe your emotional journey throughout the day...',
        layout=widgets.Layout(width='700px', height='120px'),
        style={'description_width': 'initial'}
    )

    journal_relationship = widgets.Textarea(
        description='Tech Relationship:',
        placeholder='How did you feel about the AI systems? Trust? Frustration? Partnership?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_identity = widgets.Textarea(
        description='Creative Identity:',
        placeholder='Did today affect how you see yourself as a music producer/creator?',
        layout=widgets.Layout(width='700px', height='100px'),
        style={'description_width': 'initial'}
    )

    journal_flow_state = widgets.Dropdown(
        options=['Yes, sustained', 'Yes, briefly', 'No'],
        description='Flow state:',
        value='No',
        style={'description_width': 'initial'}
    )

    journal_flow_notes = widgets.Textarea(
        description='Flow details:',
        placeholder='When/with what system? What enabled or prevented flow?',
        layout=widgets.Layout(width='700px', height='80px'),
        style={'description_width': 'initial'}
    )

    # ========================================================================
    # CONTAINER
    # ========================================================================

    container = widgets.VBox([
        widgets.HTML('<h3 style="color: #00796B; border-bottom: 2px solid #00796B; padding-bottom: 10px;">Reflection & Growth</h3>'),
        widgets.HTML('<p style="color: #777; font-size: 14px;">Reflect on skill evolution, personal observations, and creative flow experiences.</p>'),
        widgets.HTML('<p>Explore perspective shifts, emotional journey, and creative identity.</p>'),
        widgets.HTML('<h4 style="color: #555;">Evolution</h4>'),
        journal_perspectives,
        journal_rankings,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Autoethnographic Reflection</h4>'),
        journal_emotional,
        journal_relationship,
        journal_identity,
        widgets.HTML('<h4 style="color: #555; margin-top: 20px;">Flow State</h4>'),
        journal_flow_state,
        journal_flow_notes
    ])

    return {
        'container': container,
        'widgets': {
            'perspectives': journal_perspectives,
            'rankings': journal_rankings,
            'emotional': journal_emotional,
            'relationship': journal_relationship,
            'identity': journal_identity,
            'flow_state': journal_flow_state,
            'flow_notes': journal_flow_notes
        }
    }

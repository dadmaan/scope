# Option A: Modernize Existing Voila + ipywidgets Stack

## Summary

Keep the current architecture and heavily improve UX through design-system, flow, and operability upgrades.

## Why This Option

- Lowest migration risk.
- Reuses existing widget modules and data model.
- Fastest path to improved experience for non-technical users.

## Technical Direction

1. **Create a shared UI layer**
   - Centralize style tokens (colors, spacing, typography, status states).
   - Remove notebook-level duplicated inline CSS and replace with reusable style utilities/template assets.

2. **Move from tab-heavy IA to guided workflow**
   - Introduce stepper/wizard structure per phase (Setup → Work → Review → Export).
   - Keep advanced sections collapsed by default (progressive disclosure).

3. **Add persistent global shell**
   - Sticky top bar with current phase, completion %, save status, and primary actions.
   - Add breadcrumb and “next recommended action” hint.

4. **Improve form usability**
   - Split long sections into short task blocks.
   - Add inline validation and helper text near fields.
   - Introduce smart defaults and templates for common systems/sessions.

5. **Strengthen resilience**
   - Autosave with explicit restore banner on reload.
   - Draft/unsaved indicators and conflict-safe save semantics.

6. **Voila productization**
   - Build a custom Voila template for branding and layout consistency.
   - Launch Voila as default Docker app entrypoint.

## UX Outcomes Expected

- Lower onboarding time.
- Fewer abandoned sessions.
- Reduced navigation confusion.
- Higher completion rate per phase.

## Critical Considerations

- ipywidgets still limits modern web interactions compared to app-native frameworks.
- Complex responsiveness/mobile polish remains challenging.
- Must enforce strict UI conventions to prevent style regressions.

## Best Fit

Choose this if you want a meaningful UX uplift quickly with minimal rewrite.

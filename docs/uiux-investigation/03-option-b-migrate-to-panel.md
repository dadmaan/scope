# Option B: Migrate to Panel (Python-First App UI)

## Summary

Rebuild notebook workflows as a structured Panel app while staying Python-centric and Docker-friendly.

## Why This Option

- Better app-like UX primitives than raw notebook+widgets.
- Keeps development primarily in Python.
- Strong fit for data applications and multi-page dashboards.

## Technical Direction

1. **Architecture**
   - Convert each notebook phase into a routed Panel page.
   - Shared state service for session context, progress, and autosave.
   - Service layer reusing existing `aimusic_eval.core` and validation/export logic.

2. **UI Composition**
   - Use templates (`FastListTemplate`/custom template) for consistent shell.
   - Replace deep tab nesting with sidebar navigation + section cards.
   - Build reusable components for form blocks, evidence attachments, and score cards.

3. **Data & Compatibility**
   - Keep existing JSON schema and export formats unchanged.
   - Add migration adapters only if field names evolve.

4. **Deployment**
   - Ship as single container with Panel server startup command.
   - Optional reverse proxy for auth, SSL, and path routing.

## UX Outcomes Expected

- More modern and coherent app experience.
- Better maintainability of layout and theming.
- Easier responsive behavior than notebook-driven rendering.

## Critical Considerations

- Moderate migration effort from current ipywidgets code.
- Team must learn Panel component/event model.
- Some advanced custom UX may still require front-end customization.

## Best Fit

Choose this if you want a large UX improvement but still want to stay almost entirely in Python.

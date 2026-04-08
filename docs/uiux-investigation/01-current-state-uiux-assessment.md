# SCOPE UI/UX Current-State Technical Assessment

## 1) Context and Scope

This assessment focuses on the three workflow notebooks in `notebooks/` and their Voila-based delivery model for non-technical users.

## 2) What Exists Today

- Delivery model: Jupyter notebooks rendered with Voila (`notebooks/voila.json`).
- UI toolkit: `ipywidgets` assembled by Python factory functions in `src/aimusic_eval/widgets/`.
- Interaction model: multiple levels of `Tab` navigation and large forms.
- Architecture scale: widget docs describe ~149 widgets, 3 master tabs, and 16 nested sub-tabs.
- Deployment model: Dockerized Jupyter environment (`docker/`) for out-of-the-box execution.

## 3) Strengths

- Mature modular widget architecture (clear package breakdown, reusable factories).
- Strong data-capture focus and export/validation structure already in place.
- Good fit for researchers already comfortable with notebooks.
- Low rewrite cost for incremental improvements.

## 4) Core UX Risks (for Non-Technical Users)

1. **Cognitive overload**  
   Form density is very high; users must navigate many tabs and fields before feeling progress.

2. **Deep navigation hierarchy**  
   Nested tabs increase orientation loss and “where am I?” friction.

3. **Notebook-style mental model leakage**  
   Even under Voila, interaction still reflects notebook-era layout conventions rather than modern product UX.

4. **Inconsistent visual system**  
   Styling is mostly inline CSS in notebooks; this makes design consistency and long-term UX iteration difficult.

5. **Validation timing is late**  
   Completeness checks are mostly end-of-flow; users can discover major issues too late.

6. **Potential accessibility gaps**  
   Color-dependent cues and dense tab patterns can challenge keyboard/screen-reader use.

7. **Operational ergonomics mismatch**  
   Docker currently starts notebook tooling by default; Voila-first entry is not yet the primary “one-click app” mental model.

## 5) Product Constraints That Must Be Preserved

- Must remain **out-of-the-box** for non-technical users.
- Must remain **cross-system** via Docker.
- Must preserve existing evaluation methodology and data schema across all three phases.
- Must keep exportability and reproducibility of assessment artifacts.

## 6) Decision Implication

You should choose between:

- **Evolution path**: keep Voila/ipywidgets and productize UX aggressively.
- **Migration path**: move to an app framework with stronger modern UX primitives while preserving data contracts.

Both are viable; the right choice depends on acceptable rewrite cost vs long-term UX ambition.

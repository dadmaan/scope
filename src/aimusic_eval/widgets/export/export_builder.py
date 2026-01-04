"""
Export Builder Module

Builds the complete session data structure from widget values for JSON export.
"""

import logging
from datetime import datetime

# Import get_safe_value from core utilities
from aimusic_eval.core import get_safe_value

# Configure module logger
logger = logging.getLogger(__name__)


def build_session_data(all_widgets, generation_attempts):
    """
    Build complete session data dictionary from widget values.
    
    Args:
        all_widgets (dict): Organized widget references
        generation_attempts (list): List of generation attempts
    
    Returns:
        dict: Complete session data structure ready for JSON export
    """
    try:
        # Get widget shortcuts
        cs = all_widgets.get('core_session', {})
        setup_w = cs.get('setup', {})
        gen_w = cs.get('generation', {})
        ref_w = cs.get('refinement', {})
        pp_w = cs.get('post_processing', {})
        daw_w = cs.get('daw_integration', {})
        
        # Handle both old 'reflections_stats' and new split names
        rs_w = cs.get('reflections_stats', cs.get('reflections', {}))
        stats_w = cs.get('session_statistics', rs_w)
        
        ci = all_widgets.get('critical_incident', {})
        c_w = ci.get('classification', {})
        ctx_w = ci.get('context', {})
        learn_w = ci.get('learnings', {})
        doc_w = ci.get('documentation', {})
        
        wp = all_widgets.get('workflow_phase', {})
        wf_setup = wp.get('setup', {})
        wf_exec = wp.get('execution', {})
        wf_spec = wp.get('phase_specific', {})
        wf_out = wp.get('outcome', {})
        wf_exp = wp.get('experience', {})
        
        # Build session data structure
        session_data = {
            "template_metadata": {
                "template_type": "session_notebook",
                "template_version": "2.0.0",
                "created_at": datetime.now().isoformat(),
                "exported_at": None
            },
            "core_session": {
                "metadata": {
                    "session_id": f"session_{get_safe_value(setup_w, 'system_name', 'unnamed').lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "date": str(get_safe_value(setup_w, 'session_date', '')),
                    "start_time": get_safe_value(setup_w, 'session_start_time', ''),
                    "end_time": get_safe_value(setup_w, 'session_end_time', ''),
                    "system_name": get_safe_value(setup_w, 'system_name', ''),
                    "system_version": get_safe_value(setup_w, 'system_version', ''),
                    "interface_type": get_safe_value(setup_w, 'interface_type', ''),
                    "hardware": get_safe_value(setup_w, 'hardware', ''),
                    "evaluator": get_safe_value(setup_w, 'evaluator_name', ''),
                    "session_number": get_safe_value(setup_w, 'session_number', 1),
                    "session_type": get_safe_value(setup_w, 'session_type', '')
                },
                "creative_context": {
                    "musical_element": get_safe_value(setup_w, 'musical_element', ''),
                    "genre": get_safe_value(setup_w, 'genre', ''),
                    "tempo": get_safe_value(setup_w, 'tempo', ''),
                    "key": get_safe_value(setup_w, 'key', ''),
                    "intended_use": get_safe_value(setup_w, 'intended_use', ''),
                    "references": get_safe_value(setup_w, 'references', '')
                },
                "generation_attempts": generation_attempts,
                "prompt_refinement": {
                    "initial": get_safe_value(ref_w, 'initial_prompt', ''),
                    "final": get_safe_value(ref_w, 'final_prompt', ''),
                    "iterations": get_safe_value(ref_w, 'iterations', ''),
                    "responds_well": get_safe_value(ref_w, 'responds_well', ''),
                    "struggles_with": get_safe_value(ref_w, 'struggles_with', ''),
                    "unexpected": get_safe_value(ref_w, 'unexpected', ''),
                    "effective_keywords": get_safe_value(ref_w, 'effective_keywords', ''),
                    "ineffective_keywords": get_safe_value(ref_w, 'ineffective_keywords', '')
                },
                "post_processing": {
                    "separation": {
                        "needed": get_safe_value(pp_w, 'separation_needed', ''),
                        "tool": get_safe_value(pp_w, 'separation_tool', ''),
                        "quality": get_safe_value(pp_w, 'separation_quality', '')
                    },
                    "eq": {
                        "applied": get_safe_value(pp_w, 'eq_applied', False),
                        "details": get_safe_value(pp_w, 'eq_details', '')
                    },
                    "compression": {
                        "applied": get_safe_value(pp_w, 'compression_applied', False),
                        "details": get_safe_value(pp_w, 'compression_details', '')
                    },
                    "reverb": {
                        "applied": get_safe_value(pp_w, 'reverb_applied', False),
                        "details": get_safe_value(pp_w, 'reverb_details', '')
                    },
                    "trimming": {
                        "applied": get_safe_value(pp_w, 'trimming_applied', False),
                        "details": get_safe_value(pp_w, 'trimming_details', '')
                    },
                    "other": get_safe_value(pp_w, 'other_processing', ''),
                    "total_time": get_safe_value(pp_w, 'processing_total_time', '')
                },
                "daw_integration": {
                    "daw": get_safe_value(daw_w, 'daw', ''),
                    "format": get_safe_value(daw_w, 'file_format', ''),
                    "sample_rate": get_safe_value(daw_w, 'sample_rate', ''),
                    "context": get_safe_value(daw_w, 'daw_context', ''),
                    "issues": list(get_safe_value(daw_w, 'daw_issues', [])),
                    "workarounds": get_safe_value(daw_w, 'workarounds', ''),
                    "ease": get_safe_value(daw_w, 'integration_ease', ''),
                    "time": get_safe_value(daw_w, 'integration_time', ''),
                    "result": get_safe_value(daw_w, 'integration_result', '')
                },
                "reflections": {
                    "what_worked": get_safe_value(rs_w, 'what_worked', ''),
                    "frustrations": get_safe_value(rs_w, 'frustrations', ''),
                    "discoveries": get_safe_value(rs_w, 'discoveries', ''),
                    "comparisons": get_safe_value(rs_w, 'comparisons', ''),
                    "emotional_state": get_safe_value(rs_w, 'emotional_state', '')
                },
                "session_stats": {
                    "total_attempts": len(generation_attempts),
                    "usable_outputs": get_safe_value(stats_w, 'usable_outputs', 0),
                    "generation_time": get_safe_value(stats_w, 'total_generation_time', ''),
                    "processing_time": get_safe_value(stats_w, 'total_processing_time', ''),
                    "integration_time": get_safe_value(stats_w, 'total_integration_time', ''),
                    "productivity": get_safe_value(stats_w, 'productivity', ''),
                    "efficiency": get_safe_value(stats_w, 'efficiency', '')
                }
            },
            "optional_incident": {
                "logged": get_safe_value(c_w, 'incident_logged', False),
                "metadata": {
                    "date": str(get_safe_value(c_w, 'incident_date', '')),
                    "time": get_safe_value(c_w, 'incident_time', '')
                },
                "classification": {
                    "type": get_safe_value(c_w, 'incident_type', ''),
                    "severity": get_safe_value(c_w, 'incident_severity', '')
                },
                "description": {
                    "what_happened": get_safe_value(c_w, 'what_happened', ''),
                    "goal": get_safe_value(c_w, 'incident_goal', ''),
                    "expected": get_safe_value(c_w, 'expected_outcome', ''),
                    "actual": get_safe_value(c_w, 'actual_outcome', ''),
                    "why_notable": get_safe_value(c_w, 'why_notable', '')
                },
                "context": {
                    "prior_actions": get_safe_value(ctx_w, 'prior_actions', ''),
                    "system_state": get_safe_value(ctx_w, 'system_state', '')
                },
                "autoethnography": {
                    "time_of_day": get_safe_value(ctx_w, 'time_of_day', ''),
                    "fatigue_level": get_safe_value(ctx_w, 'fatigue_level', ''),
                    "emotional_state": get_safe_value(ctx_w, 'incident_emotional_state', ''),
                    "external_pressures": get_safe_value(ctx_w, 'external_pressures', '')
                },
                "analysis": {
                    "significance": get_safe_value(ctx_w, 'significance', ''),
                    "affected_criteria": list(get_safe_value(ctx_w, 'affected_criteria', [])),
                    "theoretical_insights": get_safe_value(ctx_w, 'theoretical_insights', ''),
                    "workflow_impact": get_safe_value(ctx_w, 'workflow_impact', '')
                },
                "root_cause": {
                    "probable_causes": list(get_safe_value(learn_w, 'probable_causes', [])),
                    "evidence": get_safe_value(learn_w, 'evidence', ''),
                    "alternatives": get_safe_value(learn_w, 'alternatives', '')
                },
                "learnings": {
                    "system": get_safe_value(learn_w, 'learning_system', ''),
                    "evaluation": get_safe_value(learn_w, 'learning_evaluation', ''),
                    "practice": get_safe_value(learn_w, 'learning_practice', ''),
                    "approach_changes": get_safe_value(learn_w, 'approach_changes', ''),
                    "recommendations": get_safe_value(learn_w, 'recommendations', '')
                },
                "reproducibility": {
                    "level": get_safe_value(doc_w, 'reproducibility_level', ''),
                    "steps": get_safe_value(doc_w, 'reproduction_steps', ''),
                    "conditions": get_safe_value(doc_w, 'reproduction_conditions', ''),
                    "attempts": get_safe_value(doc_w, 'reproduction_attempts', 0),
                    "success_rate": get_safe_value(doc_w, 'success_rate', '')
                },
                "documentation": {
                    "evidence_types": list(get_safe_value(doc_w, 'evidence_types', [])),
                    "location": get_safe_value(doc_w, 'evidence_location', ''),
                    "related": get_safe_value(doc_w, 'related_incidents', ''),
                    "follow_up": get_safe_value(doc_w, 'follow_up', '')
                }
            },
            "optional_workflow_phase": {
                "enabled": True,
                "metadata": {
                    "phase_type": get_safe_value(wf_setup, 'phase_type', ''),
                    "start_time": get_safe_value(wf_setup, 'phase_start_time', ''),
                    "end_time": get_safe_value(wf_setup, 'phase_end_time', ''),
                    "systems_used": get_safe_value(wf_setup, 'systems_used', '').split('\n') if get_safe_value(wf_setup, 'systems_used', '') else []
                },
                "pre_phase": {
                    "goal": get_safe_value(wf_setup, 'phase_goal', ''),
                    "materials": get_safe_value(wf_setup, 'phase_materials', ''),
                    "vision": get_safe_value(wf_setup, 'phase_vision', ''),
                    "expected_challenges": get_safe_value(wf_setup, 'phase_expected_challenges', ''),
                    "time_estimate": get_safe_value(wf_setup, 'time_estimate', 0)
                },
                "execution_log": get_safe_value(wf_exec, 'execution_log', ''),
                "system_performance": get_safe_value(wf_exec, 'system_performance', ''),
                "efficiency": {
                    "time_planned": get_safe_value(wf_out, 'eff_time_planned', 0),
                    "time_actual": get_safe_value(wf_out, 'eff_time_actual', 0),
                    "breakdown": get_safe_value(wf_out, 'eff_breakdown', ''),
                    "bottlenecks": get_safe_value(wf_out, 'eff_bottlenecks', ''),
                    "rating": get_safe_value(wf_out, 'eff_rating', '')
                },
                "outcome": {
                    "goals_achievement": get_safe_value(wf_out, 'outcome_goals', ''),
                    "quality": get_safe_value(wf_out, 'outcome_quality', ''),
                    "usable_outputs": get_safe_value(wf_out, 'outcome_usable', ''),
                    "surprises": get_safe_value(wf_out, 'outcome_surprises', ''),
                    "next_phase_impact": get_safe_value(wf_out, 'outcome_next_phase', '')
                },
                "criterion_bridge": {
                    "connections": get_safe_value(wf_out, 'criterion_connections', ''),
                    "evidence": get_safe_value(wf_out, 'criterion_evidence', '')
                },
                "creative_experience": {
                    "flow_state": get_safe_value(wf_exp, 'exp_flow_state', ''),
                    "satisfaction": get_safe_value(wf_exp, 'exp_satisfaction', 0),
                    "reflection": get_safe_value(wf_exp, 'exp_reflection', ''),
                    "would_repeat": get_safe_value(wf_exp, 'exp_would_repeat', '')
                }
            }
        }
        
        # Add phase-specific data if available
        phase_type = get_safe_value(wf_setup, 'phase_type', '')
        
        if phase_type == 'Content Generation':
            gen = wf_spec.get('generation', {})
            session_data["optional_workflow_phase"]["generation"] = {
                "approach": get_safe_value(gen, 'gen_approach', ''),
                "prompts": get_safe_value(gen, 'gen_prompts', ''),
                "iterations": get_safe_value(gen, 'gen_iterations', 0),
                "output": get_safe_value(gen, 'gen_output', '')
            }
        elif phase_type == 'Curation':
            cur = wf_spec.get('curation', {})
            session_data["optional_workflow_phase"]["curation"] = {
                "candidates_reviewed": get_safe_value(cur, 'cur_candidates_reviewed', 0),
                "candidates_selected": get_safe_value(cur, 'cur_candidates_selected', 0),
                "criteria": get_safe_value(cur, 'cur_criteria', ''),
                "notes": get_safe_value(cur, 'cur_notes', '')
            }
        elif phase_type == 'Integration':
            integ = wf_spec.get('integration', {})
            session_data["optional_workflow_phase"]["integration"] = {
                "activities": list(get_safe_value(integ, 'int_activities', [])),
                "challenges": get_safe_value(integ, 'int_challenges', ''),
                "success": get_safe_value(integ, 'int_success', '')
            }
        elif phase_type == 'Post-Production':
            pp = wf_spec.get('post_production', {})
            session_data["optional_workflow_phase"]["post_production"] = {
                "activities": list(get_safe_value(pp, 'pp_activities', [])),
                "ai_percentage": get_safe_value(pp, 'pp_ai_percentage', 0),
                "modifications": get_safe_value(pp, 'pp_modifications', ''),
                "quality": get_safe_value(pp, 'pp_quality', '')
            }
        
        return session_data
        
    except Exception as e:
        logger.error(f"Error building session data: {e}")
        raise

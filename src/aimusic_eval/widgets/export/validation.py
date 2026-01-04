"""
Validation Module

Provides session data validation and completeness checking functionality.
"""

import logging

# Configure module logger
logger = logging.getLogger(__name__)


def validate_session_completeness(all_widgets, generation_attempts):
    """
    Validate session data and display completeness statistics.
    
    Args:
        all_widgets (dict): Dictionary containing all widget sections
        generation_attempts (list): List of generation attempts
        
    Returns:
        dict: Validation results with completeness percentage and field counts
    """
    
    def count_filled_widgets(widgets_dict):
        """
        Count filled widget values recursively.
        
        Args:
            widgets_dict: Dictionary of widgets to count
            
        Returns:
            tuple: (filled_count, total_count)
        """
        filled = 0
        total = 0
        
        def traverse(obj):
            nonlocal filled, total
            if isinstance(obj, dict):
                for key, value in obj.items():
                    # Skip metadata fields
                    if key in ['container', 'widgets']:
                        traverse(value)
                    elif isinstance(value, dict):
                        traverse(value)
                    elif hasattr(value, 'value'):
                        # It's a widget
                        total += 1
                        widget_value = value.value
                        if isinstance(widget_value, str):
                            if widget_value.strip():
                                filled += 1
                        elif isinstance(widget_value, (list, tuple)):
                            if len(widget_value) > 0:
                                filled += 1
                        elif widget_value not in [0, None, False, {}]:
                            filled += 1
        
        traverse(widgets_dict)
        return filled, total
    
    filled, total = count_filled_widgets(all_widgets)
    completeness = (filled / total * 100) if total > 0 else 0
    
    logger.info("=" * 60)
    logger.info("📊 SESSION VALIDATION")
    logger.info("=" * 60)
    logger.info(f"📈 Completeness: {completeness:.1f}%")
    logger.info(f"📝 Fields filled: {filled}/{total}")
    logger.info(f"🎵 Generation Attempts: {len(generation_attempts)}")
    
    # Check critical fields
    try:
        system_name_filled = (
            all_widgets['core_session']['setup']['system_name'].value.strip() != ''
        )
        session_date_filled = all_widgets['core_session']['setup']['session_date'].value is not None
        
        if system_name_filled and session_date_filled:
            logger.info("✅ Critical fields present")
        else:
            logger.warning("⚠️ Missing critical fields (system name, date)")
    except (KeyError, AttributeError):
        logger.debug("ℹ️ Could not verify critical fields")
    
    if completeness >= 70:
        logger.info("✅ Ready to export! All critical data present.")
    elif completeness >= 50:
        logger.warning("⚠️ Consider filling more fields before exporting")
    else:
        logger.warning("❌ Please complete more required fields")
    
    logger.info("=" * 60)
    
    return {
        'completeness': completeness,
        'filled': filled,
        'total': total,
        'generation_attempts': len(generation_attempts)
    }

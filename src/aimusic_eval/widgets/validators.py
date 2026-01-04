"""
Validators Module

Provides validation functions for widget values and session data integrity.
This module can be extended to add custom validation rules for specific widgets
or data structures.

Example Usage:
    from validators import validate_time_format, validate_session_completeness
    
    # Validate time input
    is_valid = validate_time_format('14:30')
    
    # Validate required fields
    errors = validate_required_fields(session_data)
"""

import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def validate_time_format(time_str):
    """
    Validate time string in HH:MM format.
    
    Args:
        time_str (str): Time string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not time_str or not isinstance(time_str, str):
        return False
    
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))


def validate_tempo(tempo_str):
    """
    Validate tempo string (BPM values).
    
    Args:
        tempo_str (str): Tempo string (e.g., "120 BPM", "90-130 BPM")
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not tempo_str or not isinstance(tempo_str, str):
        return True  # Empty is ok (optional field)
    
    # Allow formats: "120", "120 BPM", "90-130", "90-130 BPM"
    pattern = r'^\d+(-\d+)?(\s*BPM)?$'
    return bool(re.match(pattern, tempo_str.strip(), re.IGNORECASE))


def validate_email(email_str):
    """
    Validate email format for evaluator contact.
    
    Args:
        email_str (str): Email string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not email_str or not isinstance(email_str, str):
        return True  # Optional field
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email_str))


def validate_required_fields(session_data):
    """
    Validate that required fields are present and non-empty.
    
    Args:
        session_data (dict): Complete session data dictionary
        
    Returns:
        list: List of missing required fields (empty if all present)
    """
    missing = []
    required_paths = [
        ('core_session', 'metadata', 'system_name'),
        ('core_session', 'metadata', 'date'),
        ('core_session', 'metadata', 'evaluator'),
    ]
    
    for path in required_paths:
        try:
            value = session_data
            for key in path:
                value = value[key]
            
            # Check if value is empty or None
            if not value or (isinstance(value, str) and not value.strip()):
                missing.append('.'.join(path))
        except (KeyError, TypeError):
            missing.append('.'.join(path))
    
    return missing


def validate_session_number(session_num):
    """
    Validate session number is positive integer.
    
    Args:
        session_num: Session number to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        num = int(session_num)
        return num > 0
    except (ValueError, TypeError):
        return False


def validate_percentage(value):
    """
    Validate percentage value (0-100).
    
    Args:
        value: Value to validate
        
    Returns:
        bool: True if valid (0-100), False otherwise
    """
    try:
        num = float(value)
        return 0 <= num <= 100
    except (ValueError, TypeError):
        return False


def validate_widget_value(widget, validation_type='text'):
    """
    Generic widget value validator.
    
    Args:
        widget: IPywidget to validate
        validation_type (str): Type of validation ('text', 'time', 'email', 'number', 'percentage')
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not hasattr(widget, 'value'):
        return False, "Widget has no value attribute"
    
    value = widget.value
    
    if validation_type == 'text':
        # Text should not be empty (for required fields)
        if not value or (isinstance(value, str) and not value.strip()):
            return False, "Field cannot be empty"
        return True, None
    
    elif validation_type == 'time':
        if not validate_time_format(value):
            return False, "Invalid time format (use HH:MM)"
        return True, None
    
    elif validation_type == 'email':
        if not validate_email(value):
            return False, "Invalid email format"
        return True, None
    
    elif validation_type == 'number':
        try:
            float(value)
            return True, None
        except (ValueError, TypeError):
            return False, "Must be a valid number"
    
    elif validation_type == 'percentage':
        if not validate_percentage(value):
            return False, "Must be between 0 and 100"
        return True, None
    
    else:
        return True, None  # Unknown validation type, skip


def validate_json_exportable(data):
    """
    Validate that data structure can be exported to JSON.
    
    Args:
        data: Data structure to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    import json
    
    try:
        # Attempt to serialize
        json.dumps(data)
        return True, None
    except (TypeError, ValueError) as e:
        return False, f"Data not JSON serializable: {str(e)}"


# ===== PHASE 0: SYSTEM OVERVIEW VALIDATORS =====

def validate_confidence_rating(rating):
    """
    Validate confidence rating is between 1-5.
    
    Args:
        rating: Confidence rating value (int or str)
        
    Returns:
        bool: True if valid (1-5), False otherwise
    """
    try:
        r = int(rating)
        return 1 <= r <= 5
    except (ValueError, TypeError):
        return False


def validate_phase0_assessment(assessment):
    """
    Validate Phase 0 assessment has required fields.
    
    Args:
        assessment (dict): Phase 0 system assessment data
        
    Returns:
        list: List of missing required fields (empty if all present)
    """
    missing = []
    
    # Required top-level fields
    required_top = ['system_name', 'assessment_date', 'architecture', 'interface', 'hardware']
    for field in required_top:
        if field not in assessment or not assessment[field]:
            missing.append(field)
    
    # Required sub-fields in architecture
    if 'architecture' in assessment and isinstance(assessment['architecture'], dict):
        arch_required = ['framework', 'generation_mode', 'confidence_rating']
        for field in arch_required:
            if field not in assessment['architecture']:
                missing.append(f'architecture.{field}')
    
    # Required sub-fields in interface
    if 'interface' in assessment and isinstance(assessment['interface'], dict):
        interface_required = ['interaction_modes', 'setup_complexity', 'confidence_rating']
        for field in interface_required:
            if field not in assessment['interface']:
                missing.append(f'interface.{field}')
    
    # Required sub-fields in hardware
    if 'hardware' in assessment and isinstance(assessment['hardware'], dict):
        hardware_required = ['gpu_type', 'confidence_rating']
        for field in hardware_required:
            if field not in assessment['hardware']:
                missing.append(f'hardware.{field}')
    
    return missing


# Future validation functions can be added here:
# - validate_file_path()
# - validate_url()
# - validate_system_version()
# - validate_generation_attempt_structure()
# etc.

"""
Shared Constants Module

Defines shared constants, dropdown options, and configuration values
used across multiple widget modules.

This module serves as a single source of truth for:
- Dropdown menu options
- Default values
- UI configuration
- System-wide constants

Example Usage:
    from constants import MUSICAL_ELEMENTS, GENRES, PERFORMANCE_CRITERIA
    
    # Use in widget creation
    musical_element = widgets.Dropdown(options=MUSICAL_ELEMENTS, ...)
"""

# Musical Elements
MUSICAL_ELEMENTS = [
    'Bassline',
    'Melody',
    'Harmony',
    'Drum Pattern',
    'Percussion',
    'Riffs',
    'Texture',
    'Effects',
    'Full Mix',
    'Other'
]

# DAW Options
DAWS = [
    'Ableton Live',
    'Logic Pro',
    'FL Studio',
    'Pro Tools',
    'Cubase',
    'Studio One',
    'Reaper',
    'Other',
    'None tested'
]

# Interface Types
INTERFACE_TYPES = [
    'Web Interface',
    'Local GUI',
    'Command Line',
    'VST Plugin',
    'AU Plugin',
    'Standalone App',
    'Other'
]

# Performance Criteria (8 criteria from evaluation framework)
PERFORMANCE_CRITERIA = [
    '1. Usability',
    '2. Generation Speed',
    '3. Audio Quality',
    '4. Stylistic Accuracy',
    '5. Parameter Control',
    '6. Content Generation Control',
    '7. DAW Integration',
    '8. Creative Workflow Fit'
]

# Incident Types
INCIDENT_TYPES = [
    'Breakthrough/Success',
    'Failure/Error',
    'Unexpected Behavior',
    'Workflow Discovery',
    'Creative Insight',
    'Technical Issue',
    'Prompt Engineering Discovery',
    'Integration Challenge',
    'Quality Issue'
]

# Workflow Phase Types
WORKFLOW_PHASE_TYPES = [
    'Content Generation',
    'Curation',
    'Integration',
    'Post-Production'
]

# File Formats
AUDIO_FILE_FORMATS = [
    'WAV',
    'MP3',
    'AIFF',
    'FLAC',
    'MIDI',
    'Other'
]

# ===== PHASE 0: SYSTEM OVERVIEW CONSTANTS =====
# These constants support Phase 0 system-level assessments

# AI/ML Frameworks
FRAMEWORKS = [
    'Transformer',
    'Diffusion Model',
    'Variational Autoencoder (VAE)',
    'Generative Adversarial Network (GAN)',
    'Hybrid Architecture',
    'Recurrent Neural Network (RNN/LSTM)',
    'Other',
    'Unknown'
]

# Generation Modes
GENERATION_MODES = [
    'Sequential (token-by-token)',
    'Iterative Refinement',
    'Direct Generation',
    'Conditional Generation',
    'Latent Space Interpolation',
    'Retrieval-Augmented',
    'Other',
    'Unknown'
]

# Modalities Supported
MODALITIES = [
    'Text-to-Audio',
    'Audio-to-Audio',
    'MIDI-to-Audio',
    'Image-to-Audio',
    'Text-to-MIDI',
    'Multimodal',
    'Audio Only',
    'Other'
]

# GPU Types
GPU_TYPES = [
    'NVIDIA (CUDA)',
    'AMD (ROCm)',
    'Intel',
    'Apple Silicon (Metal)',
    'CPU Only',
    'Cloud/API (Unknown)',
    'Other'
]

# Accessibility Levels for Different User Types
ACCESSIBILITY_LEVELS = [
    'Accessible (Consumer Hardware)',
    'Moderate (Mid-range GPU)',
    'High-end (Workstation Required)',
    'Enterprise Only',
    'Cloud API Only'
]

# Interaction Modes
INTERACTION_MODES = [
    'Text Prompts',
    'Parameter Sliders',
    'Audio Input',
    'MIDI Input',
    'Visual Interface',
    'Code/API',
    'Drag-and-Drop',
    'Real-time Control',
    'Batch Processing',
    'Other'
]

# Setup Complexity Levels
SETUP_COMPLEXITY = [
    'Instant (Web/No Setup)',
    'Simple (One-Click Install)',
    'Moderate (Some Configuration)',
    'Complex (Manual Dependencies)',
    'Expert (Requires Dev Experience)'
]

# UI Configuration
UI_CONFIG = {
    'default_textbox_width': '700px',
    'default_textarea_height': '80px',
    'default_description_width': 'initial',
    'gradient_header': 'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
}

# Session State Paths
PATHS = {
    'outputs_dir': '../outputs',
    'sessions_dir': '../outputs/sessions',
    'logs_dir': '../outputs/logs',
    'phase0_dir': '../outputs/phase0_results',
}

# Validation Thresholds
VALIDATION = {
    'completeness_threshold_high': 70,  # Ready to export
    'completeness_threshold_medium': 50,  # Warning
    'max_session_list_display': 10,  # Show last N sessions
}

# Template Metadata
TEMPLATE_VERSION = '2.0.0'
TEMPLATE_TYPE = 'session_notebook'

# Timezone for timestamps
TIMEZONE = 'UTC'

# Logging Configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

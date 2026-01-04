# Changelog

All notable changes to the AI Music Evaluation Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-22

### Added
- **Package Structure**: Complete restructuring to follow PEP 517/518 standards
- **Installable Package**: Can now be installed via `pip install aimusic-eval`
- **Core Utilities**: Separated pure Python utilities into `aimusic_eval.core` package
- **Configuration**: New `config.py` module for output directory management
- **Package Metadata**: Added `pyproject.toml`, `setup.py`, `MANIFEST.in`
- **Development Tools**: Added `requirements-dev.txt` with testing and linting tools
- **Documentation**: Created CHANGELOG.md, CONTRIBUTING.md, restructuring plan docs
- **Compatibility Layer**: Added `compat_imports.py` for backward compatibility

### Changed
- **Import Paths**: Changed from `widgets.*` to `aimusic_eval.widgets.*`
- **Core Utilities**: Moved from `widgets.utils.*` to `aimusic_eval.core.*`
- **Schemas**: Moved from `notebooks/` to `src/aimusic_eval/schemas/`
- **Directory Structure**: Adopted src-layout with `src/aimusic_eval/` as package root
- **Notebooks**: Moved from `phase1/notebooks/` to `notebooks/`
- **Tests**: Reorganized into `tests/unit/` and `tests/integration/`

### Migration Guide

#### For Notebook Users
```python
# Old (still works with deprecation warning)
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd().parent))
from widgets.system_metadata import create_system_metadata_section

# New (recommended)
from aimusic_eval.widgets.system_metadata import create_system_metadata_section
```

#### For Script Users
```python
# Old
from widgets.utils.exporters import export_to_markdown

# New
from aimusic_eval.core.exporters import export_to_markdown
```

#### Installation
```bash
# Development installation (from repository root)
pip install -e .

# With development dependencies
pip install -e .[dev]
```

### Backward Compatibility
- All notebooks in `phase1/notebooks/` continue to work unchanged
- Old import paths supported through v2.x with deprecation warnings
- Legacy output directory (`phase1/outputs/`) automatically detected and used if exists

### Technical Details
- Package now follows PEP 517 (build system) and PEP 518 (build requirements)
- Uses src-layout to prevent accidental imports of uninstalled package
- Comprehensive test suite maintained (150+ tests, >80% coverage)
- All 52 widget modules preserved with zero functional changes

### Breaking Changes
None in v2.0.0 - full backward compatibility maintained.

Breaking changes will be introduced in v3.0.0 (minimum 6 months from v2.0.0):
- Old `phase1/` directory structure will be removed
- Import paths without `aimusic_eval.` prefix will no longer work
- Migration tools will be provided

---

## [1.0.0] - 2025-10-21

### Initial Release
- Session Notebook with 3 master tabs (Session, Incident, Workflow)
- Synthesis Journal v2.0 with modular architecture
- Comparative Dashboard for multi-system analysis
- Automated Comparison Utility for statistical analysis
- Comprehensive widget system (52 modules, ~3,600 lines)
- Validation and export functionality (JSON, Markdown, CSV)
- Test suite with 150+ tests
- Docker support for development environment
- Hugo documentation site

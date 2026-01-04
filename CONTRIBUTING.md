# Contributing to AI Music Evaluation Framework

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

## Code of Conduct

This project follows a code of conduct. By participating, you agree to uphold this code. Please report unacceptable behavior.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/aimusic-eval.git
   cd aimusic-eval
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/aimusic-eval.git
   ```

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git
- (Optional) Docker for containerized development

### Installation

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install package in editable mode with dev dependencies**:
   ```bash
   pip install -e .[dev]
   ```

3. **Verify installation**:
   ```bash
   pytest tests/unit/
   ```

### Using Docker (Alternative)

```bash
docker-compose up jupyter
# Access Jupyter at http://localhost:8888
```

## Making Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `test/description` - Test improvements

Example:
```bash
git checkout -b feature/add-new-criterion
```

### Code Style

We follow PEP 8 with some modifications:

- **Line length**: 100 characters
- **Imports**: Use absolute imports from `aimusic_eval.*`
- **Docstrings**: Google style
- **Type hints**: Encouraged but not required

Run code formatters:
```bash
black src/ tests/ --line-length 100
isort src/ tests/
flake8 src/ tests/
```

### Project Structure

```
aimusic-eval/
├── src/aimusic_eval/          # Main package
│   ├── widgets/               # Jupyter widgets (UI components)
│   ├── core/                  # Pure Python utilities
│   ├── schemas/               # JSON schemas
│   └── templates/             # Data models
├── notebooks/                 # Example notebooks
├── tests/                     # Test suite
│   ├── unit/                  # Unit tests
│   └── integration/           # Integration tests
└── docs/                      # Documentation
```

### Coding Guidelines

**Widgets Package** (`aimusic_eval.widgets`)
- Use relative imports within widgets package
- Import from `aimusic_eval.core` for utilities
- Include comprehensive docstrings
- Keep widget modules focused (<300 lines)

**Core Package** (`aimusic_eval.core`)
- Pure Python (no Jupyter dependencies)
- Comprehensive error handling
- Type hints for public functions
- Unit tests for all public functions

**Example Function**:
```python
def validate_session_log(data: dict) -> dict:
    """
    Validate a session log data structure.
    
    Args:
        data: Session log dictionary to validate
        
    Returns:
        dict: Validation result with keys:
            - valid (bool): Whether data is valid
            - completeness (float): Percentage complete
            - missing (list): Missing required fields
            - warnings (list): Non-critical issues
            
    Example:
        >>> result = validate_session_log({'session_info': {...}})
        >>> print(result['valid'])
        True
    """
    # Implementation
```

## Testing

### Running Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/unit/test_validators.py

# With coverage
pytest --cov=aimusic_eval --cov-report=html

# Verbose output
pytest -v tests/
```

### Writing Tests

1. **Create test file** in `tests/unit/` or `tests/integration/`
2. **Use fixtures** from `conftest.py`
3. **Follow naming convention**: `test_*.py`, `Test*` classes, `test_*` methods
4. **Test one thing per test**
5. **Use descriptive test names**

**Example Test**:
```python
def test_validate_complete_session_log(sample_session_log):
    """Test validation of complete session log."""
    result = validate_session_log(sample_session_log)
    
    assert result['valid'] is True
    assert result['completeness'] == 100.0
    assert len(result['missing']) == 0
```

### Test Coverage

- Maintain **>80% overall coverage**
- **Core utilities**: >90% coverage
- **Widget modules**: >70% coverage (UI testing is complex)
- Check coverage: `pytest --cov=aimusic_eval --cov-report=term-missing`

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def function_name(arg1: str, arg2: int = 0) -> bool:
    """
    Brief description of function.
    
    Longer description if needed. Can span multiple lines
    and include implementation details.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2 (default: 0)
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If arg1 is empty
        
    Example:
        >>> result = function_name("test", 5)
        >>> print(result)
        True
    """
```

### README Updates

When adding major features, update:
- Main README.md (installation, usage)
- CHANGELOG.md (version history)
- Example notebooks (if applicable)

### API Documentation

API docs are generated from docstrings using Sphinx. Update docstrings to update API docs.

## Submitting Changes

### Commit Messages

Follow conventional commits:

```
type(scope): brief description

Longer explanation if needed.

Fixes #issue_number
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test updates
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Build/tooling changes

**Examples:**
```
feat(widgets): add new assessment criterion widget

Adds support for evaluating model latency as a new criterion.
Includes widget creation, validation, and export functionality.

Closes #123
```

```
fix(core): correct score calculation in comparative analysis

The average calculation was incorrectly handling None values.
Now properly excludes None scores from average.

Fixes #456
```

### Pull Request Process

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests locally**:
   ```bash
   pytest tests/
   black --check src/ tests/
   flake8 src/ tests/
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature
   ```

4. **Create Pull Request** on GitHub:
   - Clear title and description
   - Reference related issues
   - Include screenshots for UI changes
   - Check that CI tests pass

5. **Code Review**:
   - Address reviewer feedback
   - Push additional commits as needed
   - Keep PR focused (one feature/fix per PR)

6. **Merge**:
   - Maintainer will merge after approval
   - Your commits will be squashed unless requested otherwise

### PR Checklist

- [ ] Tests added/updated and passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] Code follows style guidelines
- [ ] No merge conflicts
- [ ] All CI checks passing

## Development Workflow

### Typical Workflow

1. **Create feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make changes**
   - Write code
   - Add tests
   - Update docs

3. **Test locally**
   ```bash
   pytest tests/
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/my-new-feature
   ```

### Staying Updated

```bash
# Fetch latest changes
git fetch upstream

# Rebase your branch
git rebase upstream/main

# Force push if needed
git push origin feature/my-new-feature --force
```

## Questions or Problems?

- **Bugs**: Open an issue with bug template
- **Features**: Open an issue with feature request template
- **Questions**: Use GitHub Discussions
- **Security**: Email security@example.com (not public issues)

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Acknowledged in release notes
- Mentioned in project documentation

Thank you for contributing! 🎵🤖

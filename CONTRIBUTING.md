# Contributing to Simple Data Explorer

Thank you for your interest in contributing to Simple Data Explorer!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/simple-data-explorer.git`
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
5. Install dependencies: `pip install -r requirements.txt`
6. Install dev dependencies: `pip install -e ".[dev]"`

## Development Workflow

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Write or update tests
4. Run tests: `pytest`
5. Run linting: `black app tests && flake8 app tests`
6. Commit your changes: `git commit -m "Description of changes"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Open a Pull Request

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting: `black app tests`
- Use type hints where appropriate
- Write docstrings for public functions and classes
- Keep functions focused and small

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for high test coverage
- Use pytest fixtures for common test setup

Run tests:
```bash
pytest
pytest --cov=app  # with coverage
```

## Documentation

- Update README.md if adding new features
- Update API.md for API changes
- Add docstrings to new functions/classes
- Update ARCHITECTURE.md for architectural changes

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all tests pass
- Update documentation as needed
- Keep PRs focused on a single feature/fix

## Questions?

Open an issue or discussion on GitHub!

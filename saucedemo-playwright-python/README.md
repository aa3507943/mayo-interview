# SauceDemo Playwright Python Automation

A professional automation testing project for [SauceDemo](https://www.saucedemo.com/) using Playwright, Python, and the Page Object Model (POM) pattern.

## Features
- **Page Object Model (POM)**: Clean separation of page logic and test cases.
- **Multi-browser Support**: Runs on Chromium, Firefox, and Webkit.
- **Cross-account Testing**: Specialized tests for all SauceDemo user types.
- **CI/CD Integrated**: GitHub Actions workflow included.
- **Reporting**: Automated HTML reports and screenshot capture on failure.

## Project Structure
```text
saucedemo-playwright-python/
├── pages/                          # Page Objects (POM)
├── tests/                          # Test Cases (pytest)
├── fixtures/                       # Test Data & Metadata
├── utils/                          # Helper functions & Utilities
├── .github/workflows/              # CI/CD config
├── pytest.ini                      # Test settings & markers
└── requirements.txt                # Dependencies
```

## Installation

1. **Clone the repository** (or navigate to the project folder).
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Playwright browsers**:
   ```bash
   playwright install
   ```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific browser
```bash
pytest --browser firefox
```

### Run by markers
- **Smoke tests**: `pytest -m smoke`
- **Regression tests**: `pytest -m regression`
- **Account-specific tests**: `pytest -m account`

### Headless mode
By default, tests run as configured in `pytest.ini`. To override:
```bash
pytest --headless
```

## CI/CD
The project includes a `.github/workflows/ci.yml` file that automatically runs tests on every push or pull request to the `main` branch. Reports and failure screenshots are uploaded as artifacts.

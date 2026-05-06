# Playwright with MCP — Python Test Framework

End-to-end test suite built with Playwright + pytest, designed to integrate with Playwright MCP for AI-assisted test generation.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Configuration

Copy `.env.example` to `.env` and set your values:

```bash
cp .env.example .env
```

| Variable     | Default                  | Description              |
|--------------|--------------------------|--------------------------|
| `BASE_URL`   | `https://example.com`    | Target app URL           |
| `HEADLESS`   | `true`                   | Run browser headlessly   |
| `BROWSER`    | `chromium`               | chromium / firefox / webkit |
| `SLOW_MO`    | `0`                      | ms delay between actions |

## Running Tests

```bash
# All tests
pytest

# Smoke suite only
pytest -m smoke

# Specific browser
pytest --browser firefox

# Headed mode
pytest --headed

# Parallel (4 workers)
pytest -n 4
```

## Project Structure

```
playwright_with_mcp/
├── conftest.py          # Fixtures and global setup
├── pytest.ini           # Pytest configuration
├── requirements.txt
├── pages/               # Page Object Models
│   └── base_page.py
├── tests/
│   ├── smoke/           # Smoke tests
│   └── regression/      # Regression tests
├── utils/               # Shared helpers
├── reports/             # HTML test reports (generated)
├── screenshots/         # Captured screenshots (generated)
└── videos/              # Recorded videos (generated)
```

## Adding Tests with Playwright MCP

Use Playwright MCP in Claude Code to record interactions and auto-generate test cases into `tests/smoke/` or `tests/regression/`.

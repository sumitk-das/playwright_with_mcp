import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, BrowserContext

load_dotenv()


def pytest_configure(config):
    os.makedirs("reports", exist_ok=True)


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://example.com")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": "videos/" if os.getenv("RECORD_VIDEO") else None,
    }


@pytest.fixture
def page(page: Page, base_url: str) -> Page:
    page.goto(base_url)
    return page

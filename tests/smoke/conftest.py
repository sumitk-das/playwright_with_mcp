import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    hp = HomePage(page)
    hp.goto()
    return hp

import re
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
def test_page_title(page: Page):
    expect(page).to_have_title(re.compile(".*"))


@pytest.mark.smoke
def test_page_loads(page: Page):
    expect(page.locator("body")).to_be_visible()

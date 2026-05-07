import pytest
from playwright.sync_api import Page
from pages.home_page import HomePage
from pages.auth_page import AuthPage
from pages.register_page import RegisterPage
from utils.helpers import timestamp

AE_BASE = "https://automationexercise.com"


@pytest.fixture
def home_page(page: Page) -> HomePage:
    hp = HomePage(page)
    hp.goto()
    return hp


@pytest.fixture
def logged_in_user(page: Page) -> dict:
    """Creates a fresh user account, logs in, and deletes the account on teardown."""
    ts = timestamp()
    user = {
        "name": "Test User",
        "email": f"qauser{ts}@testmail.com",
        "password": "Test@1234",
        "first_name": "Test",
        "last_name": "User",
        "address": "123 Test Street",
        "state": "California",
        "city": "Los Angeles",
        "zipcode": "90001",
        "mobile": "5551234567",
    }
    auth = AuthPage(page)
    auth.goto()
    auth.signup(user["name"], user["email"])
    reg = RegisterPage(page)
    reg.complete_registration(user["password"], user)
    page.locator("a[data-qa='continue-button']").click()
    yield user
    page.goto(f"{AE_BASE}/delete_account")

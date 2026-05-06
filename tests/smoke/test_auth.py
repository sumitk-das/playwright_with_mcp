import pytest
from playwright.sync_api import Page, expect
from pages.auth_page import AuthPage
from pages.register_page import RegisterPage
from utils.helpers import timestamp

AE_BASE = "https://automationexercise.com"


def _make_user() -> dict:
    ts = timestamp()
    return {
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


def _signup_and_create(auth_page: AuthPage, user: dict):
    """Signs up and completes registration. Lands on account_created page."""
    auth_page.goto()
    auth_page.signup(user["name"], user["email"])
    reg = RegisterPage(auth_page.page)
    reg.complete_registration(user["password"], user)


def _delete_account(page: Page):
    """Deletes the currently logged-in account."""
    page.goto(f"{AE_BASE}/delete_account")


@pytest.fixture
def auth_page(page: Page) -> AuthPage:
    ap = AuthPage(page)
    ap.goto()
    return ap


@pytest.fixture
def new_user() -> dict:
    return _make_user()


@pytest.mark.smoke
class TestLoginPageLoad:
    def test_title(self, auth_page: AuthPage):
        expect(auth_page.page).to_have_title("Automation Exercise - Signup / Login")

    def test_url(self, auth_page: AuthPage):
        expect(auth_page.page).to_have_url(f"{AE_BASE}/login")

    def test_login_heading_visible(self, auth_page: AuthPage):
        expect(auth_page.login_heading).to_be_visible()

    def test_signup_heading_visible(self, auth_page: AuthPage):
        expect(auth_page.signup_heading).to_be_visible()


@pytest.mark.smoke
class TestLoginForm:
    def test_email_field_visible(self, auth_page: AuthPage):
        expect(auth_page.login_email).to_be_visible()

    def test_password_field_visible(self, auth_page: AuthPage):
        expect(auth_page.login_password).to_be_visible()

    def test_login_button_visible(self, auth_page: AuthPage):
        expect(auth_page.login_btn).to_be_visible()

    def test_invalid_credentials_show_error(self, auth_page: AuthPage):
        auth_page.login("notarealuser@fake.com", "wrongpassword")
        expect(auth_page.login_error).to_be_visible()
        expect(auth_page.login_error).to_contain_text("Your email or password is incorrect!")


@pytest.mark.smoke
class TestSignupForm:
    def test_name_field_visible(self, auth_page: AuthPage):
        expect(auth_page.signup_name).to_be_visible()

    def test_email_field_visible(self, auth_page: AuthPage):
        expect(auth_page.signup_email).to_be_visible()

    def test_signup_button_visible(self, auth_page: AuthPage):
        expect(auth_page.signup_btn).to_be_visible()

    def test_existing_email_shows_error(self, auth_page: AuthPage, new_user: dict):
        _signup_and_create(auth_page, new_user)
        auth_page.page.locator("a[data-qa='continue-button']").click()
        auth_page.page.locator("a[href='/logout']").click()
        # Try to sign up again with same email
        auth_page.signup(new_user["name"], new_user["email"])
        expect(auth_page.signup_error).to_be_visible()
        expect(auth_page.signup_error).to_contain_text("Email Address already exist!")
        # Cleanup: login and delete the account created in setup
        auth_page.goto()
        auth_page.login(new_user["email"], new_user["password"])
        _delete_account(auth_page.page)


@pytest.mark.smoke
class TestSignupFlow:
    def test_signup_redirects_to_register_page(self, auth_page: AuthPage, new_user: dict):
        auth_page.signup(new_user["name"], new_user["email"])
        expect(auth_page.page).to_have_url(f"{AE_BASE}/signup")

    def test_register_page_shows_account_info_heading(self, auth_page: AuthPage, new_user: dict):
        auth_page.signup(new_user["name"], new_user["email"])
        reg = RegisterPage(auth_page.page)
        expect(reg.account_info_heading).to_be_visible()

    def test_register_page_has_password_field(self, auth_page: AuthPage, new_user: dict):
        auth_page.signup(new_user["name"], new_user["email"])
        reg = RegisterPage(auth_page.page)
        expect(reg.password).to_be_visible()

    def test_complete_signup_shows_account_created(self, auth_page: AuthPage, new_user: dict):
        _signup_and_create(auth_page, new_user)
        reg = RegisterPage(auth_page.page)
        expect(auth_page.page).to_have_url(f"{AE_BASE}/account_created")
        expect(reg.account_created_heading).to_be_visible()
        expect(reg.account_created_heading).to_contain_text("Account Created!")
        # Cleanup
        reg.continue_btn.click()
        _delete_account(auth_page.page)

    def test_account_created_has_continue_button(self, auth_page: AuthPage, new_user: dict):
        _signup_and_create(auth_page, new_user)
        reg = RegisterPage(auth_page.page)
        expect(reg.continue_btn).to_be_visible()
        # Cleanup
        reg.continue_btn.click()
        _delete_account(auth_page.page)


@pytest.mark.smoke
class TestLoginFlow:
    def test_valid_login_navigates_to_home(self, auth_page: AuthPage, new_user: dict):
        _signup_and_create(auth_page, new_user)
        auth_page.page.locator("a[data-qa='continue-button']").click()
        auth_page.page.locator("a[href='/logout']").click()
        auth_page.login(new_user["email"], new_user["password"])
        expect(auth_page.page).to_have_url(f"{AE_BASE}/")
        # Cleanup
        _delete_account(auth_page.page)

    def test_logged_in_shows_username_in_nav(self, auth_page: AuthPage, new_user: dict):
        _signup_and_create(auth_page, new_user)
        auth_page.page.locator("a[data-qa='continue-button']").click()
        auth_page.page.locator("a[href='/logout']").click()
        auth_page.login(new_user["email"], new_user["password"])
        logged_in = auth_page.page.locator("li a", has_text="Logged in as")
        expect(logged_in).to_be_visible()
        # Cleanup
        _delete_account(auth_page.page)

    def test_logout_redirects_to_login_page(self, auth_page: AuthPage, new_user: dict):
        _signup_and_create(auth_page, new_user)
        auth_page.page.locator("a[data-qa='continue-button']").click()
        auth_page.page.locator("a[href='/logout']").click()
        expect(auth_page.page).to_have_url(f"{AE_BASE}/login")
        # Cleanup: login and delete
        auth_page.login(new_user["email"], new_user["password"])
        _delete_account(auth_page.page)

from playwright.sync_api import Page
from pages.base_page import BasePage


class AuthPage(BasePage):
    URL = "https://automationexercise.com/login"

    def __init__(self, page: Page):
        super().__init__(page)
        # Login form
        self.login_heading = page.locator("h2", has_text="Login to your account")
        self.login_email = page.locator("input[data-qa='login-email']")
        self.login_password = page.locator("input[data-qa='login-password']")
        self.login_btn = page.locator("button[data-qa='login-button']")
        self.login_error = page.locator("p", has_text="Your email or password is incorrect!")
        # Signup form
        self.signup_heading = page.locator("h2", has_text="New User Signup!")
        self.signup_name = page.locator("input[data-qa='signup-name']")
        self.signup_email = page.locator("input[data-qa='signup-email']")
        self.signup_btn = page.locator("button[data-qa='signup-button']")
        self.signup_error = page.locator("p", has_text="Email Address already exist!")

    def goto(self):
        self.navigate(self.URL)

    def login(self, email: str, password: str):
        self.login_email.fill(email)
        self.login_password.fill(password)
        self.login_btn.click()

    def signup(self, name: str, email: str):
        self.signup_name.fill(name)
        self.signup_email.fill(email)
        self.signup_btn.click()

from playwright.sync_api import Page
from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.account_info_heading = page.get_by_text("Enter Account Information")
        self.password = page.locator("input[data-qa='password']")
        self.first_name = page.locator("input[data-qa='first_name']")
        self.last_name = page.locator("input[data-qa='last_name']")
        self.address = page.locator("input[data-qa='address']")
        self.country = page.locator("select[data-qa='country']")
        self.state = page.locator("input[data-qa='state']")
        self.city = page.locator("input[data-qa='city']")
        self.zipcode = page.locator("input[data-qa='zipcode']")
        self.mobile = page.locator("input[data-qa='mobile_number']")
        self.create_btn = page.locator("button[data-qa='create-account']")
        self.account_created_heading = page.locator("h2[data-qa='account-created']")
        self.continue_btn = page.locator("a[data-qa='continue-button']")

    def complete_registration(self, password: str, user: dict):
        self.password.fill(password)
        self.first_name.fill(user["first_name"])
        self.last_name.fill(user["last_name"])
        self.address.fill(user["address"])
        self.state.fill(user["state"])
        self.city.fill(user["city"])
        self.zipcode.fill(user["zipcode"])
        self.mobile.fill(user["mobile"])
        self.create_btn.click()

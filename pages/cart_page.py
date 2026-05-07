from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "https://automationexercise.com/view_cart"

    def __init__(self, page: Page):
        super().__init__(page)
        self.empty_cart_section = page.locator("#empty_cart")
        self.cart_table = page.locator("#cart_info_table")
        self.product_rows = page.locator("#cart_info_table tbody tr")
        self.product_names = page.locator(".cart_description h4 a")
        self.product_prices = page.locator(".cart_price p")
        self.product_quantities = page.locator(".cart_quantity button")
        self.product_totals = page.locator(".cart_total .cart_total_price")
        self.delete_btns = page.locator("a.cart_quantity_delete")
        self.proceed_btn = page.locator("a.btn.check_out")
        self.checkout_modal = page.locator(".modal-content")
        self.modal_login_link = page.locator(".modal-body a[href='/login']")

    def goto(self):
        self.navigate(self.URL)

    def remove_first_item(self):
        self.delete_btns.first.click()
        self.page.wait_for_load_state("domcontentloaded")

from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Checkout page (/checkout)
        self.delivery_address = page.locator("#address_delivery")
        self.billing_address = page.locator("#address_invoice")
        self.order_table = page.locator("#cart_info")
        self.comment_field = page.locator("textarea.form-control")
        self.place_order_btn = page.locator("a[href='/payment']")
        # Payment page (/payment)
        self.name_on_card = page.locator("input[data-qa='name-on-card']")
        self.card_number = page.locator("input[data-qa='card-number']")
        self.cvc = page.locator("input[data-qa='cvc']")
        self.expiry_month = page.locator("input[data-qa='expiry-month']")
        self.expiry_year = page.locator("input[data-qa='expiry-year']")
        self.pay_btn = page.locator("button[data-qa='pay-button']")
        # Order confirmed page (/payment_done/*)
        self.order_placed_heading = page.locator("h2[data-qa='order-placed']")

    def fill_payment_and_confirm(self, name: str, card: str, cvc: str, month: str, year: str):
        self.name_on_card.fill(name)
        self.card_number.fill(card)
        self.cvc.fill(cvc)
        self.expiry_month.fill(month)
        self.expiry_year.fill(year)
        self.pay_btn.click()

from playwright.sync_api import Page
from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://automationexercise.com"

    def __init__(self, page: Page):
        super().__init__(page)
        self.logo = page.locator("img[src*='logo']")
        self.nav_links = page.locator("ul.nav.navbar-nav li a")
        self.slider = page.locator("#slider-carousel")
        self.features_items = page.locator(".features_items")
        self.product_items = page.locator(".product-image-wrapper")
        self.left_sidebar = page.locator(".left-sidebar")
        self.category_section = page.locator(".category-products")
        self.brands_section = page.locator(".brands_products")
        self.subscription_email = page.locator("#susbscribe_email")
        self.subscribe_btn = page.locator("#subscribe")
        self.subscribe_success = page.locator("#success-subscribe")
        self.footer = page.locator("footer")

    def goto(self):
        self.navigate(self.URL)

    def get_nav_link_by_href(self, href: str):
        return self.page.locator(f"ul.nav.navbar-nav a[href='{href}']")

    def subscribe_newsletter(self, email: str):
        self.subscription_email.fill(email)
        self.subscribe_btn.click()

    def scroll_to_footer(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

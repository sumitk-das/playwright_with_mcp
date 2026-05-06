from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class ProductsPage(BasePage):
    URL = "https://automationexercise.com/products"

    def __init__(self, page: Page):
        super().__init__(page)
        self.all_products_heading = page.locator("h2.title.text-center")
        self.search_input = page.locator("#search_product")
        self.search_btn = page.locator("#submit_search")
        self.searched_products_heading = page.locator("h2.title.text-center", has_text="Searched Products")
        self.products_grid = page.locator(".features_items")
        self.product_items = page.locator(".product-image-wrapper")
        self.left_sidebar = page.locator(".left-sidebar")
        self.category_section = page.locator(".category-products")
        self.brands_section = page.locator(".brands_products")
        self.add_to_cart_modal = page.locator(".modal-content")
        self.modal_continue_btn = page.locator("button[data-dismiss='modal']")
        self.modal_view_cart_btn = page.locator(".modal-dialog a[href='/view_cart']")

    def goto(self):
        self.navigate(self.URL)

    def search(self, query: str):
        self.search_input.fill(query)
        self.search_btn.click()

    def get_product_names(self) -> list[str]:
        return self.page.locator(".productinfo p").all_inner_texts()

    def get_first_product_view_link(self):
        return self.page.locator("a[href*='/product_details/']").first

    def add_first_product_to_cart(self):
        self.page.locator(".productinfo a.btn.add-to-cart").first.click()

    def filter_by_category(self, category_href: str):
        self.page.locator(f"a[href='{category_href}']").click()

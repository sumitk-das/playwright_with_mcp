import re
import pytest
from playwright.sync_api import Page, expect
from pages.products_page import ProductsPage


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    pp = ProductsPage(page)
    pp.goto()
    return pp


@pytest.mark.smoke
class TestProductsPageLoad:
    def test_title(self, products_page: ProductsPage):
        expect(products_page.page).to_have_title("Automation Exercise - All Products")

    def test_url(self, products_page: ProductsPage):
        expect(products_page.page).to_have_url("https://automationexercise.com/products")

    def test_all_products_heading_visible(self, products_page: ProductsPage):
        expect(products_page.all_products_heading).to_be_visible()

    def test_all_products_heading_text(self, products_page: ProductsPage):
        expect(products_page.all_products_heading).to_contain_text("All Products")


@pytest.mark.smoke
class TestProductsGrid:
    def test_products_grid_visible(self, products_page: ProductsPage):
        expect(products_page.products_grid).to_be_visible()

    def test_products_are_displayed(self, products_page: ProductsPage):
        count = products_page.product_items.count()
        assert count > 0, f"Expected products to be listed, got {count}"

    def test_at_least_ten_products_displayed(self, products_page: ProductsPage):
        count = products_page.product_items.count()
        assert count >= 10, f"Expected at least 10 products, got {count}"

    def test_each_product_has_name(self, products_page: ProductsPage):
        names = products_page.get_product_names()
        assert all(name.strip() for name in names), "Some products are missing a name"

    def test_each_product_has_view_link(self, products_page: ProductsPage):
        view_links = products_page.page.locator("a[href*='/product_details/']")
        assert view_links.count() > 0

    def test_first_product_view_link_navigates(self, products_page: ProductsPage):
        products_page.get_first_product_view_link().click()
        expect(products_page.page).to_have_url(re.compile(r"/product_details/"))

    def test_each_product_has_add_to_cart_btn(self, products_page: ProductsPage):
        add_btns = products_page.page.locator(".productinfo a.btn.add-to-cart")
        assert add_btns.count() > 0


@pytest.mark.smoke
class TestProductSearch:
    def test_search_input_visible(self, products_page: ProductsPage):
        expect(products_page.search_input).to_be_visible()

    def test_search_button_visible(self, products_page: ProductsPage):
        expect(products_page.search_btn).to_be_visible()

    def test_search_returns_results(self, products_page: ProductsPage):
        products_page.search("Top")
        count = products_page.product_items.count()
        assert count > 0, "Search for 'Top' returned no results"

    def test_search_shows_searched_products_heading(self, products_page: ProductsPage):
        products_page.search("Top")
        expect(products_page.searched_products_heading).to_be_visible()

    def test_search_filters_to_relevant_products(self, products_page: ProductsPage):
        products_page.search("Blue Top")
        names = products_page.get_product_names()
        assert any("Blue Top" in name for name in names), "Expected 'Blue Top' in search results"

    def test_search_is_case_insensitive(self, products_page: ProductsPage):
        products_page.search("tshirt")
        count = products_page.product_items.count()
        assert count > 0, "Case-insensitive search for 'tshirt' returned no results"


@pytest.mark.smoke
class TestAddToCart:
    def test_add_to_cart_shows_modal(self, products_page: ProductsPage):
        products_page.add_first_product_to_cart()
        expect(products_page.add_to_cart_modal).to_be_visible()

    def test_modal_has_continue_shopping_button(self, products_page: ProductsPage):
        products_page.add_first_product_to_cart()
        expect(products_page.modal_continue_btn).to_be_visible()

    def test_modal_has_view_cart_button(self, products_page: ProductsPage):
        products_page.add_first_product_to_cart()
        expect(products_page.modal_view_cart_btn).to_be_visible()

    def test_continue_shopping_closes_modal(self, products_page: ProductsPage):
        products_page.add_first_product_to_cart()
        products_page.modal_continue_btn.click()
        expect(products_page.add_to_cart_modal).not_to_be_visible()

    def test_view_cart_navigates_to_cart(self, products_page: ProductsPage):
        products_page.add_first_product_to_cart()
        products_page.modal_view_cart_btn.click()
        expect(products_page.page).to_have_url("https://automationexercise.com/view_cart")


@pytest.mark.smoke
class TestProductsSidebar:
    def test_sidebar_visible(self, products_page: ProductsPage):
        expect(products_page.left_sidebar).to_be_visible()

    def test_category_section_visible(self, products_page: ProductsPage):
        expect(products_page.category_section).to_be_visible()

    def test_brands_section_visible(self, products_page: ProductsPage):
        expect(products_page.brands_section).to_be_visible()

    def test_filter_by_women_dress_category(self, products_page: ProductsPage):
        products_page.page.locator("a[href='#Women']").click()
        products_page.filter_by_category("/category_products/1")
        expect(products_page.page).to_have_url(
            "https://automationexercise.com/category_products/1"
        )

    def test_filter_by_polo_brand(self, products_page: ProductsPage):
        products_page.page.locator("a[href='/brand_products/Polo']").click()
        expect(products_page.page).to_have_url(
            "https://automationexercise.com/brand_products/Polo"
        )

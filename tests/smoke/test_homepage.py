import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage


@pytest.mark.smoke
class TestHomepageLoad:
    def test_title(self, home_page: HomePage):
        expect(home_page.page).to_have_title("Automation Exercise")

    def test_url(self, home_page: HomePage):
        expect(home_page.page).to_have_url("https://automationexercise.com/")

    def test_logo_visible(self, home_page: HomePage):
        expect(home_page.logo).to_be_visible()


@pytest.mark.smoke
class TestNavigation:
    def test_home_link_present(self, home_page: HomePage):
        expect(home_page.get_nav_link_by_href("/")).to_be_visible()

    def test_products_link_present(self, home_page: HomePage):
        expect(home_page.get_nav_link_by_href("/products")).to_be_visible()

    def test_cart_link_present(self, home_page: HomePage):
        expect(home_page.get_nav_link_by_href("/view_cart")).to_be_visible()

    def test_login_link_present(self, home_page: HomePage):
        expect(home_page.get_nav_link_by_href("/login")).to_be_visible()

    def test_test_cases_link_present(self, home_page: HomePage):
        expect(home_page.get_nav_link_by_href("/test_cases")).to_be_visible()

    def test_contact_us_link_present(self, home_page: HomePage):
        expect(home_page.get_nav_link_by_href("/contact_us")).to_be_visible()

    def test_products_link_navigates(self, home_page: HomePage):
        home_page.get_nav_link_by_href("/products").click()
        expect(home_page.page).to_have_url("https://automationexercise.com/products")


@pytest.mark.smoke
class TestHomepageContent:
    def test_slider_carousel_visible(self, home_page: HomePage):
        expect(home_page.slider).to_be_visible()

    def test_features_items_section_visible(self, home_page: HomePage):
        expect(home_page.features_items).to_be_visible()

    def test_products_are_displayed(self, home_page: HomePage):
        count = home_page.product_items.count()
        assert count > 0, f"Expected products to be displayed, got {count}"

    def test_at_least_eight_products_displayed(self, home_page: HomePage):
        count = home_page.product_items.count()
        assert count >= 8, f"Expected at least 8 products, got {count}"

    def test_left_sidebar_visible(self, home_page: HomePage):
        expect(home_page.left_sidebar).to_be_visible()


@pytest.mark.smoke
class TestCategories:
    def test_category_section_visible(self, home_page: HomePage):
        expect(home_page.category_section).to_be_visible()

    def test_women_category_link_present(self, home_page: HomePage):
        link = home_page.page.locator("a[href='#Women']")
        expect(link).to_be_visible()

    def test_men_category_link_present(self, home_page: HomePage):
        link = home_page.page.locator("a[href='#Men']")
        expect(link).to_be_visible()

    def test_kids_category_link_present(self, home_page: HomePage):
        link = home_page.page.locator("a[href='#Kids']")
        expect(link).to_be_visible()

    def test_women_subcategory_dress_present(self, home_page: HomePage):
        home_page.page.locator("a[href='#Women']").click()
        home_page.page.locator("#Women").wait_for(state="visible")
        link = home_page.page.locator("a[href='/category_products/1']")
        expect(link).to_be_visible()

    def test_women_subcategory_tops_present(self, home_page: HomePage):
        home_page.page.locator("a[href='#Women']").click()
        home_page.page.locator("#Women").wait_for(state="visible")
        link = home_page.page.locator("a[href='/category_products/2']")
        expect(link).to_be_visible()


@pytest.mark.smoke
class TestBrands:
    def test_brands_section_visible(self, home_page: HomePage):
        expect(home_page.brands_section).to_be_visible()

    def test_polo_brand_link_present(self, home_page: HomePage):
        link = home_page.page.locator("a[href='/brand_products/Polo']")
        expect(link).to_be_visible()

    def test_hm_brand_link_present(self, home_page: HomePage):
        link = home_page.page.locator("a[href='/brand_products/H&M']")
        expect(link).to_be_visible()

    def test_madame_brand_link_present(self, home_page: HomePage):
        link = home_page.page.locator("a[href='/brand_products/Madame']")
        expect(link).to_be_visible()


@pytest.mark.smoke
class TestFooter:
    def test_footer_visible(self, home_page: HomePage):
        home_page.scroll_to_footer()
        expect(home_page.footer).to_be_visible()

    def test_subscription_heading_visible(self, home_page: HomePage):
        home_page.scroll_to_footer()
        heading = home_page.page.locator("h2", has_text="Subscription")
        expect(heading).to_be_visible()

    def test_subscription_email_input_visible(self, home_page: HomePage):
        home_page.scroll_to_footer()
        expect(home_page.subscription_email).to_be_visible()

    def test_subscribe_button_visible(self, home_page: HomePage):
        home_page.scroll_to_footer()
        expect(home_page.subscribe_btn).to_be_visible()

    def test_newsletter_subscription_success(self, home_page: HomePage):
        home_page.scroll_to_footer()
        home_page.subscribe_newsletter("testuser@example.com")
        expect(home_page.subscribe_success).to_be_visible()
        expect(home_page.page.locator("#success-subscribe")).to_contain_text(
            "You have been successfully subscribed!"
        )

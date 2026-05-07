import re
import pytest
from playwright.sync_api import Page, expect
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.products_page import ProductsPage

AE_BASE = "https://automationexercise.com"

PAYMENT = {
    "name": "Test User",
    "card": "4111111111111111",
    "cvc": "123",
    "month": "12",
    "year": "2027",
}


def _add_product_to_cart(page: Page):
    """Navigates to products, adds the first item, and dismisses the modal."""
    pp = ProductsPage(page)
    pp.goto()
    pp.add_first_product_to_cart()
    pp.modal_continue_btn.click()


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    cp = CartPage(page)
    cp.goto()
    return cp


@pytest.fixture
def cart_with_product(page: Page) -> CartPage:
    _add_product_to_cart(page)
    cp = CartPage(page)
    cp.goto()
    return cp


@pytest.fixture
def checkout_page(page: Page, logged_in_user: dict) -> CheckoutPage:
    _add_product_to_cart(page)
    cp = CartPage(page)
    cp.goto()
    cp.proceed_btn.click()
    return CheckoutPage(page)


@pytest.mark.smoke
class TestCartPage:
    def test_url(self, cart_page: CartPage):
        expect(cart_page.page).to_have_url(f"{AE_BASE}/view_cart")

    def test_empty_cart_shows_message(self, cart_page: CartPage):
        expect(cart_page.empty_cart_section).to_be_visible()


@pytest.mark.smoke
class TestCartWithProduct:
    def test_product_appears_in_cart(self, cart_with_product: CartPage):
        expect(cart_with_product.cart_table).to_be_visible()
        assert cart_with_product.product_rows.count() > 0

    def test_cart_shows_product_name(self, cart_with_product: CartPage):
        name = cart_with_product.product_names.first.inner_text()
        assert name.strip() != ""

    def test_cart_shows_product_price(self, cart_with_product: CartPage):
        price = cart_with_product.product_prices.first.inner_text()
        assert "Rs." in price

    def test_cart_shows_product_quantity(self, cart_with_product: CartPage):
        qty = cart_with_product.product_quantities.first.inner_text()
        assert qty.strip().isdigit()

    def test_cart_shows_product_total(self, cart_with_product: CartPage):
        total = cart_with_product.product_totals.first.inner_text()
        assert "Rs." in total

    def test_proceed_to_checkout_visible(self, cart_with_product: CartPage):
        expect(cart_with_product.proceed_btn).to_be_visible()

    def test_remove_product_empties_cart(self, cart_with_product: CartPage):
        cart_with_product.remove_first_item()
        expect(cart_with_product.empty_cart_section).to_be_visible()


@pytest.mark.smoke
class TestGuestCheckout:
    def test_guest_proceed_shows_modal(self, cart_with_product: CartPage):
        cart_with_product.proceed_btn.click()
        expect(cart_with_product.checkout_modal).to_be_visible()

    def test_guest_modal_has_login_link(self, cart_with_product: CartPage):
        cart_with_product.proceed_btn.click()
        expect(cart_with_product.modal_login_link).to_be_visible()


@pytest.mark.smoke
class TestCheckoutPage:
    def test_checkout_url(self, checkout_page: CheckoutPage):
        expect(checkout_page.page).to_have_url(f"{AE_BASE}/checkout")

    def test_delivery_address_visible(self, checkout_page: CheckoutPage):
        expect(checkout_page.delivery_address).to_be_visible()

    def test_billing_address_visible(self, checkout_page: CheckoutPage):
        expect(checkout_page.billing_address).to_be_visible()

    def test_order_review_table_visible(self, checkout_page: CheckoutPage):
        expect(checkout_page.order_table).to_be_visible()

    def test_comment_field_visible(self, checkout_page: CheckoutPage):
        expect(checkout_page.comment_field).to_be_visible()

    def test_place_order_button_visible(self, checkout_page: CheckoutPage):
        expect(checkout_page.place_order_btn).to_be_visible()

    def test_place_order_navigates_to_payment(self, checkout_page: CheckoutPage):
        checkout_page.place_order_btn.click()
        expect(checkout_page.page).to_have_url(f"{AE_BASE}/payment")


@pytest.mark.smoke
class TestPaymentFlow:
    def test_payment_page_url(self, checkout_page: CheckoutPage):
        checkout_page.place_order_btn.click()
        expect(checkout_page.page).to_have_url(f"{AE_BASE}/payment")

    def test_payment_form_fields_visible(self, checkout_page: CheckoutPage):
        checkout_page.place_order_btn.click()
        expect(checkout_page.name_on_card).to_be_visible()
        expect(checkout_page.card_number).to_be_visible()
        expect(checkout_page.cvc).to_be_visible()
        expect(checkout_page.expiry_month).to_be_visible()
        expect(checkout_page.expiry_year).to_be_visible()

    def test_pay_button_visible(self, checkout_page: CheckoutPage):
        checkout_page.place_order_btn.click()
        expect(checkout_page.pay_btn).to_be_visible()

    def test_complete_checkout_places_order(self, checkout_page: CheckoutPage):
        checkout_page.comment_field.fill("Automated test order")
        checkout_page.place_order_btn.click()
        checkout_page.fill_payment_and_confirm(**PAYMENT)
        expect(checkout_page.page).to_have_url(re.compile(r"/payment_done/"))
        expect(checkout_page.order_placed_heading).to_be_visible()
        expect(checkout_page.order_placed_heading).to_contain_text("Order Placed!")

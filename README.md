# Playwright with MCP — Python Test Framework

End-to-end test suite built with Playwright + pytest for automationexercise.com.
Tests are organized using the Page Object Model (POM) pattern and integrate with
GitHub Actions CI/CD pipeline.

**Test Coverage:** 99 smoke tests across 5 test modules covering homepage,
products, authentication, and checkout flows.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Configuration

Copy `.env.example` to `.env` and set your values:

```bash
cp .env.example .env
```

| Variable   | Default                          | Description                 |
| ---------- | -------------------------------- | --------------------------- |
| `BASE_URL` | `https://automationexercise.com` | Target app URL              |
| `HEADLESS` | `true`                           | Run browser headlessly      |
| `BROWSER`  | `chromium`                       | chromium / firefox / webkit |
| `SLOW_MO`  | `0`                              | ms delay between actions    |

## Running Tests

```bash
# All tests
pytest

# Smoke suite only (default in CI)
pytest -m smoke

# Specific test file
pytest tests/smoke/test_homepage.py

# Specific test class
pytest tests/smoke/test_homepage.py::TestHomepageLoad

# Specific test
pytest tests/smoke/test_homepage.py::TestHomepageLoad::test_title

# Specific browser
pytest --browser firefox

# Headed mode (see browser interactions)
pytest --headed

# Parallel execution (4 workers)
pytest -n 4

# Generate HTML report
pytest --html=reports/report.html
```

## Project Structure

```
playwright_with_mcp/
├── conftest.py              # Global fixtures (logged_in_user, etc.)
├── pytest.ini               # Pytest configuration
├── requirements.txt
├── pages/                   # Page Object Models
│   ├── base_page.py         # Base class with common methods
│   ├── home_page.py         # Homepage selectors & methods
│   ├── products_page.py     # Products page selectors & methods
│   ├── auth_page.py         # Login/Signup form selectors & methods
│   ├── register_page.py     # Registration form selectors & methods
│   ├── cart_page.py         # Cart page selectors & methods
│   └── checkout_page.py     # Checkout & payment page selectors & methods
├── tests/
│   └── smoke/               # Smoke test suite (99 tests)
│       ├── conftest.py      # Test fixtures
│       ├── test_homepage.py
│       ├── test_products_page.py
│       ├── test_auth.py
│       └── test_checkout.py
├── utils/
│   └── helpers.py           # Shared utilities
├── .github/workflows/       # CI/CD pipeline
│   └── tests.yml            # GitHub Actions workflow
├── reports/                 # HTML test reports (generated)
├── screenshots/             # Captured screenshots (generated)
└── videos/                  # Recorded videos (generated)
```

## Test Coverage

### Homepage Tests (30 tests)

**TestHomepageLoad** (3 tests)

- Page title verification
- URL correctness
- Logo visibility

**TestNavigation** (7 tests)

- Navigation links presence (Home, Products, Cart, Login, Test Cases, Contact
  Us)
- Products link navigation

**TestHomepageContent** (5 tests)

- Slider/carousel visibility
- Features section visibility
- Product grid display (≥8 products)
- Left sidebar presence

**TestCategories** (6 tests)

- Category section visibility
- Women, Men, Kids category links
- Women subcategories (Dress, Tops)

**TestBrands** (4 tests)

- Brands section visibility
- Individual brand links (Polo, H&M, Madame)

**TestFooter** (5 tests)

- Footer visibility
- Newsletter subscription form
- Successful subscription confirmation

### Products Page Tests (27 tests)

**TestProductsPageLoad** (4 tests)

- Page title verification
- URL correctness
- "All Products" heading visibility & text

**TestProductsGrid** (7 tests)

- Products grid visibility
- Product count verification (≥10 products)
- Product names, view links, add-to-cart buttons

**TestProductSearch** (6 tests)

- Search input & button visibility
- Search functionality ("Top", "Blue Top")
- Case-insensitive search ("tshirt")
- "Searched Products" heading display

**TestAddToCart** (5 tests)

- Add-to-cart modal display
- Modal buttons (Continue Shopping, View Cart)
- Modal close functionality
- Navigation to cart from modal

**TestProductsSidebar** (5 tests)

- Sidebar, category, & brands sections visibility
- Filter by category (Women → Dress)
- Filter by brand (Polo)

### Authentication Tests (20 tests)

**TestLoginPageLoad** (4 tests)

- Page title verification
- URL correctness
- Login & Signup headings

**TestLoginForm** (4 tests)

- Email & password field visibility
- Login button presence
- Invalid credentials error message

**TestSignupForm** (4 tests)

- Name & email field visibility
- Signup button presence
- Duplicate email error handling

**TestSignupFlow** (5 tests)

- Signup redirects to registration page
- Account info heading on register page
- Password field on register page
- Account creation confirmation
- Continue button on account created page

**TestLoginFlow** (3 tests)

- Valid login navigation to home
- Username display in navigation (logged-in state)
- Logout redirect to login page

### Checkout & Payment Tests (22 tests)

**TestCartPage** (2 tests)

- Cart URL verification
- Empty cart message display

**TestCartWithProduct** (7 tests)

- Product appears in cart table
- Product name, price, quantity, total display
- Remove product functionality
- Proceed to checkout button visibility

**TestGuestCheckout** (2 tests)

- Guest checkout modal display
- Login link visibility in modal

**TestCheckoutPage** (7 tests)

- Checkout page URL verification
- Delivery & billing address sections visibility
- Order review table visibility
- Comments field visibility
- Place order button visibility
- Navigation to payment page

**TestPaymentFlow** (4 tests)

- Payment page URL verification
- Payment form fields visibility (name, card, CVC, expiry month/year)
- Pay button visibility
- Complete checkout flow with order confirmation

## Page Object Models

Each page is represented by a dedicated Page Object that encapsulates:

- **Locators**: CSS selectors using `data-qa` attributes for reliability
- **Methods**: Actions like `goto()`, `login()`, `add_to_cart()`, etc.
- **Base Methods**: Inherited from `BasePage` (`navigate()`, `get_title()`,
  `take_screenshot()`)

Example: `CartPage.remove_first_item()` waits for page load state after
deletion.

## Fixtures

### Global Fixtures (`conftest.py`)

- **logged_in_user**: Creates a test account, completes signup, and
  automatically deletes it after test completion. Provides unique email with
  timestamp to avoid duplicates.

### Test-Specific Fixtures

- **home_page**: Returns a `HomePage` object ready to use
- **products_page**: Returns a `ProductsPage` object on products page
- **auth_page**: Returns an `AuthPage` object on login page
- **new_user**: Returns a user dictionary with unique email & password
- **cart_page**: Returns an empty `CartPage`
- **cart_with_product**: Returns a `CartPage` with one product added
- **checkout_page**: Returns a `CheckoutPage` for logged-in user (requires
  `logged_in_user` fixture)

## CI/CD Integration

GitHub Actions workflow (`.github/workflows/tests.yml`) automatically:

1. **Smoke Tests** (on push/PR to main)
   - Runs `pytest tests/smoke/ -m smoke --browser chromium`
   - Takes ~2-3 minutes

2. **Manual Full Suite** (via workflow_dispatch)
   - Runs all tests when selected via GitHub Actions UI
   - Takes ~5-7 minutes

3. **Optimizations**
   - Caches Python dependencies (pip)
   - Caches Playwright browsers (~500MB)
   - Uploads HTML reports as artifacts (30-day retention)

## Running Tests with Playwright MCP

Use Playwright MCP in Claude Code to record browser interactions and generate
test cases. Tests should follow the Page Object Model pattern and include:

- Clear test names describing what is being tested
- Proper use of Playwright assertions (`expect()`)
- Fixture utilization for code reuse
- `@pytest.mark.smoke` marker for smoke test suite

## Debugging Tests

```bash
# Debug mode (pause on failure, helpful output)
pytest --pdb

# Trace execution (creates trace files for debugging)
pytest --trace

# View videos of failed tests
pytest --video=on

# Take screenshots on failure
pytest --screenshot=only-on-failure

# Headed mode for visual debugging
pytest --headed
```

## Test Data

- **Test Credentials**: Created dynamically with timestamps to ensure uniqueness
- **Payment Test Card**: 4111111111111111 (test card, no actual charges)
- **Automatic Cleanup**: All test accounts are deleted after tests complete to
  maintain data isolation

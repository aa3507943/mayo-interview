from pages.base_page import BasePage

class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Step 1 Locators
        self._first_name = page.locator("[data-test='firstName']")
        self._last_name = page.locator("[data-test='lastName']")
        self._postal_code = page.locator("[data-test='postalCode']")
        self._continue_button = page.locator("[data-test='continue']")
        
        # Step 2 Locators
        self._finish_button = page.locator("[data-test='finish']")
        self._item_total = page.locator(".summary_subtotal_label")
        self._tax = page.locator(".summary_tax_label")
        self._total = page.locator(".summary_total_label")

        # Step 3 Locators
        self._complete_header = page.locator(".complete-header")
        self._back_home_button = page.get_by_role("button", name="Back Home")

    def fill_information(self, first_name, last_name, postal_code):
        self._first_name.fill(first_name)
        self._last_name.fill(last_name)
        self._postal_code.fill(postal_code)
        self._continue_button.click()

    def finish_checkout(self):
        self._finish_button.click()

    def get_summary_info(self):
        return {
            "subtotal": self._item_total.inner_text(),
            "tax": self._tax.inner_text(),
            "total": self._total.inner_text()
        }

    def get_complete_message(self):
        return self._complete_header.inner_text()

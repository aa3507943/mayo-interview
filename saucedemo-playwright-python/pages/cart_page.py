from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._cart_items = page.locator(".cart_item")
        self._checkout_button = page.get_by_role("button", name="Checkout")
        self._continue_shopping_button = page.get_by_role("button", name="Continue Shopping")

    def get_items_count(self):
        return self._cart_items.count()

    def remove_item(self, item_name):
        self.page.locator(".cart_item", has_text=item_name).get_by_role("button", name="Remove").click()

    def checkout(self):
        self._checkout_button.click()
        self.wait_for_url("**/checkout-step-one.html")

    def continue_shopping(self):
        self._continue_shopping_button.click()
        self.wait_for_url("**/inventory.html")

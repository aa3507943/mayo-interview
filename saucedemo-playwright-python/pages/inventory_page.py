from pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._inventory_container = page.locator(".inventory_list")
        self._inventory_items = page.locator(".inventory_item")
        self._sort_dropdown = page.locator("[data-test='product-sort-container']")
        self._cart_badge = page.locator(".shopping_cart_badge")

    def get_all_items_count(self):
        return self._inventory_items.count()

    def add_to_cart(self, item_name):
        # Using a locator that finds the item by name then the button inside it
        self.page.locator(".inventory_item", has_text=item_name).get_by_role("button", name="Add to cart").click()

    def remove_from_cart(self, item_name):
        self.page.locator(".inventory_item", has_text=item_name).get_by_role("button", name="Remove").click()

    def sort_by(self, option_value):
        # Options: az, za, lohi, hilo
        self._sort_dropdown.select_option(option_value)

    def get_cart_count(self):
        if self._cart_badge.is_visible():
            return int(self._cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        self.page.locator(".shopping_cart_link").click()
        self.wait_for_url("**/cart.html")

    def get_item_price(self, item_name):
        return self.page.locator(".inventory_item", has_text=item_name).locator(".inventory_item_price").inner_text()

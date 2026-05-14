from pages.base_page import BasePage

class Header(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._burger_menu_button = page.get_by_role("button", name="Open Menu")
        self._logout_link = page.locator("#logout_sidebar_link")
        self._about_link = page.locator("#about_sidebar_link")
        self._reset_link = page.locator("#reset_sidebar_link")
        self._shopping_cart_link = page.locator(".shopping_cart_link")

    def logout(self):
        self._burger_menu_button.click()
        self._logout_link.click()
        self.wait_for_url("**/")

    def go_to_about(self):
        self._burger_menu_button.click()
        self._about_link.click()

    def reset_app_state(self):
        self._burger_menu_button.click()
        self._reset_link.click()
        # Closing the menu might be needed in some cases
        self.page.locator("#react-burger-cross-btn").click()

    def go_to_cart(self):
        self._shopping_cart_link.click()

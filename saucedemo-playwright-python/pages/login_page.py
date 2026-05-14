from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._username_input = page.get_by_placeholder("Username")
        self._password_input = page.get_by_placeholder("Password")
        self._login_button = page.get_by_role("button", name="Login")
        self._error_message = page.locator("[data-test='error']")

    def load(self):
        self.navigate("/")

    def login(self, username, password):
        self._username_input.fill(username)
        self._password_input.fill(password)
        self._login_button.click()

    def get_error_message(self):
        if self._error_message.is_visible():
            return self._error_message.inner_text()
        return ""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebDriver:
    """Initialize Selenium Chrome driver."""

    # ---------- SETUP ----------
    def __init__(self, headless: bool = False):
        # print('✔ WebDriver initialized ....')
        pass
        self.headless = headless
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        # print("✅ Chrome driver started")

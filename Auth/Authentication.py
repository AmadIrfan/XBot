import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver as ChromiumDriver

class CookiesAuth:
    def __init__(self, cookies: list[dict]):
        self.cookies = cookies

    def login(self, driver: ChromiumDriver):
        """Use cookies to log into X (Twitter)."""
        try:
            driver.get("https://x.com/")
            time.sleep(3)
            for ck in self.cookies:
                try:
                    driver.add_cookie(ck)
                except Exception:
                    ck.pop("domain", None)
                    try:
                        driver.add_cookie(ck)
                    except Exception as e:
                        print(f"Failed to add cookie {ck.get('name')}: {e}")
            driver.refresh()
            # print("Logged in with cookies")
            wait = WebDriverWait(driver, 5)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        except Exception as e:
            raise f"Login with cookies failed: {e}"

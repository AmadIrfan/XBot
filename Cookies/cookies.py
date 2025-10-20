import json
from pathlib import Path

class Cookies:
    def __init__(self, cookies_path: Path = Path(r'x.com.cookies.json')):
        # Make sure path is relative to this file, not current working dir
        self.cookies_path: Path = cookies_path

    def load_cookies(self) -> list[dict]:
        """Load cookies from JSON file."""
        try:
            # print("Loading 📄 file from: ", self.cookies_path.resolve())
            if not self.cookies_path.exists():
                raise FileNotFoundError(f"Cookies file not found: {self.cookies_path}")
            cookies_raw = json.loads(self.cookies_path.read_text(encoding="utf-8"))
            cookies:list[dict] = []
            for c in cookies_raw:
                cookie = {
                    "name": c.get("name"),
                    "value": c.get("value"),
                    "path": c.get("path", "/"),
                }
                if "domain" in c:
                    cookie["domain"] = c["domain"].lstrip(".")
                if "expires" in c and isinstance(c["expires"], (int, float)):
                    cookie["expires"] = int(c["expires"])
                cookies.append(cookie)
            # print("📄 file Loaded from: ", self.cookies_path.resolve())
            return cookies
        except Exception as e:
            raise

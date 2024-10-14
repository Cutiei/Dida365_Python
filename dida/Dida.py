from .didaapi import login_dida365, action2, transfer_string_to_cookies
import os
import json


class Unauthorized(Exception):
    def __init__(self, message="未登录"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Unauthorized: {self.message}"


class Dida:
    def __init__(self, auto_save_and_load_cookies: bool = True):
        self.auto_save_and_load_cookies = auto_save_and_load_cookies
        self.is_login = False
        self.cookies = self._load_cookies() if self.auto_save_and_load_cookies else None
        self.is_login = self._login_verify()

    def login_with_email(self, username, password) -> "Dida":
        self.cookies = login_dida365(username, password)
        self.auto_save_and_load_cookies and self._save_cookies(self.cookies)
        self.is_login = self._login_verify()
        return self

    def login_with_cookies(self, cookies: dict) -> "Dida":
        assert isinstance(cookies, dict), "cookies 必须是字典"
        self.cookies = cookies
        self.auto_save_and_load_cookies and self._save_cookies(self.cookies)
        self.is_login = self._login_verify()
        return self

    def login_with_cookies_string(self, cookies: str) -> "Dida":
        self.cookies = transfer_string_to_cookies(cookies)
        self.auto_save_and_load_cookies and self._save_cookies(self.cookies)
        self.is_login = self._login_verify()
        return self

    def action(self, action) -> str:
        if not self.is_login:
            raise Unauthorized("未登录")
        return action2(self.cookies, action)

    def __str__(self) -> str:
        return f"Dida(cookies={self.cookies})"

    def __repr__(self) -> str:
        return self.__str__()

    def _load_cookies(self) -> dict:
        current_path = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(current_path, "cookies.txt")):
            return None
        with open(os.path.join(current_path, "cookies.txt"), "r", encoding="utf-8") as f:
            return json.loads(f.read())

    def _save_cookies(self, cookies: dict):
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, "cookies.txt"), "w", encoding="utf-8") as f:
            f.write(json.dumps(cookies))

    def user_profile(self) -> dict:
        return json.loads(self.action("user/profile"))

    def project_all_trash_pagination(self) -> dict:
        return json.loads(self.action("project/all/trash/pagination"))

    def project_all_completed(self) -> dict:
        return json.loads(self.action("project/all/completed"))

    def batch_check_0(self) -> dict:
        return json.loads(self.action("batch/check/0"))

    def _login_verify(self) -> bool:
        if not self.cookies:
            return False
        if not action2(self.cookies, "user/profile"):
            return False
        return True

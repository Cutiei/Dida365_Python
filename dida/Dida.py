from .didaapi import login_dida365, action_dida365
import os
import json

class Dida:
    def __init__(self, auto_save_and_load_token: bool = True):
        self.auto_save_and_load_token = auto_save_and_load_token
        self.is_login = False
        self.token = self._load_token() if self.auto_save_and_load_token else None
        self.is_login = self._login_verify()

    def login_with_email(self, username, password) -> "Dida":
        self.token = login_dida365(username, password)
        self.auto_save_and_load_token and self._save_token(self.token)
        self.is_login = self._login_verify()
        return self
    
    def login_with_token(self, token: str) -> "Dida":
        self.token = token
        self.auto_save_and_load_token and self._save_token(self.token)
        self.is_login = self._login_verify()
        return self

    def action(self, action) -> str:
        if not self.is_login:
            raise Exception("未登录")
        return action_dida365(self.token, action)

    def __str__(self) -> str:
        return f"Dida(token={self.token})"

    def __repr__(self) -> str:
        return self.__str__()

    def _load_token(self) -> str:
        current_path = os.path.dirname(__file__)
        if not os.path.exists(os.path.join(current_path, "token.txt")):
            return None
        with open(os.path.join(current_path, "token.txt"), "r", encoding="utf-8") as f:
            return f.read()

    def _save_token(self, token: str):
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, "token.txt"), "w", encoding="utf-8") as f:
            f.write(token)

    def user_profile(self) -> dict:
        return json.loads(self.action("user/profile"))

    def project_all_trash_pagination(self) -> dict:
        return json.loads(self.action("project/all/trash/pagination"))

    def project_all_completed(self) -> dict:
        return json.loads(self.action("project/all/completed"))

    def batch_check_0(self) -> dict:
        return json.loads(self.action("batch/check/0"))

    def _login_verify(self) -> bool:
        if not self.token:
            return False
        if not action_dida365(self.token, "user/profile"):
            return False
        return True


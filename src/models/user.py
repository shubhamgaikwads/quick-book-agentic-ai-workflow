from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    name: str
    email: Optional[str] = None

    def update_profile(self, name=None, email=None):
        if name:
            self.name = name
        if email:
            self.email = email

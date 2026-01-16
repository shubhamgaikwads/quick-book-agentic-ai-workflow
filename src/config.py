import os
from dataclasses import dataclass


@dataclass
class Config:
    owner_email: str
    calendly_url: str
    default_time_zone: str = "UTC"

    @classmethod
    def load(cls):
        owner_email = os.getenv("OWNER_EMAIL", "owner@example.com")
        calendly_url = os.getenv("CALENDLY_URL", "https://calendly.com/your-handle")
        return cls(owner_email=owner_email, calendly_url=calendly_url)

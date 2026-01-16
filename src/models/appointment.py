from dataclasses import dataclass
from typing import Optional


@dataclass
class Appointment:
    date: Optional[str]
    time: Optional[str]
    email: Optional[str] = None
    status: str = "pending"

    def schedule(self):
        self.status = "scheduled"

    def cancel(self):
        self.status = "canceled"

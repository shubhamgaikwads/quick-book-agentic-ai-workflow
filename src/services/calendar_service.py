class CalendarService:
    def __init__(self, calendly_url):
        self.calendly_url = calendly_url

    def get_booking_link(self):
        return self.calendly_url

    def create_event(self, appointment):
        return {
            "status": "scheduled",
            "link": self.calendly_url,
            "appointment": appointment,
        }

    def delete_event(self, appointment_id):
        return {"status": "canceled", "appointment_id": appointment_id}

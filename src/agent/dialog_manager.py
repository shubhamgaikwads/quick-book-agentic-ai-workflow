class DialogManager:
    def __init__(self, calendar_service, owner_email):
        self.calendar_service = calendar_service
        self.owner_email = owner_email
        self.conversation_history = []

    def handle_intent(self, intent, entities):
        if intent == "book_appointment":
            return self._handle_booking(entities)
        if intent == "reschedule_appointment":
            return self._handle_reschedule(entities)
        if intent == "cancel_appointment":
            return self._handle_cancel(entities)
        if intent == "check_availability":
            return self._handle_availability()
        if intent == "get_appointment_details":
            return self._handle_details(entities)
        return self.respond_to_user("I can help with booking or updating appointments. What would you like to do?")

    def respond_to_user(self, response):
        self.conversation_history.append(response)
        return response

    def _handle_booking(self, entities):
        link = self.calendar_service.get_booking_link()
        date = entities.get("date")
        time = entities.get("time")
        if date or time:
            return self.respond_to_user(
                f"Got it. To confirm the slot, please pick a time on {link}."
            )
        return self.respond_to_user(
            f"Please use this link to book a time that works for you: {link}"
        )

    def _handle_reschedule(self, entities):
        link = self.calendar_service.get_booking_link()
        return self.respond_to_user(
            f"To reschedule, please choose a new time on {link}."
        )

    def _handle_cancel(self, entities):
        email = entities.get("email") or self.owner_email
        return self.respond_to_user(
            "To cancel an appointment, reply with the booking email address "
            f"or reach out to {email}."
        )

    def _handle_availability(self):
        link = self.calendar_service.get_booking_link()
        return self.respond_to_user(
            f"Here are the available slots: {link}"
        )

    def _handle_details(self, entities):
        email = entities.get("email") or self.owner_email
        return self.respond_to_user(
            "I do not have your appointment details yet. "
            f"If you already booked, please check your confirmation email or contact {email}."
        )

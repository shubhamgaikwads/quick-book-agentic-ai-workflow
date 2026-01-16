class NotificationService:
    def send_confirmation(self, email, appointment):
        confirmation_message = (
            f"Confirmation sent to {email} for the appointment on {appointment.date} at {appointment.time}."
        )
        print(confirmation_message)

    def send_reminder(self, email, appointment):
        reminder_message = (
            f"Reminder sent to {email} for the appointment on {appointment.date} at {appointment.time}."
        )
        print(reminder_message)

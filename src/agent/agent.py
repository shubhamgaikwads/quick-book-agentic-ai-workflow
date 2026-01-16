class Agent:
    def __init__(self, intent_selector, nlu, dialog_manager):
        self.intent_selector = intent_selector
        self.nlu = nlu
        self.dialog_manager = dialog_manager

    def start_conversation(self):
        return "Welcome to the Quick Booking Assistant! How can I help you today?"

    def process_input(self, user_input):
        parsed = self.nlu.parse_input(user_input)
        intent = self.intent_selector.select_intent(parsed["text"])
        confidence = self.intent_selector.get_intent_confidence()

        if not intent or confidence < 0.5:
            response = "I'm not sure what you mean. Do you want to book, reschedule, or cancel an appointment?"
        else:
            response = self.dialog_manager.handle_intent(intent, parsed["entities"])

        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "entities": parsed["entities"],
        }

import unittest
from yaml import safe_load

from src.agent.intent_selector import IntentSelector

class TestIntentSelector(unittest.TestCase):

    def setUp(self):
        with open("src/schemas/intents.yaml", "r", encoding="utf-8") as file_handle:
            intents = safe_load(file_handle)["intents"]
        self.intent_selector = IntentSelector(intents)

    def test_select_intent_booking(self):
        user_input = "I want to book an appointment"
        intent = self.intent_selector.select_intent(user_input)
        self.assertEqual(intent, "book_appointment")

    def test_select_intent_cancellation(self):
        user_input = "I need to cancel my appointment"
        intent = self.intent_selector.select_intent(user_input)
        self.assertEqual(intent, "cancel_appointment")

    def test_get_intent_confidence(self):
        user_input = "I'd like to schedule a meeting"
        self.intent_selector.select_intent(user_input)
        confidence = self.intent_selector.get_intent_confidence()
        self.assertGreater(confidence, 0.5)

    def test_select_intent_invalid(self):
        user_input = "What time is it?"
        intent = self.intent_selector.select_intent(user_input)
        self.assertIsNone(intent)

if __name__ == '__main__':
    unittest.main()

from yaml import safe_load

from src.agent.agent import Agent
from src.agent.dialog_manager import DialogManager
from src.agent.intent_selector import IntentSelector
from src.agent.nlu import NLU
from src.services.calendar_service import CalendarService


def test_booking_flow():
    with open("src/schemas/intents.yaml", "r", encoding="utf-8") as file_handle:
        intents = safe_load(file_handle)["intents"]

    intent_selector = IntentSelector(intents)
    nlu = NLU()
    calendar_service = CalendarService("https://calendly.com/test-handle")
    dialog_manager = DialogManager(calendar_service, "owner@example.com")
    agent = Agent(intent_selector, nlu, dialog_manager)

    user_input = "I would like to book an appointment next week."
    response = agent.process_input(user_input)

    assert response["intent"] == "book_appointment"
    assert "calendly.com" in response["response"]

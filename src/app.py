from pathlib import Path

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from agent.agent import Agent
from agent.dialog_manager import DialogManager
from agent.intent_selector import IntentSelector
from agent.nlu import NLU
from config import Config
from services.calendar_service import CalendarService
from services.fireworks_client import FireworksClient
from utils.validators import validate_user_input
from yaml import safe_load

app = Flask(__name__)
load_dotenv()

config = Config.load()
llm_client = FireworksClient.from_env()

intents_path = Path(__file__).resolve().parent / "schemas" / "intents.yaml"
with open(intents_path, "r", encoding="utf-8") as file_handle:
    intents = safe_load(file_handle)["intents"]

intent_selector = IntentSelector(intents, llm_client=llm_client)
nlu = NLU(llm_client=llm_client)
calendar_service = CalendarService(config.calendly_url)
dialog_manager = DialogManager(calendar_service, config.owner_email)
agent = Agent(intent_selector, nlu, dialog_manager)


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.json or {}
    user_input = payload.get("input", "")

    if not validate_user_input(user_input):
        return jsonify({"response": "Please share a short request so I can help."}), 400

    response = agent.process_input(user_input)
    return jsonify(response)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)

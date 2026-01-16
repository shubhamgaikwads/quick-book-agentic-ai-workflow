# Quick Book Assistant

This project is a Quick Booking Assistant designed to help users book appointments through natural language interactions. The main focus of the application is on intent selection, allowing the assistant to understand user requests and respond appropriately. The assistant uses a Calendly link for scheduling.

## Project Structure

```
quick-book-assistant
├── src
│   ├── app.py
│   ├── agent
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── intent_selector.py
│   │   ├── nlu.py
│   │   └── dialog_manager.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── appointment.py
│   │   └── user.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── calendar_service.py
│   │   └── notification_service.py
│   ├── schemas
│   │   └── intents.yaml
│   ├── utils
│   │   └── validators.py
│   └── config.py
├── tests
│   ├── test_intent_selector.py
│   └── test_booking_flow.py
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

## Features

- **Intent Selection**: The assistant can determine user intent based on input.
- **Appointment Management**: Users can schedule and manage appointments.
- **Natural Language Understanding**: The assistant processes user input to extract relevant information.
- **Notification System**: Users receive notifications for confirmations and reminders.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd quick-book-assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure your Calendly link, email, and Fireworks API key:
   ```
   cp .env.example .env
   ```
   Update `OWNER_EMAIL`, `CALENDLY_URL`, and `FIREWORKS_API_KEY` in `.env`.

## Usage

To run the application, execute the following command:
```
python src/app.py
```

Send a request to the API:
```
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"input":"I want to book an appointment"}'
```

## Testing

To run the tests, use:
```
pytest tests/
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

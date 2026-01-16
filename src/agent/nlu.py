import re


class NLU:
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def parse_input(self, user_input):
        text = (user_input or "").strip()
        return {
            "text": text,
            "entities": self.extract_entities(text),
        }

    def extract_entities(self, text):
        if self.llm_client:
            llm_entities = self._extract_entities_llm(text)
            if llm_entities is not None:
                return llm_entities
        entities = {}
        email = self._extract_email(text)
        if email:
            entities["email"] = email
        date = self._extract_date(text)
        if date:
            entities["date"] = date
        time = self._extract_time(text)
        if time:
            entities["time"] = time
        return entities

    @staticmethod
    def _extract_email(text):
        match = re.search(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", text)
        return match.group(0) if match else None

    @staticmethod
    def _extract_date(text):
        match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", text)
        if match:
            return match.group(0)
        month_pattern = (
            r"\b(january|february|march|april|may|june|july|august|september|october|"
            r"november|december)\s+\d{1,2}\b"
        )
        match = re.search(month_pattern, text, re.IGNORECASE)
        return match.group(0) if match else None

    @staticmethod
    def _extract_time(text):
        match = re.search(r"\b\d{1,2}(:\d{2})?\s?(am|pm)\b", text, re.IGNORECASE)
        if match:
            return match.group(0)
        match = re.search(r"\b\d{1,2}:\d{2}\b", text)
        return match.group(0) if match else None

    def _extract_entities_llm(self, text):
        system_prompt = (
            "You extract booking entities from user messages. "
            "Return JSON only."
        )
        user_prompt = (
            "Extract entities from the message. Return JSON with keys: "
            "entities (object with optional keys: date, time, email). "
            "Use null for missing values.\n\n"
            f"Message: {text}"
        )
        result = self.llm_client.complete_json(system_prompt, user_prompt)
        if not result or "entities" not in result:
            return None
        entities = result.get("entities") or {}
        return {k: v for k, v in entities.items() if v}

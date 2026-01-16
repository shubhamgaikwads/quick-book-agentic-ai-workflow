import re


class IntentSelector:
    def __init__(self, intents, llm_client=None):
        self.intents = intents or []
        self.llm_client = llm_client
        self.last_intent = None
        self.last_input = ""
        self.last_score = 0.0

    def select_intent(self, user_input):
        self.last_input = (user_input or "").strip()
        text = self.last_input.lower()
        tokens = self._tokenize(text)

        if self.llm_client:
            llm_response = self._select_intent_llm(self.last_input)
            if llm_response:
                self.last_intent = llm_response["intent"]
                self.last_score = llm_response["confidence"]
                return self.last_intent

        best_intent = None
        best_score = 0.0

        for intent in self.intents:
            intent_id = intent.get("id") or intent.get("name")
            score = self._score_intent(intent, text, tokens)
            if score > best_score:
                best_score = score
                best_intent = intent_id

        if best_score < 0.2:
            best_intent = None

        self.last_intent = best_intent
        self.last_score = best_score
        return best_intent

    def get_intent_confidence(self):
        if not self.last_intent:
            return 0.0
        return min(0.95, 0.2 + self.last_score)

    def _score_intent(self, intent, text, tokens):
        examples = intent.get("examples") or []
        keywords = intent.get("keywords") or []
        example_scores = []

        for example in examples:
            example_text = example.lower()
            if example_text in text:
                example_scores.append(1.0)
                continue
            example_tokens = self._tokenize(example_text)
            if not example_tokens:
                continue
            overlap = len(set(tokens) & set(example_tokens))
            example_scores.append(overlap / max(1, len(set(example_tokens))))

        keyword_hits = sum(1 for keyword in keywords if keyword.lower() in tokens)
        keyword_score = keyword_hits / max(1, len(keywords))

        return max(example_scores + [0.0]) * 0.7 + keyword_score * 0.3

    @staticmethod
    def _tokenize(text):
        return re.findall(r"[a-z0-9']+", text.lower())

    def _select_intent_llm(self, text):
        system_prompt = (
            "You are an intent classification engine for a booking assistant. "
            "Return JSON only."
        )
        intent_payload = [
            {
                "id": intent.get("id") or intent.get("name"),
                "name": intent.get("name"),
                "description": intent.get("description"),
                "keywords": intent.get("keywords") or [],
                "examples": intent.get("examples") or [],
            }
            for intent in self.intents
        ]
        user_prompt = (
            "Pick the best intent for the user message from the provided list. "
            "Return JSON with keys: intent (string or null), confidence (0 to 1).\n\n"
            f"User message: {text}\n\n"
            f"Intents: {intent_payload}"
        )
        result = self.llm_client.complete_json(system_prompt, user_prompt)
        if not result or "intent" not in result:
            return None
        return {
            "intent": result.get("intent"),
            "confidence": float(result.get("confidence", 0.0)),
        }

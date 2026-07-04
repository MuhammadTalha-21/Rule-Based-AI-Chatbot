# ============================================================
# DecodeLabs Internship - AI Project 1
# DecoBot v2.0 - PRO (Updated)
# Author: Muhammad Talha
# ============================================================

import re
import random
import json
import os
from datetime import datetime
from difflib import get_close_matches

# ANSI Colors for Terminal - Expo pe acha lagega
class C:
    BOT = '\033[94m'   # Blue
    USER = '\033[92m'  # Green
    SYS = '\033[93m'   # Yellow
    RESET = '\033[0m'

# ── 1. KNOWLEDGE BASE + INTENTS ───────────────
# Intent: Ek keyword ke peeche multiple tarike ke sawal
INTENTS = {
    "greet": {
        "keywords": ["hello", "hi", "hey", "salam"],
        "responses": [
            "Hello! I am DecoBot v2.0 🤖 How can I help you today?",
            "Hi there! Welcome back to DecoBot. What can I do for you?"
        ]
    },
    "about": {
        "keywords": ["who are you", "what is your name", "about you"],
        "responses": ["I am DecoBot, a rule-based AI chatbot built at DecodeLabs 🚀 with Python logic."]
    },
    "ai_knowledge": {
        "keywords": ["what is ai", "artificial intelligence"],
        "responses": ["AI (Artificial Intelligence) is the simulation of human intelligence in machines. 🧠"]
    },
    "python_knowledge": {
        "keywords": ["what is python", "python"],
        "responses": ["Python is a high-level, easy-to-learn language used in AI, web dev, and data science. 🐍"]
    },
    "ml_knowledge": {
        "keywords": ["what is machine learning", "machine learning"],
        "responses": ["Machine Learning is a subset of AI where machines learn from data instead of explicit rules. 📊"]
    },
    "joke": {
        "keywords": ["joke", "funny", "tell me a joke"],
        "responses": ["Why do programmers prefer dark mode? Because light attracts bugs! 🐛😄"]
    },
    "tips": {
        "keywords": ["tips for coding", "how to learn python", "coding tips"],
        "responses": ["💡 Tip: Read error messages carefully. Google the exact error. Build small projects daily! 🔥"]
    },
    "help": {
        "keywords": ["help", "what can i ask"],
        "responses": []  # filled dynamically at runtime
    },
    "bye": {
        "keywords": ["bye", "goodbye", "exit", "quit", "q"],
        "responses": ["Goodbye! Keep building amazing things. See you! 👋"]
    },
    "thanks": {
        "keywords": ["thanks", "thank you"],
        "responses": ["You're welcome! Happy to help anytime. 😊"]
    }
}

# Words that should NEVER be picked up as a "name" (avoids bugs like
# "my name is quit" confusing the bot)
RESERVED_WORDS = {"quit", "exit", "bye", "help", "bot", "ai", "python"}


# ── 2. CHATBOT ENGINE - THE BRAIN ───────────────
class DecoBot:
    def __init__(self, log_file="chat_history.json"):
        self.name = None
        self.question_count = 0
        self.log_file = log_file
        self.history = []
        self._build_help_response()
        self.all_keywords = [kw for intent in INTENTS.values() for kw in intent["keywords"]]

    def _build_help_response(self):
        """Dynamically list all topics instead of hardcoding them."""
        topics = []
        for name, data in INTENTS.items():
            if name in ("help", "bye", "thanks", "greet"):
                continue
            topics.append(data["keywords"][0])
        topic_str = ", ".join(f"'{t}'" for t in topics)
        INTENTS["help"]["responses"] = [
            f"Try asking about: {topic_str}. Or tell me your name! Type 'quit' to exit."
        ]

    def sanitize(self, text):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        return text

    def detect_name(self, text):
        # Memory feature: "my name is Ali" pakar lega
        match = re.search(r'\bmy name is (\w+)\b', text)
        if match:
            candidate = match.group(1)
            if candidate in RESERVED_WORDS:
                return "Haha, that doesn't sound like a real name. What's your actual name? 😄"
            self.name = candidate.capitalize()
            return f"Nice to meet you, {self.name}! I'll remember that. 😊"
        return None

    def get_intent(self, clean_input):
        # 1. Exact Match
        for intent_name, data in INTENTS.items():
            if clean_input in data["keywords"]:
                return intent_name

        # 2. Fuzzy Match: "helo" -> "hello" (only for short, single-word inputs
        # to avoid fuzzy-matching whole sentences incorrectly)
        if len(clean_input.split()) <= 2:
            close_match = get_close_matches(clean_input, self.all_keywords, n=1, cutoff=0.8)
            if close_match:
                matched_kw = close_match[0]
                for intent_name, data in INTENTS.items():
                    if matched_kw in data["keywords"]:
                        return intent_name

        # 3. Keyword in Sentence: "can you tell me about ai"
        # Uses word-boundary regex so "ai" doesn't match inside "said"/"hawaii" etc.
        # Longer keywords are checked first so "machine learning" wins over "python".
        sorted_intents = sorted(
            INTENTS.items(),
            key=lambda item: max(len(kw) for kw in item[1]["keywords"]),
            reverse=True
        )
        for intent_name, data in sorted_intents:
            for kw in data["keywords"]:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, clean_input):
                    return intent_name
        return None

    def log_interaction(self, user_input, bot_response):
        self.history.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "user": user_input,
            "bot": bot_response
        })

    def save_history(self):
        try:
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except OSError as e:
            print(f"{C.SYS}(Could not save chat history: {e}){C.RESET}")

    def get_response(self, user_input):
        clean_input = self.sanitize(user_input)

        if not clean_input:
            return "Please type something! 😊"

        # Memory Check first
        name_reply = self.detect_name(clean_input)
        if name_reply:
            return name_reply

        intent = self.get_intent(clean_input)

        if intent == "bye":
            return None  # Signal to quit

        if intent:
            self.question_count += 1
            return random.choice(INTENTS[intent]["responses"])

        return "🤔 I don't understand that yet. Try 'help' or ask about AI/Python."


# ── 3. MAIN LOOP - THE HEARTBEAT ─────────────────
def main():
    bot = DecoBot()
    print(f"{C.SYS}{'='*60}{C.RESET}")
    print(f"{C.SYS} Welcome to DecoBot v2.0 🤖 — DecodeLabs AI Pro{C.RESET}")
    print(f"{C.SYS} Type 'help' | 'quit' to exit | Tell me your name{C.RESET}")
    print(f"{C.SYS}{'='*60}{C.RESET}")

    while True:
        try:
            user_input = input(f"\n{C.USER}You: {C.RESET}")
            response = bot.get_response(user_input)

            if response is None:  # Bye intent
                bye_msg = INTENTS['bye']['responses'][0]
                print(f"{C.BOT}DecoBot: {bye_msg}{C.RESET}")
                print(f"{C.SYS}Session Stats: You asked {bot.question_count} questions. Great chat! {C.RESET}")
                bot.log_interaction(user_input, bye_msg)
                bot.save_history()
                break

            print(f"{C.BOT}DecoBot: {response}{C.RESET}")
            bot.log_interaction(user_input, response)

        except KeyboardInterrupt:
            print(f"\n{C.BOT}DecoBot: Session ended. Goodbye! 👋{C.RESET}")
            bot.save_history()
            break


if __name__ == "__main__":
    main()
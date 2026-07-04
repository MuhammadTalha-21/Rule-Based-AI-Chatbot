# 🤖 DecoBot v2.0 — Rule-Based AI Chatbot

A rule-based AI chatbot built in Python as part of the **DecodeLabs Internship – AI Project 1**. DecoBot understands user intent through keyword matching, fuzzy matching (typo tolerance), and remembers the user's name during a session.

## ✨ Features

- **Intent-based responses** — recognizes topics like greetings, AI/Python/ML knowledge, jokes, and coding tips
- **Fuzzy matching** — tolerates small typos (e.g., "helo" → "hello")
- **Word-boundary keyword detection** — avoids false matches (e.g., "ai" won't trigger inside unrelated words)
- **Name memory** — detects "my name is ___" and remembers it for the session
- **Dynamic help command** — automatically lists all available topics
- **Chat history logging** — saves the full conversation to `chat_history.json` after each session
- **Colored terminal output** for a cleaner CLI experience

## 🛠️ Requirements

- Python 3.7+
- No external libraries required (uses only the standard library)

## ▶️ How to Run

```bash
python3 decobot.py
```

## 💬 Example Commands

| Input | Response Type |
|---|---|
| `hello` | Greeting |
| `what is AI` | AI knowledge |
| `what is python` | Python knowledge |
| `joke` | Random joke |
| `my name is Ali` | Remembers your name |
| `help` | Lists all topics you can ask about |
| `quit` | Ends the session and shows a summary |

## 📁 Project Structure

```
decobot-ai-chatbot/
├── decobot.py          # Main chatbot script
├── chat_history.json   # Auto-generated conversation log (ignored in git)
└── README.md
```

## 👤 Author

Muhammad Talha— DecodeLabs Internship, AI Project 1

## 📄 License

This project is for educational purposes as part of an internship assignment.

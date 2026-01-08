# project_01_assistant.py
# Project 01: Personal Console Assistant (v4.0)

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load .env (local only) and create OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store todo.json рядом со скриптом (не зависит от папки запуска)
TODO_FILE = Path(__file__).with_name("todo.json")


def load_todo() -> list[str]:
    if not TODO_FILE.exists():
        return []
    try:
        data = json.loads(TODO_FILE.read_text(encoding="utf-8"))
        if isinstance(data, list) and all(isinstance(x, str) for x in data):
            return data
    except Exception:
        pass
    return []


def save_todo(todo: list[str]) -> None:
    TODO_FILE.write_text(
        json.dumps(todo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def ask_text(prompt: str, default: str | None = None) -> str:
    text = input(prompt).strip()
    if text == "" and default is not None:
        return default
    return text


def ask_int(prompt: str, min_value: int | None = None, max_value: int | None = None) -> int:
    while True:
        raw = input(prompt).strip()
        if raw.lstrip("-").isdigit():
            value = int(raw)

            if min_value is not None and value < min_value:
                print(f"Введите число не меньше {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Введите число не больше {max_value}.")
                continue

            return value

        print("Пожалуйста, введи целое число (например 30 или -2).")


def show_menu() -> None:
    print("\nЧто ты хочешь сделать?")
    print("1 — Узнать текущее настроение")
    print("2 — Получить совет")
    print("3 — Мини-калькулятор (сложение)")
    print("4 — Список дел (To-Do)")
    print("5 — Выйти")
    print("6 — Спросить ИИ")


def handle_mood() -> None:
    mood = ask_int("Какое у тебя настроение (1-10)? ", min_value=1, max_value=10)
    print(f"Понял тебя. Настроение: {mood}/10. Спасибо, что поделился!")


def handle_advice() -> None:
    print("Мой совет: учись регулярно по 20–30 минут в день — это сильнее, чем редкие марафоны 🙂")


def handle_sum() -> None:
    a = ask_int("Введи первое число: ")
    b = ask_int("Введи второе число: ")
    print(f"Результат: {a} + {b} = {a + b}")


def handle_ai_question() -> None:
    question = ask_text("Спроси у ИИ: ")
    if not question:
        print("Вопрос пустой.")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("Ключ OPENAI_API_KEY не найден. Проверь файл .env (он должен быть рядом со скриптом).")
        return

    print("Думаю... 🤖")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты дружелюбный и краткий помощник. Отвечай по-русски."},

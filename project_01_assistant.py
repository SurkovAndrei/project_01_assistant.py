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
            {"role": "user", "content": question},
        ],
    )

    answer = response.choices[0].message.content
    print("\nОтвет ИИ:\n")
    print(answer)


def handle_todo(todo: list[str]) -> None:
    while True:
        print("\nTo-Do меню:")
        print("1 — Показать список")
        print("2 — Добавить задачу")
        print("3 — Удалить задачу по номеру")
        print("4 — Назад")

        choice = ask_text("Выбери номер: ")

        if choice == "1":
            if not todo:
                print("Список дел пуст.")
            else:
                print("Твои задачи:")
                for i, item in enumerate(todo, start=1):
                    print(f"{i}. {item}")

        elif choice == "2":
            task = ask_text("Введи задачу: ")
            if task:
                todo.append(task)
                save_todo(todo)
                print("Добавлено.")
            else:
                print("Пустую задачу не добавляем 🙂")

        elif choice == "3":
            if not todo:
                print("Список пуст — нечего удалять.")
                continue
            index = ask_int("Номер задачи для удаления: ", min_value=1, max_value=len(todo))
            removed = todo.pop(index - 1)
            save_todo(todo)
            print(f"Удалено: {removed}")

        elif choice == "4":
            break

        else:
            print("Не понял выбор. Введи 1, 2, 3 или 4.")


def main() -> None:
    print("Привет! Я твой персональный помощник 🙂")

    name = ask_text("Как тебя зовут? ", default="друг")
    print(f"Приятно познакомиться, {name}!")

    age = ask_int("Сколько тебе лет? ", min_value=0, max_value=120)
    if age < 18:
        print("Ты ещё несовершеннолетний.")
    else:
        print("Ты уже взрослый человек.")

    todo: list[str] = load_todo()

    while True:
        show_menu()
        choice = ask_text("Выбери номер: ")

        if choice == "1":
            handle_mood()

        elif choice == "2":
            handle_advice()

        elif choice == "3":
            handle_sum()

        elif choice == "4":
            handle_todo(todo)

        elif choice == "5":
            print(f"Пока, {name}! Увидимся 🙂")
            break

        elif choice == "6":
            handle_ai_question()

        else:
            print("Не понял выбор. Введи 1, 2, 3, 4, 5 или 6.")


if __name__ == "__main__":
    main()

# project_01_assistant.py
# Project 01: Personal Console Assistant (v2.0)

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


def handle_mood() -> None:
    mood = ask_int("Какое у тебя настроение (1-10)? ", min_value=1, max_value=10)
    print(f"Понял тебя. Настроение: {mood}/10. Спасибо, что поделился!")


def handle_advice() -> None:
    print("Мой совет: учись регулярно по 20–30 минут в день — это сильнее, чем редкие марафоны 🙂")


def handle_sum() -> None:
    a = ask_int("Введи первое число: ")
    b = ask_int("Введи второе число: ")
    print(f"Результат: {a} + {b} = {a + b}")


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
                print("Добавлено.")
            else:
                print("Пустую задачу не добавляем 🙂")

        elif choice == "3":
            if not todo:
                print("Список пуст — нечего удалять.")
                continue
            index = ask_int("Номер задачи для удаления: ", min_value=1, max_value=len(todo))
            removed = todo.pop(index - 1)
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

    todo: list[str] = []

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
        else:
            print("Не понял выбор. Введи 1, 2, 3, 4 или 5.")


if __name__ == "__main__":
    main()

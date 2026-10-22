"""Главное меню лабораторной работы № 2. Остальная логика вынесена в отдельные модули."""

import cameraProperties
import cameraTest
import cameraModes
import motionDetection
import compareResolution


def print_menu() -> None:
    print("\n========== ЛАБОРАТОРНАЯ РАБОТА № 2 ==========")
    print("1 - Настройка камеры")
    print("2 - Проверка камеры (просмотр видео)")
    print("3 - Проверка разрешений и измерение FPS")
    print("4 - Обнаружение движения")
    print("5 - Сравнение разрешений")
    print("0 - Выход из программы")


def main() -> None:
    actions = {
        "1": cameraProperties.run,
        "2": cameraTest.run,
        "3": cameraModes.run,
        "4": motionDetection.run,
        "5": compareResolution.run,
    }

    while True:
        print_menu()
        try:
            choice = input("Выбери действие: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nРабота программы завершена.")
            break

        if choice == "0":
            print("Работа программы завершена.")
            break

        action = actions.get(choice)
        if action is None:
            print("Неизвестный пункт меню. Введи число от 0 до 5.")
            continue

        try:
            action()
        except Exception as error:
            print(f"Во время выполнения режима возникла ошибка: {error}")
            print("Возврат в главное меню.")


main()

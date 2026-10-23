"""Главное меню лабораторной работы № 2. Остальная логика вынесена в отдельные модули."""
import camera4Modes
import cameraProperties
import cameraTest
import cameraModes
import motionDetection
import compareResolution


def print_menu() -> None:
    print("\nМеню лабораторной работы")
    print("1 - Настройка камеры")
    print("2 - Проверка камеры (просмотр видео)")
    print("3 - Проверка разрешений и измерение FPS")
    print("4 - Обнаружение движения")
    print("5 - Сравнение 2 разрешений с отображением камеры")
    print("6 - Тестирование 4-х режимов без отображения камеры")
    print("0 - Выход из программы")


def main() -> None:
    actions = {
        "1": cameraProperties.run,
        "2": cameraTest.run,
        "3": cameraModes.run,
        "4": motionDetection.run,
        "5": compareResolution.run,
        "6": camera4Modes.run
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

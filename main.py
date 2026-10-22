import cv2
import numpy as np


def main():
    # Шаг 1-3: Инициализация камеры (аналог videoinput в MATLAB)
    # Индекс 0 обычно соответствует встроенной или первой подключенной веб-камере
    cap = cv2.VideoCapture(0)

    # Настройка разрешения (например, 1280x720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Ошибка: Не удалось открыть видеокамеру.")
        return

    # Вывод информации о текущих параметрах камеры
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Параметры камеры: Разрешение {int(width)}x{int(height)}, FPS: {fps}")
    print("Запуск захвата кадров и детектирования движения. Нажмите 'q' для выхода.")

    # Чтение первого кадра для инициализации разностного метода
    ret, prev_frame = cap.read()
    if not ret:
        print("Не удалось получить первый кадр.")
        cap.release()
        return

    # Перевод в полутоновое изображение (grayscale)
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Порог чувствительности (можно корректировать для устранения шумов)
    threshold_value = 25

    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Ошибка чтения кадра.")
            break

        frame_counter += 1

        # Шаг 6: Обработка последовательности кадров (разностный метод)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Вычисление абсолютной разности между текущим и предыдущим кадрами (аналог imabsdiff)
        diff_im = cv2.absdiff(prev_gray, gray)

        # Пороговая обработка для выделения областей движения
        _, thresh = cv2.threshold(diff_im, threshold_value, 255, cv2.THRESH_BINARY)

        # Вывод результатов в окна
        cv2.imshow('Original Video Stream', frame)
        cv2.imshow('Motion Detection (Binary)', thresh)

        # Обновляем предыдущий кадр
        prev_gray = gray.copy()

        # Остановка после 300 обработанных кадров (опционально) или по нажатию клавиши 'q'
        if cv2.waitKey(30) & 0xFF == ord('q') or frame_counter >= 300:
            break

    # Шаг 9: Очистка ресурсов
    cap.release()
    cv2.destroyAllWindows()
    print("Работа программы завершена, ресурсы освобождены.")


if __name__ == "__main__":
    main()
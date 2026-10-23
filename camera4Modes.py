import cv2
import time
import csv

# Четыре разрешения из задания
resolutions = [
    (320, 240),
    (640, 480),
    (1280, 720),
    (1920, 1080)
]

camera_index = 0
frames_to_capture = 60
results = []

for requested_width, requested_height in resolutions:
    print("\n" + "=" * 45)
    print(f"Запрошенное разрешение: "
          f"{requested_width}x{requested_height}")

    # Подключаем камеру через DirectShow
    camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

    if not camera.isOpened():
        print("Не удалось открыть камеру.")
        camera.release()
        continue

    # Пробуем использовать MJPEG — он может позволить
    # получить более высокое разрешение камеры
    camera.set(
        cv2.CAP_PROP_FOURCC,
        cv2.VideoWriter_fourcc(*"MJPG")
    )

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, requested_width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, requested_height)

    # Даём драйверу время применить настройки
    time.sleep(1)

    # Читаем несколько кадров для стабилизации
    for _ in range(10):
        success, frame = camera.read()
        if not success:
            break

    if not success:
        print("Не удалось получить кадр.")
        camera.release()
        continue

    actual_height, actual_width = frame.shape[:2]

    print(f"Фактическое разрешение: "
          f"{actual_width}x{actual_height}")

    # Измеряем частоту захвата кадров
    frame_count = 0
    start_time = time.perf_counter()

    for _ in range(frames_to_capture):
        success, frame = camera.read()

        if not success:
            print("Ошибка при получении кадра.")
            break

        frame_count += 1

    elapsed_time = time.perf_counter() - start_time
    fps = frame_count / elapsed_time if elapsed_time > 0 else 0

    # Считаем объём данных одного кадра
    pixels = actual_width * actual_height

    print(f"Получено кадров: {frame_count}")
    print(f"Время захвата: {elapsed_time:.2f} с")
    print(f"Средний FPS: {fps:.2f}")
    print(f"Количество пикселей: {pixels:,}")

    if (actual_width, actual_height) == (
        requested_width, requested_height
    ):
        status = "Режим установлен"
    else:
        status = "Камера использует другое разрешение"

    print(f"Результат: {status}")

    results.append({
        "Запрошенное разрешение":
            f"{requested_width}x{requested_height}",
        "Фактическое разрешение":
            f"{actual_width}x{actual_height}",
        "Кадров": frame_count,
        "Время, с": round(elapsed_time, 2),
        "FPS": round(fps, 2),
        "Пикселей": pixels,
        "Результат": status
    })

    camera.release()

# Сохраняем результаты
if results:
    with open(
        "camera_resolution_results.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=results[0].keys(),
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(results)

    print("\n" + "=" * 45)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("Результаты сохранены в "
          "camera_resolution_results.csv")
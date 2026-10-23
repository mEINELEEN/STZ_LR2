"""Режим 3: проверка разрешений и измерение скорости получения кадров."""

import time
import cv2
from cameraUtils import open_camera, close_camera, is_exit_key, show_camera_error


MODES = [(320, 240), (640, 480), (1280, 720), (1920, 1080)]


def run() -> None:
    camera = open_camera()
    if not camera.isOpened():
        show_camera_error(camera)
        return

    try:
        for requested_width, requested_height in MODES:
            print(f"\nЗапрашиваем режим {requested_width}x{requested_height}")
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, requested_width)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, requested_height)
            time.sleep(0.5)

            # После изменения режима пропускаем несколько кадров для стабилизации.
            for _ in range(5):
                camera.read()

            frame_count = 0
            actual_width = 0
            actual_height = 0
            start_time = time.perf_counter()
            cancelled = False

            print("Измеряем получение 60 кадров. Q или Esc — назад в меню.")
            while frame_count < 60:
                success, frame = camera.read()
                if not success:
                    print("Не удалось получить кадр.")
                    break

                actual_height, actual_width = frame.shape[:2]
                cv2.putText(
                    frame,
                    f"{actual_width}x{actual_height} | frames: {frame_count}/60",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2
                )
                cv2.imshow("Проверка режимов - Q: назад в меню", frame)
                frame_count += 1

                if is_exit_key(cv2.waitKey(1) & 0xFF):
                    cancelled = True
                    break

            elapsed = time.perf_counter() - start_time
            measured_fps = frame_count / elapsed if elapsed > 0 else 0
            print(f"Фактическое разрешение: {actual_width}x{actual_height}")
            print(f"Получено кадров: {frame_count}")
            print(f"Время измерения: {elapsed:.2f} с")
            print(f"Измеренная частота: {measured_fps:.2f} FPS")

            if cancelled:
                print("Тест прерван. Возвращаемся в меню.")
                break
    finally:
        close_camera(camera)

    print("Проверка режимов завершена. Возврат в меню.")


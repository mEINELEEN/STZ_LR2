"""Режим 5: сравнение производительности обнаружения движения при двух разрешениях."""

import time
import cv2
from cameraUtils import open_camera, close_camera, is_exit_key, show_camera_error


MODES = [(320, 240), (1280, 720)]
TEST_DURATION_SECONDS = 5.0


def run() -> None:
    camera = open_camera()
    if not camera.isOpened():
        show_camera_error(camera)
        return

    try:
        for requested_width, requested_height in MODES:
            print(f"\nТестируем режим {requested_width}x{requested_height}")
            print(f"Длительность теста: около {TEST_DURATION_SECONDS:.0f} секунд")
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, requested_width)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, requested_height)
            time.sleep(0.5)

            success, first_frame = camera.read()
            if not success:
                print("Не удалось получить начальный кадр.")
                continue

            previous_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
            actual_height, actual_width = first_frame.shape[:2]
            frames = 0
            cancelled = False
            start_time = time.perf_counter()

            while time.perf_counter() - start_time < TEST_DURATION_SECONDS:
                success, frame = camera.read()
                if not success:
                    print("Не удалось получить кадр.")
                    break

                actual_height, actual_width = frame.shape[:2]
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                difference = cv2.absdiff(previous_gray, gray)
                difference = cv2.GaussianBlur(difference, (5, 5), 0)
                _, mask = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
                mask = cv2.dilate(mask, None, iterations=2)

                contours, _ = cv2.findContours(
                    mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )
                for contour in contours:
                    if cv2.contourArea(contour) > 700:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                frames += 1
                elapsed = time.perf_counter() - start_time
                fps = frames / elapsed if elapsed > 0 else 0
                cv2.putText(
                    frame,
                    f"{actual_width}x{actual_height} | FPS: {fps:.1f}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                )
                cv2.imshow("Сравнение разрешений - Q: меню", frame)
                cv2.imshow("Маска изменений", mask)
                previous_gray = gray.copy()

                if is_exit_key(cv2.waitKey(1) & 0xFF):
                    cancelled = True
                    break

            total_time = time.perf_counter() - start_time
            measured_fps = frames / total_time if total_time > 0 else 0
            print(f"Фактическое разрешение: {actual_width}x{actual_height}")
            print(f"Обработано кадров: {frames}")
            print(f"Время: {total_time:.2f} с")
            print(f"Скорость обработки: {measured_fps:.2f} FPS")

            if cancelled:
                print("Сравнение прервано. Возвращаемся в меню.")
                break
    finally:
        close_camera(camera)

    print("Сравнение разрешений завершено. Возврат в меню.")

"""Режим 4: обнаружение движения методом разности последовательных кадров."""

import cv2
from cameraUtils import open_camera, close_camera, is_exit_key, show_camera_error


def run() -> None:
    camera = open_camera()
    if not camera.isOpened():
        show_camera_error(camera)
        return

    try:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        success, first_frame = camera.read()
        if not success:
            print("Не удалось получить первый кадр.")
            return

        previous_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
        print("\nОбнаружение движения запущено.")
        print("Нажми Q или Esc в окне видео, чтобы вернуться в меню.")

        while True:
            success, frame = camera.read()
            if not success:
                print("Не удалось получить кадр.")
                break

            current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            difference = cv2.absdiff(previous_gray, current_gray)
            difference = cv2.GaussianBlur(difference, (5, 5), 0)
            _, mask = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
            mask = cv2.dilate(mask, None, iterations=2)

            contours, _ = cv2.findContours(
                mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            motion_found = False
            for contour in contours:
                if cv2.contourArea(contour) > 700:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    motion_found = True

            status = "Movement detected" if motion_found else "No movement"
            color = (0, 0, 255) if motion_found else (255, 255, 255)
            cv2.putText(
                frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
            )
            cv2.imshow("Обнаружение движения - Q: меню", frame)
            cv2.imshow("Маска изменений - Q: меню", mask)

            previous_gray = current_gray.copy()
            if is_exit_key(cv2.waitKey(1) & 0xFF):
                break
    finally:
        close_camera(camera)

    print("Обнаружение движения завершено. Возврат в меню.")

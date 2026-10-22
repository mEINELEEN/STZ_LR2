"""Режим 2: проверка камеры и просмотр изображения."""

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

        width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        reported_fps = camera.get(cv2.CAP_PROP_FPS)

        print("\nКамера успешно подключена.")
        print(f"Ширина: {width:.0f}")
        print(f"Высота: {height:.0f}")
        if reported_fps > 0:
            print(f"FPS по данным драйвера: {reported_fps:.2f}")
        else:
            print("FPS по данным драйвера не определён; измерить его можно в пункте 3.")
        print("Нажми Q или Esc в окне видео, чтобы вернуться в меню.")

        while True:
            success, frame = camera.read()
            if not success:
                print("Не удалось получить кадр.")
                break

            actual_height, actual_width = frame.shape[:2]
            cv2.putText(
                frame,
                f"{actual_width}x{actual_height} | Q: menu",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
            )
            cv2.imshow("Проверка камеры - Q: назад в меню", frame)
            if is_exit_key(cv2.waitKey(1) & 0xFF):
                break
    finally:
        close_camera(camera)

    print("Проверка камеры завершена. Возврат в меню.")

"""Режим 1: открытие настроек драйвера и предпросмотра камеры."""

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

        print("\nРежим настройки камеры.")
        print("Если окно настроек драйвера появилось, измени нужные параметры.")
        print("Нажми Q или Esc в окне предпросмотра, чтобы вернуться в меню.")
        settings_opened = camera.set(cv2.CAP_PROP_SETTINGS, 1)
        if not settings_opened:
            print("Драйвер не подтвердил открытие окна настроек. Для некоторых камер эта функция недоступна.")

        while True:
            success, frame = camera.read()
            if not success:
                print("Не удалось получить кадр с камеры.")
                break

            cv2.imshow("Настройка камеры - Q: назад в меню", frame)
            if is_exit_key(cv2.waitKey(1) & 0xFF):
                break
    finally:
        close_camera(camera)

    print("Режим настройки завершён. Возврат в меню.")

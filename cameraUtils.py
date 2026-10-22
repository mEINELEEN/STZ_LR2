"""Общие функции для работы с веб-камерой и окнами OpenCV."""

import cv2

CAMERA_INDEX = 0


def open_camera(index: int = CAMERA_INDEX):
    """Открывает камеру. В Windows сначала пробует backend DirectShow."""
    camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(index)

    return camera


def close_camera(camera) -> None:
    """Освобождает камеру и закрывает все окна OpenCV."""
    if camera is not None:
        camera.release()
    cv2.destroyAllWindows()


def is_exit_key(key: int) -> bool:
    """Q или Esc завершают текущий режим и возвращают пользователя в меню."""
    return key in (ord("q"), ord("Q"), 27)


def show_camera_error(camera) -> None:
    print("Не удалось открыть камеру. Проверь подключение и закрой другие программы, использующие камеру.")
    close_camera(camera)

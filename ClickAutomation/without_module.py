import ctypes


def click_xy(x, y):
    user32 = ctypes.windll.user32
    user32.SetCursorPos(x, y)  # Set mouse cursor position
    user32.mouse_event(2, 0, 0, 0, 0)  # Left mouse button down
    user32.mouse_event(4, 0, 0, 0, 0)  # Left mouse button up


if __name__ == "__main__":
    click_xy(10, 11)

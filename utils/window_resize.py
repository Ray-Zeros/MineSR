import ctypes

user32 = ctypes.windll.user32

SW_RESTORE = 9
SWP_FLAGS = 0x0004 | 0x0010  # SWP_NOZORDER | SWP_NOACTIVATE
MINECRAFT_KEYWORDS = ("minecraft",)


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def _get_window_text(hwnd):
    length = user32.GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def _get_window_rect(hwnd):
    rect = RECT()
    if not user32.GetWindowRect(hwnd, ctypes.byref(rect)):
        raise RuntimeError("GetWindowRect failed")
    return rect


def _get_client_size(hwnd):
    client_rect = RECT()
    if not user32.GetClientRect(hwnd, ctypes.byref(client_rect)):
        raise RuntimeError("GetClientRect failed")
    width = client_rect.right - client_rect.left
    height = client_rect.bottom - client_rect.top
    return width, height


def resize_window_client_area(hwnd, client_width, client_height):
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)

    current_client_width, current_client_height = _get_client_size(hwnd)
    if current_client_width == client_width and current_client_height == client_height:
        return

    window_rect = _get_window_rect(hwnd)
    current_window_width = window_rect.right - window_rect.left
    current_window_height = window_rect.bottom - window_rect.top

    border_width = current_window_width - current_client_width
    border_height = current_window_height - current_client_height

    target_window_width = client_width + border_width
    target_window_height = client_height + border_height

    ok = user32.SetWindowPos(
        hwnd,
        None,
        window_rect.left,
        window_rect.top,
        target_window_width,
        target_window_height,
        SWP_FLAGS,
    )
    if not ok:
        raise RuntimeError("SetWindowPos failed")


def resize_minecraft_window(
    client_width=1280,
    client_height=720,
):
    hwnd = user32.GetForegroundWindow()
    if not hwnd or not user32.IsWindow(hwnd):
        return False, "Foreground window is not Minecraft"

    title = _get_window_text(hwnd)
    title_lower = title.lower()
    if not title or not any(kw in title_lower for kw in MINECRAFT_KEYWORDS):
        return False, "Foreground window is not Minecraft"

    try:
        resize_window_client_area(hwnd, client_width, client_height)
    except Exception as exc:
        return False, str(exc)

    return True, "Window size processed"

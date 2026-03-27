import os
SPREAD_ERROR_KEYWORDS = ("空间过小", "too many entities")


def init_log_cursor(log_path):
    if not os.path.exists(log_path):
        return None
    return os.path.getsize(log_path)


def check_spread_exception(log_path, start_pos):
    if not os.path.exists(log_path):
        return start_pos, None

    pos = max(0, int(start_pos or 0))
    with open(log_path, "r", encoding="gbk", errors="ignore") as f:
        f.seek(pos)
        lines = f.readlines()
        pos = f.tell()

    for line in lines:
        clean_line = line.strip()
        if clean_line and any(k in clean_line for k in SPREAD_ERROR_KEYWORDS):
            return pos, clean_line

    return pos, None

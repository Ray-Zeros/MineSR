import logging
from datetime import datetime
from pathlib import Path


def build_timestamped_log_file(log_prefix):
    prefix_path = Path(log_prefix)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix_name = prefix_path.stem if prefix_path.suffix else prefix_path.name
    return str(prefix_path.with_name(f"{timestamp}_{prefix_name}.log"))


def get_logger(name, log_file, include_console=False):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    if include_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_file, encoding="utf-8", delay=True)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
import pyautogui
import json
import time
from utils.config_loader import load_config
from utils.window_resize import resize_minecraft_window
from utils.logger_utils import build_timestamped_log_file, get_logger

CONFIG_SCHEMA = [
    {"name": "input_file", "type": "str", "default": "./data/coords_list_1_0_0.json", "help": "Input task JSON"},
    {"name": "log_suffix", "type": "str", "default": "./logs/capture", "help": "Capture log suffix"},
    {"name": "lr_res", "type": "int_pair", "default": [480, 270], "help": "Target window resolution"},
    {"name": "hr_res", "type": "int_pair", "default": [1920, 1080], "help": "High-resolution value, used only for logging, requires manual input in the Resolution Control Menu"},
    {"name": "wait_time", "type": "float", "default": 3.5, "help": "Wait time before every doubled-screenshot"},
    {"name": "mod_key", "type": "str", "default": "]", "help": "Resolution Control Mod screenshot hotkey"},
    {"name": "mc_key", "type": "str", "default": "f2", "help": "Minecraft screenshot hotkey"},
]

# 3840x2160 1920x1080 960x540 480x270
# 2560x1440 1280x720 640x360 320x180

def send_cmd(cmd):
    pyautogui.press('t')
    pyautogui.write(cmd)
    pyautogui.press('enter')

def run_capture(cfg):
    input_file = cfg["input_file"]
    log_suffix = cfg["log_suffix"]
    log_file = build_timestamped_log_file(log_suffix)
    lr_res = cfg["lr_res"]
    hr_res = cfg["hr_res"]
    wait_time = cfg["wait_time"]
    mod_key = cfg["mod_key"]
    mc_key = cfg["mc_key"]

    logger = get_logger("capture", log_file, include_console=True)
    start_time = time.perf_counter()

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error("The coordinate list file was NOT found. Please run the generator script first.")
        return
    
    
    config = data.get("config", {})
    coords = data.get("coords", [])

    enable_y = bool(config.get("enable_y", False))

    logger.info(
        "Capture started: input=%s, total=%d, enable_y=%s, wait_time=%.2f, lr_res=%sx%s, hr_res=%sx%s",
        input_file,
        len(coords),
        enable_y,
        wait_time,
        lr_res[0],
        lr_res[1],
        hr_res[0],
        hr_res[1],
    )

    logger.info("Script will start in 5 seconds. Please click into the Minecraft window and press F1 to hide the GUI")
    time.sleep(5)

    ok, message = resize_minecraft_window(
            client_width=lr_res[0],
            client_height=lr_res[1],
        )
    if not ok:
        logger.error("Window resizing failed: %s", message)
        return

    logger.info("Window resizing successful: %s", message)

    for entry in coords:
        biome_name = entry.get("biome", "Unknown")
        print(f"Processing data id {entry['id']}, current biome: {biome_name}...")

        send_cmd(f"/weather clear")
        
        y_value = entry.get("y", None)
        use_exact_y = False
        parsed_y = None

        if enable_y and y_value is not None:
            try:
                parsed_y = int(y_value)
                use_exact_y = True
            except (TypeError, ValueError):
                logger.error("Invalid y for ID %s, y=%r. This record is skipped.", entry.get("id", "Unknown"), y_value)
                continue

        if use_exact_y:
            send_cmd(f"/tp @s {entry['x']} {parsed_y} {entry['z']} {entry['yaw']} {entry['pitch']}")
        else:
            # Fallback path: use surface placement when y is disabled or y is null.
            send_cmd(f"/tp @s {entry['x']} ~ {entry['z']} {entry['yaw']} {entry['pitch']}") # load chunk
            send_cmd(f"/execute positioned {entry['x']} 0 {entry['z']} positioned over ocean_floor run tp @s ~ ~ ~ {entry['yaw']} {entry['pitch']}")

            # send_cmd(f"/spreadplayers {entry['x']} {entry['z']} 0 1 false @s")
            # send_cmd(f"/tp @s {entry['x']} ~ {entry['z']} {entry['yaw']} {entry['pitch']}")
        
        send_cmd(f"/time set {entry['time']}")

        time.sleep(wait_time)

        # 截图
        pyautogui.hotkey(mc_key, mod_key)
        
        logger.info("Screenshots for ID %s are complete", entry["id"])
        time.sleep(0.1)
        
    elapsed = time.perf_counter() - start_time
    logger.info("Data collection is complete. Total time: %.2f seconds. Total records processed: %d", elapsed, len(coords))

if __name__ == "__main__":
    config = load_config(
        schema=CONFIG_SCHEMA,
        description="Minecraft sample screenshot script",
    )
    run_capture(config)
import json
import random
import csv
from utils.config_loader import load_config

CONFIG_SCHEMA = [
    {"name": "total_samples", "type": "int", "default": 1, "help": "Total number of samples, i.e., how many pairs of screenshots to capture."},
    {"name": "seed", "type": "int", "default": 5277617577473417202, "allow_none": False, "help": "Map seed (required non-null integer, used for recording/reproducibility)"},
    {"name": "enable_y", "type": "bool", "default": False, "help": "Whether to enable Y-axis coordinates"},
    {"name": "random_y", "type": "bool", "default": False, "help": "When enable_y is true in auto mode, whether to randomly generate y; if false, y will be null"},
    {"name": "enable_manual", "type": "bool", "default": False, "help": "Whether to enable manual input mode, if enabled, the script will read coordinates from a CSV file instead of generating them randomly"},
    {"name": "manual_csv_file", "type": "str", "default": "./data/coords_1_0_0.csv", "help": "Manual task input CSV"},
    {"name": "biomes_csv_file", "type": "str", "default": "./data/biomes_1_0_0.csv", "help": "Biome center input CSV"},
    {"name": "coordinate_offset", "type": "int", "default": 200, "help": "Random offset radius from the center point during auto-generation(±N)"},
    {"name": "yaw_range", "type": "int_pair", "default": [-180, 180], "help": "Random range for yaw, format [min, max]"},
    {"name": "pitch_range", "type": "int_pair", "default": [-30, 60], "help": "Random range for pitch, format [min, max]"},
    {"name": "time_points", "type": "str", "default": "1000,6000,13000,18000", "help": "Optional time points, comma-separated"},
    {"name": "output_file", "type": "str", "default": "./data/coords_list_1_0_0.json", "help": "Output JSON path"},
]


def _load_biomes(biomes_csv_file):
    required_columns = ["biome", "x", "z"]

    with open(biomes_csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        if fieldnames != required_columns:
            raise ValueError(
                f"BIOME CSV column order does not match, expected order: {required_columns}, actual: {fieldnames}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("BIOME CSV cannot be empty")

    biomes = []
    for index, row in enumerate(rows):
        biome = str(row["biome"]).strip()
        if not biome:
            raise ValueError(f"BIOME CSV row {index + 1} has an empty biome")

        try:
            x = int(row["x"])
            z = int(row["z"])
        except ValueError as exc:
            raise ValueError(
                f"BIOME CSV row {index + 1} has invalid x/z values, must be integers, actual: x={row['x']} z={row['z']}"
            ) from exc

        biomes.append((biome, x, z))

    return biomes


def _load_biome_coords(
    biomes_csv_file,
    total_samples,
    coordinate_offset,
    yaw_min,
    yaw_max,
    pitch_min,
    pitch_max,
    time_points,
    enable_y,
    random_y,
):
    biomes = _load_biomes(biomes_csv_file)
    coords_list = []

    biome_count = len(biomes)
    samples_per_biome = total_samples // biome_count
    extra_samples = total_samples % biome_count

    sample_id = 0
    for biome_index, (biome_name, base_x, base_z) in enumerate(biomes):
        # Distribute remainder by biome order to ensure total sample count is exact.
        current_count = samples_per_biome + (1 if biome_index < extra_samples else 0)

        for _ in range(current_count):
            x = base_x + random.randint(-coordinate_offset, coordinate_offset)
            z = base_z + random.randint(-coordinate_offset, coordinate_offset)

            yaw = random.uniform(yaw_min, yaw_max)
            pitch = random.uniform(pitch_min, pitch_max)

            time_point = random.choice(time_points)

            coords_list.append(
                _build_coord_entry(
                    sample_id=sample_id,
                    biome_name=biome_name,
                    x=x,
                    z=z,
                    yaw=yaw,
                    pitch=pitch,
                    time_point=time_point,
                    enable_y=enable_y,
                    random_y=random_y,
                )
            )
            sample_id += 1

    return coords_list


def _get_manual_seed(seed):
    if seed is None:
        raise ValueError("Please fill in the SEED manually")
    if not isinstance(seed, int):
        raise ValueError("SEED must be an integer")
    return seed


def _required_columns(enable_y):
    columns = ["id", "biome", "yaw", "pitch", "time", "x", "z"]
    if enable_y:
        columns.append("y")
    return columns


def _build_coord_entry(sample_id, biome_name, x, z, yaw, pitch, time_point, enable_y, random_y):
    entry = {
        "id": sample_id,
        "biome": biome_name,
        "yaw": round(yaw, 2),
        "pitch": round(pitch, 2),
        "time": time_point,
        "x": x,
        "z": z,
    }
    if enable_y:
        if random_y:
            entry["y"] = random.randint(-64, 319)
        else:
            entry["y"] = None
    return entry


def _parse_manual_row(row, enable_y):
    entry = {
        "id": int(row["id"]),
        "biome": row["biome"],
        "yaw": round(float(row["yaw"]), 2),
        "pitch": round(float(row["pitch"]), 2),
        "time": int(row["time"]),
        "x": int(row["x"]),
        "z": int(row["z"]),
    }
    if enable_y:
        y_value = int(row["y"])
        if y_value < -64 or y_value > 319:
            raise ValueError("CSV y value is out of range, must be between -64 and 319")
        entry["y"] = y_value
    return entry


def _load_manual_coords(manual_csv_file, total_samples, enable_y):
    required_columns = _required_columns(enable_y)

    with open(manual_csv_file, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        if len(fieldnames) != len(required_columns):
            raise ValueError(
                f"CSV column count does not match, expected {len(required_columns)} columns: {required_columns}"
            )

        if fieldnames != required_columns:
            raise ValueError(
                f"CSV column order does not match, expected order: {required_columns}, actual: {fieldnames}"
            )

        missing = [name for name in required_columns if name not in fieldnames]
        extra = [name for name in fieldnames if name not in required_columns]
        if missing or extra:
            raise ValueError(
                f"CSV column names do not match, missing: {missing}, extra: {extra}, expected columns: {required_columns}"
            )

        rows = list(reader)

    if len(rows) != total_samples:
        raise ValueError(
            f"CSV row count does not match, expected {total_samples} rows, got {len(rows)}"
        )

    coords_list = []
    for row in rows:
        coords_list.append(_parse_manual_row(row, enable_y))
    return coords_list


def _normalize_range(name, value_pair):
    min_value, max_value = int(value_pair[0]), int(value_pair[1])
    if min_value > max_value:
        raise ValueError(f"{name} minimum value cannot be greater than maximum value, actual: {value_pair}")
    return min_value, max_value


def _parse_time_points(time_points):
    if isinstance(time_points, str):
        parts = [part.strip() for part in time_points.split(",") if part.strip()]
    elif isinstance(time_points, (list, tuple)):
        parts = [str(part).strip() for part in time_points if str(part).strip()]
    else:
        raise ValueError("time_points must be a comma-separated string")

    if not parts:
        raise ValueError("time_points cannot be empty")

    parsed = []
    for part in parts:
        try:
            parsed.append(int(part))
        except ValueError as exc:
            raise ValueError(f"time_points contains invalid integer: {part}") from exc

    return parsed

def generate_list(cfg):
    total_samples = cfg["total_samples"]
    seed = _get_manual_seed(cfg["seed"])
    enable_y = cfg["enable_y"]
    random_y = cfg["random_y"]
    enable_manual = cfg["enable_manual"]
    manual_csv_file = cfg["manual_csv_file"]
    biomes_csv_file = cfg["biomes_csv_file"]
    coordinate_offset = cfg["coordinate_offset"]
    yaw_min, yaw_max = _normalize_range("yaw_range", cfg["yaw_range"])
    pitch_min, pitch_max = _normalize_range("pitch_range", cfg["pitch_range"])
    time_points = _parse_time_points(cfg["time_points"])
    output_file = cfg["output_file"]

    if coordinate_offset < 0:
        raise ValueError("coordinate_offset cannot be a negative number")

    random.seed(seed)

    # random_y only applies in auto mode with enable_y=true.
    bool_random_y = bool(enable_y and random_y and (not enable_manual))

    if enable_manual:
        coords_list = _load_manual_coords(manual_csv_file, total_samples, enable_y)
    else:
        coords_list = _load_biome_coords(
            biomes_csv_file=biomes_csv_file,
            total_samples=total_samples,
            coordinate_offset=coordinate_offset,
            yaw_min=yaw_min,
            yaw_max=yaw_max,
            pitch_min=pitch_min,
            pitch_max=pitch_max,
            time_points=time_points,
            enable_y=enable_y,
            random_y=bool_random_y,
        )

    output_config = {
        "total_samples": total_samples,
        "enable_y": enable_y,
        "random_y": bool_random_y,
        "enable_manual": enable_manual,
        "seed": seed,
        "coordinate_offset": coordinate_offset,
        "yaw_range": [yaw_min, yaw_max],
        "pitch_range": [pitch_min, pitch_max],
        "time_points": time_points,
    }
    if enable_manual:
        output_config["manual_csv_file"] = manual_csv_file
    else:
        output_config["biomes_csv_file"] = biomes_csv_file

    payload = {
        "config": output_config,
        "coords": coords_list
    }
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)
    print(f"Successfully generated {total_samples} coordinate data entries in {output_file}")

if __name__ == "__main__":
    config = load_config(
        schema=CONFIG_SCHEMA,
        description="Minecraft coordinate generating script",
    )
    generate_list(config)
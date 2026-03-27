import argparse
from copy import deepcopy

import yaml


SUPPORTED_TYPES = {"str", "int", "float", "bool", "int_pair"}


def _str_to_bool(value):
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off"}:
        return False

    raise argparse.ArgumentTypeError(f"Unable to parse boolean value: {value}")


def _convert_value(name, value, item):
    value_type = item["type"]
    allow_none = item.get("allow_none", False)

    if value is None:
        if allow_none:
            return None
        raise ValueError(f"Configuration item {name} cannot be null")

    if value_type == "str":
        return str(value)

    if value_type == "int":
        if isinstance(value, bool):
            raise ValueError(f"Configuration item {name} must be an integer")
        return int(value)

    if value_type == "float":
        if isinstance(value, bool):
            raise ValueError(f"Configuration item {name} must be a number")
        return float(value)

    if value_type == "bool":
        return _str_to_bool(value)

    if value_type == "int_pair":
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            raise ValueError(f"The configuration option {name} must be a list of integers of length 2")
        return [int(value[0]), int(value[1])]

    raise ValueError(f"Configuration item {name} uses an unsupported type: {value_type}")


def _load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError("YAML file must be a mapping object at the top level")

    return data


def _build_parser(description, schema):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", type=str, default=None, help="YAML file path")

    for item in schema:
        name = item["name"]
        value_type = item["type"]
        if value_type not in SUPPORTED_TYPES:
            raise ValueError(f"Unsupported type: {value_type}")

        option_names = [f"--{name.replace('_', '-')}"]
        if "_" in name:
            option_names.append(f"--{name}")

        kwargs = {
            "dest": name,
            "default": None,
            "help": item.get("help", ""),
        }

        if value_type == "bool":
            kwargs["type"] = _str_to_bool
        elif value_type == "int_pair":
            kwargs["type"] = int
            kwargs["nargs"] = 2
            kwargs["metavar"] = ("W", "H")
        elif value_type == "int":
            kwargs["type"] = int
        elif value_type == "float":
            kwargs["type"] = float
        else:
            kwargs["type"] = str

        parser.add_argument(*option_names, **kwargs)

    return parser


def load_config(schema, description=""):
    schema_map = {item["name"]: item for item in schema}
    parser = _build_parser(description, schema)
    args = parser.parse_args()

    if not args.config:
        parser.error("Missing required argument: --config <path_to_yaml>")

    final_config = {name: deepcopy(item["default"]) for name, item in schema_map.items()}

    yaml_data = _load_yaml(args.config)
    for key, value in yaml_data.items():
        if key not in schema_map:
            raise ValueError(f"The configuration file contains an unknown field: {key}")
        final_config[key] = _convert_value(key, value, schema_map[key])

    for name, item in schema_map.items():
        cli_value = getattr(args, name)
        if cli_value is None:
            continue

        if item["type"] == "int_pair":
            final_config[name] = [int(cli_value[0]), int(cli_value[1])]
        else:
            final_config[name] = _convert_value(name, cli_value, item)

    return final_config
__author__ = 'tian'

import jsonschema
import logging
import json
import pkg_resources


__SCHEMA_DATA = pkg_resources.resource_string(__name__, "knitting_pattern_schema.json")
# file("./knitting_pattern_schema.json", "rb")
__SCHEMA_DICT = json.loads(__SCHEMA_DATA)


def validate_dict(loaded_json_data):
    """Checks if a dict is a valid Knitpat format.

    Validates if a dict, loaded from a json file, is valid according to the Knitpat scheme.

    Returns:
        True if valid, False if not.
    """
    try:
        jsonschema.validate(loaded_json_data, __SCHEMA_DICT)
        return True
    except Exception as e:
        logging.error(e)
        return False


def parse_ustring(string_data):
    """Parses a string into a dict and validates it."""
    loaded_json_data = json.loads(string_data)
    if validate_dict(loaded_json_data):
        return loaded_json_data
    else:
        raise ValueError("Invalid data string")


def parse_dict_from_cli(cli_dict):
    """Parses from CLI dict into a valid Knitpat."""
    # TODO add parsing for size and measurement.
    parsed_dict = {}
    for k, v in cli_dict.items():
        if k in ["colors"]:
            parsed_dict[k] = int(v)
        else:
            parsed_dict[k] = v
    if validate_dict(parsed_dict):
        return parsed_dict
    else:
        return dict()

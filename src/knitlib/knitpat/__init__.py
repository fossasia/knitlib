__author__ = 'tian'

import jsonschema
import logging
import json
import pkg_resources


__SCHEMA_DATA = pkg_resources.resource_string(__name__, "knitting_pattern_schema.json")
# file("./knitting_pattern_schema.json", "rb")
__SCHEMA_DICT = json.loads(__SCHEMA_DATA)


def validate_dict(loaded_json_data):
    try:
        jsonschema.validate(loaded_json_data, __SCHEMA_DICT)
        return True
    except Exception as e:
        logging.error(e)
        return False


def parse_ustring(string_data):
    loaded_json_data = json.loads(string_data)
    jsonschema.validate(loaded_json_data, __SCHEMA_DICT)
    return loaded_json_data


def parse_dict_from_cli(cli_dict):
    pass

__author__ = 'tian'

import validictory
import json


__SCHEMA_FILE = file("knitting_pattern_schema.json", "rb")
__SCHEMA_DICT = json.load(__SCHEMA_FILE)


def validate(loaded_json_data):
    validictory.validate(loaded_json_data, __SCHEMA_DICT)


def parse():
    pass

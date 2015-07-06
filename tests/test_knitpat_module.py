__author__ = 'tian'

import json
from knitlib.knitpat import validate_dict
from knitlib.knitpat import parse_ustring


def test_validate_simple_data_knitpat_method():
    test_sample = ("{\n"
                   "      \"file_url\":\"mypat.png\",\n"
                   "      \"name\":\"a small sweater\",\n"
                   "      \"colors\": 2}")
    sample_dict = json.loads(test_sample)
    validation = validate_dict(sample_dict)
    assert validation is True


def test_validate_invalid_data_knitpat_method():
    test_sample = ("{\n"
                   "      \"file_location\":\"mypat.png\",\n"
                   "      \"colors\": 2}")
    sample_dict = json.loads(test_sample)
    validation = validate_dict(sample_dict)
    assert validation is False

def test_parse():
    test_sample = ("{\n"
                   "      \"file_url\":\"mypat.png\",\n"
                   "      \"name\":\"a small sweater\",\n"
                   "      \"colors\": 2}")
    test_dict = {u"file_url": u"mypat.png",
                 u"name": u"a small sweater",
                 u"colors": 2}
    parsed_sample = parse_ustring(test_sample)
    assert test_dict == parsed_sample

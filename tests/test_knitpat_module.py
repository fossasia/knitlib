__author__ = 'tian'

import json
from knitlib.knitpat import validate_dict


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

import pytest
import config
from main import prepare_response
from main import send_request
from main import type_filter
import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, script_path + "/../")


@pytest.mark.parametrize("params, expected", [({"key": config.key, "action": "services"}, True),
                                              ('<div>test</div>', True),
                                              ({}, True),
                                              ([], True),
                                              ('', True)])
def test_send_request_type_check(params, expected):
    response = send_request(params)
    assert bool(isinstance(response, bytes)) == expected


@pytest.mark.parametrize("response, response_type, expected", [(
                                                b'[{"service":"3331","name":"Default","type":"Default","rate":"1.00","min":"10","max":"100","dripfeed":false,"refill":true,"category":"zzzzzzz"},'
                                                b'{"service":"3332","name":"SEO","type":"SEO","rate":"1.00","min":"10","max":"100","dripfeed":false,"refill":false,"category":"zzzzzzz"}]',
                                                list, True),
                                                ('<div>test</div>', None, False),
                                                ({}, None, False),
                                                (1231, None, False),
                                                ([], None, False)])
def test_prepare_response_type_check(response, response_type, expected):
    converted_response = prepare_response(response)
    if converted_response is None:
        assert bool(converted_response) == expected
    else:
        assert bool(isinstance(converted_response, response_type)) == expected


@pytest.mark.parametrize("list_data, expected", [([{'service': '3331', 'name': 'Default', 'type': 'Default',
                                                    'rate': '1.00', 'min': '10', 'max': '100', 'dripfeed': False,
                                                    'refill': True, 'category': 'zzzzzzz'},
                                                   {'service': '3332', 'name': 'SEO', 'type': 'SEO', 'rate': '1.00',
                                                    'min': '10', 'max': '100', 'dripfeed': False, 'refill': False,
                                                    'category': 'zzzzzzz'}],
                                                  [{'service': '3331', 'name': 'Default', 'type': 'Default',
                                                    'rate': '1.00', 'min': '10', 'max': '100', 'dripfeed': False,
                                                    'refill': True, 'category': 'zzzzzzz'}]
                                                  ),
                                                 ([{'service': '1', 'type': 'Default'},
                                                   {'service': '2', 'type': 'Test'}],
                                                 [{'service': '1', 'type': 'Default'}]),
                                                 ('string', 'string'),
                                                 ([], []),
                                                 ({}, {}),
                                                 (None, None)])
def test_type_filter(list_data, expected):
    filtering_list = type_filter(list_data)
    assert filtering_list == expected

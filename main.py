from io import BytesIO
from random import choice, randint
import pycurl
import config
import json


# functions

def json_decode(string):
    try:
        return json.loads(string)
    except:
        print('Error then decode json')
        return {}


def prepare_response(bytes_response):
    try:
        str_response = bytes_response.decode("UTF-8")
        return json_decode(str_response)
    except:
        print('Error then convert Bytes to List')
        return None


def send_request(payload, headers=None):
    if headers is None:
        headers = config.default_headers
    try:
        buffer = BytesIO()
        conn = pycurl.Curl()
        conn.setopt(pycurl.URL, config.url)
        conn.setopt(pycurl.HTTPHEADER, headers)
        conn.setopt(pycurl.POST, 1)
        conn.setopt(pycurl.POSTFIELDS, '%s' % json.dumps(payload))
        conn.setopt(pycurl.WRITEDATA, buffer)
        conn.perform()
        return buffer.getvalue()
    except:
        print('Request error')
        return None


def type_filter(data):
    if isinstance(data, list):
        data = list(filter(lambda x: x['type'] == config.service_type, data))
    return data


if __name__ == '__main__':
    # Get services list and filter only default types. Print result
    payload_services = {"key": config.key,
                        "action": "services"}
    list_services = prepare_response(send_request(payload_services))
    print(list_services)
    service = choice(type_filter(list_services))
    print(service)

    # Get order id. Print result
    payload_order = {"key": config.key,
                     "action": "add",
                     "service": service['service'],
                     "link": "https://instagram.com/goganasan",
                     "quantity": randint(int(service['min']), int(service['max']))}

    order = prepare_response(send_request(payload_order))
    print(order)

    # Get order status. Print result
    payload_status = {"key": config.key,
                      "action": "status",
                      "order": order['order']}
    status = prepare_response(send_request(payload_status))
    print(status)

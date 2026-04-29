import requests

IP_ADDRESS = "http://<IP_ADDRESS>"


def _make_request(action):
    url = f"{IP_ADDRESS}/api?action={action}"
    response = requests.get(url)
    return response

def turn_on():
    return _make_request("on")

def turn_off():
    return _make_request("off")

def set_color(hex_color):
    return _make_request(f"color&hex={hex_color}")

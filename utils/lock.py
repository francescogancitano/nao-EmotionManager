import request

IP_ADDRESS = "http://192.168.178.x"
API = ""

def posso_parlare():
    request = requests.get(IP_ADDRESS+API)

    while request.text == 1:

        logger.info("aspettando che Oberon finisce di parlare...")

    return
        
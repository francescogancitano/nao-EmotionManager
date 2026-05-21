# -*- coding: utf-8 -*-

import requests
from time import sleep
from utils.log import logger
from utils.utils import hex_to_rgb

URL = "http://192.168.178."
IP_ADDRESS_LED = URL+"21"
IP_ADDRESS_FARO = URL+"40:8080"

def _make_request(oggetto, action):
    if oggetto == "faro":
        
        if action == "on":
            return requests.get("{}/?ch=6&val=255".format(IP_ADDRESS_FARO))
        
        elif action == "off":
            return requests.get("{}/?ch=6&val=0".format(IP_ADDRESS_FARO))
        
        else:
            try:
                # Estraiamo il valore esadecimale (es. da "color&hex=ff0000")
                hex_val = action.split('=')[-1]
                colore = hex_to_rgb(hex_val)

                ch = 7
                for val in colore:       
                    requests.get("{0}/?ch={1}&val={2}".format(IP_ADDRESS_FARO, ch, val))
                    ch+=1

            except Exception as e:
                logger.warning("impossibile trasformare il codice hex in rgb: {}".format(e))
            
    
    url = "{0}/{1}?action={2}".format(IP_ADDRESS_LED, oggetto, action)
    response = requests.get(url)
    return response

def turn_on(oggetto):
    request = _make_request(oggetto, "on")
    logger.info("risposta: {0}".format(request))

def turn_off(oggetto):
    if(oggetto=="fumo"):
        _make_request(oggetto, "on")
        sleep(0.2)
        request = _make_request(oggetto, "on")

        logger.info("risposta: {0}".format(request))

    else:
        request = _make_request(oggetto, "off")
        logger.info("risposta: {0}".format(request))

def set_color(oggetto, hex_color):
    if isinstance(hex_color, int):
        hex_color = "{:06x}".format(hex_color)
        
    request = _make_request(oggetto, "color&hex={0}".format(hex_color))
    logger.info("risposta: {0}".format(request))



def cambia_colore_luci(colore):
    set_color("striscia", colore)
    set_color("ring", colore)
    set_color("faro", colore)
    

def accendi_luci():
    loggrt.info("accendendo luci...")
    try:
        turn_on("striscia")
        turn_on("ring")
        turn_on("faro")

    except Exception as e:
        logger.warning("impossibile accendere luci: {}".format(e))


def spegni_luci():
    try:
        turn_off("striscia")
        turn_off("ring")
        turn_off("faro")

    except Exception as e:
        logger.warning("impossibile spegnere luci: {}".format(e))

if "__main__" == __name__:
    COLORE = 0xffff00
    set_color("striscia", COLORE)
    set_color("ring", COLORE)
    
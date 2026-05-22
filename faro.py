# -*- coding: utf-8 -*-

import requests
from time import sleep
from utils.log import logger
from utils.utils import hex_to_rgb

URL = "http://192.168.178."
IP_ADDRESS_LED = URL+"21"
IP_ADDRESS_FARO = URL+"40:8080"
IP_ADDRESS_FUMO = URL+"14"

def _make_request(oggetto, action, colori=None):
    if oggetto == "faro":
        if action == "on":
            return requests.get("{}/?ch=6&val=255".format(IP_ADDRESS_FARO))
        elif action == "off":
            return requests.get("{}/?ch=6&val=0".format(IP_ADDRESS_FARO))
        else:
            try:
                vals = None
                if isinstance(action, (list, tuple)):
                    vals = action
                elif isinstance(colori, (list, tuple)):
                    vals = colori
                else:
                    # Estraiamo il valore esadecimale
                    s_action = hex(action) if isinstance(action, int) else str(action)
                    hex_val = s_action.split('=')[-1]
                    vals = hex_to_rgb(hex_val)

                if vals:
                    ch = 7
                    resp = None
                    for val in vals:      
                        resp = requests.get("{0}/?ch={1}&val={2}".format(IP_ADDRESS_FARO, ch, val))
                        ch+=1
                    return resp
                else:
                    logger.warning("Nessun colore valido per il faro: action={}, colori={}".format(action, colori))
                    return None
            except Exception as e:
                logger.warning("impossibile gestire colore faro (action={}, colori={}): {}".format(action, colori, e))
                return None
        
    if oggetto == "fumo":
        url = "{0}/{1}?action={2}".format(IP_ADDRESS_FUMO, oggetto, action)

    else:
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

def set_color(oggetto, colori):
    if oggetto == "faro":
        if colori is None:
            return
        request = _make_request(oggetto, colori)
        logger.info("risposta faro: {0}".format(request))
        return

    # Per altri oggetti (striscia/ring), formattiamo l'hex
    h = "{:06x}".format(colori) if isinstance(colori, int) else colori
    request = _make_request(oggetto, "color&hex={0}".format(h))
    logger.info("risposta {0}: {1}".format(oggetto, request))



def cambia_colore_luci(colore, colori_faro=None):
    set_color("striscia", colore)
    #set_color("ring", colore)
    set_color("faro", colori_faro)
    

def accendi_luci():
    logger.info("accendendo luci...")
    try:
        turn_on("striscia")
        #turn_on("ring")
        turn_on("faro")
        turn_on("fumo")

    except Exception as e:
        logger.warning("impossibile accendere luci: {}".format(e))


def spegni_luci():
    try:
        turn_off("striscia")
        #turn_off("ring")
        turn_off("faro")

        spegni_fumo()

    except Exception as e:
        logger.warning("impossibile spegnere luci: {}".format(e))


def spegni_fumo():
    turn_on("fumo")
    turn_on("fumo")

if "__main__" == __name__:

    #COLORE = 0xffff00
    #set_color("striscia", COLORE)
    #set_color("ring", COLORE)
    spegni_luci

    accendi_luci()

    cambia_colore_luci(0x00ff00)
    set_color("faro", (255, 0, 0))

    sleep(5)

    spegni_luci()
    
    
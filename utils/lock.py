import requests
import sys
import tty
import termios

from log import logger

URL = "http://192.168.178.172/"


def posso_parlare():
    request = requests.get(URL)

    while request.text == "1":

        logger.info("aspettando che Oberon finisce di parlare...")
        request = requests.get(URL)

    return


def aspetta():
    """Blocca l'esecuzione finche' non viene premuto un tasto su Linux."""
    # Salva il descrittore del file dello standard input
    fd = sys.stdin.fileno()
    # Salva le impostazioni originali del terminale
    vecchie_impostazioni = termios.tcgetattr(fd)
    try:
        # Imposta il terminale in modalita' raw (intercetta i singoli tasti)
        tty.setraw(fd)
        # Legge esattamente 1 byte (un carattere)
        sys.stdin.read(1)
    finally:
        # Ripristina sempre le impostazioni originali del terminale
        termios.tcsetattr(fd, termios.TCSADRAIN, vecchie_impostazioni)


        
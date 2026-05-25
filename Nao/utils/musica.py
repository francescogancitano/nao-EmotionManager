import requests
from time import sleep

"""chiedere a george come funziona lo stop"""

URL = "http://192.168.178.164:8081/?"

def musica(fase):
    if fase == 1:
        requests.get(URL+"track=prima_fase")

    if fase == 2:
        requests.get(URL+"track=seconda_fase")

def stop_musica():
    requests.get(URL+"stop=1")



# -*- coding: utf-8 -*-

import time, sys

from EmotionManager import EmotionManager

from utils.utils_positions import head, arms_both, right_arm_magic_pose
from faro import *
from utils.audio import *


VERDE    = 0x00FF00
VIOLETTO = 0xC58EE8
ROSSO    = 0x80190E

# Inizializzazione EmotionManager (default localhost)
em = EmotionManager()
nao = em.nao


def prima_fase():
    try:
        #nao.motion.wakeUp()
        nao.posture.goToPosture("StandInit", 0.5)
        nao.motion.setStiffnesses("Body", 0.6)  #imposta la rigidità del corpo
        pass

        try:
            nao.set_body_color(0xffffff)

        except:
            pass

    except Exception as e:
        print("Errore inizializzazione: " + str(e))

    try:
        # (Buio. Pausa.)
        

        """
            arriva incazzato
            dice: 'ANCORA NON AVETE FATTO NIENTE'
            sventola le mani basso siddiato

            grida: 'ACCENDETEMI IL FARO E PREPARATEMI LA SCENA'

            sleep(1)
            grida: 'SI VA IN SCENA'
        
        """
        """
        
            QUI CI DEVE ESSERE
            TUTTA LA PARTE 
            DELLA PROVA TECNICA
        
        """
        nao.set_body_color(ROSSO)

        em.perform(AUDIO_FILES["urlo"])
        
        # Camminata bloccante di 75cm (lenta)
        nao.motion.moveTo(0.60, 0.0, 0.0)

        # Avvio audio in background per muoversi mentre parla
        if nao.audio_player:
            nao.audio_player.post.playFile(AUDIO_FILES["ancora non avete fatto niente"])
        else:
            em.perform(AUDIO_FILES["ancora non avete fatto niente"])
        
        # Movimento braccia <> e || per 5 volte
        for _ in range(5):
            # Forma <>
            nao.motion.angleInterpolation(
                ["LShoulderRoll", "RShoulderRoll", "LElbowRoll", "RElbowRoll"],
                [0.7, -0.7, -1.2, 1.2],
                [0.4, 0.4, 0.4, 0.4],
                True
            )
            # Forma ||
            nao.motion.angleInterpolation(
                ["LShoulderRoll", "RShoulderRoll", "LElbowRoll", "RElbowRoll"],
                [0.1, -0.1, -0.05, 0.05],
                [0.4, 0.4, 0.4, 0.4],
                True
            )

        nao.motion.angleInterpolation(["RShoulderPitch"], [-0.5], [2.0], True)
        em.perform(AUDIO_FILES["accendete le luci"])

        time.sleep(3)
        accendi_luci()

        time.sleep(0.5)
        cambia_colore_luci(ROSSO)
        
        time.sleep(2)

        em.perform(AUDIO_FILES["si va in scena"])
        
        time.sleep(1)
        cambia_colore_luci(VERDE)
        
        
        # OBERON: Perfetto. Le luci sono accese... e lo sfondo impostato. Siamo pronti a entrare in scena.
        # time.sleep(4.0)
        
        # (NAO abbassa il braccio e si porta in posizione neutra. Sfondo: bosco)
        nao.posture.goToPosture("StandInit", 1.0)
        
        # CAMMINATA: 3 secondi normale + 2 secondi lenta
        nao.motion.setWalkTargetVelocity(0.6, 0.0, 0.0, 0.4)
        time.sleep(3.0)
        nao.motion.setWalkTargetVelocity(0.22, 0.0, 0.0, 0.4)
        time.sleep(2.0)
        nao.motion.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.4)
        time.sleep(0.5)

        # LUCI
        try:
            nao.set_body_color(0xffffff)
        except:
            pass

        time.sleep(0.8)

        # **NAO PUCK**
        # _set_felice_
        em.set_mood("felice")
        
        # (Braccia leggermente aperte, movimento leggero del busto)
        arms_both(nao, 0.7, 0.9, 0.7, -0.9, 1.5)
        

        em.perform(input_data=AUDIO_FILES["per il bosco"])        
        #em.perform(input_data="Per il bosco ho scorrazzato e nessun ateniese vi ho trovato sui cui occhi provare se il fiore è poi vero che suscita amore...")
        time.sleep(0.5)

        # _set_sorpresa_
        em.set_mood("sorpresa")
        # (Testa che scatta a destra, poi a sinistra)
        head(nao, 0.42, -0.08, 0.5)
        time.sleep(0.3)
        head(nao, -0.42, -0.08, 0.5)
        time.sleep(0.3)
        head(nao, 0.0, -0.05, 0.5)


        # Alza le braccia verso il cielo
        nao.motion.angleInterpolation(
            ["LShoulderPitch", "RShoulderPitch"],
            [-0.5, -0.5],
            [1.0, 1.0],
            True
        )

        # Avvio audio e discesa lenta delle braccia
        if nao.audio_player:
            nao.audio_player.post.playFile(AUDIO_FILES["notte e pace"])
        else:
            em.perform(AUDIO_FILES["notte e pace"])

        nao.motion.angleInterpolation(
            ["LShoulderPitch", "RShoulderPitch"],
            [1.5, 1.5],
            [4.0, 4.0],
            True
        )

        """nello stacco tra pace e ma chi, cambiare la luce a viola chiaro"""

        cambia_colore_luci(VIOLETTO)

        em.perform(input_data=AUDIO_FILES["ma chi è la"]) 
        
        # Alza braccio sinistro dritto
        nao.motion.angleInterpolation(["LShoulderPitch"], [-1.5], [0.6], True)
        time.sleep(0.5)
        # Lo abbassa
        nao.motion.angleInterpolation(["LShoulderPitch"], [1.5], [0.6], True)

        # _set_triste_
        em.set_mood("triste")
        # (Testa leggermente abbassata, braccia più vicine al corpo)
        nao.motion.angleInterpolation(
            ["HeadPitch", "LShoulderPitch", "RShoulderPitch"],
            [0.28, 1.45, 1.45],
            [1.0, 1.0, 1.0],
            True
        )

        cambia_colore_luci(VERDE)
        
        # Braccio destro in angolo retto verso destra e poi torna
        nao.motion.angleInterpolation(["RShoulderPitch", "RShoulderRoll"], [0.0, -1.5], [0.5, 0.5], True)
        time.sleep(0.5)
        nao.motion.angleInterpolation(["RShoulderPitch", "RShoulderRoll"], [1.5, -0.15], [0.5, 0.5], True)

        em.perform(input_data=AUDIO_FILES["poverina"])        
        time.sleep(1.0)

        # _set_rabbia_
        em.set_mood("arrabbiato")
        # (Un braccio si alza deciso in avanti)
        nao.motion.angleInterpolation(
            ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand"],
            [0.95, -0.15, 1.0, 0.6, 1.0],
            [0.8, 0.8, 0.8, 0.8, 0.8],
            True
        )

        #prima della battuta il colore deve diventare rosso scurissimo
        cambia_colore_luci(ROSSO)
        
        # Avvio audio incantesimo
        if nao.audio_player:
            nao.audio_player.post.playFile(AUDIO_FILES["sui tuoi occhi"])
        else:
            em.perform(AUDIO_FILES["sui tuoi occhi"])

        # Movimento incantesimo: braccia dritte che oscillano
        for _ in range(3):
            nao.motion.angleInterpolation(
                ["LShoulderPitch", "RShoulderPitch"],
                [0.8, 1.2],
                [0.4, 0.4],
                True
            )
            nao.motion.angleInterpolation(
                ["LShoulderPitch", "RShoulderPitch"],
                [1.2, 0.8],
                [0.4, 0.4],
                True
            )
        
        # MAGIA (movimento della mano)
        right_arm_magic_pose(nao, 1.0)
        nao.motion.angleInterpolation(["RWristYaw"], [-0.65], [0.5], True)
        nao.motion.angleInterpolation(["RWristYaw"], [0.45], [0.5], True)
        time.sleep(0.5)

        # _set_felice_
        em.set_mood("felice")
        # (Braccia aperte, piccolo passo avanti)
        nao.motion.moveTo(0.06, 0.0, 0.0)
        arms_both(nao, 0.65, 1.0, 0.65, -1.0, 1.2)

        cambia_colore_luci(0xffffff)
        #luce torna colore normale
        em.perform(input_data=AUDIO_FILES["ma allora"])        
        #em.perform(input_data="Ma allora saro lontano....... perche da Oberon faccio ritorno!")
        time.sleep(1.0)

        # (Fine Fase 1)
        # USCITA
        nao.motion.moveTo(0.20, 0.0, 0.25)

        # SPEGNIMENTO LUCI
        try:
            nao.set_body_color(0xffffff)
        except:
            pass

    except Exception as e:
        print("Errore durante l'esecuzione: " + str(e))



if __name__ == "__main__":
    nao.set_body_color(0xffffff)
    prima_fase()

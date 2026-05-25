# -*- coding: utf-8 -*-

import time, sys

from EmotionManager import EmotionManager

from utils.utils_positions import head, arms_both, right_arm_magic_pose
from faro import *
from utils.audio import *
from utils.lock import *
from utils.musica import *


VERDE    = 0x00FF00
VIOLETTO = 0xC58EE8
ROSSO    = 0x80190E



# Inizializzazione EmotionManager (default localhost)
em = EmotionManager()
nao = em.nao


"""
PROBLEMI:

PROVA TECNICA:
DEVE ALZARE IL BRACCIO E SPOSTARLO A SINISTRA

PRIMA PARTE:
FARLO ANDARE AVANTI DI POCO NELLA CAMMINATA DOPO L'URLO (MAX 20CM)

UN ONDEGGIAMENTO IN MENO DI BRACCIA QUANDO DICE "ANCORA NON AVETE FATTO NIENTE"

MENO SLEEP MENTRE DOPO CHE DICE NOTTE E PACE

QUANDO DICE "MA CHI È LA" DEVE ALZARE DI MENO IL BRACCIO E PIÙ LENTAMENTE

MENTRE CHE DICE MA CHI È LA PARTE L'AUDIO DI DOPO, METTERE UNO SLEEP O QUALCOSA

DOPO CHE VERSA IL SUCCO ARCANO AGGIUSTARE LA PARTE DOVE SI GIRA



"""


"""
parti di suddivisione:

PROVA TECNICA:


si alza e va avanti

prende il microfono

si gira di 180 gradi e va avanti

si gira di 90 gradi e sta fermo per x secondi



PRIMA PARTE:
continua a suddividere seguendo la stessa logica

"""

def inizializzazione_robot():
    try:
        # Assicuriamoci che il robot sia sveglio e pronto
        if nao.motion and not nao.motion.robotIsWakeUp():
            nao.motion.wakeUp()
            
        nao.posture.goToPosture("StandInit", 0.5)
        # Rigidità massima per la performance
        nao.motion.setStiffnesses("Body", 1.0) 

        try:
            nao.set_body_color(0xffffff)
        except:
            pass

    except Exception as e:
        print("Errore inizializzazione: " + str(e))




def prova_tecnica():
    # --- PROVA TECNICA (Sequenza lenta) ---
    
    # 1. Alzarsi bene
    #nao.posture.goToPosture("Stand", 1.0)
    time.sleep(1.0) # Aspetta 1 sec

    # 2. Andare avanti di 70cm lentamente
    nao.prepare_for_walk()
    time.sleep(1)
    # MaxStepX ridotto per lentezza
    nao.motion.moveTo(0.45, 0.0, 0.0, [["MaxStepX", 0.01]])

    #aspetta()

    # 3. Microfono: alza il braccio a circa 85 gradi (centrale, palmo aperto)
    # Pitch 0.08 rad è circa 85° dalla verticale giù
    nao.motion.angleInterpolation(
        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand"],
        [0.08, 0.3, 0.0, 0.0, 1.0],
        [3.0, 3.0, 3.0, 3.0, 3.0],
        True
    )
    time.sleep(1.0)

    #aspetta()

    # 4. Abbassa il braccio
    nao.motion.angleInterpolation(
        ["RShoulderPitch", "RHand"],
        [1.5, 0.0],
        [2.5, 2.5],
        True
    )

    #aspetta()

    # 5. Si gira lentamente di 180 gradi
    nao.prepare_for_walk()
    #nao.motion.moveTo(0.0, 0.0, 2.3, [["MaxStepTheta", 0.1]])
    nao.rotate_deg(180)

    #aspetta()

    # 6. Va avanti di approssimativamente 30cm lentamente
    nao.motion.moveTo(0.10, 0.0, 0.0, [["MaxStepX", 0.01]])

    #aspetta()

    #SI DEVE GIRARE DI 90°
    nao.prepare_for_walk()
    #nao.motion.moveTo(0.0, 0.0, 1.5, [["MaxStepTheta", 0.1]])
    nao.rotate_deg(-90)

    # 7. Sta fermo per 5 sec
    time.sleep(5.0)

def inizio_prima_parte():
    # --- INIZIO PERFORMANCE ---
    nao.set_body_color(ROSSO)

    em.perform(AUDIO_FILES["urlo"])
    
    # Preparazione camminata e spostamento 20cm
    nao.prepare_for_walk()
    nao.motion.moveTo(0.40, 0.0, 0.0)

    # Avvio audio in background per muoversi mentre parla
    if nao.audio_player:
        nao.audio_player.playFile(AUDIO_FILES["ancora non avete fatto niente"], _async=True)
    else:
        em.perform(AUDIO_FILES["ancora non avete fatto niente"])
    
    # Movimento braccia <> e || per 4 volte
    for _ in range(4):
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
    #accendi_luci()

    time.sleep(0.5)
    #cambia_colore_luci(ROSSO)
    set_color("faro", (255, 0, 0))
    
    time.sleep(2)

    em.perform(AUDIO_FILES["si va in scena"])
    
    time.sleep(1)
    #cambia_colore_luci(VERDE)
    set_color("faro", (0, 255, 0))

    musica(1)

    time.sleep(4)

    # (NAO abbassa il braccio e si porta in posizione neutra. Sfondo: bosco)
    nao.posture.goToPosture("StandInit", 1.0)
    nao.motion.setStiffnesses("Body", 1.0)
    
    # Preparazione camminata: 3 secondi normale + 2 secondi lenta
    nao.prepare_for_walk()
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



def per_il_bosco_ho_scorrazzato():
    time.sleep(0.8)

    # **NAO PUCK**
    # _set_felice_
    em.set_mood("felice")
    
    # (Braccia leggermente aperte, movimento leggero del busto)
    arms_both(nao, 0.7, 0.9, 0.7, -0.9, 1.5)
    

    em.perform(input_data=AUDIO_FILES["per il bosco"])        
    time.sleep(0.5)


def notte_e_pace():
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

    # Avvio audio e discesa lenta delle braccia (dritte e vicine al corpo)
    if nao.audio_player:
        nao.audio_player.playFile(AUDIO_FILES["notte e pace"], _async=True)
    else:
        em.perform(AUDIO_FILES["notte e pace"])

    nao.motion.angleInterpolation(
        ["LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"],
        [1.5, 1.5, 0.15, -0.15],
        [2.0, 2.0, 2.0, 2.0],
        True
    )

def ma_chi_e_la():
    """nello stacco tra pace e ma chi, cambiare la luce a viola chiaro"""

    #cambia_colore_luci(VIOLETTO)
    set_color("faro", (134, 115, 161))

    nao.prepare_for_walk()
    nao.rotate_deg(-90)

    nao.audio_player.playFile(AUDIO_FILES["ma chi è la"], _async=True)
    
    # Alza braccio sinistro dritto (meno alzato e più lento)
    nao.motion.angleInterpolation(["LShoulderPitch"], [-0.5], [1.2], True)
    time.sleep(1.0)
    # Lo abbassa
    nao.motion.angleInterpolation(["LShoulderPitch"], [1.5], [1.2], True)
    
    # Sleep per evitare sovrapposizione audio successivo
    time.sleep(2.0)

    nao.prepare_for_walk()

    nao.motion.moveTo(0.20, 0.0, 0.0)


def succo_arcano():
    # _set_triste_
    em.set_mood("triste")
    # (Testa leggermente abbassata, braccia più vicine al corpo)
    nao.motion.angleInterpolation(
        ["HeadPitch", "LShoulderPitch", "RShoulderPitch"],
        [0.28, 1.45, 1.45],
        [1.0, 1.0, 1.0],
        True
    )

    #cambia_colore_luci(VERDE)
    set_color("faro", (0, 255, 0))
    
    # Braccio destro in angolo retto verso destra e poi torna
    #nao.motion.angleInterpolation(["RShoulderPitch", "RShoulderRoll"], [0.0, -1.5], [0.5, 0.5], True)
    #time.sleep(0.5)
    #nao.motion.angleInterpolation(["RShoulderPitch", "RShoulderRoll"], [1.5, -0.15], [0.5, 0.5], True)

    # SI GIRA VERSO ANITA (90 gradi a sinistra)

    """
    questo è il pezzo dove sta davanti alla regina
    poi va verso il duca e gli versa il succo arcano    
        
    """
    

    # CHIAMATA NON BLOCCANTE
    if nao.audio_player:
        nao.audio_player.playFile(AUDIO_FILES["poverina"], _async=True)
    else:
        em.perform(AUDIO_FILES["poverina"])

    # ABBASSA UN POCHINO LA TESTA
    nao.move_head(0.2)
    time.sleep(2.0)


    # ALZA LA TESTA DRITTA
    nao.move_head(0.0)

    time.sleep(5)


    # _set_rabbia_
    em.set_mood("arrabbiato")
    # (Un braccio si alza deciso in avanti)
    """nao.motion.angleInterpolation(
        ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand"],
        [0.95, -0.15, 1.0, 0.6, 1.0],
        [0.8, 0.8, 0.8, 0.8, 0.8],
        True
    )"""

    #prima della battuta il colore deve diventare rosso scurissimo
    #cambia_colore_luci(ROSSO)
    set_color("faro", (255, 0, 0))
    
    # SI GIRA DI 180° (chiamata bloccante)
    nao.prepare_for_walk()
    #nao.motion.moveTo(0.0, 0.0, 3.14159)
    nao.rotate_deg(180)

    # Avvio audio incantesimo
    if nao.audio_player:
        nao.audio_player.playFile(AUDIO_FILES["sui tuoi occhi"], _async=True)
    else:
        em.perform(AUDIO_FILES["sui tuoi occhi"])

    # VA AVANTI DI 90cm (chiamata bloccante)
    
    print(nao.motion.moveTo(0.5, 0.0, 0.0))

    for _ in range(6):
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


def ad_oberon_faccio_ritorno():
    # _set_felice_
    em.set_mood("felice")
    # (Braccia aperte, piccolo passo avanti)
    nao.prepare_for_walk()
    #nao.motion.moveTo(0.06, 0.0, 0.0)

    #cambia_colore_luci(0xffffff)
    set_color("faro", (255, 255, 255))
    #luce torna colore normale



    # SI GIRA DI 180°
    #nao.motion.moveTo(0.0, 0.0, 3.14159)
    nao.rotate_deg(180)


    # CHIAMATA NON BLOCCANTE
    if nao.audio_player:
        nao.audio_player.playFile(AUDIO_FILES["ma allora"], _async=True)
    else:
        em.perform(AUDIO_FILES["ma allora"])

    # VA AVANTI DI 45CM
    nao.motion.moveTo(0.20, 0.0, 0.0)

    # SI GIRA DI 90°
    #nao.motion.moveTo(0.0, 0.0, 1.57)
    nao.rotate_deg(90)


    arms_both(nao, 0.65, 1.0, 0.65, -1.0, 1.2)

    #lascia questo commento così FIXME : GEMINI chiamata audio bloccante "perchè ad oberon facico ritorno"  

    em.perform(AUDIO_FILES["ad oberon faccio ritorno"])

def prima_fase():
    logger.info("inizio prima parte")
    inizio_prima_parte()
    logger.info("fine prima parte")

    #aspetta()

    logger.info("inizio monologo 'per il bosco'")
    per_il_bosco_ho_scorrazzato()
    logger.info("fine monologo 'per il bosco'")

    #aspetta()

    logger.info("inizio monologo 'notte e pace'")
    notte_e_pace()
    logger.info("fine monologo 'notte e pace'")

    #aspetta()

    logger.info("inizio monologo 'spaventato ma chi è la?'")
    ma_chi_e_la()
    logger.info("fine monologo 'spaventato ma chi è la?'")

    #aspetta()
    
    logger.info("inizio versamento succo")
    succo_arcano()
    logger.info("fine versamento succo")

    #aspetta()

    logger.info("inizio monologo ad oberon faccio ritorno")
    ad_oberon_faccio_ritorno()
    logger.info("fine monologo ad oberon faccio ritorno")

def fase_completa():
    inizializzazione_robot()

    try:
        logger.info("inizio prova tecnica")
        prova_tecnica()
        logger.info("fine prova tecnica")

        #aspetta()

        logger.info("INIZIO PRIMA FASE")
        prima_fase()
        logger.info("FINE SECONDA FASE")

        
        
        

        
        """
        spezzare audio "ma allora sarò lontano"
        "perchè a oberon faccio ritorno"
        
        """
        time.sleep(1.0)

        # (Fine Fase 1)
        # USCITA
        #nao.prepare_for_walk()
        #nao.motion.moveTo(0.20, 0.0, 0.25)

        # SPEGNIMENTO LUCI
        try:
            nao.set_body_color(0x000000)
            #spegni_luci()
        except:
            pass

    except Exception as e:
        print("Errore durante l'esecuzione: " + str(e))



if __name__ == "__main__":
    #fase_completa()
    #musica(1)

    time.sleep(5)

    fase_completa()

    time.sleep(5)

    stop_musica()
    

    
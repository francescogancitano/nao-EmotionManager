# -*- coding: utf-8 -*-

import time, sys

from EmotionManager import EmotionManager

from utils.utils_positions import (
    head, close_arms, indicate_jury, pour_motion, 
    close_right_hand, open_arms_small, arms_sad, 
    arms_open_happy, final_pose, arms_both
)

from utils.audio import AUDIO_FILES
from faro import *

from utils.lock import *

from utils.musica import *

# Definizioni colori per la scena
VERDE    = 0x00FF00  # Bosco / Natura
VIOLETTO = 0xC58EE8  # Magia / Amore
ROSSO    = 0x80190E  # Tensione / Errore
BLU      = 0x0000FF  # Tristezza / Esitazione
CIANO    = 0x00FFFF  # Determinazione
BIANCO   = 0xFFFFFF  # Neutro / Inizio

# Inizializzazione EmotionManager (default localhost)
em = EmotionManager()
nao = em.nao

def fase2(mood1, mood2):
    try:
        # Inizializzazione
        #nao.posture.goToPosture("StandInit", 0.8)
        #nao.motion.setStiffnesses("Body", 1.0)
        set_color("faro", (255, 255, 255)) # Luce bianca
        time.sleep(0.5)
        close_arms(nao, 0.6)
        time.sleep(0.5)

        # Entra e si ferma davanti a Oberon (movimento minimo)
        #nao.motion.moveTo(0.10, 0.0, 0.0)
        time.sleep(0.5)

        # Inchino rispettoso
        head(nao, 0.0, 0.3, 0.8)
        time.sleep(0.4)
        head(nao, 0.0, 0.0, 0.6)
        
        posso_parlare()

        # --- RACCONTO DEL BOSCO ---
        set_color("faro", (0, 255, 0)) # VERDE
        
        # "Nei pressi del suo giaciglio..."
        if nao.audio_player:
            nao.audio_player.playFile(AUDIO_FILES["nei pressi"], _async=True)
            # Gesto descrittivo con le braccia (apertura ampia)
            arms_both(nao, 0.8, 0.6, 0.8, -0.6, 1.5)
            time.sleep(1.5)
            arms_both(nao, 1.1, 0.2, 1.1, -0.2, 1.2)
        else:
            em.perform(AUDIO_FILES["nei pressi"], mood=mood1)
        
        time.sleep(1)

        # "Uno di questi uscì..."
        indicate_jury(nao, 0.8) # Indica i giudici
        em.perform(AUDIO_FILES["uno di questi"], mood=mood1)
        time.sleep(0.1)

        # "E allora io..." (Nuovo audio)
        # Puck si pavoneggia un po'
        nao.motion.angleInterpolation(["LShoulderRoll", "RShoulderRoll"], [0.3, -0.3], [0.8, 0.8], True)
        em.perform(AUDIO_FILES["e allora io"], mood="felice")
        
        # --- IL SUCCO ARCANO ---
        set_color("faro", (197, 142, 232)) # VIOLETTO
        
        # Movimento di versamento
        pour_motion(nao, 1.2)
        # "le versai nell'occhio..."
        em.perform(AUDIO_FILES["le versai nell'occhio"], mood=mood1)

        close_right_hand(nao, 0.4)
        time.sleep(0.1)

        # Puck soddisfatto
        open_arms_small(nao, 1.0)
        # "La regina si destò..."
        em.perform(AUDIO_FILES["la regina si desto"], mood="felice")
        
        # OBERON: La cosa è riuscita meglio di quanto pensassi!
        
        
        # --- IL PROBLEMA ---
        set_color("faro", (0, 0, 255)) # BLU: Esitazione
        
        # Puck si rimpicciolisce
        head(nao, 0.0, 0.25, 1.0)
        arms_sad(nao, 1.2)
        posso_parlare()

        # "Sì, mio re... ma..."
        em.perform(AUDIO_FILES["si mio re ma"], mood="triste")
        
        # OBERON: Ovvero?
        posso_parlare()
        
        # Sguardo basso e braccia vicine
        head(nao, 0.2, 0.35, 1.5)
        # "Guardai il volto della regina..."
        em.perform(AUDIO_FILES["guardai il volto della regina"], mood="triste")
        time.sleep(0.5)

        # "E mai sfortuna..."
        em.perform(AUDIO_FILES["e mai sfortuna"], mood="triste")
        time.sleep(0.5)

        # --- IL DUCA PEDEMONTE ---
        set_color("faro", (255, 0, 0)) # ROSSO: Errore/Tensione
        
        # Scatto della testa verso il re, poi indica il "disastro"
        head(nao, 0.0, -0.05, 0.3)
        indicate_jury(nao, 0.6)
        # "Era... il Duca Pedemonte."
        em.perform(AUDIO_FILES["era il duca"], mood="paura")
        
        posso_parlare()

        # OBERON: Puck! Sei l’assistente più inutile!

        # Puck si giustifica (Palmi aperti, movimento del busto/testa)
        nao.motion.angleInterpolation(
            ["LShoulderRoll", "RShoulderRoll", "LElbowRoll", "RElbowRoll", "HeadYaw"],
            [0.5, -0.5, -0.6, 0.6, 0.2],
            [1.0, 1.0, 1.0, 1.0, 1.0],
            True
        )
        # "Maestà... era buio..."
        em.perform(AUDIO_FILES["maesta era buio"], mood="disgusto")
        
        # "e poi i giudici..."
        head(nao, -0.2, 0.1, 0.8)
        em.perform(AUDIO_FILES["e poi i giudici si assomigliano tutti"], mood="noia")

        posso_parlare()

        # OBERON: Ora la mia regina si è innamorata di un idiota! No... si può ancora sistemare.
        
        # BLOCCO 1 (Tristezza/Riflessione)
        head(nao, 0.0, 0.45, 1.5) # Testa molto bassa
        arms_sad(nao, 1.0)
        em.perform(AUDIO_FILES["blocco 1"], mood="triste")

        posso_parlare()

        # OBERON: Basta esitazioni. Serve una soluzione... subito.
        
        # BLOCCO 2 (Ripresa/Speranza)
        head(nao, 0.0, -0.1, 1.0) # Alza lo sguardo
        open_arms_small(nao, 1.2)
        em.perform(AUDIO_FILES["blocco 2"], mood="determinato")

        posso_parlare()

        # OBERON: Vai, Puck. E questa volta... non sbagliare bersaglio.
        
        # --- FINALE DETERMINATO ---
        set_color("faro", (0, 255, 255)) # CIANO: Determinazione
        
        final_pose(nao, 0.8)
        # "Stavolta no, mio re..."
        em.perform(AUDIO_FILES["stavolta no mio re"], mood="determinato")
        
        # "Guarderò meglio..."
        em.perform(AUDIO_FILES["guardero meglio agiro meglio"], mood="determinato")

        time.sleep(0.5)
        
        # CONCLUSIONE
        set_color("faro", (255, 255, 255)) # BIANCO
        
        # Sguardo complice/furbo verso il pubblico
        head(nao, 0.4, 0.1, 0.8) 
        # "...forse."
        em.perform(AUDIO_FILES["forse"], mood="felice")
        
        # (Blackout)
        time.sleep(1.0)
        set_color("faro", (0, 0, 0)) # SPEGNIMENTO
        
        nao.posture.goToPosture("Sit", 1.5)
        nao.motion.rest()

    except Exception as e:
        print("Errore durante Fase 2: " + str(e))

if __name__ == "__main__":

    musica(2)

    time.sleep(5)
    
    fase2("felice", "triste")

    time.sleep(5)

    stop_musica()
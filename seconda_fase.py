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



"""
PROBLEMI: 



"""









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

def esegui_blocco1(mood):
    """
    BLOCCO 1: Gestione emozioni dinamiche
    Testi da COPIONE.MD: Tristezza, Rabbia, Paura, Disgusto, Noia
    """
    testi = {
        "triste": "È colpa mia... ho rovinato tutto...",
        "arrabbiato": "Non è giusto! Io eseguo gli ordini!",
        "paura": "Siamo perduti... non posso rimediare...",
        "disgusto": "Che errore terribile... è insopportabile...",
        "noia": "Sì... ho sbagliato... che novità...",
        "felice": "È un success! Tutto sta andando a meraviglia!",
        "sorpresa": "Cosa? Com'è possibile tutto questo?",
        "determinato": "Riuscirò nella mia missione, costi quel che costi!",
        "neutro": "Sì, mio signore. Procederò come richiesto."
    }
    
    m = mood.lower().strip()
    if m in testi:
        # Applica posizione specifica
        if m == "triste":
            arms_sad(nao, 1.0)
            head(nao, 0.0, 0.30, 1.0)
        elif m == "arrabbiato":
            # Gesto secco
            nao.motion.angleInterpolation(
                ["LShoulderPitch", "RShoulderPitch"], [1.1, 1.1], [0.6, 0.6], True
            )
            head(nao, 0.0, 0.0, 0.6)
        elif m == "paura":
            head(nao, 0.2, 0.05, 0.4)
            time.sleep(0.2)
            head(nao, -0.2, 0.05, 0.4)
        elif m == "disgusto":
            head(nao, 0.35, 0.15, 0.8)
        elif m == "noia":
            head(nao, 0.0, 0.25, 1.5)
            
        #em.set_mood(m)
        #nao.say(testi[m])
        time.sleep(1.0)
    else:
        print("Mood '{}' non riconosciuto per Blocco 1".format(mood))

def esegui_blocco2(mood):
    """
    BLOCCO 2: Gestione emozioni dinamiche
    Testi da COPIONE.MD: Felicità, Determinazione, Sorpresa, Paura Attiva, Tristezza Profonda
    """
    testi = {
        "felice": "Posso rimediare! Non è finita!",
        "determinato": "Rimedierò. Non fallirò di nuovo.",
        "sorpresa": "#aspetta! E se esistesse un modo?",
        "paura": "Devo agire subito!",
        "triste": "Forse... non sono fatto per questo...",
        "arrabbiato": "Non è giusto! Io eseguo gli ordini!",
        "disgusto": "È rivoltante... dobbiamo cambiare rotta.",
        "noia": "Uff... un'altra incombenza noiosa...",
        "neutro": "Sì, mio signore. Procederò come richiesto."
    }
    
    m = mood.lower().strip()


    if m in testi:
        if m == "felice":
            arms_open_happy(nao, 1.0)
        elif m == "determinato":
            final_pose(nao, 1.0)
        elif m == "sorpresa":
            head(nao, 0.0, -0.15, 0.5)
        elif m == "paura":
            head(nao, 0.1, 0.0, 0.2)
            head(nao, -0.1, 0.0, 0.2)
        elif m == "triste":
            head(nao, 0.0, 0.45, 2.0)
            
        #em.set_mood(m)
        #nao.say(testi[m])
        time.sleep(1.0)
    else:
        print("Mood '{}' non riconosciuto per Blocco 2".format(mood))

def fase2(mood1, mood2):
    try:
        # Inizializzazione
        nao.posture.goToPosture("StandInit", 0.8)
        nao.motion.setStiffnesses("Body", 1.0)
        #cambia_colore_luci(BIANCO) # Luce bianca per iniziare la scena
        time.sleep(0.5)
        close_arms(nao, 0.6)
        time.sleep(0.5)

        # Entra e si ferma davanti a Oberon
        nao.motion.moveTo(0.15, 0.0, 0.0)
        time.sleep(0.8)

        # Inchino leggero
        head(nao, 0.0, 0.22, 0.8)
        time.sleep(0.4)
        head(nao, 0.0, 0.0, 0.6)
        
        posso_parlare()

        # **NAO PUCK**
        #em.set_mood(mood1)
        #nao.say("Nei pressi del suo giaciglio... un branco di giudici di una gara s’era riunito a vedere un dramma...")
        #cambia_colore_luci(VERDE) # Luce verde: Puck racconta del bosco
        if nao.audio_player:
            nao.audio_player.playFile(AUDIO_FILES["nei pressi"], _async=True)
            # Piccolo movimento descrittivo
            arms_both(nao, 1.0, 0.3, 1.0, -0.3, 1.5)
            time.sleep(1.5)
            arms_both(nao, 1.2, 0.1, 1.2, -0.1, 1.5)
        else:
            em.perform(AUDIO_FILES["nei pressi"], mood=mood1)
        time.sleep(0.5)

        #em.set_mood(mood2)
        indicate_jury(nao, 0.8)

        #aspetta()

        
        #nao.say("Uno di questi uscì... per parlare con la regina.")
        em.perform(AUDIO_FILES["uno di questi usci"], mood=mood2)
        time.sleep(0.5)

        #aspetta()
        
        #nao.say("E allora io"
        
        #cambia_colore_luci(VIOLETTO) # Luce violetta: momento magico del succo
        pour_motion(nao, 1.2)
        #nao.say("le versai nell’occhio il succo arcano!")
        em.perform(AUDIO_FILES["le versai nell’occhio il succo arcano"], mood=mood2)

        close_right_hand(nao, 0.4)
        time.sleep(0.2)

        #em.set_mood(mood1)
        open_arms_small(nao, 1.0)

        #aspetta()


        #nao.say("La regina si destò... e di lui subito s’innamorò!")
        em.perform(AUDIO_FILES["la regina si desto"], mood=mood1)
        # OBERON: La cosa è riuscita meglio di quanto pensassi!
        
        time.sleep(3.4)       #TEMPO CHE OBERON DICE LA BATTUTA
        #em.set_mood(mood2)
        #cambia_colore_luci(BLU) # Luce blu: Puck introduce il problema con esitazione
        head(nao, 0.0, 0.25, 1.0)
        arms_sad(nao, 1.2)

        #aspetta()

        posso_parlare()


        #nao.say("Sì, mio re... ma... c’è stato un leggerissimo problema...")
        em.perform(AUDIO_FILES["si mio re ma"], mood=mood2)
        # OBERON: Ovvero?

        posso_parlare()
        #em.set_mood(mood1)
        head(nao, 0.2, 0.35, 1.5)

        #nao.say("Guardai il volto della regina... e mai sfortuna fu così in#aspettata...")
        em.perform(AUDIO_FILES["e mai sfortuna"], mood=mood1)
        time.sleep(1.0)


        #em.set_mood(mood2)
        #cambia_colore_luci(ROSSO) # Luce rossa: colpo di scena del Duca Pedemonte
        head(nao, 0.0, -0.05, 0.3)
        indicate_jury(nao, 0.6)
        #nao.say("Era... il Duca Pedemonte.")
        em.perform(AUDIO_FILES["era il duca"], mood=mood2)
        
        #aspetta()

        posso_parlare()

        # OBERON: Puck! Sei l’assistente più inutile!

        #em.set_mood(mood1)
        nao.prepare_for_walk()
        nao.motion.moveTo(-0.05, 0.0, 0.0)
        # Gesto con palmi verso l'alto (aperti)
        nao.motion.angleInterpolation(
            ["LShoulderRoll", "RShoulderRoll", "LElbowRoll", "RElbowRoll"],
            [0.4, -0.4, -0.5, 0.5],
            [1.0, 1.0, 1.0, 1.0],
            True
        )
        #nao.say("Maestà... era buio... e poi... i giudici si assomigliano tutti...")
        em.perform(AUDIO_FILES["maesta era buio"], mood=mood1)

        #aspetta()

        posso_parlare()

        # OBERON: Ora la mia regina si è innamorata di un idiota! (pausa) No... si può ancora sistemare.
        
        # INSERISCI BLOCCO 1
        #cambia_colore_luci(BLU) # Luce blu: tristezza per l'errore commesso
        #esegui_blocco1(mood2)
        head(nao, 0.0, 0.4, 1.5) # Testa molto bassa
        em.perform(AUDIO_FILES["si ho sbagliato"], mood=mood2)

        posso_parlare()

        # OBERON: Basta esitazioni. Serve una soluzione... subito.
        #time.sleep(5.5)
        # INSERISCI BLOCCO 2

        posso_parlare()
        #em.perform(AUDIO_FILES[""])

        # FINALE
        # OBERON: Vai, Puck. E questa volta... non sbagliare bersaglio.
        #time.sleep(5.5)     #temp della battuta
        #em.set_mood(mood2)
        #cambia_colore_luci(CIANO) # Luce ciano: nuova determinazione
        final_pose(nao, 0.8)
        #nao.say("Stavolta no, mio re. Guarderò meglio. Agirò meglio.")
        em.perform(AUDIO_FILES["posso rimediare"], mood=mood2)

        #aspetta()

        time.sleep(0.5)
        #cambia_colore_luci(BIANCO) # Luce bianca: conclusione della scena
        head(nao, 0.3, -0.1, 0.6) # Sguardo complice al pubblico
        #nao.say("...forse.")
        em.perform(AUDIO_FILES["forse"], mood=mood2)
        
        # (Blackout)
        time.sleep(1.0)
        #spegni_luci() # Spegnimento luci finale
        nao.posture.goToPosture("Sit", 1.5)
        nao.motion.rest()

    except Exception as e:
        print("Errore durante Fase 2: " + str(e))

if __name__ == "__main__":
    fase2("felice", "arrabbiato")

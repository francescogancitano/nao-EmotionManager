# -*- coding: utf-8 -*-

import time, sys

from EmotionManager import EmotionManager

from utils.utils_positions import (
    head, close_arms, indicate_jury, pour_motion, 
    close_right_hand, open_arms_small, arms_sad, 
    arms_open_happy, final_pose
)

from utils.audio import AUDIO_FILES
from faro import *



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
        "felice": "È un successo! Tutto sta andando a meraviglia!",
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
        "sorpresa": "Aspetta! E se esistesse un modo?",
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
        #nao.posture.goToPosture("StandInit", 0.8)
        time.sleep(1.0)
        close_arms(nao, 0.6)
        time.sleep(0.5)

        # Entra e si ferma davanti a Oberon
        #nao.motion.moveTo(0.15, 0.0, 0.0)
        time.sleep(0.8)

        # Inchino leggero
        head(nao, 0.0, 0.22, 0.8)
        time.sleep(0.4)
        head(nao, 0.0, 0.0, 0.6)
        time.sleep(6)

        # **NAO PUCK**
        #em.set_mood(mood1)
        #nao.say("Nei pressi del suo giaciglio... un branco di giudici di una gara s’era riunito a vedere un dramma...")
        em.perform(AUDIO_FILES["nei pressi"], mood=mood1)
        time.sleep(0.5)

        #em.set_mood(mood2)
        indicate_jury(nao, 1.0)
        #nao.say("Uno di questi uscì... per parlare con la regina.")
        em.perform(AUDIO_FILES["uno di questi usci"], mood=mood2)
        time.sleep(1.0)
        
        #nao.say("E allora io")
        pour_motion(nao, 1.2)
        #nao.say("le versai nell’occhio il succo arcano!")
        em.perform(AUDIO_FILES["le versai nell’occhio il succo arcano"], mood=mood2)

        close_right_hand(nao, 0.4)
        time.sleep(0.2)

        #em.set_mood(mood1)
        open_arms_small(nao, 1.0)
        #nao.say("La regina si destò... e di lui subito s’innamorò!")
        em.perform(AUDIO_FILES["la regina si desto"], mood=mood1)
        # OBERON: La cosa è riuscita meglio di quanto pensassi!
        
        time.sleep(3.4)       #TEMPO CHE OBERON DICE LA BATTUTA
        #em.set_mood(mood2)
        head(nao, 0.0, 0.20, 1.1)
        #nao.say("Sì, mio re... ma... c’è stato un leggerissimo problema...")
        em.perform(AUDIO_FILES["si mio re ma"], mood=mood2)
        # OBERON: Ovvero?

        #em.set_mood(mood1)
        head(nao, 0.0, 0.35, 1.5)
        #FIXME: mi sono scordato nell'audio di mettere il pezzo guardai il volto della regina, se va tutto bene rigener l'audio e aggiungi questo pezzo mancante
        #nao.say("Guardai il volto della regina... e mai sfortuna fu così inaspettata...")
        em.perform(AUDIO_FILES["e mai sfortuna"], mood=mood1)
        time.sleep(1.0)

        #em.set_mood(mood2)
        head(nao, 0.0, -0.05, 0.3)
        indicate_jury(nao, 0.6)
        #nao.say("Era... il Duca Pedemonte.")
        em.perform(AUDIO_FILES["era il duca"], mood=mood2)
        
        # OBERON: Puck! Sei l’assistente più inutile!
        time.sleep(3)
        #em.set_mood(mood1)
        #nao.motion.moveTo(-0.05, 0.0, 0.0)
        #nao.say("Maestà... era buio... e poi... i giudici si assomigliano tutti...")
        em.perform(AUDIO_FILES["maesta era buio"], mood=mood1)

        # OBERON: Ora la mia regina si è innamorata di un idiota! (pausa) No... si può ancora sistemare.

        time.sleep(8)
        # INSERISCI BLOCCO 1
        #esegui_blocco1(mood2)
        em.perform(AUDIO_FILES["si ho sbagliato"], mood=mood2)

        # OBERON: Basta esitazioni. Serve una soluzione... subito.
        time.sleep(5.5)
        # INSERISCI BLOCCO 2
        #em.perform(AUDIO_FILES[""])

        # FINALE
        # OBERON: Vai, Puck. E questa volta... non sbagliare bersaglio.
        #time.sleep(5.5)     #temp della battuta
        #em.set_mood(mood2)
        final_pose(nao, 1.0)
        #nao.say("Stavolta no, mio re. Guarderò meglio. Agirò meglio.")
        em.perform(AUDIO_FILES["posso rimediare"], mood=mood2)

        time.sleep(0.5)
        head(nao, 0.0, -0.05, 0.6)
        #nao.say("...forse.")
        em.perform(AUDIO_FILES["forse"], mood=mood2)
        
        # (Blackout)
        nao.posture.goToPosture("Sit", 1.0)
        nao.motion.rest()

    except Exception as e:
        print("Errore durante Fase 2: " + str(e))

if __name__ == "__main__":
    fase2("felice", "arrabbiato")

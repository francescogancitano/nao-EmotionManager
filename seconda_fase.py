# -*- coding: utf-8 -*-
from EmotionManager import EmotionManager
from utils_positions import (
    head, close_arms, indicate_jury, pour_motion, 
    close_right_hand, open_arms_small, arms_sad, 
    arms_open_happy, final_pose
)
import time

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
        "rabbia": "Non è giusto! Io eseguo gli ordini!",
        "paura": "Siamo perduti... non posso rimediare...",
        "disgusto": "Che errore terribile... è insopportabile...",
        "noia": "Sì... ho sbagliato... che novità..."
    }
    
    m = mood.lower().strip()
    if m in testi:
        # Applica posizione specifica
        if m == "triste":
            arms_sad(nao, 1.0)
            head(nao, 0.0, 0.30, 1.0)
        elif m == "rabbia":
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
            
        em.set_mood(m)
        nao.say(testi[m])
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
        "triste": "Forse... non sono fatto per questo..."
    }
    
    m = mood.lower().strip()
    # Mappatura nomi lunghi del copione a quelli brevi del sistema
    if m == "determinazione": m = "determinato"
    if m == "felicità": m = "felice"
    if m == "paura attiva": m = "paura"
    if m == "tristezza profonda": m = "triste"

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
            
        em.set_mood(m)
        nao.say(testi[m])
        time.sleep(1.0)
    else:
        print("Mood '{}' non riconosciuto per Blocco 2".format(mood))

def fase2(mood1, mood2):
    try:
        # Inizializzazione
        nao.posture.goToPosture("StandInit", 0.8)
        time.sleep(1.0)
        close_arms(nao, 0.6)
        time.sleep(0.5)

        # Entra e si ferma davanti a Oberon
        nao.motion.moveTo(0.15, 0.0, 0.0)
        time.sleep(0.8)

        # Inchino leggero
        head(nao, 0.0, 0.22, 0.8)
        time.sleep(0.4)
        head(nao, 0.0, 0.0, 0.6)
        time.sleep(0.5)

        # **NAO PUCK**
        em.set_mood("felice")
        nao.say("Nei pressi del suo giaciglio... un branco di giudici di una gara s’era riunito a vedere un dramma...")
        time.sleep(0.5)

        em.set_mood("sorpresa")
        indicate_jury(nao, 1.0)
        nao.say("Uno di questi uscì... per parlare con la regina.")
        time.sleep(1.0)
        
        nao.say("E allora io")
        pour_motion(nao, 1.2)
        nao.say("le versai nell’occhio il succo arcano!")
        
        close_right_hand(nao, 0.4)
        time.sleep(0.2)

        em.set_mood("felice")
        open_arms_small(nao, 1.0)
        nao.say("La regina si destò... e di lui subito s’innamorò!")
        
        # OBERON: La cosa è riuscita meglio di quanto pensassi!
        
        em.set_mood("triste")
        head(nao, 0.0, 0.20, 1.1)
        nao.say("Sì, mio re... ma... c’è stato un leggerissimo problema...")
        
        # OBERON: Ovvero?

        em.set_mood("triste")
        head(nao, 0.0, 0.35, 1.5)
        nao.say("Guardai il volto della regina... e mai sfortuna fu così inaspettata...")
        time.sleep(1.0)

        em.set_mood("arrabbiato")
        head(nao, 0.0, -0.05, 0.3)
        indicate_jury(nao, 0.6)
        nao.say("Era... il Duca Pedemonte.")
        
        # OBERON: Puck! Sei l’assistente più inutile!

        em.set_mood("triste")
        nao.motion.moveTo(-0.05, 0.0, 0.0)
        nao.say("Maestà... era buio... e poi... i giudici si assomigliano tutti...")
        
        # OBERON: Ora la mia regina si è innamorata di un idiota! (pausa) No... si può ancora sistemare.

        # INSERISCI BLOCCO 1
        esegui_blocco1(mood1)

        # OBERON: Basta esitazioni. Serve una soluzione... subito.

        # INSERISCI BLOCCO 2
        esegui_blocco2(mood2)

        # FINALE
        # OBERON: Vai, Puck. E questa volta... non sbagliare bersaglio.

        em.set_mood("determinato")
        final_pose(nao, 1.0)
        nao.say("Stavolta no, mio re. Guarderò meglio. Agirò meglio.")
        
        time.sleep(0.5)
        head(nao, 0.0, -0.05, 0.6)
        nao.say("...forse.")
        
        # (Blackout)
        nao.posture.goToPosture("Sit", 1.0)
        nao.motion.rest()

    except Exception as e:
        print("Errore durante Fase 2: " + str(e))

if __name__ == "__main__":
    fase2("arrabbiato", "felice")

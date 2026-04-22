# -*- coding: utf-8 -*-
from EmotionManager import EmotionManager
from utils_positions import head, arms_both, right_arm_magic_pose
import time

# Inizializzazione EmotionManager (default localhost)
em = EmotionManager()
nao = em.nao

def prima_fase():
    try:
        nao.motion.wakeUp()
        nao.posture.goToPosture("StandInit", 0.5)
        nao.motion.setStiffnesses("Body", 1.0)

        try:
            nao.leds.fadeRGB("FaceLeds", 0x000000, 0.5)
            nao.leds.fadeRGB("ChestLeds", 0x000000, 0.5)
        except:
            pass

    except Exception as e:
        print("Errore inizializzazione: " + str(e))

    try:
        # (Buio. Pausa.)
        time.sleep(2.0)

        # (NAO accende le luci alzando lentamente un braccio verso l’alto)
        nao.motion.angleInterpolation(["RShoulderPitch"], [-0.5], [2.0], True)
        
        # OBERON: Perfetto. Le luci sono accese... e lo sfondo impostato. Siamo pronti a entrare in scena.
        # time.sleep(4.0)
        
        # (NAO abbassa il braccio e si porta in posizione neutra. Sfondo: bosco)
        nao.posture.goToPosture("StandInit", 1.0)
        
        # CAMMINATA: 3 secondi normale + 2 secondi lenta
        nao.motion.setWalkTargetVelocity(0.6, 0.0, 0.0, 0.5)
        time.sleep(3.0)
        nao.motion.setWalkTargetVelocity(0.22, 0.0, 0.0, 0.5)
        time.sleep(2.0)
        nao.motion.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.5)
        time.sleep(0.5)

        # LUCI
        try:
            nao.leds.fadeRGB("FaceLeds", 0xFFFFFF, 2.0)
            nao.leds.fadeRGB("ChestLeds", 0xFFFFFF, 2.0)
        except:
            pass
        time.sleep(0.8)

        # **NAO PUCK**
        # _set_felice_
        em.set_mood("felice")
        
        # (Braccia leggermente aperte, movimento leggero del busto)
        arms_both(nao, 0.7, 0.9, 0.7, -0.9, 1.5)
        
        nao.say("Per il bosco ho scorrazzato e nessun ateniese vi ho trovato sui cui occhi provare se il fiore è poi vero che suscita amore...")
        time.sleep(0.5)

        # _set_sorpresa_
        em.set_mood("sorpresa")
        # (Testa che scatta a destra, poi a sinistra)
        head(nao, 0.42, -0.08, 0.5)
        time.sleep(0.3)
        head(nao, -0.42, -0.08, 0.5)
        time.sleep(0.3)
        head(nao, 0.0, -0.05, 0.5)

        nao.say("Notte e pace... ma chi è là? Son d’Atene i vestimenti! È sicuramente questi colui che sdegna, come ha detto il mio Re, la sua fanciulla!")
        time.sleep(0.5)

        # _set_triste_
        em.set_mood("triste")
        # (Testa leggermente abbassata, braccia più vicine al corpo)
        nao.motion.angleInterpolation(
            ["HeadPitch", "LShoulderPitch", "RShoulderPitch"],
            [0.28, 1.45, 1.45],
            [1.0, 1.0, 1.0],
            True
        )
        
        nao.say("Poverina... non s’azzarda certo a giacersi accanto a lui... lui che tanto ne disprezza affetto e cortesia...")
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
        
        nao.say("Sui tuoi occhi, a te, villano, ecco verso il succo arcano! Quando gli occhi riaprirai, da essi Amor bandisca il sonno!")
        
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
        
        nao.say("Ma allora saro lontano....... perche da Oberon faccio ritorno!")
        time.sleep(1.0)

        # (Fine Fase 1)
        # USCITA
        nao.motion.moveTo(0.20, 0.0, 0.25)

        # SPEGNIMENTO LUCI
        try:
            nao.leds.fadeRGB("FaceLeds", 0x000000, 1.5)
            nao.leds.fadeRGB("ChestLeds", 0x000000, 1.5)
        except:
            pass

    except Exception as e:
        print("Errore durante l'esecuzione: " + str(e))

if __name__ == "__main__":
    prima_fase()

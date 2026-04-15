# -*- coding: utf-8 -*-
import time
import qi
from EmotionManager import EmotionManager
from utils import logger

# Configurazione Robot
IP_ADDRESS = "192.168.178.36"

# Inizializzazione EmotionManager e servizi
try:
    nao_manager = EmotionManager(IP_ADDRESS)
    robot = nao_manager.nao
    session = robot.session
    
    # Servizi Nao
    motion = robot.motion
    leds = robot.leds
    posture = robot.posture
except Exception as e:
    logger.error("Errore durante l'inizializzazione: {}".format(e))
    exit(1)


def functionSetup():
    """Prepara il robot per la performance."""
    try:
        if motion:
            motion.wakeUp()
            motion.setStiffnesses("Body", 1.0)
        
        if posture:
            posture.goToPosture("StandInit", 0.5)

        if leds:
            try:
                leds.fadeRGB("FaceLeds", 0x000000, 0.5)
                leds.fadeRGB("ChestLeds", 0x000000, 0.5)
            except:
                pass
    except Exception as e:
        logger.error("Errore in functionSetup: {}".format(e))


# ----------------------------
# FUNZIONI DI MOVIMENTO
# ----------------------------

def head(yaw, pitch, duration):
    if motion:
        motion.angleInterpolation(
            ["HeadYaw", "HeadPitch"],
            [yaw, pitch],
            [duration, duration],
            True
        )

def arms_both(l_pitch, l_roll, r_pitch, r_roll, duration):
    if motion:
        motion.angleInterpolation(
            ["LShoulderPitch", "LShoulderRoll", "RShoulderPitch", "RShoulderRoll"],
            [l_pitch, l_roll, r_pitch, r_roll],
            [duration]*4,
            True
        )

def right_arm_magic_pose(duration):
    if motion:
        motion.angleInterpolation(
            ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw", "RHand"],
            [0.95, -0.22, 1.0, 0.65, 0.15, 1.0],
            [duration]*6,
            True
        )


# ----------------------------
# PRIMA FASE
# ----------------------------

def onInput_onStart():
    try:
        # ----------------------------
        # CAMMINATA
        # ----------------------------
        if motion:
            motion.setWalkTargetVelocity(0.6, 0.0, 0.0, 0.5)
            time.sleep(3.0)

            motion.setWalkTargetVelocity(0.22, 0.0, 0.0, 0.5)
            time.sleep(2.0)

            motion.setWalkTargetVelocity(0.0, 0.0, 0.0, 0.5)

        time.sleep(0.5)

        # ----------------------------
        # LUCI
        # ----------------------------
        if leds:
            try:
                leds.fadeRGB("FaceLeds", 0xFFFFFF, 2.0)
                leds.fadeRGB("ChestLeds", 0xFFFFFF, 2.0)
            except:
                pass


        time.sleep(1.0)

        # ----------------------------
        # ALI (MOVIMENTO LENTO + PAUSA LUNGA)
        # ----------------------------
        arms_both(0.7, 0.9, 0.7, -0.9, 2.0)  # lento
        time.sleep(4.0)  # 🔥 tiene la posa

        # Testa lenta (NON tocca le braccia)
        head(0.25, -0.05, 1.2)
        time.sleep(0.6)

        head(-0.25, -0.05, 1.4)
        time.sleep(0.6)

        head(0.0, -0.05, 1.2)
        time.sleep(0.6)


       
        #nao_manager.perform(stringa)

        time.sleep(1.0)

        # ----------------------------
        # TESTA DX/SX
        # ----------------------------
        head(0.42, -0.08, 1.3)
        time.sleep(0.5)

        head(-0.42, -0.08, 1.5)
        time.sleep(0.5)

        head(0.0, -0.08, 1.2)
        time.sleep(0.5)

        # Passo indietro
        if motion:
            motion.moveTo(-0.05, 0.0, 0.0)
        time.sleep(0.8)

        # Guarda uomo
        head(0.45, 0.05, 1.2)
        time.sleep(1.2)

        # Guarda donna
        head(-0.45, 0.0, 1.3)
        time.sleep(1.2)

        # Ritorna
        head(0.35, 0.0, 1.1)
        time.sleep(0.7)

        # ----------------------------
        # POSA MAGIA
        # ----------------------------
        if motion:
            motion.angleInterpolation(
                ["HeadPitch", "LShoulderPitch", "RShoulderPitch"],
                [0.28, 1.45, 1.45],
                [1.2, 1.2, 1.2],
                True
            )
        time.sleep(1.0)

        # Mano tesa
        if motion:
            motion.angleInterpolation(
                ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RHand"],
                [0.95, -0.15, 1.0, 0.6, 1.0],
                [1.2]*5,
                True
            )
        time.sleep(1.0)

        # DIALOGO: osservazione
        # Inserisci qui il dialogo

        time.sleep(1.0)

        # ----------------------------
        # MAGIA LUNGA
        # ----------------------------
        right_arm_magic_pose(1.2)

        # DIALOGO: formula magica
        # Inserisci qui il dialogo

        # Movimento continuo (NON cambia posa)
        if motion:
            motion.angleInterpolation(["RWristYaw"], [-0.65], [1.6], True)
            motion.angleInterpolation(["RWristYaw"], [0.45], [1.6], True)
            motion.angleInterpolation(["RWristYaw"], [-0.35], [1.4], True)
            motion.angleInterpolation(["RWristYaw"], [0.20], [1.2], True)

        time.sleep(1.2)

        # ----------------------------
        # RESET
        # ----------------------------
        if posture:
            posture.goToPosture("StandInit", 1.0)
        time.sleep(1.0)

        # Verso pubblico
        if motion:
            motion.moveTo(0.06, 0.0, 0.0)
        time.sleep(0.8)

        # ----------------------------
        # ALI FINALI (SUPER EVIDENTI)
        # ----------------------------
        arms_both(0.65, 1.0, 0.65, -1.0, 2.2)  # molto lento
        time.sleep(4.0)  # 🔥 posa lunga

        # DIALOGO finale
        # Inserisci qui il dialogo

        time.sleep(0.5)

        # Uscita
        if motion:
            motion.moveTo(0.20, 0.0, 0.25)

        # Spegne luci
        if leds:
            try:
                leds.fadeRGB("FaceLeds", 0x000000, 1.5)
                leds.fadeRGB("ChestLeds", 0x000000, 1.5)
            except:
                pass

    except Exception as e:
        logger.error("Errore durante l'esecuzione: {}".format(e))


if __name__ == "__main__":
    functionSetup()
    onInput_onStart()

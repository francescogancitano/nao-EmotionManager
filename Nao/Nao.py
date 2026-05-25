# -*- coding: utf-8 -*-

import qi, sys
from utils.log import logger

DEFAULT_COLOR_FADE_TIME = 0.2
DEFAULT_MOTION_SPEED    = 0.2


class Nao(object):

    def __init__(self, ip_address="192.168.178.36", port=9559):
        """inizializza la connessione e carica i servizi di Nao."""
        logger.info("connessione a Nao su {}:{}".format(ip_address, port))

        self.session = qi.Session()
        try:
            self.session.connect("tcp://{}:{}".format(ip_address, port))
            logger.info("connessione riuscita")
        except RuntimeError as e:
            logger.critical("impossibile connettersi: {}".format(e))
            sys.exit(1)

        self.tts = self.session.service("ALTextToSpeech")

        try:
            self.leds         = self.session.service("ALLeds")
            self.motion       = self.session.service("ALMotion")
            self.posture      = self.session.service("ALRobotPosture")
            self.audio_player = self.session.service("ALAudioPlayer")

            if self.motion and not self.motion.robotIsWakeUp():
                self.motion.wakeUp()

            logger.info("robot fisico inizializzato")

        except RuntimeError:
            logger.warning("servizi fisici non disponibili, modalita' virtuale attiva")
            self.leds         = None
            self.motion       = None
            self.posture      = None
            self.audio_player = None


    def say(self, text):
        """Fa parlare Nao."""
        # Se il testo è unicode (Python 2), lo codifichiamo in utf-8 per il robot.
        try:
            if isinstance(text, unicode):
                text = text.encode('utf-8')
        except NameError:
            # Python 3: str è già unicode, solitamente va bene così o si può codificare in bytes
            pass

        logger.info("dico: {}".format(text))
        self.tts.say(text)


    def set_voice(self, speed, tone):
        """
        imposta velocità e tono della voce.
        speed: intero, 100 = normale
        tone:  float, 1.0 = normale
        """
        logger.info("voce -> speed={} tone={}".format(speed, tone))
        self.tts.setParameter("speed", speed)
        self.tts.setParameter("pitchShift", tone)


    def set_body_color(self, color_hex):
        """
        imposta il colore degli occhi (LED).
        color_hex: intero esadecimale, es. 0xFF0000 per rosso
        """
        logger.info("nao -> colore={}".format(hex(color_hex)))
        if self.leds:
            self.leds.fadeRGB("FaceLeds", color_hex, DEFAULT_COLOR_FADE_TIME)
            self.leds.fadeRGB("ChestLeds", color_hex, DEFAULT_COLOR_FADE_TIME)


    def move_head(self, pitch_angle):
        """
        inclina la testa verticalmente.
        pitch_angle: radianti — positivo = abbassa, negativo = alza
        """
        logger.info("testa -> pitch={} rad".format(pitch_angle))
        if self.motion:
            self.motion.setAngles("HeadPitch", pitch_angle, DEFAULT_MOTION_SPEED)


    def rotate_deg(self, degrees, is_async=False):
        """
        Fa ruotare Nao su se stesso usando i gradi.
        degrees: positivi = sinistra, negativi = destra.
        """
        import math
        radians = math.radians(degrees)
        logger.info("rotazione -> {} gradi ({} rad)".format(degrees, radians))
        if self.motion:
            if is_async:
                self.motion.moveTo(0.0, 0.0, radians, _async=True)
            else:
                self.motion.moveTo(0.0, 0.0, radians)


    def prepare_for_walk(self):
        """Ottimizza i parametri del robot per una camminata più stabile."""
        if self.motion:
            logger.info("ottimizzazione parametri camminata...")
            # Rigidità massima alle gambe per evitare cedimenti
            self.motion.setStiffnesses("Legs", 0.8)
            # Abilita il bilanciamento automatico delle braccia durante il passo
            self.motion.setMoveArmsEnabled(True, True)
            # Parametri di camminata più 'morbidi' (altezza passo ridotta per stabilità)
            self.motion.setWalkArmsEnabled(True, True)
        else:
            logger.warning("motion non disponibile: impossibile preparare la camminata")


    def play_audio(self, audio_file):
        """
        riproduce un file audio.
        rfrmati supportati: .wav, .mp3, .ogg
        """
        logger.info("audio -> {}".format(audio_file))
        if self.audio_player:
            self.audio_player.playFile(audio_file)
        else:
            logger.warning("audio non disponibile in modalita' virtuale")

            

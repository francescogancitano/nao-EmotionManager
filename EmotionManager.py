# -*- coding: utf-8 -*-

""""
        !!!ATTENZIONE!!!
    questo script deve essere eseguito sulla versione 2.7 di python
    funzionerà solo ed esclusivamente su questa versione
    perchè questo script si basa sulle funzioni di naoqi

"""

import qi
import sys
import time
import re
import io
import colorlog
import logging


DEFAULT_COLOR_FADE_TIME = 0.2           #questa costante definisce quanto tempo ci impiega nao a cambiare colore degli occhi
DEFAULT_MOTION_SPEED = 0.2        #questa costante definisce la velocità in cui nao va a muovere la testa da una posizione a un altra

handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s[%(lineno)d]\t[%(levelname)s] [%(funcName)s]%(reset)s %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = colorlog.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class EmotionManager:

    def __init__(self, ip_address, port=9559):
        #inizializza la connessione a nao
        logger.info("inizializzando classe EmotionManager")

        self.session = qi.Session()
        logger.info("inizializzando connessione con nao")
        try:
            self.session.connect("tcp://{}:{}".format(ip_address, port))
            logger.info("connessione effettuata con successo all'indirizzo {}".format(ip_address))
        except RuntimeError as e:
            logger.critical("impossibile connettersi a {}".format(ip_address))
            logger.error("{}".format(e))
            sys.exit(1)

        # Carico i servizi necessari (alcuni potrebbero non essere disponibili sul virtuale)
        logger.info("inizializzando il robot fisico")

        logger.info("inizializzando il text to speech")
        self.tts = self.session.service("ALTextToSpeech")

        try:
            logger.debug("inizializzando i led")
            self.leds = self.session.service("ALLeds")

            logger.debug("inizializzando i motori")
            self.motion = self.session.service("ALMotion")

            logger.debug("inizializzando l'audio player")
            self.audio_player = self.session.service("ALAudioPlayer")

            if not self.motion.robotIsWakeUp():
                self.motion.wakeUp()


            logger.info("nao e' stato inizializzato correttamente")


        except RuntimeError:
            """siccome nao fisico non c'è allora utilizzerà le api di naoqi"""
            logger.warning("servizzi di ALdebaran non disponibili, entrando in modalita' virtuale")
            self.leds         = None
            self.motion       = None
            self.audio_player = None


    def _move_head(self, pitch_angle):
        """
        nao misura i movimenti di testa in radianti,
        se il numero e' positivi abbassera' la testa,
        se il numero e' negativo alzera' la testa
        """
        logger.info("muovendo la testa di: {} radianti".format(pitch_angle))

        if self.motion:
            self.motion.setAngles("HeadPitch", pitch_angle, DEFAULT_MOTION_SPEED)

    def _set_leds(self, eyesColor):
        """
        questa funzione imposta il colore dei led in base ai parametri dati
        se ci si trova in una modalità virtuale allora non verranno utilizzati per evitare gli errori
        """
        logger.info("cambiando colore occhi in {}".format(eyesColor))
        if self.leds:
            self.leds.fadeRGB("FaceLeds", eyesColor, DEFAULT_COLOR_FADE_TIME)


    def _set_voice(self, voiceSpeed, voiceTone):
        """
        questa funzione va a impostare la voce di nao,
        in modo da poter cambiare la velocità della sua voce e del suo tono
        """
        logger.info("impostando velocita' voce a: {}".format(voiceSpeed))
        logger.info("impostando tono di voce a {}".format(voiceTone))
        self.tts.setParameter("speed", voiceSpeed)
        self.tts.setParameter("pitchShift", voiceTone)


    def set_mood(self, mood_name):
        """
        questa è la funzione su cui si basa questa classe
        dove passando un semplice 'mood'
        la funzione andrà a gestirsi tutte le componentistiche di nao, cioè:
            movimento della testa;
            colore degli occhi;
            la velocità della voce;
            il tono della voce;

        il 'mood' può essere scritto in italiano o in inglese senza nessun problema
        """

        mood = mood_name.lower().strip() #ricava il "mood" in forma "pura"

        """
        questi sono i dati nudi e crudi delle impostazioni, cioè delle chiavi e delle configurazioni
        le chiavi sono scritte come ho detti sia in italiano sia in inglese
        """
        _MOOD_DEFAULTS = {            #mv testa       mood per log          colore degli occhi          velocità voce      tono di voce
            ("felice", "happy"):     {"head": -0.4,  "log": "FELICE",      "coloreOcchiHEX": 0x00FF00, "voiceSpeed": 120, "voiceTone": 1.2},
            ("triste", "sad"):       {"head": 0.4,   "log":  "TRISTE",     "coloreOcchiHEX": 0x0000FF, "voiceSpeed": 75,  "voiceTone": 0.8},
            ("arrabbiato", "angry"): {"head": 0.0,   "log":  "ARRABBIATO", "coloreOcchiHEX": 0xFF0000, "voiceSpeed": 110, "voiceTone": 0.9},
            ("neutro", "neutral"):   {"head": 0.0,   "log":  "NEUTRI",     "coloreOcchiHEX": 0xFFFFFF, "voiceSpeed": 100, "voiceTone": 1.0},
        }


        """qui i dati vengono elaborati in modo puliti per essere interpretati da python"""
        MOOD_CONFIG = {}
        for keys, config in _MOOD_DEFAULTS.items():
            for key in keys:
                MOOD_CONFIG[key] = config

        config = MOOD_CONFIG.get(mood)

        """qui va a cambiare fisicamente colore occhi voce etc"""
        if config:
            logger.info("imposto emozione: {}".format(config["log"]))
            self._set_leds(config["coloreOcchiHEX"])
            self._set_voice(config["voiceSpeed"], config["voiceTone"])
            self._move_head(config["head"])
        else:
            logger.warning("mood non riconosciuto, impostando NEUTRO di default")
            self._set_leds(MOOD_CONFIG["neutro"]["coloreOcchiHEX"])
            self._set_voice(MOOD_CONFIG["neutro"]["voiceSpeed"], MOOD_CONFIG["neutro"]["voiceTone"])
            self._move_head(0.0)

    def perform_script(self, input_data, mood=None):
        """
        DESCRIZIONE
        questa funzione è la 'principale' perchè va a eseguire il 'copione' di nao
        come funziona:

        TESTI
        il parametro input_data può essere una qualsiasi cosa, un file di testo, una stringa, o un file audio (nao supporta solo wav o ogg come formati)
        i testi in generale di default andrà a recitarli con un mood, che troverà nel testo o che sarà specificato nei parametri con "mood"
        specificando questo parametro nao se troverà nel testo l'istruzione che gli dirà di cambiare emozione, la ignorerà

        AUDIO
        nel caso di file audio nao ovviamente non può trovare istruzioni per cambiare le emozioni quindi gli audio verranno riprodotti per come sono
        se si aggiunge il 'mood' nei parametri cambierà la sua emozione ma ovviamente solo per il tempo di esecuzione e non nel mentre
        """

        # Determina il tipo di input
        if self._is_audio_file(input_data):
            # E' un file audio — riproducilo direttamente
            self._play_audio(input_data)
            return
        elif self._is_text_file(input_data):
            # E' un file testo — leggi il contenuto
            try:
                with io.open(input_data, 'r', encoding='utf-8') as f:
                    text = f.read()
            except IOError as e:
                logger.error("errore lettura file: {}".format(e))
                return
        else:
            # E' una stringa
            text = input_data

        # Elabora il testo
        if mood:
            # Applica un'emozione fissa, ignorando i comandi inline
            self.set_mood(mood)
            logger.info("il modd e' stato fissato a: {}".format(mood))
            # Rimuovi i comandi *set_xxx dal testo
            clean_text = re.sub(r'\*set_\w+\s*', '', text)
            self.say(clean_text.strip())
        else:
            # Elabora normalmente con emozioni inline
            pattern = r'(\*set_\w+)'
            parts = re.split(pattern, text.strip())

            for part in parts:
                part = part.strip()
                if not part:
                    continue

                if re.match(r'\*set_\w+', part):
                    # E' un comando — estraggo il nome del mood ed eseguo
                    mood_name = part[5:]  # rimuove il *set_ -> "happy"
                    self.set_mood(mood_name)
                else:
                    # E' testo normale — lo mando al TTS
                    self.say(part)

    @staticmethod
    def _is_audio_file(path):
        """Controlla se il percorso è un file audio."""
        audio_extensions = ('.wav', '.mp3', '.ogg')         #questi sono gli unici formati audio supportati da nao
        try:
            return any(path.lower().endswith(ext) for ext in audio_extensions)
        except (AttributeError, TypeError):
            return False

    @staticmethod
    def _is_text_file(path):
        """Controlla se il percorso è un file testo."""
        try:
            return path.lower().endswith('.txt')
        except (AttributeError, TypeError):
            return False

    def _play_audio(self, audio_file):
        """
        Riproduce un file audio.
        Nota: Richiede ALAudioPlayer sul robot.
        """
        if self.audio_player:
                self.audio_player.playFile(audio_file)
                logger.debug("riproducendo audio: {}".format(audio_file))
        else:
            logger.warning("l'audio non e' disponibile")


    def say(self, text):
        """Wrapper per far parlare il robot."""
        self.tts.say(text)


# --- ESEMPIO DI UTILIZZO ---
if __name__ == "__main__":
    NAO_IP = "127.0.0.1"    #ip di nao a cui connettersi

    nao = EmotionManager(NAO_IP)


    """test delle emozioni"""
    nao.set_mood("angry")

    time.sleep(3)

    nao.set_mood("sad")

    time.sleep(3)

    nao.set_mood("happy")

    time.sleep(3)

    """test per stringa normale"""
    script = "per il bosco ho scorrazzato e nessun ateniese vi ho trovato su cui occhi provare se il fiore e' poi vero che suscita amore notte e pace... ma chi e' la? son d'atene i vestimenti! e sicuramente questi e' colui che sdegna come ha detto il mio re la sua fanciulla"
    nao.perform_script(script)

    """test per file di testo"""
    nao.perform_script("test.txt")


    """test per file audio wav"""
    nao.perform_script("test.wav")


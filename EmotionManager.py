# -*- coding: utf-8 -*-

import re
import sys
from time import sleep

from Nao import Nao

from utils.log import logger
from utils.utils import determine_file_type
from utils.emotions import MOOD_CONFIG, NEUTRAL_CONFIG

class EmotionManager(object):

    def __init__(self):
        """Inizializza EmotionManager e il robot Nao."""
        self.nao = Nao()


    def set_mood(self, mood_name):
        """
        Applica un'emozione a Nao: occhi, voce e testa cambiano di conseguenza.
        Accetta sia italiano che inglese (es. 'felice' o 'happy').
        """
        config = MOOD_CONFIG.get(mood_name.lower().strip())

        if config:
            logger.info("emozione -> {}".format(config["log"]))
            self.nao.set_body_color(config["coloreOcchiHEX"])
            self.nao.set_voice(config["voiceSpeed"], config["voiceTone"])
            self.nao.move_head(config["head"])
        else:
            logger.warning("mood '{}' non riconosciuto, uso neutro".format(mood_name))
            self.nao.set_body_color(NEUTRAL_CONFIG["coloreOcchiHEX"])
            self.nao.set_voice(NEUTRAL_CONFIG["voiceSpeed"], NEUTRAL_CONFIG["voiceTone"])
            self.nao.move_head(0.0)

        sleep(0.3)


    def perform(self, input_data, mood=None):
        """
        Fa eseguire a Nao un contenuto: stringa, file .txt o file audio.
        Se mood è specificato, sovrascrive eventuali emozioni inline nel testo.
        """
        file_type, content = determine_file_type(input_data)
        if file_type is None:
            logger.warning("esecuzione annullata: input_data non valido o inaccessibile")
            return

        if file_type == "audio":
            self.nao.play_audio(content)
            return

        if mood:
            self._perform_with_fixed_mood(content, mood)
        else:
            self._perform_with_inline_moods(content)


    def _perform_with_fixed_mood(self, text, mood):
        """Esegue il testo con un'emozione fissa, ignorando i comandi inline."""
        self.set_mood(mood)
        clean_text = re.sub(r'\*set_\w+\s*', '', text).strip()
        self.nao.say(clean_text)


    def _perform_with_inline_moods(self, text):
        """Esegue il testo rispettando i comandi *set_mood inline."""
        parts = re.split(r'(\*set_\w+)', text.strip())

        for part in parts:
            part = part.strip()
            if not part:
                continue

            if re.match(r'\*set_\w+', part):
                self.set_mood(part[5:])  # estrae il nome dopo *set_
            else:
                self.nao.say(part)


if __name__ == "__main__":
    manager = EmotionManager()

    manager.perform("cetttu", mood="sad")
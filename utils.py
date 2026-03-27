# -*- coding: utf-8 -*-

import colorlog
import logging
import io





"""QUESTI SONO UTILS PER L'EMOZIONI"""
_MOOD_DEFAULTS = {                      #mv testa       mood per log          colore degli occhi          velocità voce      tono di voce
            ("felice", "happy"):       {"head": -0.4,  "log":  "FELICE",     "coloreOcchiHEX": 0xFFFF00, "voiceSpeed": 120, "voiceTone": 1.2},
            ("triste", "sad"):         {"head": 0.4,   "log":  "TRISTE",     "coloreOcchiHEX": 0x0000FF, "voiceSpeed": 75,  "voiceTone": 0.8},
            ("arrabbiato", "angry"):   {"head": 0.0,   "log":  "ARRABBIATO", "coloreOcchiHEX": 0xFF0000, "voiceSpeed": 110, "voiceTone": 0.9},
            ("neutro", "neutral"):     {"head": 0.0,   "log":  "NEUTRI",     "coloreOcchiHEX": 0xFFFFFF, "voiceSpeed": 100, "voiceTone": 1.0},
            ("sorpresa", "surprised"): {"head": 0.0,   "log":  "SORPRESA",   "coloreOcchiHEX": 0xFFA500, "voiceSpeed": 100, "voiceTone": 1.1},
            ("paura", "afraid"):       {"head": -0.2,  "log":  "PAURA",      "coloreOcchiHEX": 0xFF00FF, "voiceSpeed": 90,  "voiceTone": 0.7},
            ("disgusto", "disgusted"): {"head": 0.2,   "log":  "DISGUSTO",   "coloreOcchiHEX": 0x00FF00, "voiceSpeed": 85,  "voiceTone": 0.9},
            ("noia", "bored"):         {"head": 0.1,   "log":  "NOIA",       "coloreOcchiHEX": 0x808080, "voiceSpeed": 70,  "voiceTone": 0.95},
}


MOOD_CONFIG = {}
for _keys, _config in _MOOD_DEFAULTS.items():
    for _key in _keys:
        MOOD_CONFIG[_key] = _config

NEUTRAL_CONFIG = MOOD_CONFIG["neutro"]



"""QUESTI SONO UTILS PER IL LOGGING"""
_handler = colorlog.StreamHandler()
_handler.setFormatter(colorlog.ColoredFormatter(
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
logger.addHandler(_handler)
logger.setLevel(logging.DEBUG)



"""QUI CI SONO UTILS PER I FILE"""
def is_audio_file(path):
    """controlla se il percorso è un file audio."""
    audio_extensions = ('.wav', '.mp3', '.ogg')         #questi sono gli unici formati audio supportati da nao
    try:
        return any(path.lower().endswith(ext) for ext in audio_extensions)
    except (AttributeError, TypeError):
        return False


def is_text_file(path):
    """controlla se il percorso è un file testo."""
    try:
        return path.lower().endswith('.txt')
    except (AttributeError, TypeError):
        return False


def determine_file_type(file):
    if is_audio_file(file):
        return "audio", file       # caso file audio

    elif is_text_file(file):       # caso file di testo
        try:
            with io.open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                return "text", text
        except IOError as e:
            logger.error("errore lettura file: {}".format(e))
            # FIX: Restituiamo una tupla di None invece di un return vuoto
            return None, None 
    else:
        return "text", file        # caso stringa normale
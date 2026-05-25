# -*- coding: utf-8 -*-

import io
from log import logger


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


def determine_file_type(file_input):
    if is_audio_file(file_input):
        return "audio", file_input

    content = None
    if is_text_file(file_input):
        try:
            with io.open(file_input, 'r', encoding='utf-8') as f:
                content = f.read()
        except IOError as e:
            logger.error("errore lettura file: {}".format(e))
            return None, None
    else:
        content = file_input

    # Forza la conversione in unicode per Python 2 se riceve stringhe di byte (str)
    # In Python 3, 'bytes' è distinto da 'str', quindi il decode funziona correttamente.
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            logger.warning("impossibile decodificare il testo in utf-8, procedo con il formato originale")

    return "text", content




def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('0x')
    
    # Estrae le coppie e le converte in interi (base 16)
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))


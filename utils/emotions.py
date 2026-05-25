# -*- coding: utf-8 -*-
_MOOD_DEFAULTS = {                  #mv testa       mood per log          colore degli occhi          velocità voce      tono di voce
    ("felice",     "happy"):       {"head": -0.4,  "log":  "FELICE",      "coloreOcchiHEX": 0xFFFF00, "voiceSpeed": 100, "voiceTone": 1.2},
    ("triste",     "sad"):         {"head":  0.4,  "log":  "TRISTE",      "coloreOcchiHEX": 0x0000FF, "voiceSpeed": 75,  "voiceTone": 0.8},
    ("arrabbiato", "angry"):       {"head":  0.0,  "log":  "ARRABBIATO",  "coloreOcchiHEX": 0xFF0000, "voiceSpeed": 100, "voiceTone": 0.9},
    ("neutro",     "neutral"):     {"head":  0.0,  "log":  "NEUTRI",      "coloreOcchiHEX": 0xFFFFFF, "voiceSpeed": 100, "voiceTone": 1.0},
    ("sorpresa",   "surprised"):   {"head":  0.0,  "log":  "SORPRESA",    "coloreOcchiHEX": 0xFFA500, "voiceSpeed": 100, "voiceTone": 1.1},
    ("paura",      "afraid"):      {"head": -0.2,  "log":  "PAURA",       "coloreOcchiHEX": 0xFF00FF, "voiceSpeed": 90,  "voiceTone": 0.7},
    ("disgusto",   "disgusted"):   {"head":  0.2,  "log":  "DISGUSTO",    "coloreOcchiHEX": 0x00FF00, "voiceSpeed": 85,  "voiceTone": 0.9},
    ("noia",       "bored"):       {"head":  0.1,  "log":  "NOIA",        "coloreOcchiHEX": 0x808080, "voiceSpeed": 70,  "voiceTone": 0.95},
    ("determinato", "determined"): {"head": -0.4,  "log":  "DETERMINATO", "coloreOcchiHEX": 0x00FFFF, "voiceSpeed": 100, "voiceTone": 1.1},
}

MOOD_CONFIG = {}
for _keys, _config in _MOOD_DEFAULTS.items():
    for _key in _keys:
        MOOD_CONFIG[_key] = _config

NEUTRAL_CONFIG = MOOD_CONFIG["neutro"]


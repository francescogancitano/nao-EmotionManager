# EmotionManager

Sistema per far recitare il robot NAO con emozioni espressive controllate via Python 2.7.
Il robot cambia LED, voce e posizione della testa in base allo stato emotivo impostato,
e può eseguire script teatrali con cambi di emozione inline.

---

## Requisiti

- **Python 2.7** (compilato dai sorgenti o installato separatamente)
- **NAOqi SDK 2.8.x** per Linux (scaricabile da SoftBank Robotics)
- Un robot **NAO fisico** oppure un'istanza di **naoqi-bin** in esecuzione localmente

---

## Installazione

### 1. Python 2.7

Se non disponibile nei repo della tua distro (es. Fedora), compilalo dai sorgenti:

```bash
cd ~/Scaricati
wget https://www.python.org/ftp/python/2.7.18/Python-2.7.18.tgz
tar -xvzf Python-2.7.18.tgz
cd Python-2.7.18
./configure --prefix=/usr/local/python2.7
make -j$(nproc) CFLAGS="-std=c11 -fwrapv -O2"
sudo make install
```

Verifica:

```bash
/usr/local/python2.7/bin/python2.7 --version
# Python 2.7.18
```

### 2. NAOqi SDK

Scarica il SDK da:
```
https://maxtronics.com/en/support/kb/nao6/downloads/nao6-software-downloads/
```

Estrai nella home nascosta:

```bash
tar -xvzf naoqi-sdk-2.8.x-linux64.tar.gz -C ~/
mv naoqi-sdk-2.8.x-linux64 ~/.naoqi-sdk-2.8.x-linux64
```

### 3. Variabili d'ambiente

Aggiungi al tuo `.bashrc`:

```bash
export PYTHONPATH=~/.naoqi-sdk-2.8.x-linux64/lib/python2.7/site-packages
export LD_LIBRARY_PATH=~/.naoqi-sdk-2.8.x-linux64/lib
alias python-nao="/usr/local/python2.7/bin/python2.7"
```

Ricarica:

```bash
source ~/.bashrc
```

Verifica che il modulo `qi` sia raggiungibile:

```bash
python-nao -c "import qi; print('ok')"
```

---

## Utilizzo

### Avvio con robot fisico

Imposta l'IP del tuo NAO nel file:

```python
NAO_IP = "192.168.1.100"  # sostituisci con l'IP del tuo robot
```

Poi esegui:

```bash
python-nao EmotionManager.py
```

### Avvio con robot virtuale (naoqi-bin)

In un terminale avvia il simulatore:

```bash
~/.naoqi-sdk-2.8.x-linux64/bin/naoqi-bin --verbose
```

In un secondo terminale esegui lo script con IP locale:

```python
NAO_IP = "127.0.0.1"
```

```bash
python-nao EmotionManager.py
```

> **Nota:** con il robot virtuale, ALLeds e ALMotion non sono disponibili
> e vengono saltati automaticamente. Solo ALTextToSpeech risponde.

---

## Struttura del codice

### Classe `EmotionManager`

Gestisce la connessione al robot e il controllo delle emozioni tramite un sistema di mood (stati emotivi).

#### `__init__(ip_address, port=9559)`

Inizializza la connessione al robot tramite il protocollo TCP NAOqi e carica i servizi disponibili:

- `ALTextToSpeech` — **obbligatorio**, gestisce il sintetizzatore vocale
- `ALLeds` — opzionale, gestisce i LED del viso
- `ALMotion` — opzionale, gestisce i movimenti della testa
- `ALAudioPlayer` — opzionale, gestisce la riproduzione di file audio

Se ALLeds, ALMotion o ALAudioPlayer non sono disponibili (ad es. con il robot virtuale),
vengono impostati a `None` e le funzionalità corrispondenti vengono saltate automaticamente senza errori.

```python
nao = EmotionManager("192.168.1.100")  # Robot fisico
# oppure
nao = EmotionManager("127.0.0.1")      # Robot virtuale
```

---

#### `_move_head(pitch_angle)` (privato)

Muove la testa del robot sull'asse verticale (pitch).

| Valore | Effetto |
|--------|---------|
| `-0.4` | Testa alzata (sguardo verso l'alto) |
| `0.0`  | Testa dritta (posizione neutra) |
| `+0.4` | Testa abbassata (sguardo verso il basso) |

Il parametro è espresso in **radianti** e la velocità è controllata dalla costante `DEFAULT_MOTION_SPEED`.

---

#### `_set_leds(eyesColor)` (privato)

Cambia il colore dei LED frontali del viso del robot con una transizione smooth.

```python
self._set_leds(0x00FF00)  # Verde
self._set_leds(0xFF0000)  # Rosso
self._set_leds(0x0000FF)  # Blu
```

La velocità di transizione è controllata dalla costante `DEFAULT_COLOR_FADE_TIME`.

---

#### `_set_voice(voiceSpeed, voiceTone)` (privato)

Configura i parametri vocali del robot:

- `voiceSpeed` — velocità di elocuzione (0-200, default 100)
- `voiceTone` — intonazione/tono della voce (0.5-2.0, default 1.0)

```python
self._set_voice(120, 1.2)   # Voce veloce e acuta
self._set_voice(75, 0.8)    # Voce lenta e bassa
```

---

#### `set_mood(mood_name)`

Metodo principale per impostare lo stato emotivo del robot. Accetta il nome dell'emozione
come stringa, sia in **italiano** che in **inglese**, e applica automaticamente:

- Colore dei LED
- Posizione della testa
- Velocità e tono della voce

```python
nao.set_mood("felice")      # oppure "happy"
nao.set_mood("triste")      # oppure "sad"
nao.set_mood("arrabbiato")  # oppure "angry"
nao.set_mood("neutro")      # oppure "neutral"
```

Se il mood non è riconosciuto, il robot torna automaticamente allo stato **neutro**.

**Tabella degli stati emotivi:**

| Emozione    | LED           | Velocità voce | Tono voce | Testa    |
|-------------|---------------|---------------|-----------|----------|
| Felice      | Verde (0x00FF00) | 120%        | +1.2      | Su (-0.4)|
| Triste      | Blu (0x0000FF)   | 75%         | -0.8      | Giù (+0.4)|
| Arrabbiato  | Rosso (0xFF0000) | 110%        | -0.9      | Dritta (0.0)|
| Neutro      | Bianco (0xFFFFFF)| 100%        | 1.0       | Dritta (0.0)|

---

#### `say(text)`

Wrapper semplice che invia una stringa di testo al sintetizzatore vocale.

```python
nao.say("Ciao a tutti!")
nao.say("Oggi è una bellissima giornata!")
```

---

#### `perform_script(input_data, mood=None)`

Esegue uno script con cambi di emozione inline. Accetta tre tipi di input:

1. **Una stringa di testo diretto**
2. **Un file di testo** (`.txt`)
3. **Un file audio** (`.wav`, `.ogg`, `.mp3`)

**Per testo con emozioni inline:**

Il testo può contenere comandi nella forma `*set_nomeemozione` che cambiano lo stato emotivo al volo:

```python
script = """
*set_happy
Buongiorno a tutti, che bella giornata!

*set_sad
Pero mi mancate tanto quando non siamo insieme.

*set_angry
E non mi piace quando mi ignorate!
"""

nao.perform_script(script)
```

**Per testo con mood fisso:**

Se specifichi un `mood` nei parametri, il robot ignorerà i comandi inline e manterrà
l'emozione specificata per tutto lo script:

```python
nao.perform_script(script, mood="happy")  # Tutto sarà letto con gioia
```

**Per file:**

```python
# File di testo
nao.perform_script("copione.txt")

# File audio (riprodotto tal quale)
nao.perform_script("dialogo.wav")
```

**Come funziona internamente:**

1. Usa `re.split()` con un pattern catturante per separare il testo dai comandi `*set_xxx`
2. Itera sui blocchi risultanti: se è un comando esegue il mood corrispondente, se è testo lo invia al TTS
3. I metodi `_is_audio_file()` e `_is_text_file()` determinano il tipo di input
4. Per i file audio, riproduce il file tramite ALAudioPlayer senza processare comandi inline
5. Per i file testo, carica il contenuto e lo elabora come una stringa normale

---

#### `_is_audio_file(path)` e `_is_text_file(path)` (@staticmethod)

Funzioni di utilità che controllano l'estensione del file per determinare il tipo di input.
Non dipendono dallo stato dell'istanza, per questo sono dichiarate come `@staticmethod`.

```python
EmotionManager._is_audio_file("dialogo.wav")    # True
EmotionManager._is_text_file("copione.txt")     # True
EmotionManager._is_audio_file("testo.txt")      # False
```

---

#### `_play_audio(audio_file)` (privato)

Riproduce un file audio tramite il servizio ALAudioPlayer.
Disponibile solo sul robot fisico.

```python
self._play_audio("dialogo.wav")
```

---

## Script da file esterno

Puoi caricare lo script da un file `.txt` esterno invece di scriverlo nel codice:

```python
# -*- coding: utf-8 -*-
import io

nao = EmotionManager("192.168.1.100")
nao.perform_script("copione.txt")
```

Il file `copione.txt` ha la stessa struttura dello script inline,
con i tag `*set_xxx` su righe separate:

```
*set_happy
Buongiorno a tutti!

*set_sad
Pero mi mancate tanto.

*set_angry
E non tornate più!
```

---

## Esempio completo

```python
# -*- coding: utf-8 -*-
import qi, sys, time, re, io
from EmotionManager import EmotionManager

if __name__ == "__main__":
    nao = EmotionManager("192.168.1.100")

    # Test emozioni singole
    nao.set_mood("felice")
    nao.say("Ciao a tutti!")
    time.sleep(2)

    nao.set_mood("triste")
    nao.say("Pero oggi piove...")
    time.sleep(2)

    # Script con emozioni inline
    script = """
*set_happy
Che bello rivedervi!

*set_sad
Mi mancate sempre voi.

*set_neutral
Comunque continuo a sorridere.
"""
    nao.perform_script(script)

    # Script da file
    nao.perform_script("copione.txt")
```

---

## Note e limitazioni

- Il codice è scritto per **Python 2.7** per compatibilità con il NAOqi SDK 2.8.x
- Le **f-string** non sono supportate in Python 2.7: usare `.format()`
- I **type hints** non sono supportati in Python 2.7
- Il `# -*- coding: utf-8 -*-` in cima al file è necessario per i caratteri italiani
- I file di testo con accenti devono essere aperti con `io.open(..., encoding="utf-8")`
- Su robot virtuale, solo ALTextToSpeech funziona; ALLeds, ALMotion e ALAudioPlayer sono disabilitati

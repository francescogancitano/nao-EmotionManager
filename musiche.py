from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import socket
import os
import pygame  # Libreria per gestire la riproduzione audio

# --- CONFIGURAZIONE ---
# cartella dove sono contenuti i file MP3
PATH_MUSICHE = "C:/Users/iisve/Desktop/NAO_2026/musiche_nao/musiche"

# Dizionario delle musiche: "comando" -> "nome_file.mp3"
PLAYLIST = {
    "prima_fase": "fase1.mp3",
    "seconda_fase": "fase2.mp3",
}

class MusicRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        # L'API si aspetta un parametro 'track' (es: ?track=prima_fase)
        if 'track' in params:
            track_key = params['track'][0]
            
            if track_key in PLAYLIST:
                nome_file = PLAYLIST[track_key]
                full_path = os.path.join(PATH_MUSICHE, nome_file)
                
                if os.path.exists(full_path):
                    try:
                        # Gestione riproduzione audio
                        pygame.mixer.music.load(full_path)
                        pygame.mixer.music.play()
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(f"In riproduzione: {track_key} ({nome_file})".encode())
                        return
                    except Exception as e:
                        self.send_error(500, f"Errore riproduzione: {e}")
                        return
                else:
                    self.send_error(404, f"File non trovato nel percorso: {full_path}")
                    return
            else:
                self.send_error(400, f"Traccia '{track_key}' non presente nel dizionario")
                return

        # Comando per fermare la musica (?stop=1)
        if 'stop' in params:
            pygame.mixer.music.stop()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Musica fermata.")
            return
        
        self.send_response(400)
        self.end_headers()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# Inizializzazione Mixer Audio
pygame.mixer.init()

IP_ASCOLTO = '0.0.0.0'
PORTA = 8081 # viene utilizzata una porta diversa dai fari per non fare conflitto con i fari (8080)

server = HTTPServer((IP_ASCOLTO, PORTA), MusicRequestHandler)
ip_locale = get_local_ip()

print("=" * 60)
print(f"SERVER AUDIO PER NAO ATTIVO")
print(f"Cartella musica: {PATH_MUSICHE}")
print(f"-> Chiamata Interna: http://127.0.0.1:{PORTA}/?track=prima_fase")
print(f"-> Chiamata Esterna: http://{ip_locale}:{PORTA}/?track=prima_fase")
print(f"-> Per fermare: http://{ip_locale}:{PORTA}/?stop=1")
print("=" * 60)

server.serve_forever()
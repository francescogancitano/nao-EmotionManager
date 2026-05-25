from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import socket
from websocket import create_connection

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        if 'ch' in params and 'val' in params:
            try:
                # Canale reale preso dall'URL (es. ch=6)
                ch_reale = int(params['ch'][0])
                val = int(params['val'][0])
                
                # Universo 1 di default -> canale assoluto coincide con ch_reale
                universo = 1 
                ch_assoluto = ((universo - 1) * 512) + ch_reale
                
                # Stringa esatta usata da simpledesk.js: "CH|canale|valore"
                comando_nativo = f"CH|{ch_assoluto}|{val}"
                
                # Connessione WebSocket locale verso QLC+
                ws = create_connection("ws://127.0.0.1:9999/qlcplusWS", timeout=2)
                ws.send(comando_nativo)
                ws.close()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Inviato correttamente: {comando_nativo}".encode())
                return
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(f"Errore di comunicazione con QLC+: {e}".encode())
                return
        
        self.send_response(400)
        self.end_headers()

# Funzione ausiliaria per mostrare l'IP corretto nei log
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

# '0.0.0.0' indica al sistema di accettare connessioni da QUALSIASI scheda di rete (Wi-Fi, Ethernet, ecc.)
IP_ASCOLTO = '0.0.0.0'
PORTA = 8080

server = HTTPServer((IP_ASCOLTO, PORTA), RequestHandler)
ip_locale = get_local_ip()

print("=" * 60)
print(f"Traduttore SimpleDesk ATTIVO SU TUTTE LE RETI")
print(f"-> Da questo PC puoi usare: http://127.0.0.1:{PORTA}/?ch=6&val=128")
print(f"-> Da smartphone o altri dispositivi usa: http://{ip_locale}:{PORTA}/?ch=6&val=128")
print("=" * 60)

server.serve_forever()

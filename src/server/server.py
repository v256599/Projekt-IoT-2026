import socket
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- KONFIGURACE ---
HOST = '0.0.0.0'
UDP_PORT = 5005
HTTP_PORT = 8080
TOKEN = 123456 #Auth Token



class Brana:
    def __init__(self):
        self._stav = "Zavřeno"

    def _proved_hw_operaci(self, nazev_operace):
        """
        Emuluje provedení fyzické akce s určitou pravděpodobností selhání.
       Prozatím vracíme vždy True
        """
        # Pro zapnutí náhodného selhání odkomentujte následující řádek:
        # uspesno = random.random() > 0.2  # 80% šance na úspěch, 20% šance na chybu
        
        uspesno = True  # Nyní vždy vrací True dle zadání

        if not uspesno:
            print(f"[-] EMULACE CHYBA: Fyzická operace '{nazev_operace}' selhala (emulováno)!")
        
        return uspesno

    def open(self):
        if self._proved_hw_operaci("Otevřít"):
            self._stav = "Otevřeno"
            return True
        return False

    def close(self):
        if self._proved_hw_operaci("Zavřít"):
            self._stav = "Zavřeno"
            return True
        return False

    def toggle(self):
        if self.isClosed():
            return self.open()
        else:
            return self.close()

    def isClosed(self):
        return self._stav == "Zavřeno"

    def isOpened(self):
        return self._stav == "Otevřeno"

    def getState(self):
        return self._stav


brana = Brana()

# --- HTTP SERVER (Webové rozhraní) ---
class StavovyHandler(BaseHTTPRequestHandler):
    # Skip HTTP logs on trminal
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        # Brana state get
        aktualni_stav = brana.getState()
        
        # If opened for colors
        je_otevreno = brana.isOpened()
        bg_color = '#d4edda' if je_otevreno else '#f8d7da'
        text_color = '#155724' if je_otevreno else '#721c24'

        html = f"""
        <!DOCTYPE html>
        <html lang="cs">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>IoT Ovladač Brány</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                .status {{ font-size: 2em; padding: 20px; border-radius: 10px; display: inline-block; 
                           background-color: {bg_color}; color: {text_color}; }}
            </style>
            <meta http-equiv="refresh" content="2">
        </head>
        <body>
            <h1>Stav vjezdové brány</h1>
            <div class="status">
                {aktualni_stav}
            </div>
            <p><small>Stránka se automaticky aktualizuje každé 2 vteřiny.</small></p>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

def start_http_server():
    server = HTTPServer((HOST, HTTP_PORT), StavovyHandler)
    print(f"[*] HTTP Dashboard běží na http://{HOST}:{HTTP_PORT}")
    server.serve_forever()


# --- UDP SERVER (Komunikace s IoT modulem) ---
def start_udp_server():
    global TOKEN

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, UDP_PORT))
    print(f"[*] UDP Server naslouchá na portu {UDP_PORT}")

    try:
        while True:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode('utf-8').strip()
            print(f"\n[+] Přijata zpráva od {addr[0]}: {message}")
            
            try:
                payload = json.loads(message)
                akce = payload.get("action")
                token = int(payload.get("token"))
                
                # Kontrola tokenu (zabezpečení)
                if token != TOKEN:
                    print(f"    [-] Odmítnuto: Neplatný token. Přišel {token}, požadován {TOKEN}")
                else:
                   
                    if akce == "open":
                        vysledek_akce = brana.open()
                    elif akce == "close":
                        vysledek_akce = brana.close()
                    elif akce == "toggle":
                        vysledek_akce = brana.toggle()
                    else:
                        print(f"    [-] Neznámá akce: {akce}")
                        response = json.dumps({"successful": False, "error": "Neznama akce"})
                        server_socket.sendto(response.encode('utf-8'), addr)
                        continue
                    
                    # Sestavení odpovědi na základě úspěchu hardwarové operace
                    if vysledek_akce:
                        print(f"    [+] OK! Nový stav brány: {brana.getState()}")
                        response = json.dumps({
                            "successful": True
                        })
                    else:
                        # Tento blok se spustí, pokud emulace selže
                        print(f"    [+] BranaErr! Brána simuluje chybu. Stav brány: {brana.getState()}")
                        response = json.dumps({
                            "successful": False, 
                            "error": "brana_err"
                        })

            except json.JSONDecodeError:
                print("    [-] Chyba parsování JSONu.")
                response = json.dumps({"successful": False, "error": "Neplatny JSON formát"})

            # Odeslání odpovědi zpět
            server_socket.sendto(response.encode('utf-8'), addr)

    finally:
        server_socket.close()

# --- HLAVNÍ SPUŠTĚNÍ ---
if __name__ == "__main__":
    # Spuštění HTTP serveru ve vedlejším vlákně (daemon=True zajistí, že se ukončí s hlavním programem)
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()

    # Spuštění UDP serveru v hlavním vlákně
    start_udp_server()
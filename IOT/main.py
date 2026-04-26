import machine
import time
import neopixel
import BG77

# --- KONFIGURACE HARDWARU ---
modem_en = machine.Pin(25, machine.Pin.OUT, value=1)   # MOD_EN
btn = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)  # BUT0
np = neopixel.NeoPixel(machine.Pin(16), 3, bpp=4)      # RGBW NeoPixel

uart0 = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
module = BG77.BG77(uart0, verbose=True)

# --- KONFIGURACE SÍTĚ ---
APN = "lpwa.vodafone.iot"
SERVER_IP = "127.0.0.1"    
SERVER_PORT = 1234

def set_color(r, g, b, w=0):
    np[0] = (r, g, b, w)
    np.write()

def init_modem():
    print("Konfiguruji modem...")
    set_color(50, 30, 0, 0)  # oranžová = inicializace

    if not module.setAPN(APN):
        print("Chyba: APN se nepodařilo nastavit.")
        return False

    print("APN nastaveno.")

    # Připojení k packetové síti
    if not module.attachToNetwork():
        print("Varování: attachToNetwork selhalo nebo modem již může být připojen.")

    print("Čekám na registraci do sítě...")

    for i in range(60):
        if module.isRegistered():
            print("Modem je registrován v síti.")
            return True

        print("Čekám...", i + 1)
        time.sleep(1)

    print("Chyba: Modem se nezaregistroval do sítě.")
    return False

def open_gate():
    set_color(0, 0, 50, 0)  # modrá = komunikace

    if not module.isRegistered():
        print("Chyba: Modul není registrován v síti.")
        return False

    result, sock = module.socket(BG77.AF_INET, BG77.SOCK_DGRAM)

    if not result:
        print("Chyba: Nepodařilo se vytvořit socket.")
        return False

    sock.settimeout(10)

    try:
        print("Otevírám UDP spojení...")

        if not sock.connect(SERVER_IP, SERVER_PORT):
            print("Chyba: Nepodařilo se otevřít UDP socket.")
            sock.close()
            return False

        print("Posílám příkaz OPEN_GATE...")
        if not sock.send("OPEN_GATE"):
            print("Chyba: Odeslání selhalo.")
            sock.close()
            return False

        print("Čekám na odpověď serveru...")
        size, data = sock.recv(1024)

        sock.close()

        if size > 0 and data is not None:
            print("Odpověď serveru:", data)

            if "ACK" in data:
                return True
            else:
                print("Server odpověděl, ale ne ACK.")
                return False

        print("Timeout: Server neodpověděl.")
        return False

    except Exception as e:
        print("Chyba komunikace:", e)

        try:
            sock.close()
        except:
            pass

        return False

# --- START ---
print("Inicializace zařízení...")

if init_modem():
    set_color(0, 100, 0, 0)
    print("Zařízení připraveno.")
    time.sleep(1)
else:
    set_color(100, 0, 0, 0)
    print("Inicializace selhala.")

set_color(0, 0, 0, 0)

# --- HLAVNÍ SMYČKA ---
while True:
    if btn.value() == 0:
        print("\nStisk tlačítka - spouštím otevírání brány.")

        if open_gate():
            set_color(0, 100, 0, 0)
            print("Brána se otevírá.")
        else:
            set_color(100, 0, 0, 0)
            print("Akce selhala.")

        time.sleep(3)
        set_color(0, 0, 0, 0)

        # čekání na puštění tlačítka
        while btn.value() == 0:
            time.sleep_ms(50)

    time.sleep_ms(100)
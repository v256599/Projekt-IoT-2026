import machine
import time
import neopixel
import BG77
import config  

# HARDWARE KONFIGURACE
modem_en = machine.Pin(9, machine.Pin.OUT, value=0)       # MOD_EN
btn = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)  # BUT0
np = neopixel.NeoPixel(machine.Pin(16), 3, bpp=4)          # RGBW LED

uart0 = machine.UART(0, baudrate=115200, tx=machine.Pin(0), rx=machine.Pin(1))
module = None


ACTION = "toggle"

# JSON msg for server
MESSAGE = '{"action":"%s","token":%d}' % (ACTION, config.TOKEN)


# LED FUNKCE
def set_color(r, g, b, w=0):
    np[0] = (r, g, b, w)
    np.write()


# KONTROLA SIM
def check_sim():
    print("Kontroluji SIM kartu...")

    cpin = module.sendCommand("AT+CPIN?\r\n", timeout=3)
    print(cpin)

    if "+CPIN: READY" in cpin:
        print("SIM karta je připravena.")
        return True

    print("SIM karta není připravena, restartuji rádio...")

    module.sendCommand("AT+CFUN=0\r\n", timeout=5)
    time.sleep(2)

    module.sendCommand("AT+CFUN=1\r\n", timeout=10)
    time.sleep(5)

    cpin = module.sendCommand("AT+CPIN?\r\n", timeout=3)
    print(cpin)

    if "+CPIN: READY" in cpin:
        print("SIM karta je po restartu připravena.")
        return True

    print("Chyba: SIM karta není připravena.")
    return False


# INICIALIZACE MODEMU
def init_modem():
    print("Inicializuji modem...")
    
    set_color(50, 30, 0, 0)  # oranžová
    
    modem_en.high()
    time.sleep(0.3)
    modem_en.low()
    time.sleep(3)
    
    global module
    module = BG77.BG77(uart0, verbose=True)

    module.sendCommand("AT+CMEE=2\r\n", timeout=2)
    module.sendCommand('AT+QPSMS=1,,,"00111000","00000011"\r\n', timeout=5)  # nastavení PSM 24h/6s
    module.sendCommand('AT+QPTWEDRXS=0\r\n', timeout=5)     # vypnout eDRX 
    module.sendCommand('AT+QPSMS?\r\n')
    
    if not check_sim():
        return False

    print("Nastavuji APN...")
    if not module.setAPN(config.APN):
        print("Chyba: APN se nepodařilo nastavit.")
        return False

    print("Nastavuji LTE Cat-M režim...")
    module.setRATType(BG77.RAT_CAT_M_ONLY)

    print("Nastavuji Vodafone operátora...")
    cops = module.sendCommand("AT+COPS=1,2,23003\r\n", timeout=60)
    print(cops)

    print("Čekám na registraci do sítě...")

    for i in range(90):
        if module.isRegistered():
            print("Modem je registrován v síti.")
            break

        print("Čekám na síť...", i + 1)
        time.sleep(1)
    else:
        print("Chyba: modem se nezaregistroval do sítě.")
        return False

    print("Připojuji modem do packetové sítě...")
    module.attachToNetwork()

    print("Aktivuji PDP kontext...")
    qiact = module.sendCommand("AT+QIACT=1\r\n", timeout=20)
    print(qiact)

    print("Kontroluji PDP kontext...")
    qiact_status = module.sendCommand("AT+QIACT?\r\n", timeout=5)
    print(qiact_status)

    if "+QIACT:" not in qiact_status:
        print("Chyba: PDP kontext není aktivní.")
        return False

    print("PDP kontext je aktivní.")
    return True


# ODESLÁNÍ PŘÍKAZU
def send_gate_command():
    set_color(0, 0, 50, 0)  # modrá = komunikace
    
    if not module.testAT(): # start modem kdyz nebezi
       modem_en.high()
       time.sleep(0.3)
       modem_en.low()
       time.sleep(3)

    print("Kontroluji registraci před odesláním...")

    if not module.isRegistered():
        print("Chyba: modem není registrován v síti.")
        return False

    result, sock = module.socket(BG77.AF_INET, BG77.SOCK_DGRAM)

    if not result:
        print("Chyba: nepodařilo se vytvořit socket.")
        return False

    sock.settimeout(10)

    try:
        print("Otevírám UDP socket...")

        # Použití IP a portu z configu
        if not sock.connect(config.SERVER_IP, config.SERVER_PORT):
            print("Chyba: nepodařilo se otevřít UDP socket.")
            sock.close()
            return False

        print("Odesílám JSON:", MESSAGE)

        if not sock.send(MESSAGE, rai=2):
            print("Chyba: zpráva nebyla odeslána.")
            sock.close()
            return False

        print("Čekám na odpověď serveru...")

        size, data = sock.recv(1024)

        sock.close()

        print("Přijatá odpověď:", data)

        if size > 0 and data is not None:
            if '"successful": true' in data or '"successful":true' in data:
                print("Server potvrdil úspěch.")
                return True

        print("Server vrátil chybu nebo neplatnou odpověď.")
        return False

    except Exception as e:
        print("Chyba komunikace:", e)

        try:
            sock.close()
        except:
            pass

        return False


# START PROGRAMU
print("Start zařízení...")

if init_modem():
    print("Zařízení připraveno.")
    set_color(0, 100, 0, 0) # green
    time.sleep(1)
else:
    print("Inicializace selhala.")
    set_color(100, 0, 0, 0) # red

    while True:
        time.sleep(1)

set_color(0, 0, 0, 0)


# HLAVNÍ SMYČKA
while True:
    if btn.value() == 0:
        print("\nStisk tlačítka - odesílám příkaz.")
        if send_gate_command():
            set_color(0, 100, 0, 0)
            print("Úspěch: příkaz byl potvrzen.")
        else:
            set_color(100, 0, 0, 0)
            print("Chyba: příkaz nebyl potvrzen.")

        time.sleep(3)
        set_color(0, 0, 0, 0)

        while btn.value() == 0:
            time.sleep_ms(50)

    time.sleep_ms(100)
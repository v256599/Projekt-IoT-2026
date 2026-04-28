# Bezdrátový ovladač vjezdových vrat

## 1. Popis aplikace
Cílem projektu je navrhnout, naprogramovat a zprovoznit bezdrátový ovladač pro otevírání a ovládání vjezdové brány. Zařízení je určeno pro mobilní scénáře, například pro použití ve vozidle. Uživatel požaduje možnost otevření brány odkudkoliv bez nutnosti použití mobilní aplikace, přičemž je vyžadováno samostatné fyzické zařízení.

Systém je napájen z baterie a využívá obousměrnou komunikaci. Po stisku tlačítka na zařízení je odeslán požadavek na vzdálený server, který následně provede požadovanou akci (otevření / zavření brány) a odešle zpětnou odpověď. O výsledku operace je uživatel informován pomocí LED signalizace.

---

## 2. Využité komponenty

- **Řídící mikrokontrolér (MCU):** Raspberry Pi RP2040  
- **Komunikační modul:** Quectel BG77  
- **Uživatelské rozhraní:** Tlačítko (vstup) a RGBW LED (výstup)  
- **Napájení:** Bateriový zdroj  
- **SIM karta:** Vodafone IoT SIM s APN `lpwa.vodafone.iot`

---

## 3. Zvolená technologie a anténa

Pro komunikaci byla zvolena technologie **LTE Cat-M1 (LTE-M)**.

### Zdůvodnění volby
Zákazník požaduje spolehlivé otevření brány odkudkoliv, včetně mobilního použití ve vozidle. Technologie krátkého dosahu, například Bluetooth nebo Wi-Fi, by tento požadavek nesplnily bez nutnosti další infrastruktury.

LTE Cat-M je vhodnější než NB-IoT zejména díky:

- podpoře mobility a handover při pohybu zařízení  
- nižší latenci komunikace  
- lepší podpoře roamingu  
- stále velmi nízké spotřebě energie  
- dostatečnému pokrytí v mobilních sítích

Technologie je vhodná zejména pro zařízení, která většinu času spí a pouze občas odesílají krátké zprávy.

### Zvolená anténa
Byla použita externí LTE anténa s SMA konektorem určená pro pásma používaná mobilními operátory v České republice.

### Zdůvodnění volby antény
Externí anténa poskytuje vyšší citlivost a stabilnější příjem signálu než integrované PCB antény. To je důležité zejména při použití ve vozidle nebo v místech s horším pokrytím.

---

## 4. Zvolený transportní a aplikační protokol

### Transportní protokol: UDP

#### Zdůvodnění
Byl zvolen protokol UDP, protože přenáší minimální množství režijních dat oproti TCP. Díky tomu se snižuje objem přenesených dat, zkracuje doba aktivního vysílání modemu a prodlužuje životnost baterie.

UDP je vhodný pro krátké jednorázové zprávy typu příkaz / potvrzení.

### Aplikační protokol: JSON nad UDP

#### Zdůvodnění
Byl zvolen jednoduchý vlastní aplikační protokol využívající formát JSON. Ten umožňuje snadné rozšíření systému o další příkazy, identifikaci zařízení nebo doplnění bezpečnostních prvků.

#### Formát zprávy odesílané ze zařízení

```json
{"action":"toggle","token":123456}

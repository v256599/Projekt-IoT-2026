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

Pro komunikaci byla zvolena technologie **NB-IoT**.

### Zdůvodnění volby
Zákazník požaduje spolehlivé otevření brány odkudkoliv. Technologie krátkého dosahu, například Bluetooth nebo Wi-Fi, by tento požadavek nesplnily bez nutnosti další infrastruktury. NB-IoT umožňuje komunikaci přes mobilní síť s velmi nízkou spotřebou energie, vysokým dosahem a dobrou prostupností signálu.

Technologie je vhodná zejména pro zařízení, která většinu času spí a pouze občas odesílají krátké zprávy.

### Zvolená anténa
Byla použita externí LTE / NB-IoT anténa s SMA konektorem určená pro pásma používaná mobilními operátory v České republice.

### Zdůvodnění volby antény
Externí anténa poskytuje vyšší citlivost a stabilnější příjem signálu než integrované PCB antény. To je důležité zejména při použití ve vozidle nebo v místech s horším pokrytím.

---

## 4. Zvolený transportní a aplikační protokol

### Transportní protokol: UDP

#### Zdůvodnění
Byl zvolen protokol UDP, protože přenáší minimální množství režijních dat oproti TCP. Díky tomu se snižuje objem přenesených dat, zkracuje doba aktivního vysílání modemu a prodlužuje životnost baterie.

UDP je vhodný pro krátké jednorázové zprávy typu příkaz / potvrzení.

### Aplikační protokol: vlastní implementace nad UDP

#### Popis protokolu
1. Uživatel stiskne tlačítko.
2. MCU ověří registraci modemu do sítě příkazem `AT+CEREG?`
3. Odešle paket `OPEN_GATE`
4. Spustí časovač pro čekání na odpověď.
5. Pokud server vrátí `ACK`, operace je úspěšná.
6. Pokud odpověď nedorazí do timeoutu, operace je vyhodnocena jako neúspěšná.

### Signalizace LED

- **Modrá:** probíhá komunikace  
- **Zelená:** operace úspěšná  
- **Červená:** chyba / timeout  

---

## 5. Zvolená baterie

### Typ baterie
Li-Ion akumulátor 3,7 V / 3000 mAh

### Zdůvodnění volby
Li-Ion akumulátor nabízí:

- vysokou energetickou hustotu  
- možnost opakovaného nabíjení  
- malé rozměry  
- nízké samovybíjení  
- vhodné proudové zatížení pro krátkodobé špičky modemu při vysílání

Kapacita 3000 mAh je dostatečná pro dlouhodobý provoz zařízení.

---

## 6. Implementace úspory energie a kalkulace životnosti

### Implementace úspory energie

Byly použity následující metody:

- MCU přechází po dokončení komunikace do režimu spánku
- Probuzení probíhá pouze stiskem tlačítka
- LED svítí pouze krátkou dobu po operaci
- Modem využívá režim **PSM (Power Saving Mode)**
- Zařízení nevysílá periodicky

### Odhad životnosti

Předpoklad:

- klidový proud zařízení: 0,2 mA  
- 5 otevření brány denně  
- aktivní komunikace 10 s / den  
- průměrná denní spotřeba cca 0,35 mAh

Výpočet:
3000 / 0,35 = 8571 dní = 23 let

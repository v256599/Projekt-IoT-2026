# Bezdrátový ovladač vjezdových vrat

## 1. Popis aplikace
Cílem projektu je navrhnout, naprogramovat a zprovoznit bezdrátový ovladač pro otevírání a ovládání vjezdové brány. Zařízení je určeno pro mobilní scénáře, například pro použití ve vozidle. Uživatel požaduje možnost otevření brány odkudkoliv bez nutnosti použití mobilní aplikace, přičemž je vyžadováno samostatné fyzické zařízení.

Systém je napájen z baterie a využívá obousměrnou komunikaci. Po stisku tlačítka na zařízení je odeslán požadavek na vzdálený server, který následně provede požadovanou akci (otevření nebo zavření brány) a odešle zpětnou odpověď. O výsledku operace je uživatel informován pomocí LED signalizace.

---

## 2. Využité komponenty

- **Řídící mikrokontrolér (MCU):** Raspberry Pi RP2040  
- **Komunikační modul:** Quectel BG77  
- **Uživatelské rozhraní:** Tlačítko (vstup) a RGBW LED (výstup)  
- **Napájení:** Li-Ion akumulátor + DC-DC měnič  
- **SIM karta:** Vodafone IoT SIM s APN `lpwa.vodafone.iot`

---

## 3. Zvolená technologie a anténa

Pro komunikaci byla zvolena technologie **LTE Cat-M1 (LTE-M)**.

### Zdůvodnění volby
Zákazník požaduje spolehlivé otevření brány odkudkoliv. Technologie krátkého dosahu, například Bluetooth nebo Wi-Fi, by tento požadavek nesplnily bez nutnosti další infrastruktury.

LTE Cat-M bylo zvoleno z těchto důvodů:

- podpora mobility a roamingu  
- nižší latence oproti NB-IoT  
- dostatečně nízká spotřeba energie  
- komunikace přes veřejnou mobilní síť  
- vhodnost pro zařízení umístěné ve vozidle

Technologie je vhodná pro zařízení, která většinu času spí a pouze občas odesílají krátké zprávy.

### Zvolená anténa
Byla použita externí LTE anténa s SMA konektorem určená pro pásma využívaná operátory v České republice.

### Zdůvodnění volby antény
Externí anténa poskytuje vyšší citlivost a stabilnější příjem signálu než integrované PCB antény. To je důležité zejména při použití ve vozidle nebo v místech s horším pokrytím.

---

## 4. Zvolený transportní a aplikační protokol

### Transportní protokol: UDP

### Zdůvodnění
Byl zvolen protokol UDP, protože přenáší minimální množství režijních dat oproti TCP. Díky tomu se snižuje objem přenesených dat, zkracuje doba aktivního vysílání modemu a prodlužuje životnost baterie.

UDP je vhodný pro krátké jednorázové zprávy typu příkaz / potvrzení.

### Aplikační protokol: vlastní implementace nad UDP (JSON)

### Popis protokolu
1. Uživatel stiskne tlačítko.  
2. MCU ověří registraci modemu do sítě příkazem `AT+CEREG?`  
3. Odešle JSON zprávu ve tvaru `{"action":"toggle","token":123456}`  
4. Server provede požadovanou akci.  
5. Server vrátí odpověď `{"successful": true}`  
6. Pokud odpověď nedorazí do timeoutu, operace je vyhodnocena jako neúspěšná.

### Signalizace LED

- **Modrá:** probíhá komunikace  
- **Zelená:** operace úspěšná  
- **Červená:** chyba nebo timeout  

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

Napětí akumulátoru je přes DC-DC měnič převáděno na požadované napětí elektroniky.

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
- aktivní komunikace 10 s denně  
- průměrná denní spotřeba cca 0,35 mAh  

Výpočet:

- 3000 / 0,35 = 8571 dní  
- teoreticky cca 23 let

Reálná životnost bude nižší kvůli samovybíjení baterie, teplotě a stárnutí článku.

Reálně lze očekávat přibližně **5 až 8 let provozu** bez výměny baterie.

---

## 7. Zdůvodnění dalších parametrů

### Interval vysílání
Zařízení nevysílá periodicky. Data jsou odesílána pouze po stisku tlačítka. Tím je zamezeno zbytečné komunikaci i vybíjení baterie.

### Bezpečnost
Server přijímá pouze zprávy obsahující správný autentizační token. Řešení lze dále rozšířit o šifrování komunikace.

### Spolehlivost
Každý příkaz vyžaduje potvrzení od serveru. Pokud odpověď nedorazí, uživatel je informován chybovou signalizací LED.

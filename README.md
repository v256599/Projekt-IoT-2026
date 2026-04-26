# Popis technického řešení: Bezdrátový ovladač vjezdových vrat

## 1. Popis aplikace
[cite_start]Cílem projektu je naprogramovat a zprovoznit bezdrátový ovladač pro otevírání a ovládání vjezdové brány[cite: 4]. [cite_start]Zařízení je určeno pro mobilní scénáře, tedy např. do vozidla[cite: 6]. [cite_start]Zákazník požaduje možnost otevření brány zařízením odkudkoliv[cite: 7]. [cite_start]Zákazník vyžaduje fyzické zařízení[cite: 8]. [cite_start]Systém bude napájen z baterie [cite: 10] [cite_start]a poskytuje obousměrnou komunikaci – po stisku tlačítka na zařízení bude odeslána zpráva na vzdálený server s příkazem [cite: 11] [cite_start]a po realizaci příkazu dojde k zaslání odpovědi od vzdáleného serveru[cite: 12]. [cite_start]O úspěchu/neúspěchu otevření bude uživatel informován pomocí světelné indikace LED[cite: 13].

## 2. Využité komponenty
* **Řídící mikrokontrolér (MCU):** *[Zde doplň svůj MCU, např. ESP32, STM32, RPi Pico]*[cite: 32, 53, 64].
* **Komunikační modul:** *[Zde doplň svůj modul, např. Quectel BG77]*[cite: 64].
* [cite_start]**Uživatelské rozhraní:** Tlačítko (vstup) a indikační LED (výstup)[cite: 11, 13, 64].

## 3. Zvolená technologie a anténa
Pro komunikaci byla zvolena technologie **NB-IoT / LTE Cat-M**. 
* [cite_start]**Zdůvodnění volby:** Zákazník požaduje spolehlivé otevření brány odkudkoliv[cite: 7]. Technologie s krátkým dosahem by tento požadavek nesplnily bez nutnosti dedikované mobilní brány ve vozidle. [cite_start]Volba technologie splňuje požadavek využití bezdrátové technologie [cite: 28, 50] [cite_start]a zohledňuje mobilní scénář[cite: 6].
* [cite_start]**Zvolená anténa:** *[Zde doplň typ antény]*[cite: 22]. [cite_start]Anténa byla vhodně zvolena pro dané zařízení[cite: 14].

## 4. Zvolený transportní a aplikační protokol
* [cite_start]**Transportní protokol:** UDP[cite: 21, 66].
    * [cite_start]**Zdůvodnění:** Je vhodné preferovat protokoly založené na UDP z důvodu přeneseného objemu dat, který je zpoplatněn[cite: 88]. UDP minimalizuje síťovou režii a zkracuje dobu aktivního vysílání, což pozitivně ovlivňuje životnost baterie.
* [cite_start]**Aplikační protokol:** Vlastní implementace nad UDP[cite: 21, 67, 68].
    * [cite_start]**Zdůvodnění a popis protokolu:** Z důvodu maximální úspory dat byla vytvořena vlastní implementace[cite: 88]. Protokol funguje jako stavový automat: po stisku tlačítka se odešle paket a MCU spustí časovač. Pokud ze vzdáleného serveru nedorazí potvrzovací zpráva do nastaveného limitu, je operace vyhodnocena jako neúspěšná. [cite_start]Před každou zprávou je ověřena registrace do sítě příkazem `AT+CEREG?`[cite: 87].

## 5. Zvolená baterie
* **Typ baterie:** *[Např. [cite_start]Primární lithiová baterie Li-SOCl2 / Li-Po článek]*[cite: 15, 23, 69].
* [cite_start]**Zdůvodnění:** Byla zvolena vhodná napájecí baterie pro dané zařízení s ohledem na požadavky[cite: 15]. Nabízí adekvátní vlastnosti pro zařízení, které většinu času tráví v režimu spánku.

## 6. Implementace úspory energie a kalkulace životnosti
* [cite_start]**Implementace:** Byly implementovány vhodné režimy úspory energie[cite: 16]. MCU po vyřízení požadavku a zhasnutí indikační LED přechází do režimu spánku a probouzí se výhradně externím přerušením od tlačítka. Modem využívá funkci **PSM (Power Saving Mode)**.
* [cite_start]**Kalkulace (DOPLNIT PO MĚŘENÍ):** Kalkulace odhadu životnosti zařízení byla provedena na základě měření proudové spotřeby zařízení proudovou sondou v laboratoři[cite: 16, 24].
    * Odběr v režimu spánku: *[doplň naměřené µA]*
    * Odběr při odesílání/příjmu a svícení LED: *[doplň naměřené mA]*
    * Předpokládaný počet stisků: 4x denně.
    * Odhadovaná životnost při kapacitě baterie *[kapacita]* mAh: **[výsledek výpočtu] měsíců/let**.

## 7. Zdůvodnění dalších parametrů a polemika
* [cite_start]**Interval vysílání:** Zařízení nevysílá periodicky, čímž je zamezeno odesílání v nekonečné smyčce bez delay[cite: 58]. [cite_start]Vysílání probíhá výhradně na základě stisku tlačítka, což je hlavní důvod pro úsporu energie[cite: 25].
* [cite_start]**Polemika nad dosaženými výsledky:** *[Zde doplň zhodnocení po finálním zprovoznění]*[cite: 71]. [cite_start]Nedostatky řešení zahrnují například absenci šifrování na aplikační vrstvě[cite: 25].

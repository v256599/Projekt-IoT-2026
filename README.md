# Bezdrátový ovladač vjezdových vrat

## 1. Popis aplikace
Cílem projektu je naprogramovat a zprovoznit bezdrátový ovladač pro otevírání a ovládání vjezdové brány. Zařízení je určeno pro mobilní scénáře, tedy např. do vozidla. Zákazník požaduje možnost otevření brány zařízením odkudkoliv. Zákazník vyžaduje fyzické zařízení. Systém bude napájen z baterie a poskytuje obousměrnou komunikaci – po stisku tlačítka na zařízení bude odeslána zpráva na vzdálený server s příkazem a po realizaci příkazu dojde k zaslání odpovědi od vzdáleného serveru. O úspěchu/neúspěchu otevření bude uživatel informován pomocí světelné indikace LED.

## 2. Využité komponenty
* **Řídící mikrokontrolér (MCU):** 
* **Komunikační modul:** 
* **Uživatelské rozhraní:** Tlačítko (vstup) a indikační LED (výstup)

## 3. Zvolená technologie a anténa
Pro komunikaci byla zvolena technologie **NB-IoT / LTE Cat-M**. 
* **Zdůvodnění volby:** Zákazník požaduje spolehlivé otevření brány odkudkoliv. Technologie s krátkým dosahem by tento požadavek nesplnily bez nutnosti dedikované mobilní brány ve vozidle. Volba technologie splňuje požadavek využití bezdrátové technologie a zohledňuje mobilní scénář.
* **Zvolená anténa:** 

## 4. Zvolený transportní a aplikační protokol
* **Transportní protokol:** UDP.
    * **Zdůvodnění:** Je vhodné preferovat protokoly založené na UDP z důvodu minimalizace přeneseného objemu dat, který je zpoplatněn. UDP snižuje síťovou režii a zkracuje dobu aktivního vysílání, což pozitivně ovlivňuje životnost baterie.
* **Aplikační protokol:** Vlastní implementace nad UDP.
    * **Zdůvodnění a popis protokolu:** Z důvodu maximální úspory dat byla vytvořena vlastní implementace. Protokol funguje jako stavový automat: po stisku tlačítka se odešle paket a MCU spustí časovač. Pokud ze vzdáleného serveru nedorazí potvrzovací zpráva do nastaveného limitu, je operace vyhodnocena jako neúspěšná. Před každou zprávou je ověřena registrace do sítě příkazem AT+CEREG?.

## 5. Zvolená baterie
* **Typ baterie:** 
* **Zdůvodnění:** Byla zvolena vhodná napájecí baterie pro dané zařízení s ohledem na požadavky. Nabízí adekvátní vlastnosti pro zařízení, které většinu času tráví v režimu spánku a vyžaduje stabilní napětí pro občasné vysílání.

## 6. Implementace úspory energie a kalkulace životnosti
* **Implementace:** Byly implementovány vhodné režimy úspory energie. MCU po vyřízení požadavku a zhasnutí indikační LED přechází do režimu spánku a probouzí se výhradně externím přerušením od tlačítka. Modem využívá funkci **PSM (Power Saving Mode)**.
* **Kalkulace:** 

## 7. Zdůvodnění dalších parametrů
* **Interval vysílání:** Zařízení nevysílá periodicky, čímž je zamezeno odesílání v nekonečné smyčce. Vysílání probíhá výhradně na základě stisku tlačítka, což je hlavní důvod pro úsporu energie.

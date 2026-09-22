# Sortiment pro bezobslužný obchod 24/7 – analýza prodejů Piskora a syn

Cíl: z reálných prodejů prodejny 1 (drogerie, barvy/laky, elektro, voda) v Solnici odvodit, které zboží se prodává tak často, levně a bez poradenství, že se hodí do malé bezobslužné prodejny v menším městě.

## Shrnutí

- **Zákazník prodejny nakupuje drobně a často.** Průměrný nákup je 300–320 Kč (drogerie) a 210 Kč (železářství). 57 % prodaných kusů stojí do 60 Kč, 82 % do 150 Kč. Přesně takové zboží bezobslužný formát unese.
- **Prodej je extrémně koncentrovaný.** Z 12 897 skladových karet se za měsíc prodá jen 3 200 a **316 položek dělá polovinu všech prodaných kusů**, 1 300 položek 80 %. Malá prodejna s 300–400 položkami tedy pokryje většinu poptávky.
- **Jádro sortimentu pro 24/7: 282 položek** z 13 skupin (tabulka níže). Tvoří 38 % prodaných kusů a 16 % obratu prodejny 1, průměrná marže 30–50 %. Dalších 82 položek je vhodných podmíněně (kabely v předbalených návinech, spojovací materiál v blistrech, malá ředidla).
- **Co bezobslužně nejde:** nátěrové hmoty (24 % obratu prodejny, ale kbelíky, tónování, poradenství), stavební chemie v pytlích, pyrotechnika, spreje, sortiment na metry a na kusy.
- **Chybí data z prodejny 2** (železářství, zahrada, rybařina). Ta je pro 24/7 formát velmi relevantní a stejný export „Zásoby“ z jejího skladu analýzu doplní.

## Data

| Zdroj | Co obsahuje |
| --- | --- |
| `Zásoby.xlsx` (Google Drive, export 8. 4. 2025) | 12 897 skladových karet prodejny 1 s obratem, ziskem a prodanými kusy za 30 dní (9. 3. – 8. 4. 2025) a za stejné okno o rok dříve. Roční sloupce byly prázdné. |
| `Prumerny_nakup (1).xlsx` | Měsíční tržby a počet nákupů obou prodejen 2023 a 1–8/2024. |

Prodejna 1 udělá 52 nákupů denně (v létě 63), prodejna 2 asi 34. Sezónnost je silná: květen–srpen má 2,2× vyšší tržby než leden–únor. Analyzované okno (březen/duben) je průměrný měsíc, nezachycuje tedy zimní zboží (podpalovače, svíčky) ani předvánoční prodej; ty jsou v číslech níže podhodnocené.

Položky jsem zařadil do produktových skupin podle názvu (klíčová slova); 10 % kusů zůstalo nezařazených v dlouhém chvostu. Detail a metodika jsou v `sortiment_24-7_analyza.xlsx`.

## Produktové skupiny podle vhodnosti pro 24/7

Vhodnost 1–5 hodnotí frekvenci prodeje, cenu, nutnost poradenství, právní a požární omezení, rozměr a trvanlivost. Kusy a obrat jsou průměr za měsíc z obou oken, obrat bez DPH.

| Skupina | Vhodnost | ks/měsíc | Podíl kusů | Obrat/měsíc Kč | Marže | Prům. cena Kč |
| --- | :-: | --: | --: | --: | --: | --: |
| Baterie | 5 | 389 | 6,7 % | 8 900 | 50 % | 23 |
| Lepicí a maskovací pásky | 5 | 256 | 4,4 % | 13 600 | 46 % | 53 |
| Žárovky a světelné zdroje | 5 | 142 | 2,4 % | 7 400 | 48 % | 52 |
| Malířské potřeby (štětce, válečky, fólie, brusivo) | 4 | 771 | 13,3 % | 32 100 | 41 % | 42 |
| Vodoinstalace (objímky, spony, fitinky, těsnění) | 4 | 420 | 7,2 % | 20 700 | 38 % | 49 |
| Lepidla, tmely, silikony, PU pěny | 4 | 358 | 6,2 % | 43 400 | 30 % | 121 |
| Elektroinstalační drobný materiál (WAGO, pojistky, vidlice) | 4 | 328 | 5,7 % | 16 400 | 36 % | 50 |
| Úklid a čisticí prostředky | 4 | 314 | 5,4 % | 21 100 | 36 % | 67 |
| Semena, hnojiva, ochrana rostlin | 4 | 190 | 3,3 % | 6 800 | 41 % | 36 |
| Ochranné pomůcky (rukavice) | 4 | 88 | 1,5 % | 9 700 | 39 % | 110 |
| Hubení škůdců | 4 | 68 | 1,2 % | 3 300 | 35 % | 49 |
| Podpalovače, zapalovače, uhlí | 4 | 65 | 1,1 % | 3 300 | 33 % | 50 |
| Svíčky a hřbitovní zboží | 4 | 42 | 0,7 % | 1 700 | 37 % | 39 |
| Kabely a vodiče | 3 | 300 | 5,2 % | 10 000 | 39 % | 33 |
| Ředidla a technická chemie | 3 | 190 | 3,3 % | 20 500 | 44 % | 108 |
| Domácnost (věšáky, skřipce, šňůry) | 3 | 138 | 2,4 % | 6 200 | 36 % | 45 |
| Ruční nářadí a měřidla | 3 | 125 | 2,2 % | 13 300 | 39 % | 106 |
| Hygiena a papírové zboží | 3 | 101 | 1,7 % | 3 300 | 31 % | 33 |
| Klíče, kroužky, rozlišovače | 3 | 92 | 1,6 % | 500 | 45 % | 5 |
| Papírnictví | 3 | 82 | 1,4 % | 3 300 | 36 % | 40 |
| Spojovací materiál | 3 | 67 | 1,2 % | 2 200 | 36 % | 34 |
| Nátěrové hmoty (barvy, laky, lazury) | 2 | 336 | 5,8 % | 122 300 | 37 % | 364 |
| Spreje | 2 | 113 | 1,9 % | 14 900 | 37 % | 132 |
| Osobní kosmetika | 2 | 67 | 1,2 % | 6 200 | 30 % | 93 |
| Stavební chemie, sádra | 1 | 67 | 1,2 % | 10 500 | 38 % | 157 |
| Pyrotechnika, zahradní technika | 1 | 0 | 0 % | 0 | – | – |

Sezónní skupiny (velikonoční zboží, zavařování, autodoplňky) mají v tomto okně malý objem a jsou v tabulce v Excelu.

## Doporučené jádro sortimentu (282 položek)

Filtr: aspoň 3 prodané kusy měsíčně v obou letech, cena do 300 Kč, skupina s vhodností 4–5. Kompletní seznam s EAN, cenou, prodeji a stavem zásob je v listu „Kandidatni polozky“.

| Skupina | Položek | ks/měsíc | Obrat/měsíc Kč | Příklady nejprodávanějších |
| --- | --: | --: | --: | --- |
| Malířské potřeby | 81 | 541 | 16 700 | zakrývací fólie 4×5 m (25 Kč, 63 ks/měs), nopová fólie, brusná plátna 80/120, štětce TOP Q 40/50 mm, válečky |
| Baterie | 17 | 368 | 7 000 | AA/AAA Panasonic po kuse (8–25 Kč, 45–70 ks/měs), CR2032 (38 ks/měs), 10ks packy GETI, LR14, 9V, A23, LR44 |
| Vodoinstalace | 37 | 259 | 6 000 | hadicové spony 8–50 mm (8–10 Kč, 10–20 ks/měs), trubkové objímky, PPR kolena 20 mm, teflonová páska, těsnění |
| Elektroinstalace | 25 | 218 | 5 700 | WAGO svorky 221/2273 (6–19 Kč, 20–30 ks/měs), přístrojové pojistky, faston zdířky, úhlové vidlice, instalační krabice |
| Lepicí pásky | 20 | 176 | 7 600 | papírové maskovací pásky TX 25–48 mm (37–63 Kč, marže 140 %), izolační pásky, teflon |
| Semena a ochrana rostlin | 5 | 166 | 4 700 | semena 19/23/42 Kč (marže 42–107 %; 155 ks/měs jen ze tří položek) – sezónní stojan |
| Lepidla, tmely, pěny | 30 | 142 | 17 500 | Mamut Glue 290 ml (199 Kč, 26 ks/měs), Mamut 25 ml, sanitární silikon, akryl, PU pěna, Loctite |
| Úklid | 28 | 119 | 5 700 | osvěžovač vzduchu, Solvina, Praganda, Savo, Domestos, pytle na odpad, lopatka |
| Žárovky | 12 | 72 | 2 500 | G9 Kanlux, E27 40/60 W, E14 svíčka, GU10 LED, LED 8 W E27 |
| Ochranné pomůcky | 10 | 44 | 1 600 | pracovní rukavice Petrax vel. 8–11 (59 Kč), Allstar, zátky do uší |
| Hubení škůdců | 9 | 42 | 1 400 | pastičky na myši dřevo/kov, Feroset na moly, Ratimor 150 g, mucholapky |
| Podpalovače | 3 | 36 | 1 100 | Pepo pevný podpalovač 40 ks (35 Kč, 29 ks/měs i v březnu), zapalovače, dřevěné uhlí |
| Hřbitovní svíčky | 5 | 28 | 700 | patrony 120/180 g (25–32 Kč), svíčky Theresia |

Celkem: 2 200 ks a asi 78 000 Kč obratu měsíčně, tedy 38 % prodaných kusů prodejny 1 v jedné pětině jejího sortimentu. Bezobslužná prodejna v jiném městě bude mít jiný objem, ale skladba nákupů zůstane.

## Co přidat mimo data a co řešit před spuštěním

- **Kabely a spojovací materiál jinak balit.** CYKY 3×2,5 a CYSY se prodávají na metry (100–150 m/měsíc), šrouby po kuse za 0,40 Kč. Bezobslužně jde jen předbalený návin 5/10 m a blistry/sáčky se sadami vrutů, hmoždinek a šroubů.
- **Nátěrové hmoty jen minimálně.** Het Klasik 15+3 kg (799 Kč, 15 ks/měs) je nejsilnější položka prodejny, ale těžká a náchylná na krádež. Zvážit jen bílou malířskou barvu do 4 kg, malé lazury 0,75 l a Bochemit proti plísním.
- **Hořlaviny.** Ředidla S6006/S6005 0,7 l (40 ks/měs) a technický líh se prodávají dobře, ale v bezobslužném prostoru je nutné ověřit požární předpisy a limity skladovaného množství. Technický benzín (spotřební daň) a kyselinu solnou vynechat.
- **Zakázané nebo nevhodné bez obsluhy:** pyrotechnika (zákon č. 206/2015 Sb., ověření věku), barvy ve spreji (hořlavé, riziko zneužití), dražší nářadí, cokoliv nad cca 500 Kč kvůli riziku krádeže.
- **Sezónní stojany.** Semena (únor–květen), velikonoční barvy na vejce, zavařovací víčka a špejle (léto–podzim), podpalovače a hřbitovní svíčky (podzim–zima). Jeden stojan střídat podle sezóny.
- **Opravit nákupní ceny.** V exportu má několik položek zápornou marži kvůli chybné nákupní ceně (Váleček nylon 6 cm −12 322 Kč, PPR koleno 20 mm −921 Kč, Mamut Glue Total, těsnicí guma K profil). Před oceněním sortimentu je potřeba je opravit.
- **Doplnit data.** Stejný export „Zásoby“ z prodejny 2 (železářství, zahrada, rybařina) a ideálně roční sloupce, aby se ověřila zimní sezóna a doplnily rybářské potřeby, zahradní drobnosti a hospodářské zboží, které v malých městech v bezobslužném formátu chybí.

## Návrh nutného základu (DIY) – 184 položek

Minimální sortiment pro první bezobslužnou jednotku, po sekcích. Sloupec „Solnice ks/měs“ je průměrný měsíční prodej z dat prodejny 1; „doplnit“ značí položku mimo tato data (železářství, zahrada, nouzové zboží), doplněnou podle zkušenosti. Sečteno: 134 položek podložených daty prodává v Solnici asi 2 100 ks a 108 tis. Kč bez DPH měsíčně. Tabulka je i v listu *Zakladni sortiment* v Excelu a v `zakladni_sortiment.csv`; skript `zakladni_sortiment.py` ji generuje.


### Baterie (13)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| AA alkalická po kuse (Panasonic) | 8 | 46 |  |
| AA alkalická 10 ks (GETI) | 120 | 73 |  |
| AAA alkalická po kuse | 25 | 43 |  |
| AAA alkalická 10 ks | 120 | 41 |  |
| CR2032 knoflíková | 45 | 38 |  |
| CR2025 knoflíková | 39 | 6 |  |
| C / LR14 (2 ks) | 39 | 14 | zinkové R14 + alkalické LR14 |
| D / LR20 (2 ks) | 60 | doplnit | svítilny, plynové kotle |
| 9V blok 6LR61 | 60 | doplnit | kouřové hlásiče |
| A23 12V | 39 | 7 | dálkové ovladače vrat |
| LR44 / A76 | 25 | 6 |  |
| PR312 do naslouchátek | 18 | 6 |  |
| Lithium AA (2 ks) | 74 | 10 |  |

### Žárovky a svítidla (11)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| LED E27 8–10 W teplá bílá | 89 | 8 | nahrazuje 60 W |
| LED E27 13–15 W teplá bílá | 119 | doplnit | nahrazuje 100 W |
| LED E14 svíčka 5–6 W | 79 | doplnit | klasické E14 25/40 W se prodávají 10 ks/měs |
| Žárovka E27 40 W / 60 W (tes-lamp, klasik) | 20 | 21 | dokud je dostupná |
| Žárovka E14 svíčka 25 W / 40 W | 20 | 10 |  |
| GU10 LED 5 W | 69 | 5 |  |
| G9 halogen / LED | 39 | 14 |  |
| Reflektor R50 E14 40 W | 39 | 3 |  |
| LED trubice 120 cm T8 | 149 | doplnit | garáže, dílny |
| Startér do zářivky S2/S10 | 15 | doplnit |  |
| Svítilna / čelovka LED na AA/AAA | 119 | 5 |  |

### Elektroinstalace (19)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| WAGO 221-412 (2×4 mm) s páčkou | 13 | 15 |  |
| WAGO 221-413 (3×4 mm) s páčkou | 16 | 30 | nejprodávanější |
| WAGO 221-415 (5×4 mm) s páčkou | 20 | 5 |  |
| WAGO 2273-203 (3×2,5 mm) | 6 | 21 |  |
| WAGO 2273-204 (4×2,5 mm) | 8 | 20 |  |
| Pojistky přístrojové 5×20 mm – sada hodnot | 9 | 17 | prodávat v sadě 10 ks |
| Pojistka 16 A válcová | 25 | 6 |  |
| Vidlice úhlová bílá | 53 | 7 |  |
| Vidlice gumová IP44 černá | 109 | 6 |  |
| Zásuvka pohyblivá (na kabel) bílá / gumová | 60 | doplnit |  |
| Prodlužovací kabel 3 zásuvky, 3 m a 5 m | 199 | doplnit | nejčastější nouzový nákup elektro |
| Prodlužovací kabel 1 zásuvka 10 m (zahradní) | 299 | doplnit |  |
| Spínač jednopólový + zásuvka nástěnná (Tango/Classic) | 91 | 4 |  |
| Instalační krabice KU 68 (do zdi) a do SDK | 8 | 15 |  |
| Svorkovnice 12pól. 2,5 mm | 25 | doplnit |  |
| Husí krk 16 / 23 mm (návin 5 m) | 80 | 26 | v datech na metry |
| Lišta vkládací 17×17 mm 2 m | 66 | 5 |  |
| Faston zdířky 6,3 mm (sáček 20 ks) | 30 | 14 |  |
| Zvonek bezdrátový / bateriový tlačítko | 249 | doplnit |  |

### Kabely (předbalené náviny) (6)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| CYSY 3G×1,5 návin 5 m a 10 m | 160 | 72 | v datech 72 m/měs po metrech |
| CYKY 3×2,5 návin 10 m | 380 | 49 |  |
| CYKY 3×1,5 návin 10 m | 280 | 30 |  |
| CYSY 2×1 návin 5 m | 85 | 33 |  |
| CYSY 3G×1 návin 5 m | 105 | 12 |  |
| Dvojlinka 2×0,75 návin 20 m | 60 | 22 |  |

### Pásky (10)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Maskovací páska TX 25 mm 50 m | 59 | 72 | marže 144 % |
| Maskovací páska TX 30 / 38 / 48 mm | 50 | 25 |  |
| Krepová páska 50 mm 50 m (60 °C) | 76 | 7 |  |
| Izolační páska 15 mm černá + sada barev | 12 | 14 |  |
| Izolační páska 25 mm | 22 | 6 |  |
| Teflonová páska 12 mm | 22 | 6 |  |
| Balicí páska 48 mm 66 m | 55 | 6 |  |
| Univerzální textilní (duct) páska 50 mm | 145 | 5 |  |
| Oboustranná montážní páska | 89 | doplnit |  |
| Stahovací pásky 200 mm a 300 mm (50 ks) | 50 | 8 |  |

### Lepidla, tmely, pěny (14)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Mamut Glue High tack 290 ml bílý | 199 | 26 | nosná položka |
| Mamut Glue Crystal transparent 290 ml | 235 | 4 |  |
| Mamut Glue 25 ml (tuba) | 75 | 5 |  |
| Sekundové lepidlo 3 g (Loctite) | 53 | 3 |  |
| Herkules / Chemoprén univerzál 50–120 g | 60 | doplnit |  |
| Sanitární silikon 280 ml bílý a transparent | 155 | 13 |  |
| Akryl bílý 310 ml | 95 | 5 |  |
| Montážní pěna trubičková 750 ml | 169 | 4 |  |
| Pěna 500 ml s aplikátorem (Pattex Control) | 169 | 6 |  |
| Pistole na kartuše | 99 | doplnit | bez ní se silikon neprodá |
| Aplikační špičky na kartuše 5 ks | 44 | 4 |  |
| Tmel na dřevo 250 g (smrk, dub) | 62 | 5 |  |
| Sádra bílá 1 kg a 3 kg | 45 | 10 |  |
| Univerzální štukový tmel 400 g (Uniflex) | 65 | 3 |  |

### Malířské potřeby (14)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Zakrývací fólie 4×5 m | 25 | 63 | nejprodávanější kus prodejny |
| Zakrývací plachta 4×12,5 m | 55 | 16 |  |
| Štětec plochý 40 / 50 / 70 mm | 37 | 26 |  |
| Váleček velvet 10 cm + držadlo | 22 | 10 |  |
| Váleček 18 / 25 cm + rukojeť | 90 | 9 |  |
| Malířská mřížka / vanička | 39 | doplnit |  |
| Brusné plátno 60 / 80 / 120 | 17 | 35 |  |
| Brusný papír pod vodu 600 / 800 | 15 | 20 |  |
| Špachtle 60 mm a 100 mm | 39 | doplnit |  |
| Míchací pohár 385 ml | 21 | 4 |  |
| Nopová fólie 0,5 m a 1 m × 20 m | 38 | 40 | izolace základů, silný prodej |
| Bílá malířská barva 4 kg (Primalex/HET) | 199 | doplnit | jediná barva, kterou bezobslužně držet |
| Univerzální lazura 0,75 l ořech / teak | 259 | 5 |  |
| Bochemit proti plísním 500 ml | 99 | 6 |  |

### Vodoinstalace (13)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Hadicové spony 8–12 / 12–20 / 16–25 / 20–32 / 25–40 / 32–50 | 9 | 77 | celá řada |
| Objímka trubková 2-šroub 31–38 mm | 16 | 25 |  |
| Objímka trubková 2-šroub 54–59 mm | 22 | 14 |  |
| Příchytka na potrubí 20 / 25 mm | 8 | 17 |  |
| PPR koleno 90° 20 mm, T-kus 20, nátrubek 20 | 8 | 15 | jen dimenze 20 a 25 |
| Mosazná vsuvka 3/4", 1/2" | 48 | 9 |  |
| Tubex izolace 20×10 mm (2 m) | 12 | 14 |  |
| Těsnění gumová sada 1/2"–3/4" | 25 | doplnit | nejčastější havárie |
| Flexi hadička 3/8" 30–50 cm | 79 | doplnit |  |
| Perlátor M22/M24 | 39 | doplnit |  |
| Sprchová hadice 150 cm | 245 | 3 |  |
| Sifon umyvadlový plast | 89 | doplnit |  |
| Zahradní hadice 1/2" 20 m + rychlospojky | 399 | doplnit | ověřit z dat prodejny 2 |

### Spojovací materiál (blistry) (8)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Hmoždinky 6 / 8 / 10 mm (sady) | 39 | doplnit | v datech kusový prodej |
| Vruty univerzální 4×40, 4×50, 5×60 (sady) | 59 | doplnit |  |
| Šrouby do plechu 2,9×13 (sada 50 ks) | 29 | 37 | v datech 37 ks/měs po 0,40 Kč |
| Hřebíky 40 / 60 / 80 mm (sáček) | 39 | doplnit |  |
| Skoby, háčky, oka (sada) | 39 | doplnit |  |
| Hmoždinka rámová 10×100 (sada) | 79 | doplnit |  |
| Vázací drát pozink | 49 | doplnit |  |
| Zárohák (hák do zdi) | 69 | 5 |  |

### Ruční nářadí (12)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Svinovací metr 5 m | 99 | 9 |  |
| Odlamovací nůž 18 mm kovový | 89 | 7 |  |
| Náhradní čepele 18 mm 10 ks | 40 | 12 |  |
| Šroubovák s bity (ráčna + 20 bitů) | 199 | doplnit |  |
| Kleště kombinované 180 mm | 149 | doplnit |  |
| Kladivo 300 g | 129 | doplnit |  |
| Ocelový kartáč 5řadý | 68 | 5 |  |
| Pilka na kov / pilový list | 99 | doplnit |  |
| Vodováha 40 cm | 99 | doplnit |  |
| Sada imbus klíčů | 89 | doplnit |  |
| Zavírací nůž | 163 | 4 |  |
| Vědro stavební 12 l | 49 | 6 |  |

### Ochranné pomůcky (6)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Pracovní rukavice vel. 8 / 9 / 10 / 11 | 59 | 30 | celá řada velikostí |
| Rukavice profi 1+1 | 28 | 5 |  |
| Jednorázové nitrilové rukavice (10 ks) | 39 | doplnit |  |
| Zátky do uší | 10 | 3 |  |
| Respirátor FFP2 (2 ks) | 39 | doplnit | broušení, barvy |
| Ochranné brýle | 49 | doplnit |  |

### Technická chemie (11)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Ředidlo S6006 0,7 l | 85 | 21 | hořlavina – ověřit požární předpisy |
| Ředidlo S6005 0,7 l | 95 | 12 |  |
| Nitroředidlo C6000 0,7 l | 95 | 9 |  |
| Líh technický 0,7 l | 98 | 7 |  |
| Lakový benzín 0,7 l | 109 | 4 |  |
| WD-40 / univerzální mazivo sprej 200 ml | 129 | doplnit |  |
| Odrezovač 0,5 l | 112 | 3 |  |
| Kyselina citronová 100 g | 22 | 6 |  |
| Vazelína bílá | 195 | 4 |  |
| Destilovaná voda 5 l | 70 | 6 |  |
| Nemrznoucí směs do ostřikovačů 3 l | 99 | doplnit | sezónně |

### Úklid (13)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Savo Original 1,2 l | 67 | 5 |  |
| Savo proti plísni 500 ml | 99 | 5 |  |
| Domestos 750 ml / 2 l | 59 | 10 |  |
| Jar / prostředek na nádobí 900 ml | 59 | doplnit |  |
| Univerzální čistič (Ajax, Cif) | 59 | doplnit |  |
| Pytle na odpad 60 l a 120 l | 39 | 11 |  |
| Houbičky na nádobí 5 ks | 25 | doplnit |  |
| Hadr podlahový | 32 | 4 |  |
| Osvěžovač vzduchu | 29 | 9 |  |
| Solvina / Praganda (mycí pasta na ruce) | 20 | 15 | typicky DIY |
| WC blok | 39 | 5 |  |
| Lopatka + smetáček | 49 | 6 |  |
| Zamražovací / svačinové sáčky | 39 | 4 |  |

### Hygiena (4)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Toaletní papír Jumbo / 8 rolí | 39 | 30 |  |
| Papírové ručníky ZZ | 45 | 15 |  |
| Kapesníky krabička 150 ks | 38 | 3 |  |
| Kuchyňské utěrky 2 role | 39 | doplnit |  |

### Hubení škůdců (7)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Pastička na myši dřevo / kov | 16 | 12 |  |
| Nástraha na myši Ratimor 150 g | 42 | 8 | balení pro veřejnost |
| Lepová deska na myši | 35 | 3 |  |
| Mucholapka | 7 | 4 |  |
| Feroset – lapač moučných molů | 16 | 8 |  |
| Sprej na vosy / hmyz (Biolit) | 119 | doplnit | léto |
| Proti mravencům (Bioformatox) | 109 | 2 |  |

### Topení a zapalování (6)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Pepo pevný podpalovač 40 ks | 35 | 29 | celoročně |
| Tekutý podpalovač 1 l | 96 | 3 |  |
| Zapalovač kuchyňský dlouhý | 37 | 3 |  |
| Zapalovače turbo (2 ks) | 15 | 4 |  |
| Zápalky (balení 10 krabiček) | 25 | 2 |  |
| Dřevěné uhlí 2,5 kg | 112 | 3 | sezónně |

### Svíčky (4)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Hřbitovní patrona 120 g a 180 g | 28 | 18 |  |
| Svíčka Theresia 4,5 dne | 47 | 3 |  |
| Iluminační svíčky 10 ks | 59 | 3 |  |
| Čajové svíčky 30 ks | 49 | doplnit |  |

### Domácnost (9)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Skřipce záclonové | 6 | 22 |  |
| Háčky samolepicí | 30 | 5 |  |
| Věšák nástěnný chrom | 62 | 10 |  |
| Kolíčky na prádlo 24 ks | 39 | doplnit |  |
| Prádelní šňůra 20 m | 49 | doplnit |  |
| Provázek / polypropylenové lano 20 m | 59 | doplnit |  |
| Kroužky na klíče + rozlišovače | 4 | 46 | u pokladny |
| Visací zámek 30 / 40 mm | 129 | doplnit |  |
| Magnety 10 ks | 50 | 3 |  |

### Sezónní stojan (rotace) (4)

| Položka | Cena Kč | Solnice ks/měs | Poznámka |
| --- | --: | --: | --- |
| Semena zeleniny a květin (stojan) | 25 | 153 | únor–květen, marže 40–100 % |
| Barvy na vejce, obtisky | 12 | 15 | březen–duben |
| Zavařovací víčka Twist, špejle, střeva | 40 | 15 | červenec–říjen |
| Posypová sůl 5 kg, škrabka na led | 79 | doplnit | listopad–únor |

## Soubory

- `sortiment_24-7_analyza.xlsx` – list *Skupiny* (32 skupin, vhodnost a komentář), *Kandidatni polozky* (364 položek: jádro a podmíněné), *Metodika*.
- `skupiny.csv`, `kandidatni_polozky.csv` – totéž v CSV.
- `analyza.py` – skript, který z `Zasoby.xlsx` tabulky vytvoří (klasifikace názvů, skóring, export).
- `zakladni_sortiment.csv`, `zakladni_sortiment.py` – návrh nutného základu 184 položek po sekcích (též list *Zakladni sortiment* v Excelu).

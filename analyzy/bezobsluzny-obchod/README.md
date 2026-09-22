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

## Soubory

- `sortiment_24-7_analyza.xlsx` – list *Skupiny* (32 skupin, vhodnost a komentář), *Kandidatni polozky* (364 položek: jádro a podmíněné), *Metodika*.
- `skupiny.csv`, `kandidatni_polozky.csv` – totéž v CSV.
- `analyza.py` – skript, který z `Zasoby.xlsx` tabulky vytvoří (klasifikace názvů, skóring, export).

"""Analýza sortimentu pro bezobslužný obchod 24/7.

Použití: python3 analyza.py Zasoby.xlsx [výstupní_složka]
Vstup: export skladových karet (list "Zásoby") se sloupci Název, Členění, Prodejní, Marže,
Realizováno 30, Obrat 30, Zisk 30, Realizováno 30 (před rokem), Obrat 30 (před rokem).
"""
import sys
import pandas as pd, numpy as np, unicodedata, re
def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii','ignore').decode().lower()
    return ' '+re.sub(r'\s+',' ',s)+' '
RULES = [
 ('Baterie', ['bater','lr06','lr6 ','lr03','cr-20','cr20','lithium','r14','r20','lr14','lr20',' 9v','knoflik','supercell','alkal','zinkov','aaa','tuzkov']),
 ('Žárovky a světelné zdroje', ['zarov','led ','led-','e27','e14',' g9','gu10','trubice','zariv','halogen','techlamp','tes-lamps','svitidl','svitiln','baterka','celovka','reflektor','kanlux']),
 ('Kabely a vodiče', ['cyky','cysy','vodic','kabel','dvojlinka','husi krk','lanko']),
 ('Elektroinstalační drobný materiál', ['wago','svork','krabice','inst.','zasuvk','vypinac','vidlice','prodluz','rozdvojk','pojistk','jistic','faston','zdir','konektor','objimka e','stmivac','zvonek','kolik','lišta','lista','klips','prichytka kab']),
 ('Lepicí a maskovací pásky', ['paska','pasky','izolacni','tx ']),
 ('Lepidla, tmely, silikony, PU pěny', ['lepidl','mamut','tmel','silikon','pena','sekund','herkules','chemopren','montaz','fixace','spar','kit ']),
 ('Malířské potřeby (štětce, válečky, fólie, brusivo)', ['stetec','valecek','folie','plachta','zakryvac','brusn','spachtle','mrizk','vanick','skrabk','nopov','krycí']),
 ('Nátěrové hmoty (barvy, laky, lazury)', ['primalex','het ','klasik','malir','interier','dulux',' du ','remal','balakryl','eternal','osmo','luxol','lazur','lak ','email','syntet','zaklad','remmers','alkyton','chemolak','sadolin','xyladecor','barva','naterov','fasad','penetra','rapidry','hardener','plnic','pigment','tonov','odstin']),
 ('Ředidla a technická chemie', ['redidl','s6006','s6005','s6001','benzin','aceton','lih','petrolej','odrezov','wd-40','wd40','maziv','olej','vazelin','odstranov','kyselina','chlornan','odmast']),
 ('Spreje', ['sprej','spray','motip','efekt']),
 ('Úklid a čisticí prostředky', ['cist','savo','domestos','jar ','pur ','cif ','ajax','myci','praci','persil','ariel','avivaz','lenor','tablet','houb','hadr','uterk','mop','koste','smetak','lopatk','pytle','sacky','odpadk','leste','bref','wc ','okena','pronto','drevo','odpad ','sifo','krtek','fresh']),
 ('Hygiena a papírové zboží', ['toalet','rucnik','harmasan','kapesnik','ubrousk','papir','vlhcen','tampon','vlozk','plen']),
 ('Osobní kosmetika', ['mydlo','sampon','sprch','zubni','pasta','krem','holen','deodor','nivea','dezinf','gel','tekute','vata','vatov']),
 ('Semena, hnojiva, ochrana rostlin', ['semen','semin','hnojiv','substrat','zemin','postrik','herbicid','roundup','insektic','msic','slimak','hubeni','jed ','lapac','past ','pasti','floria','agro','cibul','sadb','trav','osivo','plevel','mravenc','vosy','moucha','mol ','komar','hlodav']),
 ('Podpalovače, topení, zapalování', ['pepo','podpalov','zapalov','brikety','uhli','sirky','zapalk','kominik','krb','komin']),
 ('Vodoinstalace a hadice', ['ppr','koleno','objimka','prichytka na potrubi','hadic','ventil','sifon','tesneni','fitink','natrubek','redukce','spojka','kohout','pvc','splachov','odpadni','trubk','zatka','stoupac','sprchov','perlator','vodovod']),
 ('Spojovací materiál', ['sroub','vrut','hmozdin','matice','podlozk','hrebik','skob','hak ','haky','zavitov','nyt','kotva','sponka','sponky']),
 ('Ruční nářadí a měřidla', ['metr ','kladiv','kleste','sroubovak','nuz','bit ','bity','vrtak','kotouc','pilka','pila','pilnik','sada','vodovah','klic ocko','gola','stetka','strouhac','hoblik','dlato','pistol','stavec','sekera','lopata','hrabe','motyka','rukojet','nasada','kartac','kartace']),
 ('Klíče, zámky, kroužky', ['klic','klic','krouzek','rozlisovac','visaci','zamek','petlice','retez','retizek']),
 ('Svíčky a hřbitovní zboží', ['svick','patron','hrbitov','kahan','lampov','olej do lamp','vosk','cajov']),
 ('Domácnost (šňůry, kolíčky, věšáky, garnýže)', ['skripec','zaclon','vesak','kolick','snur','provaz','lano','garnyz','zaves','hacek','dvere','rohoz','kos ','krabicka','dozy','dozy','kbelik','vedro','lavor','plastov','konev','prkénko','prkenko','misk','miska','hrnec']),
 ('Krmiva a chovatelské potřeby', ['drubez','krmiv','granul','psy','kocky','steliv','ptactv','zrni','slunecnic','hospodar']),
 ('Ochranné pomůcky', ['rukavic','respirat','bryle','rousk','chranic','spunt','zastera','overal']),
 ('Autodoplňky', ['nemrznouc','ostrikov','autokosm','auto ','12v','aku ','startovac','okna aut']),
 ('Zahradní technika a příslušenství', ['struna','sekack','plotostrih','retez pil','zahrad','zavlah','rozstrik','kropic','postrikovac']),
 ('Pyrotechnika', ['petard','rachej','ohnostroj','pyrotech']),
]

EXTRA = [
 ('Baterie', ['naslouch','lr44','a76','energizer','gp ']),
 ('Hygiena a papírové zboží', ['jumbo','linteo','kapesnic']),
 ('Papírnictví a psací potřeby', ['popisova','fix ','fixy','tuzka','propis','sesit','obalk','lepic tyc','nuzky','sacek celof','celofan']),
 ('Velikonoční a sezónní zboží', ['na vejce','obtisky','ovo ','velikon','vanoc']),
 ('Vodoinstalace a hadice', ['vsuvka','tubex','izolace 2','ep ms','ep ppr','nipl','kolinko','t-kus','tkus','uzaver','flexi']),
 ('Úklid a čisticí prostředky', ['osvezov','solvina','praganda','rejzak','pytel','houbic','drat','kartac na','kbel']),
 ('Hubení škůdců', ['feroset','mucholap','lepinox','ratimor','moli','myši','mysi','potkan','nastrah','lep na','biolit','raid','repel','odpuzov','sit proti']),
 ('Stavební chemie a sádra', ['sadra','omitk','na obkl','malta','beton','cement','vapno','sterk','nivel','penetr']),
 ('Semena, hnojiva, ochrana rostlin', ['skalice','forestina','bioseptik','septik','kompost']),
 ('Elektroinstalační drobný materiál', ['vidlick','vidl.','spina','strojek','ramecek','kryt ','rozvodn','svorkovn','prodlu','zásuv','kabelov']),
 ('Domácí zavařování a uzení', ['spejle','vicko','zavar','sklenic','streva','uzenar','tlac.','sit na','uzeni']),
 ('Ruční nářadí a měřidla', ['cepel','cepelk','ostri','nahrady','festa','strouhat','kotouc','pilov']),
 ('Malířské potřeby (štětce, válečky, fólie, brusivo)', ['drzadlo','valec','pohar','michac','mrizka','vana']),
 ('Lepidla, tmely, silikony, PU pěny', ['aplikacni','kartus','loctite','super bond','lepidl','tesnici gum','akryl']),
 ('Ředidla a technická chemie', ['louh','destilov','hydroxid','nemrz','kyselin','vapenat','odvapn']),
 ('Domácnost (šňůry, kolíčky, věšáky, garnýže)', ['magnet','sklapk','drzak','poutko','uchytk','madlo','stopka','kolecko','kolecka','nabytk','skrin']),
 ('Ochranné pomůcky', ['zatky do usi','do usi','ochrann']),
 ('Osobní kosmetika', ['francovka','alpa','lekarn','naplast','obvaz','vata']),
 ('Nátěrové hmoty (barvy, laky, lazury)', ['laksil','komaprim','pragoprimer','prago','tuzid','tuzidlo','fermez','olejov','industrol','sokrates','colorlak','bori','lignofix','bochemit','tenax','autoemail']),
]
RULES = RULES[:4] + EXTRA + RULES[4:]

def classify(name):
    n = norm(name)
    for cat, kws in RULES:
        for k in kws:
            if k in n: return cat
    return 'Nezařazeno'

def load(path):
    df = pd.read_excel(path, sheet_name=0)
    lvl = df['Členění'].fillna('').str.split('/')
    for i in range(1, 4):
        df[f'L{i}'] = lvl.str[i-1]
    df['ks30'] = df['Realizováno 30'].fillna(0); df['ks30ly'] = df['Realizováno 30 (před rokem)'].fillna(0)
    df['obrat30'] = df['Obrat 30'].fillna(0); df['obrat30ly'] = df['Obrat 30 (před rokem)'].fillna(0)
    df['zisk30'] = df['Zisk 30'].fillna(0)
    df['ks'] = df['ks30'] + df['ks30ly']; df['obrat'] = df['obrat30'] + df['obrat30ly']
    df['Skupina_produkt'] = df['Název'].map(classify)
    df.loc[df['L3'].eq('JHPAP') & df['Název'].str.contains('Semena', case=False), 'Skupina_produkt'] = 'Semena, hnojiva, ochrana rostlin'
    df.loc[df['L2'].eq('Pyrotechnika'), 'Skupina_produkt'] = 'Pyrotechnika'
    df.loc[df['L2'].eq('žaluzie'), 'Skupina_produkt'] = 'Domácnost (šňůry, kolíčky, věšáky, garnýže)'
    return df

VHODNOST = {  # (skóre 1-5, poznámka)
 'Baterie': (5,'Nouzový nákup, nízká cena, dlouhá trvanlivost, minimální prostor. Drobné zboží – umístit do zorného pole kamery.'),
 'Žárovky a světelné zdroje': (5,'Typický večerní/víkendový nouzový nákup. Omezit na 15–20 nejběžnějších patic (E27, E14, G9, GU10) + LED.'),
 'Lepicí a maskovací pásky': (5,'Vysoká frekvence i marže (140 %+ u TX pásek), bez poradenství, netrvanlivost neřeší.'),
 'Elektroinstalační drobný materiál': (4,'WAGO svorky, pojistky, vidlice, zásuvky, krabice – běžné položky nevyžadují radu. Vynechat drahé jističe a přístroje.'),
 'Lepidla, tmely, silikony, PU pěny': (4,'Mamut, sekundová lepidla, sanitární silikon, akryl, pěna. Střední cena (100–200 Kč), dobrá marže.'),
 'Malířské potřeby (štětce, válečky, fólie, brusivo)': (4,'Nejprodávanější skupina v kusech. Fólie, štětce, válečky, brusné papíry. Zkontrolovat nákupní ceny (v datech je několik položek se zápornou marží).'),
 'Vodoinstalace a hadice': (4,'Havarijní nákup (praská hadice, teče spoj). Objímky, hadicové spony, PPR fitinky 20–25 mm, těsnění, teflon. Bez velkých trubek.'),
 'Úklid a čisticí prostředky': (2,'Savo, Domestos, pytle, houbičky. Konkuruje každý supermarket, nejnižší marže ze všech skupin (36 %) a objemné. Ze základu vyřazeno rozhodnutím majitele.'),
 'Semena, hnojiva, ochrana rostlin': (4,'Sezónní stojan (únor–květen). Semena 19–42 Kč s marží 40–100 %, minimální prostor. Mimo sezónu nahradit jiným stojanem.'),
 'Ochranné pomůcky': (4,'Pracovní rukavice 28–65 Kč, zátky do uší, respirátory. Vysoká frekvence, bez poradenství.'),
 'Podpalovače, topení, zapalování': (4,'Pepo, zapalovače, zápalky, dřevěné uhlí. Silně sezónní (podzim–zima + grilování), v malých městech s lokálním topením velmi žádané.'),
 'Hubení škůdců': (4,'Pastičky, mucholapky, nástrahy na myši (balení do 150 g pro veřejnost). Nouzový a diskrétní nákup – vhodné pro bezobslužný prodej.'),
 'Svíčky a hřbitovní zboží': (4,'Hřbitovní patrony 25–50 Kč, iluminační svíčky. V malých městech stálá poptávka, špičky před Dušičkami a svátky. Neomezená trvanlivost.'),
 'Hygiena a papírové zboží': (3,'Toaletní papír, ručníky, kapesníky. Nouzová potřeba 24/7, ale objemné a nízká marže (31 %). Držet 3–5 položek.'),
 'Kabely a vodiče': (3,'V datech se prodává na metry (nutná obsluha). Pro bezobslužný prodej předbalit 5 m / 10 m návin CYKY, CYSY a dvojlinky.'),
 'Ředidla a technická chemie': (3,'Ředidla 0,7 l a líh se prodávají dobře, ale jde o hořlaviny – nutné posoudit požární předpisy prostoru. Technický benzín (spotřební daň) a kyseliny vynechat.'),
 'Ruční nářadí a měřidla': (3,'Jen základ: svinovací metr, odlamovací nůž + čepelky, šroubovák, kartáč. Dražší nářadí = riziko krádeže.'),
 'Spojovací materiál': (3,'V datech kusový prodej za 0,3–0,4 Kč – bez obsluhy nefunguje. Nabídnout v blistrech/sáčcích (šrouby, hmoždinky, vruty – sady).'),
 'Papírnictví a psací potřeby': (3,'Popisovače, lepicí tyčinky, sáčky. Doplňkový sortiment, nízká cena, zabere málo místa.'),
 'Domácnost (šňůry, kolíčky, věšáky, garnýže)': (3,'Skřipce, háčky, věšáky, kolíčky, šňůry. Doplněk, pomalejší obrátka.'),
 'Klíče, zámky, kroužky': (3,'Kroužky a rozlišovače za 3–10 Kč – zanedbatelný obrat, ale zvyšují počet položek v košíku. Klíče se nedají bez obsluhy vyrábět.'),
 'Velikonoční a sezónní zboží': (3,'Sezónní stojan (barvy na vejce, obtisky). Střídat se semeny a vánočním zbožím.'),
 'Domácí zavařování a uzení': (3,'Víčka, špejle, střeva – sezónní (léto/podzim), malé rozměry.'),
 'Spreje': (4,'Barvy ve spreji 120–250 Kč, 113 ks/měs. Hořlavé a lákavé ke krádeži, proto omezená řada a zamčená vitrína nebo zorné pole kamery. Značkovací fluo sprej jede 18 ks/měs.'),
 'Nátěrové hmoty (barvy, laky, lazury)': (3,'Největší obrat prodejny (24 %). Tónované báze bez obsluhy nejdou, hotová bílá v pevných baleních ano: Het Klasik 15+3 kg je nejsilnější položka do 1 000 Kč (8,2 tis. Kč/měs).'),
 'Osobní kosmetika': (2,'V hobbymarketu se prodává málo (67 ks/měs), silná konkurence supermarketů. Jen dezinfekce, náplasti.'),
 'Stavební chemie a sádra': (3,'Pytle 25 kg se bezobslužně prodávají dobře: špatně se kradou a zvedají košík. Patří na paletu u vstupu. Lepidlo na dlažbu, cement, sloupkobeton, omítka.'),
 'Autodoplňky': (2,'Minimální prodej v datech; nemrznoucí směs a destilovaná voda jako doplněk.'),
 'Krmiva a chovatelské potřeby': (2,'Zanedbatelný prodej v datech (nesledovaný sortiment prodejny 1).'),
 'Zahradní technika a příslušenství': (1,'Bez prodejů, drahé, potřebuje obsluhu.'),
 'Pyrotechnika': (1,'Zákon č. 206/2015 Sb. – prodej jen osobám nad 18/21 let s ověřením, bez obsluhy nelze.'),
 'Nezařazeno': (0,'Dlouhý chvost (688 aktivních položek), ručně projít.'),
}

def groups(df):
    g = df.groupby('Skupina_produkt').agg(SKU_celkem=('Název', 'size'), SKU_aktivní=('ks', lambda s: (s > 0).sum()),
        ks_2025=('ks30', 'sum'), ks_2024=('ks30ly', 'sum'), obrat_2025=('obrat30', 'sum'), obrat_2024=('obrat30ly', 'sum'), zisk_2025=('zisk30', 'sum'))
    g['ks_měsíc_prům'] = ((g['ks_2025'] + g['ks_2024']) / 2).round(0)
    g['podíl_ks_%'] = (g['ks_měsíc_prům'] / g['ks_měsíc_prům'].sum() * 100).round(1)
    g['obrat_měsíc_prům'] = ((g['obrat_2025'] + g['obrat_2024']) / 2).round(0)
    g['podíl_obrat_%'] = (g['obrat_měsíc_prům'] / g['obrat_měsíc_prům'].sum() * 100).round(1)
    # marže bez položek s evidentně chybnou nákupní cenou (zisk < -100 Kč)
    ok = df[df['zisk30'] > -100].groupby('Skupina_produkt').agg(z=('zisk30', 'sum'), o=('obrat30', 'sum'))
    g['marže_%'] = (ok['z'] / ok['o'].replace(0, np.nan) * 100).round(0)
    g['prům_cena_Kč'] = (g['obrat_měsíc_prům'] / g['ks_měsíc_prům'].replace(0, np.nan)).round(0)
    g['vhodnost_24/7'] = [VHODNOST.get(i, (0, ''))[0] for i in g.index]
    g['komentář'] = [VHODNOST.get(i, (0, ''))[1] for i in g.index]
    g.index.name = 'Produktová skupina'
    return g.sort_values(['vhodnost_24/7', 'ks_měsíc_prům'], ascending=[False, False])

def candidates(df, min_ks=6, max_price=300):
    rec = [k for k, (s, _) in VHODNOST.items() if s >= 4]
    cond = [k for k, (s, _) in VHODNOST.items() if s == 3]
    c = df[(df['ks'] >= min_ks) & (df['Prodejní'] <= max_price) & (df['Prodejní'] > 0)].copy()
    c['ks_měsíc_prům'] = (c['ks'] / 2).round(1)
    c['obrat_měsíc_prům'] = (c['obrat'] / 2).round(0)
    c['marže_%'] = c['Marže'].round(0)
    c['doporučení'] = np.where(c['Skupina_produkt'].isin(rec), 'jádro', np.where(c['Skupina_produkt'].isin(cond), 'podmíněně', 'ne'))
    c = c.sort_values(['doporučení', 'Skupina_produkt', 'ks'], ascending=[True, True, False])
    cols = ['doporučení', 'Skupina_produkt', 'Název', 'Čárkód', 'Prodejní', 'ks30', 'ks30ly', 'ks_měsíc_prům', 'obrat_měsíc_prům', 'marže_%', 'Stav zásoby', 'Dodavatel', 'Členění']
    return c[cols].rename(columns={'Prodejní': 'Prodejní cena Kč', 'ks30': 'ks 3-4/2025', 'ks30ly': 'ks 3-4/2024', 'Stav zásoby': 'Stav zásoby (8.4.2025)'})

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'Zasoby.xlsx'
    out = (sys.argv[2].rstrip('/') + '/') if len(sys.argv) > 2 else './'
    df = load(src)
    g, c = groups(df), candidates(df)
    with pd.ExcelWriter(out + 'sortiment_24-7_analyza.xlsx', engine='openpyxl') as w:
        g.to_excel(w, sheet_name='Skupiny'); c.to_excel(w, sheet_name='Kandidatni polozky', index=False)
    g.to_csv(out + 'skupiny.csv'); c.to_csv(out + 'kandidatni_polozky.csv', index=False)
    pd.set_option('display.width', 250)
    print(g[['SKU_aktivní', 'ks_měsíc_prům', 'podíl_ks_%', 'obrat_měsíc_prům', 'marže_%', 'prům_cena_Kč', 'vhodnost_24/7']].to_string())
    for lab in ['jádro', 'podmíněně']:
        d = c[c['doporučení'] == lab]
        print(f"{lab}: {len(d)} SKU, {d['ks_měsíc_prům'].sum():.0f} ks/měs, {d['obrat_měsíc_prům'].sum():.0f} Kč/měs")

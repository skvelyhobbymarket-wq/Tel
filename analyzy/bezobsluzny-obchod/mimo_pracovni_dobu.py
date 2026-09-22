"""Poptávka mimo pracovní dobu – odhad podle charakteru zboží.

POZOR: sestava "Zásoby" obsahuje jen 30denní součty, ne jednotlivé účtenky.
Rozpad na dny v týdnu (pátek, sobota) ani na hodiny z ní spočítat nelze.
Tento model proto nahrazuje chybějící data expertním skóre:

  naléhavost  1–5  nákup nesnese odklad (havárie, přestalo svítit/téct/držet)
  víkend      1–5  typický kutilský projekt o víkendu (malování, broušení, zahrada)

Odhadovaný podíl poptávky mimo otevírací dobu:
  podíl = 0,10 + 0,06 × naléhavost + 0,04 × víkend   (strop 0,60)

Kalibrace: při otevírací době Po–Pá 7–17 a So 8–11 (53 z 168 hodin) připadá
asi 47 % bdělého času týdne mimo otevírací dobu. Zboží s nulovou naléhavostí
a nulovou víkendovostí se ale mimo dobu nekoupí skoro vůbec (zákazník počká),
proto model začíná na 10 % a k 47 % se blíží jen u havarijního zboží.
"""
import pandas as pd, numpy as np

# skupina: (naléhavost, víkend, důvod)
SKORE = {
 'Žárovky a světelné zdroje':        (5, 2, 'Přestane svítit večer. Nákup nesnese odklad a nedá se odložit na pracovní den.'),
 'Baterie':                          (5, 2, 'Vybité ovladače, hlásiče, hračky, svítilny. Klasický večerní a nedělní nákup.'),
 'Vodoinstalace a hadice':           (5, 3, 'Prasklá hadice, teče spoj. Havárie nečeká do pondělí.'),
 'Elektroinstalační drobný materiál':(4, 3, 'Vyhozená pojistka, utržená vidlice, prodlužovačka.'),
 'Lepidla, tmely, silikony, PU pěny':(4, 4, 'Rozbité, odlepené, zatéká. Zároveň nutné pro víkendovou opravu.'),
 'Hubení škůdců':                    (4, 2, 'Myš v domě nebo vosy se neřeší za tři dny.'),
 'Podpalovače, topení, zapalování':  (4, 3, 'Podpalovač a zapalovač dojdou v sobotu večer, topí se i v neděli.'),
 'Úklid a čisticí prostředky':       (3, 3, 'Došlo Savo, pytle, houbičky. Uklízí se hlavně o víkendu.'),
 'Hygiena a papírové zboží':         (4, 1, 'Došel toaletní papír. Nejbanálnější nouzový nákup.'),
 'Malířské potřeby':                 (2, 5, 'Fólie, štětce, brusivo, válečky. Kupuje se v pátek večer a v sobotu ráno před malováním.'),
 'Nátěrové hmoty (barvy na zeď)':    (2, 5, 'Malování je víkendová akce. Chybí-li barva v sobotu, projekt stojí.'),
 'Spojovací materiál':               (3, 5, 'Došly vruty nebo hmoždinky uprostřed víkendové práce. Typický dokup.'),
 'Lepicí a maskovací pásky':         (3, 5, 'Bez maskovací pásky se nedá malovat, bez izolepy dodělat oprava.'),
 'Ochranné pomůcky':                 (3, 4, 'Rukavice, brýle, respirátor k víkendové práci.'),
 'Ruční nářadí a měřidla':           (3, 4, 'Zlomená čepel, ztracený metr, chybí šroubovák.'),
 'Kabely a vodiče':                  (3, 3, 'Prodlužovačka a kabel k opravě.'),
 'Ředidla a technická chemie':       (2, 4, 'Ředidlo a líh k víkendovému natírání a čištění.'),
 'Domácnost (věšáky, šňůry, háčky)': (2, 3, 'Drobné doplňky k úklidu a zabydlení.'),
 'Semena a ochrana rostlin':         (1, 5, 'Sází se o víkendu, sezónní špička únor–květen.'),
 'Svíčky a hřbitovní zboží':         (2, 4, 'Návštěva hřbitova je nedělní a svátek (Dušičky, Vánoce), kdy je zavřeno.'),
 'Papírnictví':                      (2, 2, 'Popisovač, sáčky. Doplňkový nákup.'),
 'Stavební chemie a sádra':          (2, 4, 'Sádra k zaplácnutí díry, lepidlo na obklady.'),
}

# ks/měsíc z dat prodejny 1 (průměr obou 30denních oken); u skupin sloučených ručně
KS = {'Žárovky a světelné zdroje':142,'Baterie':389,'Vodoinstalace a hadice':420,
 'Elektroinstalační drobný materiál':328,'Lepidla, tmely, silikony, PU pěny':358,'Hubení škůdců':68,
 'Podpalovače, topení, zapalování':65,'Úklid a čisticí prostředky':314,'Hygiena a papírové zboží':101,
 'Malířské potřeby':771,'Nátěrové hmoty (barvy na zeď)':54,'Spojovací materiál':174,
 'Lepicí a maskovací pásky':256,'Ochranné pomůcky':88,'Ruční nářadí a měřidla':125,'Kabely a vodiče':300,
 'Ředidla a technická chemie':190,'Domácnost (věšáky, šňůry, háčky)':138,'Semena a ochrana rostlin':190,
 'Svíčky a hřbitovní zboží':42,'Papírnictví':82,'Stavební chemie a sádra':67}
# průměrná cena položky Kč (z dat)
CENA = {'Žárovky a světelné zdroje':52,'Baterie':23,'Vodoinstalace a hadice':49,
 'Elektroinstalační drobný materiál':50,'Lepidla, tmely, silikony, PU pěny':121,'Hubení škůdců':49,
 'Podpalovače, topení, zapalování':50,'Úklid a čisticí prostředky':67,'Hygiena a papírové zboží':33,
 'Malířské potřeby':42,'Nátěrové hmoty (barvy na zeď)':361,'Spojovací materiál':40,
 'Lepicí a maskovací pásky':53,'Ochranné pomůcky':110,'Ruční nářadí a měřidla':106,'Kabely a vodiče':33,
 'Ředidla a technická chemie':108,'Domácnost (věšáky, šňůry, háčky)':45,'Semena a ochrana rostlin':36,
 'Svíčky a hřbitovní zboží':39,'Papírnictví':40,'Stavební chemie a sádra':157}

def tabulka():
    rows=[]
    for g,(nal,vik,duvod) in SKORE.items():
        podil=min(0.60, 0.10+0.06*nal+0.04*vik)
        ks=KS[g]; cena=CENA[g]
        rows.append([g,nal,vik,round(podil,2),ks,round(ks*podil),round(ks*podil*cena/1.21),duvod])
    t=pd.DataFrame(rows,columns=['Skupina','Naléhavost','Víkend','Podíl mimo dobu','ks/měs Solnice',
        'ks/měs mimo dobu','Obrat mimo dobu Kč bez DPH','Proč'])
    return t.sort_values('Obrat mimo dobu Kč bez DPH',ascending=False)

if __name__=='__main__':
    from openpyxl import load_workbook
    from openpyxl.styles import Font, PatternFill
    t=tabulka()
    pd.set_option('display.width',250); pd.set_option('display.max_colwidth',30)
    print(t.drop(columns='Proč').to_string(index=False))
    print('\nCelkem mimo pracovní dobu: %d ks/měs, %d Kč/měs bez DPH' %
          (t['ks/měs mimo dobu'].sum(), t['Obrat mimo dobu Kč bez DPH'].sum()))
    print('Podíl z celkového prodeje těchto skupin: %.0f%%' %
          (t['ks/měs mimo dobu'].sum()/t['ks/měs Solnice'].sum()*100))
    t.to_csv('mimo_pracovni_dobu.csv',index=False)
    wb=load_workbook('sortiment_24-7_analyza.xlsx')
    if 'Mimo pracovni dobu' in wb.sheetnames: del wb['Mimo pracovni dobu']
    ws=wb.create_sheet('Mimo pracovni dobu',1)
    ws.append(['Odhad poptávky mimo otevírací dobu (Po–Pá 7–17, So 8–11). Skóre je expertní, ne z dat – účtenkový export by ho nahradil skutečností.'])
    ws['A1'].font=Font(bold=True); ws.append([])
    ws.append(list(t.columns))
    for c in ws[3]: c.font=Font(bold=True); c.fill=PatternFill('solid',fgColor='DDEBF7')
    for r in t.itertuples(index=False): ws.append(list(r))
    for col,w in zip('ABCDEFGH',(36,12,10,16,16,18,26,80)): ws.column_dimensions[col].width=w
    wb.save('sortiment_24-7_analyza.xlsx')
    print('list Mimo pracovni dobu zapsán')

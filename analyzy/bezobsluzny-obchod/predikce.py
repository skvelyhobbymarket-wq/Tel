"""Predikce obratu bezobslužné prodejny 24/7 – parametrický model.

Východisko: prodej základního sortimentu (184 položek) v Solnici = 108 289 Kč bez DPH
za měsíc v okně březen/duben (list Zakladni sortiment). Sezónní index z měsíčních
tržeb prodejny Drogerie 2023 a 1–8/2024 (Prumerny_nakup.xlsx).
Vytvoří list "Predikce" v sortiment_24-7_analyza.xlsx s živými vzorci.
"""
import numpy as np, pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L

MESICE = ['leden','únor','březen','duben','květen','červen','červenec','srpen','září','říjen','listopad','prosinec']
dro23 = [266.8,288.1,385.0,425.7,612.5,605.4,622.5,607.2,538.9,497.5,470.7,440.7]
dro24 = [318.8,354.8,424.3,499.1,579.6,558.0,685.0,625.5]
# sezónní index: průměr 2023 a 2024 (kde je), normovaný na roční průměr 2023
idx = np.array([(a+b)/2 if b else a for a,b in zip(dro23, dro24+[None]*4)])
idx = idx/np.mean(dro23)
BASE_MAR_APR = 108289.0   # Kč bez DPH/měs, okno březen/duben
idx_mar_apr = (idx[2]+idx[3])/2
BASE_AVG = BASE_MAR_APR/idx_mar_apr   # průměrný měsíc v Solnici

SCEN = {  # parametry scénářů
 'Pesimistický': dict(lokalita=0.25, uplift=1.05, ztraty=0.05, marze=0.36),
 'Realistický':  dict(lokalita=0.40, uplift=1.15, ztraty=0.03, marze=0.38),
 'Optimistický': dict(lokalita=0.60, uplift=1.25, ztraty=0.02, marze=0.40),
}
RAMP = [0.5,0.65,0.8,0.9,1,1,1,1,1,1,1,1]
NAKLADY = dict(najem=12000, energie=3000, technologie=7000, doplnovani=8000, pojisteni=1000, poplatky=0.012)
NAKLADY_ROZSIRENI = dict(najem=0, energie=1500, technologie=7000, doplnovani=3000, pojisteni=500, poplatky=0.012)

def rok(p, start_month=1, ramp=True):
    out=[]
    for m in range(12):
        mi=(start_month-1+m)%12
        obr = BASE_AVG*idx[mi]*p['lokalita']*p['uplift']*(RAMP[m] if ramp else 1)
        out.append(obr)
    return np.array(out)

if __name__=='__main__':
    fixed = sum(v for k,v in NAKLADY.items() if k!='poplatky')
    print('Sezónní index:', dict(zip(MESICE, idx.round(2))))
    print('Základ Solnice: %.0f Kč/měs (březen/duben), průměrný měsíc %.0f, rok %.0f' % (BASE_MAR_APR, BASE_AVG, BASE_AVG*12))
    print('Fixní náklady samostatné jednotky: %d Kč/měs' % fixed)
    rows=[]
    for name,p in SCEN.items():
        r1 = rok(p, start_month=4)          # start v dubnu, s rozjezdem
        r2 = rok(p, start_month=1, ramp=False)  # ustálený rok
        for lab, r in [('rok 1 (start duben)', r1), ('ustálený rok', r2)]:
            hz = r*p['marze']*(1-p['ztraty']) - r*NAKLADY['poplatky']  # hrubý zisk po ztrátách a poplatcích
            res = hz - fixed
            be = fixed/(p['marze']*(1-p['ztraty'])-NAKLADY['poplatky'])
            rows.append([name, lab, r.sum(), r.mean(), hz.sum(), res.sum(), be])
    t=pd.DataFrame(rows, columns=['Scénář','Období','Obrat/rok Kč','Obrat/měs Kč','Hrubý zisk po ztrátách/rok','Výsledek po fix. nákladech/rok','Break-even obrat/měs'])
    print(t.round(0).to_string(index=False))
    # varianta rozšíření stávající prodejny: přírůstek = uplift-1 z celého základu Solnice + noví zákazníci 10 %
    fixed2 = sum(v for k,v in NAKLADY_ROZSIRENI.items() if k!='poplatky')
    for uplift in (0.10,0.15,0.25):
        obr = BASE_AVG*12*uplift
        hz = obr*(0.38*(1-0.03)-0.012)
        print('Rozšíření Solnice 24/7: přírůstek %.0f%% -> obrat %.0f Kč/rok, hrubý zisk %.0f, po nákladech %.0f (fix %d/měs)' % (uplift*100, obr, hz, hz-fixed2*12, fixed2))

    # ---- Excel list s vzorci ----
    wb = load_workbook('sortiment_24-7_analyza.xlsx')
    if 'Predikce' in wb.sheetnames: del wb['Predikce']
    ws = wb.create_sheet('Predikce', 0)
    bold=Font(bold=True); inp=PatternFill('solid', fgColor='FFF2CC'); hdr=PatternFill('solid', fgColor='DDEBF7')
    ws['A1']='Predikce obratu bezobslužné prodejny 24/7 (Kč bez DPH). Žluté buňky = parametry k úpravě.'; ws['A1'].font=bold
    ws['A3']='Parametr'; ws['B3']='Pesimistický'; ws['C3']='Realistický'; ws['D3']='Optimistický'
    for c in 'ABCD': ws[c+'3'].font=bold; ws[c+'3'].fill=hdr
    params=[('Základ: prodej základního sortimentu v Solnici, průměrný měsíc (Kč bez DPH)', [round(BASE_AVG)]*3, 'Z listu Zakladni sortiment, 108 289 Kč v okně březen/duben, přepočteno sezónním indexem'),
            ('Faktor lokality (poptávka nového města vs. Solnice)', [0.25,0.40,0.60], 'Solnice = zavedená prodejna od 2012, 52 nákupů/den; nové město bez historie'),
            ('Uplift 24/7 (nákupy mimo běžnou otevírací dobu)', [1.05,1.15,1.25], ''),
            ('Ztráty krádežemi a šlonky (% obratu)', [0.05,0.03,0.02], ''),
            ('Obchodní marže', [0.36,0.38,0.40], 'Prodejna 1 podle exportu 38 %'),
            ('Poplatky za platby (% obratu)', [0.012,0.012,0.012], ''),
            ('Nájem Kč/měs', [12000]*3, 'samostatná jednotka; při rozšíření stávající prodejny 0'),
            ('Energie Kč/měs', [3000]*3, ''),
            ('Technologie (vstup, samoobslužná pokladna, kamery, SW) Kč/měs', [7000]*3, 'amortizace + licence'),
            ('Doplňování zboží a úklid Kč/měs', [8000]*3, ''),
            ('Pojištění Kč/měs', [1000]*3, '')]
    for i,(n,v,note) in enumerate(params, start=4):
        ws.cell(i,1,n); 
        for j,x in enumerate(v): c=ws.cell(i,2+j,x); c.fill=inp
        ws.cell(i,5,note)
    # rows: 4 base,5 lok,6 uplift,7 ztraty,8 marze,9 poplatky,10..14 naklady
    ws['A16']='Sezónní index (tržby Drogerie 2023–24)'; ws['A16'].font=bold
    ws['A17']='Měsíc'; ws['B17']='Index'; ws['C17']='Rozjezd rok 1'
    for c in 'ABC': ws[c+'17'].font=bold; ws[c+'17'].fill=hdr
    for m in range(12):
        ws.cell(18+m,1,MESICE[m]); ws.cell(18+m,2,round(float(idx[m]),3)); c=ws.cell(18+m,3,RAMP[m]); c.fill=inp
    ws['E17']='Rozjezd: podíl plného prodeje v 1.–12. měsíci provozu (počítá se od ledna; start v jiném měsíci = posunout hodnoty)'
    # scenario tables
    r0=31
    ws.cell(r0,1,'Měsíční predikce – ustálený rok (bez rozjezdu)').font=bold
    ws.cell(r0+1,1,'Měsíc')
    cols=[('Obrat','P'),('Hrubý zisk po ztrátách a poplatcích','Z'),('Výsledek po fixních nákladech','V')]
    col=2
    for s,scol in zip(['Pesimistický','Realistický','Optimistický'],'BCD'):
        for cn,_ in cols:
            ws.cell(r0+1,col,f'{s} – {cn}').font=bold; ws.cell(r0+1,col).fill=hdr; col+=1
    for m in range(12):
        r=r0+2+m; ws.cell(r,1,MESICE[m]); col=2
        for scol in 'BCD':
            obr=f'={scol}$4*$B{18+m}*{scol}$5*{scol}$6'
            ws.cell(r,col,obr); 
            ws.cell(r,col+1,f'={L(col)}{r}*({scol}$8*(1-{scol}$7)-{scol}$9)')
            ws.cell(r,col+2,f'={L(col+1)}{r}-SUM({scol}$10:{scol}$14)')
            col+=3
    r=r0+14; ws.cell(r,1,'Celkem rok').font=bold
    for c in range(2,11): ws.cell(r,c,f'=SUM({L(c)}{r0+2}:{L(c)}{r0+13})').font=bold
    r=r0+15; ws.cell(r,1,'Break-even obrat/měs')
    for i,scol in enumerate('BCD'): ws.cell(r,2+3*i,f'=SUM({scol}10:{scol}14)/({scol}8*(1-{scol}7)-{scol}9)')
    # year 1 with ramp
    r1=r0+18
    ws.cell(r1,1,'Rok 1 s rozjezdem (start v lednu; pro start v dubnu posuňte sloupec C17:C29)').font=bold
    ws.cell(r1+1,1,'Měsíc')
    col=2
    for s in ['Pesimistický','Realistický','Optimistický']:
        for cn,_ in cols: ws.cell(r1+1,col,f'{s} – {cn}').font=bold; ws.cell(r1+1,col).fill=hdr; col+=1
    for m in range(12):
        r=r1+2+m; ws.cell(r,1,MESICE[m]); col=2
        for scol in 'BCD':
            ws.cell(r,col,f'={scol}$4*$B{18+m}*$C{18+m}*{scol}$5*{scol}$6')
            ws.cell(r,col+1,f'={L(col)}{r}*({scol}$8*(1-{scol}$7)-{scol}$9)')
            ws.cell(r,col+2,f'={L(col+1)}{r}-SUM({scol}$10:{scol}$14)')
            col+=3
    r=r1+14; ws.cell(r,1,'Celkem rok 1').font=bold
    for c in range(2,11): ws.cell(r,c,f'=SUM({L(c)}{r1+2}:{L(c)}{r1+13})').font=bold
    # number formats & widths
    for row in ws.iter_rows(min_row=r0+2, max_row=r1+14, min_col=2, max_col=10):
        for c in row: c.number_format='#,##0'
    for rr in (4,10,11,12,13,14):
        for c in 'BCD': ws[f'{c}{rr}'].number_format='#,##0'
    for rr in (7,8,9):
        for c in 'BCD': ws[f'{c}{rr}'].number_format='0.0%'
    ws.column_dimensions['A'].width=62
    for c in range(2,11): ws.column_dimensions[L(c)].width=22
    ws.column_dimensions['E'].width=22
    wb.save('sortiment_24-7_analyza.xlsx')
    print('list Predikce zapsán')

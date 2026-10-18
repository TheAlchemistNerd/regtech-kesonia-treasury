"""Build named Python charts and synchronize the Deposit Beta publication."""
from pathlib import Path
import csv,json,re,hashlib,math,textwrap
from PIL import Image,ImageDraw,ImageFont
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/deposit_beta_dynamic_case_2026-10-18'
PUB=ROOT/'publications/linkedin'
CHARTS=PUB/'deposit_beta_diagrams'
ARTICLE=PUB/'Deposit_Beta_KESONIA_and_Bank_Risk_2026-10-16.md'
SUM=json.loads((OUT/'scenario_summary.json').read_text())
S={(r['scenario'],r['policy']):r for r in SUM}
CFG=json.loads((OUT/'assumptions.json').read_text())
ROWS={}
for r in SUM:
    key=(r['scenario'],r['policy'])
    with (OUT/f'{key[0]}__{key[1]}'/'monthly.csv').open() as f:
        ROWS[key]=[{k:float(v) if k not in ('scenario','policy','start','end') else v for k,v in row.items()} for row in csv.DictReader(f)]
W,H=1800,1120
NAVY='#152F49';TEAL='#007C91';ORANGE='#B66309';RED='#AA3546';PURPLE='#725AA5';GREY='#52606D';LIGHT='#DAE2E8'
FONT=Path('C:/Windows/Fonts/arial.ttf');BOLD=Path('C:/Windows/Fonts/arialbd.ttf')
def font(n,bold=False):return ImageFont.truetype(str(BOLD if bold else FONT),n)
def canvas(title,subtitle):
    im=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(im)
    d.text((85,45),title,font=font(43,True),fill=NAVY)
    d.text((85,107),subtitle,font=font(25),fill=GREY)
    d.text((85,H-68),'Synthetic expected-cohort case | KES | 24 months | reproducible Python and CSV records',font=font(22),fill=GREY)
    return im,d

def plot(title,subtitle,series,ylabel,filename,zero=True,percent=False):
    im,d=canvas(title,subtitle);l,t,r,b=130,320,W-95,H-150
    values=[v for _,_,v in series];lo=min(min(v) for v in values);hi=max(max(v) for v in values)
    if zero:lo=min(lo,0)
    span=hi-lo or 1;lo=lo-span*.06 if lo<0 else 0;hi+=span*.12
    def point(i,v):return (l+i*(r-l)/23,b-(v-lo)/(hi-lo)*(b-t))
    for j in range(6):
        v=lo+(hi-lo)*j/5;y=point(0,v)[1]
        d.line((l,y,r,y),fill=LIGHT,width=2)
        label=f'{v:.1f}'
        d.text((l-18-d.textlength(label,font=font(23)),y-12),label,font=font(23),fill=GREY)
    for i in (0,2,5,8,11,14,17,20,23):
        x=point(i,0)[0];d.text((x-12,b+18),str(i+1),font=font(23),fill=GREY)
    d.text((l,t-42),ylabel,font=font(25,True),fill=NAVY)
    d.text(((l+r)/2-50,b+60),'Month',font=font(25),fill=GREY)
    for idx,(name,color,vs) in enumerate(series):
        x=100+(idx%3)*560;y=168+(idx//3)*50
        d.line((x,y+13,x+50,y+13),fill=color,width=6);d.text((x+63,y),name,font=font(24),fill=NAVY)
        pts=[point(i,v) for i,v in enumerate(vs)];d.line(pts,fill=color,width=6)
        for x,y in pts:d.ellipse((x-4,y-4,x+4,y+4),fill=color)
    im.save(CHARTS/filename)

J=ROWS['joint_stress','standard'];B=ROWS['baseline','standard']
with (OUT/'joint_stress__standard/loans.csv').open() as f:
    loan_details=[{k:(float(v) if k in ('month','opening','loan_rate') else v) for k,v in row.items()} for row in csv.DictReader(f)]
loan_coupons=[sum(x['opening']*x['loan_rate'] for x in loan_details if x['month']==m)/sum(x['opening'] for x in loan_details if x['month']==m)*100 for m in range(1,25)]
plot('Market rates reach assets and liabilities at different speeds','Joint stress begins in month 3; deposits include a delayed response and fixed term cohorts',[
    ('Market benchmark',NAVY,[r['market_rate']*100 for r in J]),
    ('Savings offer',TEAL,[r['savings_rate']*100 for r in J]),
    ('Operating account offer',ORANGE,[r['operating_rate']*100 for r in J]),
    ('New term deposit offer',PURPLE,[r['term_offer']*100 for r in J]),
    ('Weighted loan coupon',RED,loan_coupons)
],'Annual rate (%)','03_MONTHLY_RATE_TRANSMISSION.png')
plot('Loan collections and deposit runoff reshape the funding requirement','Joint stress: amortising loans, continued new lending and wholesale replacement',[
    ('Performing loans',NAVY,[r['gross_loans']/1e6 for r in J]),
    ('Deposits',TEAL,[r['deposits']/1e6 for r in J]),
    ('Wholesale funding',ORANGE,[r['wholesale']/1e6 for r in J]),
    ('Original deposit cohort',PURPLE,[r['original_deposits_remaining']/1e6 for r in J])], 'KES million','04_DEPOSITS_LOANS_AND_FUNDING.png')
plot('The credit allowance changes the earnings interpretation','Joint stress: a forward-looking allowance increase is recognised when conditions deteriorate',[
    ('Net interest income',TEAL,[r['nii']/1e6 for r in J]),
    ('Impairment expense',ORANGE,[r['impairment_expense']/1e6 for r in J]),
    ('Profit after operating costs',NAVY,[r['profit']/1e6 for r in J])], 'KES million per month','05_NII_CREDIT_COST_AND_PROFIT.png')
plot('Equity and cash answer different questions','Equity absorbs earnings and allowance changes; Treasury maintains the KES 6 million cash floor',[
    ('Baseline equity',NAVY,[r['equity']/1e6 for r in B]),
    ('Joint stress equity',ORANGE,[r['equity']/1e6 for r in J]),
    ('Baseline cash',TEAL,[r['cash']/1e6 for r in B]),
    ('Joint stress cash',PURPLE,[r['cash']/1e6 for r in J])], 'KES million','07_EQUITY_AND_CASH_RECONCILIATION.png')
# Horizontal bars carry lending output beside profit so lower volume remains visible.
im,d=canvas('ALCO alternatives have different economic trade-offs','The same joint shock is applied to four pre-specified management policies')
policies=[('standard','Maintain current policy'),('retain_deposits','Savings offer +50 bp'),('term_prefunding','KES 10m term prefunding'),('controlled_growth','Retention and lower lending')]
maxp=max(S['joint_stress',p]['profit'] for p,_ in policies)/1e6
for i,(p,name) in enumerate(policies):
    r=S['joint_stress',p];y=245+i*170
    d.text((85,y),name,font=font(29,True),fill=NAVY)
    val=r['profit']/1e6;x=630;end=x+val/maxp*690
    d.rectangle((x,y-3,end,y+53),fill=[NAVY,TEAL,ORANGE,PURPLE][i])
    d.text((end+18,y+4),f'{val:.3f}m profit',font=font(27,True),fill=NAVY)
    d.text((85,y+67),f"New loans KES {r['originations']/1e6:.0f}m   |   Peak wholesale KES {r['peak_wholesale']/1e6:.2f}m   |   Minimum capital proxy {r['minimum_capital_proxy']*100:.2f}%",font=font(25),fill=GREY)
d.text((85,965),'Capital proxy: equity / (performing principal + gross workout claims); teaching threshold 12%.',font=font(24),fill=GREY)
im.save(CHARTS/'06_ALCO_POLICY_COMPARISON.png')
# Explicit process and accounting links for a presentation walkthrough.
im,d=canvas('One monthly ledger connects behaviour to a bank decision','Each dated record preserves inputs, contract terms, transitions, cash and the accounting reconciliation')
boxes=[
 (85,200,540,360,'1  Shared scenario',['Benchmark path and calendar','Borrower cash and macro shock','Deposit runoff and new inflows']),
 (670,200,1125,360,'2  Contract and behaviour',['Compounded reference and resets','Deposit offers and term renewals','Migration and external withdrawals']),
 (1255,200,1710,360,'3  Borrower outcomes',['Debt service and cash coverage','Conditional default probability','Amortisation and workout transfer']),
 (1255,485,1710,660,'4  Cash and funding',['Interest cash and principal receipts','Dated recoveries and loan advances','Wholesale maturities and replacement']),
 (670,485,1125,660,'5  Earnings and balance sheet',['NII and operating costs','Allowance roll and retained earnings','Assets = liabilities + equity']),
 (85,485,540,660,'6  Feasible ALCO choices',['Cash floor and funding headroom','Capital capacity and lending volume','Approved retention or term funding']),
 (330,805,1460,970,'7  Next month and independent verification',['Carry all closing balances and contract states into the next period','Reconstruct cash, allowance, principal and equity from their own records','Compare policies under the same scenario and inspect residuals'])]
for l,t,r,b,title,lines in boxes:
    d.rounded_rectangle((l,t,r,b),radius=8,outline=NAVY,width=3,fill='#F6F8FA')
    d.text((l+18,t+17),title,font=font(27,True),fill=NAVY)
    for j,line in enumerate(lines):d.text((l+18,t+65+j*28),line,font=font(21 if r-l<500 else 24),fill=NAVY)
def arrow(a,b):
    d.line((*a,*b),fill=TEAL,width=6);ang=math.atan2(b[1]-a[1],b[0]-a[0]);n=17
    pts=[b,(b[0]-n*math.cos(ang-.45),b[1]-n*math.sin(ang-.45)),(b[0]-n*math.cos(ang+.45),b[1]-n*math.sin(ang+.45))];d.polygon(pts,fill=TEAL)
for a,b in [((540,280),(670,280)),((1125,280),(1255,280)),((1480,360),(1480,485)),((1255,570),(1125,570)),((670,570),(540,570)),((310,660),(310,740)),((310,740),(900,740)),((900,740),(900,805))]:arrow(a,b)
im.save(CHARTS/'08_LINKED_BANK_CASE_FLOW.png')

# Preserve the complete existing article; replace only this bounded generated insert on rerun.
s=ARTICLE.read_text(encoding='utf-8')
s=s.replace('Its training error rises materially when the invented future repricing regime changes.','Its frozen model produces a materially larger error on the future holdout when the invented repricing regime changes.')
s=re.sub(r'\n<!-- DYNAMIC CASE START -->.*?<!-- DYNAMIC CASE END -->\n','\n',s,flags=re.S)
b=S['baseline','standard'];j=S['joint_stress','standard'];u=S['rates_up','standard'];c=S['joint_stress','controlled_growth'];t=S['joint_stress','term_prefunding'];ret=S['joint_stress','retain_deposits']
insert=f'''
<!-- DYNAMIC CASE START -->
## A reproducible monthly loan deposit and funding case

The annual bridge above is now an independently tested limiting example within a larger research package. A new 24-month case starts in January 2027 with KES 100 million of performing loans, KES 80 million of deposits, KES 10 million of wholesale funding and KES 6 million of cash. A KES {b['opening_allowance']/1e6:.3f} million opening management allowance leaves KES {b['opening_equity']/1e6:.3f} million of opening equity. Each subsequent month reconciles assets, liabilities and equity. The scenario amounts describe an invented bank and make the funding mechanism reproducible. The borrower interpretation builds on *Underwrite for Collection*, especially its treatment of cash provenance, contractual payment obligations, expected loss and funding over a facility's life. [13]

Three opening loan cohorts amortise over 36, 24 and 18 months. Their illustrative coupon-reset frequencies are one, three and six months. New lending is proposed at KES 5 million a month and is admitted through explicit cash, funding and capital-capacity tests. Operating accounts, savings and term deposits have different price and withdrawal behaviour. Savings can move into the bank's term product, preserving bank funding while changing its cost. External withdrawals leave the bank. Newly acquired deposits carry their own identifiers, so they can never replenish the original-cohort retention measure.

![Rates and deposit offers through the joint stress](deposit_beta_diagrams/03_MONTHLY_RATE_TRANSMISSION.png)

Figure 3. Market-rate changes reach deposit products at different speeds. Existing term cohorts retain their contracted rate until renewal; the chart's term rate is the offer for newly placed or renewing money.

The simulator reuses the repository's existing segmented asymmetric-lag estimates and dated compounding functions. It then adds the missing connections: loan amortisation, contract resets, deposit cohort migration, external runoff, wholesale maturity, replacement funding, borrower coverage, default transfers and delayed recovery. A rate increase changes scheduled debt service; a separate operating shock changes estimated cash available for debt service. Their ratio feeds an explicitly assumed default-risk relationship. Expected collections follow the surviving loan cohorts. This is a deterministic expected-cash path: the full merchant operating-ledger applications in Underwrite provide the deeper borrower-level implementation. [13]

The central accounting check is:

Cash + performing principal + gross workout claims + interest receivable − allowance = deposits + wholesale funding + equity.

Loan interest is accrued this month and collected next month. Expected default principal moves into a separate workout balance. Three months later, 55% is recovered and 45% is written off. The allowance roll is equally explicit:

Credit expenseₜ = allowanceₜ − allowanceₜ₋₁ + writeoffsₜ.

This identity makes the distinction between an expense, a principal write-off and a cash recovery visible. The case's allowance is an undiscounted 12-month expected-principal-loss approximation; the IFRS 9 measurement framework supplies the institutional accounting specification when this research is extended to bank records. [12]

![Loans deposits and wholesale funding through the joint stress](deposit_beta_diagrams/04_DEPOSITS_LOANS_AND_FUNDING.png)

Figure 4. A smaller performing book can coexist with sustained funding pressure. Collections, new lending, deposit withdrawals and recoveries all have different dates.

Across the 24 months, the baseline produces KES {b['nii']/1e6:.3f} million of NII and KES {b['profit']/1e6:.3f} million of profit after the modelled operating and credit costs. A 200-basis-point increase on its own produces KES {u['profit']/1e6:.3f} million of profit. Combine that increase with additional deposit runoff, weaker deposit acquisition and a 25% borrower cash shock, however, and NII becomes KES {j['nii']/1e6:.3f} million while profit becomes KES {j['profit']/1e6:.3f} million. The joint scenario generates KES {j['impairment_expense']/1e6:.3f} million of credit expense, versus KES {b['impairment_expense']/1e6:.3f} million in the baseline. A large allowance increase appears immediately when the changed outlook is recognised; cash recoveries arrive later.

![NII credit expense and profit in the joint stress](deposit_beta_diagrams/05_NII_CREDIT_COST_AND_PROFIT.png)

Figure 5. Positive monthly NII can coexist with a loss when the expected-loss outlook changes. The cash ledger separately records when the underlying payments and recoveries settle.

Management choices now have a common comparison basis. A 50-basis-point savings premium retains more money under the assumed response but reduces joint-stress profit to KES {ret['profit']/1e6:.3f} million. Pre-specified KES 10 million term prefunding produces KES {t['profit']/1e6:.3f} million. Combining retention with term funding and a lower lending plan produces KES {c['profit']/1e6:.3f} million, alongside KES {c['originations']/1e6:.0f} million of new lending compared with KES {j['originations']/1e6:.0f} million under the standard plan. Volume is part of that result. The term-funding comparison evaluates a stated decision made in month two; it demonstrates a policy trade-off under a scenario. Article 4 of the five-article research series develops the wider stochastic-control and ALCO framework, and Article 5 explains how registered computation, approval and execution records fit into a bank-controlled workflow. [14], [15]

![ALCO policy comparison showing profit lending and funding together](deposit_beta_diagrams/06_ALCO_POLICY_COMPARISON.png)

Figure 6. The same joint shock is used across the four policies. Profit, new lending, funding needs and minimum capital headroom are shown together.

Every main scenario maintains the KES 6 million teaching cash floor and the 12% internal capital proxy. Separate tests tighten the funding and capital constraints and verify that proposed lending is curtailed. Nine additional sensitivity runs vary repricing coefficients and runoff assumptions; their range is a scenario sensitivity, with Bayesian posterior uncertainty remaining a bank-data estimation step. The package includes 21 passing tests, monthly loan and deposit records, scenario summaries and SHA-256 hashes. The complete case narrative explains each formula, cash convention and result; readers can rerun the calculation from the repository. [16]

The cash and equity paths provide another useful explanation. At month 24, the baseline holds KES {b['closing_cash']/1e6:.3f} million of cash and KES {b['closing_equity']/1e6:.3f} million of equity. Joint stress leaves KES {j['closing_cash']/1e6:.3f} million of cash and KES {j['closing_equity']/1e6:.3f} million of equity. Baseline cash builds because scheduled collections eventually exceed the fixed new-lending plan and other payments; surplus cash earns the specified 3% yield. ALCO could compare reinvestment or different lending plans using the same ledger. Equity instead accumulates earnings after credit expense. Reading these curves together prevents a cash balance from being mistaken for profit or capital capacity.

![Cash and equity through baseline and joint stress](deposit_beta_diagrams/07_EQUITY_AND_CASH_RECONCILIATION.png)

Figure 7. Monthly cash and equity have distinct drivers. The baseline's later cash build reflects amortisation and the stated lending plan, while the joint case continues to rely on replacement funding to meet its floor.

The complete flow chart shows the order in which these connections enter the calculation. A shared market and business scenario reaches contract pricing and customer behaviour. Borrower outcomes generate principal, interest and workout records; those dates then determine Treasury's cash requirement. Accounting carries the same evidence into earnings and equity. Finally, the policy checks determine feasible new lending and the next month's opening state. A reviewer can follow this sequence in the CSV records, and a bank-controlled workflow can attach source versions, the committee decision and an execution receipt to the relevant transition. This is the point at which a reproducible research case becomes a concrete specification for a governed decision-support service. [15]

![The complete monthly bank scenario workflow](deposit_beta_diagrams/08_LINKED_BANK_CASE_FLOW.png)

Figure 8. The linked calculation runs from scenario assumptions to closing balances and the next decision. Each stage exposes its input, economic meaning and reconciliation record.
<!-- DYNAMIC CASE END -->
'''
s=s.replace('## 10. Connect credit risk through cash flows',insert+'\n## 10. Connect credit risk through cash flows')
# Append new bibliography once, then make numbering follow first use in the article body.
refs_extra='''
[13] N. Maloba, *Underwrite for Collection*, integrated research edition, 2026, especially Parts 2 and 5. doi: 10.5281/zenodo.23343888. [Online]. Available: https://doi.org/10.5281/zenodo.23343888

[14] N. Maloba, "Can Reinforcement Learning Help Run a Bank's Balance Sheet?", Article 4 in *Causal Credit and Treasury Decision-Making*, 2026. [Online]. Available: https://github.com/TheAlchemistNerd/underwrite-for-collection/blob/main/series/publications/linkedin/2026-10-08_causal_credit_series/ARTICLE_4_TREASURY_ALM_STOCHASTIC_CONTROL.md

[15] N. Maloba, "Bringing the Methods into the Bank", Article 5 in *Causal Credit and Treasury Decision-Making*, 2026. [Online]. Available: https://github.com/TheAlchemistNerd/underwrite-for-collection/blob/main/series/publications/linkedin/2026-10-08_causal_credit_series/ARTICLE_5_BANK_CONTROLLED_AGENTIC_AI_CREDIT_AND_TREASURY.md

[16] N. Maloba, "Deposit Beta Dynamic Loan Deposit and Funding Case", RegTech KESONIA research laboratory, Oct. 18, 2026. [Online]. Available: https://github.com/TheAlchemistNerd/regtech-kesonia-treasury/tree/codex/kesonia-reviewed-reference-lab/research_lab/deposit_beta_dynamic_case
'''
# An immutable local source is used only for deterministic rebuilds of this article.
base=Path(__file__).resolve().parent/'article_source_before_dynamic_update.md'
if not base.exists():base.write_text(ARTICLE.read_text(encoding='utf-8'),encoding='utf-8')
# References are regenerated from original source to make repeated builds idempotent.
original=base.read_text(encoding='utf-8')
original_body,original_refs=original.split('## References',1)
original_body=original_body.replace('Its training error rises materially when the invented future repricing regime changes.','Its frozen model produces a materially larger error on the future holdout when the invented repricing regime changes.')
s=original_body.replace('## 10. Connect credit risk through cash flows',insert+'\n## 10. Connect credit risk through cash flows')+'## References'+original_refs+refs_extra
body,refs=s.split('## References',1)
refmap={int(n):txt.strip() for n,txt in re.findall(r'(?ms)^\[(\d+)\]\s+(.*?)(?=^\[\d+\]|\Z)',refs)}
# Remove access note from the last original reference before reconstructing.
for k in refmap:refmap[k]=re.sub(r'\nAll online sources accessed.*','',refmap[k],flags=re.S).strip()
order=[]
for x in re.findall(r'\[(\d+)\]',body):
    if int(x) not in order:order.append(int(x))
renumber={n:i+1 for i,n in enumerate(order)}
body=re.sub(r'\[(\d+)\]',lambda m:f'[{renumber[int(m.group(1))]}]',body)
count=len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b",body.split('<!-- ARTICLE BODY START -->')[1].split('<!-- ARTICLE BODY END -->')[0]))
body=re.sub(r'^\*\*Editorial metadata:\*\*.*',f'**Editorial metadata:** Updated 18 October 2026. Article body approximately {count:,} words including headings, captions and equations. Includes the complete original discussion and a reproducible monthly case.',body,count=1)
s=body+'## References\n\n'+'\n\n'.join(f'[{renumber[n]}] {refmap[n]}' for n in order)+'\n\nSources rechecked for the dynamic case on 18 October 2026.\n'
ARTICLE.write_text(s,encoding='utf-8')

# Unicode Word: visible equations are ordinary editable text, with live links and embedded figures.
def link(p,label,url):
    part=p.part;rid=part.relate_to(url,'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',is_external=True)
    h=OxmlElement('w:hyperlink');h.set(qn('r:id'),rid);run=OxmlElement('w:r');pr=OxmlElement('w:rPr')
    color=OxmlElement('w:color');color.set(qn('w:val'),'0563C1');pr.append(color);run.append(pr);txt=OxmlElement('w:t');txt.text=label;run.append(txt);h.append(run);p._p.append(h)
def rich(p,text):
    pattern=re.compile(r'\[([^\]]+)\]\(([^)]+)\)|\*\*([^*]+)\*\*|\*([^*]+)\*')
    start=0
    for m in pattern.finditer(text):
        if m.start()>start:p.add_run(text[start:m.start()])
        if m.group(1):link(p,m.group(1),m.group(2))
        elif m.group(3):p.add_run(m.group(3)).bold=True
        else:p.add_run(m.group(4)).italic=True
        start=m.end()
    p.add_run(text[start:])

def build_word(text,path):
    doc=Document();sec=doc.sections[0]
    sec.page_width=Inches(8.27);sec.page_height=Inches(11.69)
    sec.top_margin=sec.bottom_margin=Inches(.65);sec.left_margin=sec.right_margin=Inches(.72)
    for name in ('Normal','Title','Heading 1','Heading 2','Heading 3','Caption'):
        st=doc.styles[name];st.font.name='Arial';st.font.color.rgb=RGBColor(0,0,0)
        st.element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'Arial')
    doc.styles['Normal'].font.size=Pt(11)
    doc.styles['Normal'].paragraph_format.space_after=Pt(7)
    doc.styles['Normal'].paragraph_format.line_spacing=1.1
    doc.styles['Title'].font.size=Pt(23);doc.styles['Title'].paragraph_format.space_after=Pt(10)
    doc.styles['Heading 1'].font.size=Pt(15);doc.styles['Heading 2'].font.size=Pt(13)
    doc.styles['Caption'].font.size=Pt(9.5)
    for border in doc.styles.element.xpath('.//w:pBdr'):
        border.getparent().remove(border)
    text=re.sub(r'<!--.*?-->','',text,flags=re.S)
    for block in text.split('\n\n'):
        block=block.strip()
        if not block or block.startswith('<!--') or block.startswith('**Editorial metadata:'):continue
        if block.startswith('# '):doc.add_paragraph(block[2:],'Title');continue
        if block.startswith('## '):doc.add_paragraph(block[3:],'Heading 1');continue
        if block.startswith('### '):doc.add_paragraph(block[4:],'Heading 2');continue
        m=re.match(r'!\[([^\]]*)\]\(([^)]+)\)',block)
        if m:
            p=doc.add_paragraph();p.paragraph_format.keep_with_next=True
            p.add_run().add_picture(str(PUB/m.group(2)),width=Inches(6.6))
            drawing=p._p.xpath('.//wp:docPr')
            if drawing:drawing[0].set('descr',m.group(1))
            continue
        if re.match(r'\d+\. ',block):
            for line in block.splitlines():
                if line.strip():rich(doc.add_paragraph(),line)
        else:rich(doc.add_paragraph(style='Caption' if block.startswith('Figure ') else None),block.replace('\n',' '))
    sec.footer.paragraphs[0].alignment=WD_ALIGN_PARAGRAPH.CENTER
    field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');sec.footer.paragraphs[0]._p.append(field)
    doc.core_properties.title='Deposit Beta KESONIA and the Economics of a Resilient Bank'
    doc.core_properties.author='Nevil Maloba'
    doc.save(path)
build_word(s,ARTICLE.with_suffix('.docx'))

post=f'''Deposit Beta, KESONIA and Bank Risk

How does a change in market rates travel through a bank's deposits, loans and lending decisions?

The answer is now backed by a reproducible 24-month synthetic case in RegTech KESONIA. It connects deposit repricing and product migration with external withdrawals, loan resets, borrower debt service, expected defaults, delayed recovery and replacement funding. Every month reconciles cash and the balance sheet.

Three questions guide the case:

1. When does slower deposit repricing improve earnings, and when do withdrawals make that funding advantage expensive?
2. How do higher loan payments and weaker borrower cash flows change collections, credit costs and capital headroom?
3. Which ALCO response preserves an acceptable combination of funding, profitability and lending capacity?

Starting with KES 100m of loans, the baseline produces KES {b['profit']/1e6:.2f}m of modelled profit over 24 months. A 200-basis-point increase alone produces KES {u['profit']/1e6:.2f}m. Combining it with runoff and borrower stress reduces profit to KES {j['profit']/1e6:.2f}m.

The comparison also shows the cost of action. Paying more for savings retains funding but reduces profit under these assumptions. Term prefunding changes refinancing exposure. Lower planned lending improves the joint-stress outcome while delivering KES 90m of new credit rather than KES 120m. Both results belong in the decision.

The article builds on Underwrite for Collection's borrower cash-flow and funding framework, and the five-article series on causal credit, Treasury control and bank-controlled workflows.

Whitepaper: https://doi.org/10.5281/zenodo.23343888

The accompanying code, named charts, monthly records and 21 tests make the assumptions and calculations open to inspection. These are synthetic research scenarios for a practical bank-data study.

#KESONIA #Banking #Treasury #CreditRisk #ALM #FinancialModelling'''
assert len(post)<=2000,len(post)
(PUB/'Deposit_Beta_Companion_Post_2026-10-16.md').write_text(post+'\n',encoding='utf-8')
write={'article_words_approx':count,'post_characters':len(post),'chart_files':[p.name for p in sorted(CHARTS.glob('0[3-8]_*.png'))],
       'article_sha256':hashlib.sha256(ARTICLE.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(ARTICLE.with_suffix('.docx').read_bytes()).hexdigest(),
       'reference_order':[renumber[n] for n in order]}
(OUT/'publication_manifest.json').write_text(json.dumps(write,indent=2)+'\n',encoding='utf-8')
print(json.dumps(write,indent=2))

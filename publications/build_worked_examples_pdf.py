#!/usr/bin/env python3
"""Build the existing nine-chapter casebook with Pandoc and native XeLaTeX math.
Research source Markdown is read-only; the PDF is replaced after compilation.
"""
from __future__ import annotations
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EDITION = '2026-10-01'
SOURCES = ['WORKED_EXAMPLES.md', 'OPERATIONS_METHODOLOGY.md', 'SYMBOLS_AND_UNITS.md',
    'LIFECYCLE_WORKED_CASES.md', 'OPTION_AND_COLLATERAL_CASES.md', 'REGULATORY_WORKED_CASES.md',
    'ACCOUNTING_AND_CONNECTED_CASES.md', 'REVIEW_INTEGRATION_AND_REMAINING_WORK.md', 'SOKOINTEL_CANDIDATE_MAP.md']
TITLES = ['Part I. Original worked examples', 'Part II. Funding, deposits and processing',
    'Part III. Symbols and units', 'Part IV. Contract and execution lifecycle',
    'Part V. Options, hedges and collateral', 'Part VI. Liquidity and capital components',
    'Part VII. Accounting and connected finance', 'Part VIII. Implementation and remaining work',
    'Part IX. SokoIntel candidates']
GITHUB = 'https://github.com/TheAlchemistNerd/regtech-kesonia-treasury/blob/main/'
MATH_CODES = {
 'H_D = drawn x days / 365': r'H_D=\mathrm{drawn}\times\mathrm{days}/365',
 'H_U = (limit - drawn) x days / 365': r'H_U=(\mathrm{limit}-\mathrm{drawn})\times\mathrm{days}/365',
 'H_D x customer rate + H_U x customer commitment fee': r'H_D r_{\mathrm{customer}}+H_U f_{\mathrm{customer}}',
 'H_D x drawn FTP rate': r'H_D r_{\mathrm{FTP}}',
 'H_U x internal liquidity rate': r'H_U r_{\mathrm{liquidity}}',
 'H_D x external drawn rate + H_U x external commitment cost rate': r'H_D r_{\mathrm{external}}+H_U f_{\mathrm{external}}',
 "(X'X)^-1 X'y": r'(X^{\mathsf T}X)^{-1}X^{\mathsf T}y',
 'original-cohort closing = original-cohort opening - bank withdrawals - same-bank product migration': r'C_{t+1}=C_t-W_t-M_t',
 'original-product closing = original-product opening + new inflow - cohort withdrawals - cohort migration': r'B_{t+1}=B_t+I_t-W_t-M_t',
}
MATH_CODES.update({'sqrt(x)':r'\sqrt{x}','ln(x)':r'\ln(x)','log(x)':r'\log(x)','exp(x)':r'\exp(x)',
 'max(x, 0)':r'\max(x,0)','min(x, 0)':r'\min(x,0)','x^2':'x^2','x^-1':'x^{-1}',
 '10^-8':'10^{-8}','10^-20':'10^{-20}'})
LONG_DEPOSIT = 'change_in_paid_rate = intercept + b_up x max(market_change,0) + b_down x min(market_change,0) + lag_up x max(previous_market_change,0) + lag_down x min(previous_market_change,0) + error'
SYMBOLS = {'P','G','B','H','N','T','PV','EC','H_D','H_U','r_i','n_i','I_benchmark','I_margin',
 'D_n','D_j','D(t)','q_1','c_n','t_j','D_P(t)','D_D(t)','f_j','C_fund','C_op','EL_principal','C_cap',
 'Fee','tau','X',"X'",'b_up','b_down','lag_up','lag_down'}

def symbol_tex(s):
 if s in ('D_P(t)','D_D(t)'):return 'D_{'+s[2]+'}(t)'
 if s=='tau': return r'\tau'
 if s=="X'": return r'X^{\mathsf T}'
 if '_' in s:
  a,b=s.split('_',1)
  return a+'_{'+(r'\mathrm{'+b+'}' if len(b)>1 else b)+'}'
 if s in ('PV','EC','Fee'): return r'\mathrm{'+s+'}'
 return s

def run(args, *, text=None, cwd=None):
 p=subprocess.run([str(a) for a in args],input=text,text=True,encoding='utf-8',errors='replace',
                  capture_output=True,cwd=cwd,timeout=240)
 if p.returncode:
  raise RuntimeError('Command failed: '+' '.join(map(str,args))+'\n'+p.stdout[-3500:]+'\n'+p.stderr[-3500:])
 return p.stdout

def tool(name, fallback):
 found=shutil.which(name)
 if found:return found
 p=Path(fallback).expanduser()
 if p.exists():return str(p)
 raise FileNotFoundError(name+' is required')

def math_node(s, display=False):
 return {'t':'Math','c':[{'t':'DisplayMath' if display else 'InlineMath'},s]}

def prepare(text,name):
 text=text.replace('| A |','| $A$ |')
 text=text.replace('about -2.22 × 10^-16',r'about $-2.22\times10^{-16}$')
 text=text.replace('sum((residual PV01/1000)^2) + 0.001 × cost/1000',r'$\sum_j(\mathrm{residual\ PV01}_j/1000)^2+0.001\,\mathrm{cost}/1000$')
 if name=='SYMBOLS_AND_UNITS.md':
  text=text.replace("| (X'X)^-1 X'y |",r'| $(X^{\mathsf T}X)^{-1}X^{\mathsf T}y$ |')
  text=text.replace("(X'X)^-1.",r'$(X^{\mathsf T}X)^{-1}$.')
 text=text.replace('\u2011','-').replace('\u2212','-')
 text=text.replace('\x15\x15','sections ').replace('\x15','section ').replace('\x1a',r' -> ')
 text=text.replace('calculations \ufffd reviewed','calculations - reviewed').replace('central \ufffd1 bp','central $\\pm1$ bp')
 text=text.replace('2.22x10?16',r'$2.22\times10^{-16}$')
 text=text.replace('about -2.22 x 10^-16',r'about $-2.22\times10^{-16}$')
 text=text.replace('10^-8 currency',r'$10^{-8}$ currency').replace('10^-20 in',r'$10^{-20}$ in')
 text=text.replace('D(1.5) = sqrt(D(1)D(2)) = 0.850376678812',r'$D(1.5)=\sqrt{D(1)D(2)}=0.850376678812$')
 text=text.replace('sum((residual PV01/1000)^2) + 0.001 x cost/1000',r'$\sum_j(\mathrm{residual\ PV01}_j/1000)^2+0.001\,\mathrm{cost}/1000$')
 text=text.replace('`'+LONG_DEPOSIT.replace(' x ',' × ')+'`',r'''$$
\begin{aligned}
\Delta r_t={}&\alpha+b_{\mathrm{up}}\max(\Delta m_t,0)
+b_{\mathrm{down}}\min(\Delta m_t,0)\\
&+\ell_{\mathrm{up}}\max(\Delta m_{t-1},0)
+\ell_{\mathrm{down}}\min(\Delta m_{t-1},0)+\varepsilon_t.
\end{aligned}
$$

Here $\Delta r_t$ is change_in_paid_rate, $\alpha$ is intercept, $\Delta m_t$ is market_change, $\ell_{\mathrm{up}}$ and $\ell_{\mathrm{down}}$ are lag_up and lag_down, and $\varepsilon_t$ is error; the index $t$ denotes a monthly observation.''')
 if name=='OPERATIONS_METHODOLOGY.md':
  start=text.index('## Source anchors and reading scope')
  end=text.index('## 1. Dated product-level FTP')
  text=text[:start]+text[end:]
  text=text.replace('Adding business-unit and Treasury margins',r'The rate symbols $r_{\mathrm{customer}}$, $r_{\mathrm{FTP}}$, $r_{\mathrm{liquidity}}$ and $r_{\mathrm{external}}$ denote the matching annual decimal rates in the table; $f_{\mathrm{customer}}$ and $f_{\mathrm{external}}$ denote the annual commitment-fee and commitment-cost rates. Adding business-unit and Treasury margins')
  text=text.replace('The original cohort cannot',r'In the two balance identities, $C_t$ is the original tagged-cohort balance, $B_t$ the original-product balance, $W_t$ withdrawals, $M_t$ same-bank migration and $I_t$ new inflow; all are money for month $t$. The original cohort cannot')
 if name=='ACCOUNTING_AND_CONNECTED_CASES.md':
  replacement=r'''$$
\begin{aligned}
V_{\mathrm{adjusted}}&=50/1.06+1050/1.06^2=981.666073,\\
L_{\mathrm{item}}&=1000-V_{\mathrm{adjusted}}=18.333927,\\
G_{\mathrm{derivative}}&=18.000000,\\
G_{\mathrm{ineffectiveness}}&=18.000000-18.333927=-0.333927.
\end{aligned}
$$

Here $V_{\mathrm{adjusted}}$ is adjusted carrying amount; $L_{\mathrm{item}}$ is the hedged-item loss; $G_{\mathrm{derivative}}$ is the supplied derivative gain; and $G_{\mathrm{ineffectiveness}}$ is net hedge ineffectiveness. All quantities are in KES.'''
  text=re.sub(r'```text\nadjusted carrying amount.*?```',lambda m:replacement,text,count=1,flags=re.S)
 return text

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--output',type=Path,default=ROOT/'output/pdf'/f'RegTech_KESONIA_Worked_Examples_{EDITION}.pdf')
 args=ap.parse_args()
 output=args.output.resolve()
 build=ROOT/'publications/build/worked_examples_tex'
 build.mkdir(parents=True,exist_ok=True)
 output.parent.mkdir(parents=True,exist_ok=True)
 pandoc=tool('pandoc','~/AppData/Local/Pandoc/pandoc.exe')
 xelatex=tool('xelatex','~/AppData/Local/Programs/MiKTeX/miktex/bin/x64/xelatex.exe')
 asts=[]; heading_maps={}; repairs=[]
 for i,name in enumerate(SOURCES,1):
  original=(ROOT/'docs/methods'/name).read_text(encoding='utf-8')
  text=prepare(original,name)
  ast=json.loads(run([pandoc,'-f','markdown+tex_math_dollars+tex_math_single_backslash','-t','json'],text=text))
  blocks=ast['blocks']
  if blocks and blocks[0]['t']=='Header':blocks.pop(0)
  heads={}
  def headings(node):
   if isinstance(node,dict):
    if node.get('t')=='Header':
     old=node['c'][1][0];new=f'part-{i}-'+old
     heads[old]=new;node['c'][1][0]=new
    for v in node.values():headings(v)
   elif isinstance(node,list):
    for v in node:headings(v)
  headings(blocks);heading_maps[name]=heads;asts.append(ast)
  if original!=text:repairs.append(name)
 counts=Counter();links=[];equation_counts={}
 for i,(name,ast) in enumerate(zip(SOURCES,asts),1):
  counter=0
  def walk(node):
   nonlocal counter
   if isinstance(node,list):return [walk(v) for v in node]
   if not isinstance(node,dict):return node
   kind=node.get('t');c=node.get('c')
   if kind=='Code' and c[1].replace('×','x') in MATH_CODES:
    counts['code_formulas_converted']+=1
    return math_node(MATH_CODES[c[1].replace('×','x')])
   if kind=='Str' and c in SYMBOLS:
    counts['plain_symbols_typeset']+=1
    return math_node(symbol_tex(c))
   if kind=='Math':
    counts['display_math' if c[0]['t']=='DisplayMath' else 'inline_math']+=1
    formula=c[1]
    for word in ('Cash','Loans','Collateral','Deposits','Wholesale','Equity','Fee','PV'):
     formula=re.sub(r'(?<![A-Za-z\\])'+word+r'(?![A-Za-z])',lambda m:r'\mathrm{'+m.group(0)+'}',formula)
    formula=re.sub(r'_\{([A-Za-z]{3,})\}',lambda m:r'_{\mathrm{'+m.group(1)+'}}',formula)
    if c[0]['t']=='DisplayMath':
     counter+=1
     if len(formula)>110 and not '\\begin{' in formula:
      if '\\qquad' in formula:formula=r'\begin{gathered}'+formula.replace(r'\qquad',r'\\')+r'\end{gathered}'
      elif len(formula)>170 and '\\quad' in formula:formula=r'\begin{gathered}'+formula.replace(r'\quad',r'\\')+r'\end{gathered}'
     return {'t':'RawInline','c':['latex',r'\begin{equation}'+formula+r'\tag{'+str(i)+'.'+str(counter)+r'}\label{eq:'+str(i)+'-'+str(counter)+r'}\end{equation}']}
    return math_node(formula)
   if kind=='Link':
    target=c[2][0]
    if not re.match(r'^(https?://|mailto:)',target):
     path,_,fragment=target.partition('#')
     resolved=(ROOT/'docs/methods'/name).parent/path if path else ROOT/'docs/methods'/name
     resolved=resolved.resolve()
     if resolved.name in SOURCES and resolved.parent==ROOT/'docs/methods':
      j=SOURCES.index(resolved.name)+1
      anchor=heading_maps[resolved.name].get(fragment,f'part-{j}') if fragment else f'part-{j}'
      c[2][0]='#'+anchor
     else:
      c[2][0]=GITHUB+resolved.relative_to(ROOT).as_posix()+('#'+fragment if fragment else '')
    links.append(c[2][0])
   if kind=='CodeBlock':
    escape={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','#':r'\#','%':r'\%','&':r'\&','_':r'\_','$':r'\$','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    lines=[''.join(escape.get(ch,ch) for ch in line) for line in c[1].splitlines()]
    return {'t':'RawBlock','c':['latex',r'\begin{quote}\small\ttfamily\raggedright '+r'\par '.join(lines)+r'\end{quote}']}
   return {k:walk(v) for k,v in node.items()}
  ast['blocks']=walk(ast['blocks']);equation_counts[name]=counter
 blocks=[]
 lead='This casebook combines the original benchmark, pricing and funding cases with their symbol reference, dated contract events, options and collateral, liquidity and capital components, hedge accounting, connected finance, the implementation register and SokoIntel candidate map. Symbols and units are defined beside the equations and in Part III. Equations are numbered by part. The numerical edition remains 1 October 2026; this TeX typesetting revision was produced on 16 October 2026.'
 blocks.extend(json.loads(run([pandoc,'-f','markdown','-t','json'],text=lead))['blocks'])
 for i,(title,ast) in enumerate(zip(TITLES,asts),1):
  blocks.append({'t':'RawBlock','c':['latex',r'\clearpage']})
  blocks.append({'t':'Header','c':[1,[f'part-{i}',[],[]],[{'t':'Str','c':title}]]})
  blocks.extend(ast['blocks'])
 combined=asts[0];combined['blocks']=blocks;combined['meta']={}
 jsonpath=build/'casebook.json';jsonpath.write_text(json.dumps(combined,ensure_ascii=False),encoding='utf-8')
 header=build/'preamble.tex'
 header.write_text(r'''\usepackage{etoolbox}
\usepackage{fancyvrb}
\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\}}
\RecustomVerbatimEnvironment{verbatim}{Verbatim}{fontsize=\footnotesize}
\AtBeginEnvironment{longtable}{\footnotesize\setlength{\tabcolsep}{3pt}}
\let\originaltexttt\texttt
\renewcommand{\texttt}[1]{{\small\originaltexttt{#1}}}
\allowdisplaybreaks
\setlength{\emergencystretch}{3em}
\AtBeginDocument{\hypersetup{colorlinks=false,pdfborder={0 0 0}}}
''',encoding='utf-8')
 tex=build/'RegTech_KESONIA_Worked_Examples.tex'
 run([pandoc,jsonpath,'-f','json','-t','latex','--standalone','--toc','--toc-depth=2',
      '-V','geometry:margin=0.7in','-V','mainfont:Segoe UI','-V','fontsize:11pt',
      '-V','documentclass:article','-V','linestretch:1.08',
      '-M','title:RegTech KESONIA: Worked Examples, Symbols and Units',
      '-M','author:Nevil Maloba','-M','date:1 October 2026',
      '--include-in-header',header,'--output',tex])
 content=tex.read_text(encoding='utf-8').replace(r'\real{0.1667}',r'\real{0.166666}').replace('Deposit/wholesale',r'Deposit/\allowbreak wholesale').replace(r'research\_lab/option\_cases.py',r'research\_lab/\allowbreak option\_cases.py').replace(r'tests/test\_option\_cases.py',r'tests/\allowbreak test\_option\_cases.py')
 content=content.replace('}.\n'+r'\texttt{option\_examples()}', '}.\n\n'+r'\texttt{option\_examples()}')
 tex.write_text(content,encoding='utf-8')
 for _ in range(3):run([xelatex,'-halt-on-error','-interaction=nonstopmode',f'-output-directory={build}',tex],cwd=ROOT)
 log=tex.with_suffix('.log').read_text(encoding='utf-8',errors='replace')
 issues={k:len(re.findall(pattern,log)) for k,pattern in {'missing_glyphs':r'Missing character:',
    'undefined_references':r'(?:Reference|Citation) .+ undefined','overfull_boxes':r'Overfull \\[hv]box'}.items()}
 if issues['missing_glyphs'] or issues['undefined_references']:raise RuntimeError('TeX validation failed: '+str(issues))
 staged=tex.with_suffix('.pdf');output.write_bytes(staged.read_bytes())
 manifest={'edition':EDITION,'typesetting_revision':'2026-10-16','output':str(output),
 'sha256':sha256(output.read_bytes()).hexdigest(),'bytes':output.stat().st_size,'renderer':'Pandoc + XeLaTeX; native TeX math',
 'sources':{n:sha256((ROOT/'docs/methods'/n).read_bytes()).hexdigest() for n in SOURCES},
 'equations_by_part':equation_counts,'conversion_counts':dict(counts),'tex_checks':issues,
 'links':links,'presentation_transformations':['Same nine sources and original operations inventory omission as prior PDF.',
 'Code-formula expressions typeset in TeX; added local aliases defined beside them.',
 'Known damaged separators, paragraph symbols and scientific exponent repaired in render input only.',
 'Local included-source links point to chapter anchors; other local links point to GitHub.',
 'Canonical research Markdown remains unedited.'],'visual_verification':'Render and inspect before release.'}
 output.with_suffix('.manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({k:manifest[k] for k in ['output','sha256','bytes','equations_by_part','conversion_counts','tex_checks']},indent=2))

if __name__=='__main__':main()

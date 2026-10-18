"""Run all named scenarios, paired policies, sensitivity grid and independent tests."""
from copy import deepcopy
import csv
import hashlib
import json
from pathlib import Path
import unittest
from .model import assumptions, run_case, source_models, static_bridge

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'output/deposit_beta_dynamic_case_2026-10-18'

def write_json(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

def write_csv(path,rows):
    if not rows: return
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    cfg=assumptions(); sources=source_models()
    write_json(OUT/'assumptions.json',cfg);write_json(OUT/'existing_component_provenance.json',sources)
    write_json(OUT/'static_article_bridge.json',static_bridge())
    summaries=[]
    pairs=[(s,'standard') for s in cfg['scenarios']]+[('joint_stress',p) for p in cfg['policies'] if p!='standard']
    for scenario,policy in pairs:
        result=run_case(scenario,policy,cfg,sources['fit'])
        folder=OUT/f'{scenario}__{policy}';folder.mkdir(exist_ok=True)
        for k in ('monthly','loans','deposits','events'):write_csv(folder/f'{k}.csv',result[k])
        write_json(folder/'summary.json',result['summary']);summaries.append(result['summary'])
    write_csv(OUT/'scenario_summary.csv',summaries);write_json(OUT/'scenario_summary.json',summaries)
    sensitivities=[]
    for beta_factor in (.75,1,1.25):
        for extra_runoff in (.01,.025,.04):
            c=deepcopy(cfg);c['scenarios']['joint_stress']['extra_runoff']=extra_runoff
            fitted=deepcopy(sources['fit'])
            for seg in fitted.values():
                for k in ('beta_up','beta_down','lag_beta_up','lag_beta_down'):seg['coefficients'][k]*=beta_factor
            x=run_case('joint_stress','standard',c,fitted)['summary']
            sensitivities.append(dict(beta_multiplier=beta_factor,extra_monthly_runoff=extra_runoff,profit=x['profit'],peak_wholesale=x['peak_wholesale'],lending_deferred=x['lending_deferred'],cash_floor_breaches=x['cash_floor_breaches'],minimum_capital_proxy=x['minimum_capital_proxy']))
    write_csv(OUT/'behaviour_sensitivity.csv',sensitivities)
    suite=unittest.defaultTestLoader.loadTestsFromName('tests.test_deposit_beta_dynamic_case')
    with (OUT/'test_results.txt').open('w',encoding='utf-8') as stream:
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    verification={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
                  'passed':result.wasSuccessful(),'case_count':len(summaries),'sensitivity_cases':len(sensitivities),
                  'maximum_reconciliation_error_KES':max(x['maximum_reconciliation_error'] for x in summaries),
                  'scope':'Deterministic expected-cohort scenario engine. All inputs synthetic. Independent arithmetic, conservation, timing and monotonicity checks.'}
    write_json(OUT/'verification.json',verification)
    hashed=[*Path(__file__).parent.glob('*.py'),Path(__file__).parent/'assumptions.json',ROOT/'tests/test_deposit_beta_dynamic_case.py',ROOT/'research_lab/operations.py',ROOT/'research_lab/benchmark.py']
    hashed+=sorted(p for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json')
    write_json(OUT/'manifest.json',{'sha256':{p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in hashed}})
    print(json.dumps(verification,indent=2))
    for row in summaries:print(row['scenario'],row['policy'],'profit',round(row['profit']),'NII',round(row['nii']),'deferred',round(row['lending_deferred']),'peak wholesale',round(row['peak_wholesale']))
    if not result.wasSuccessful():raise SystemExit(1)

if __name__=='__main__':main()

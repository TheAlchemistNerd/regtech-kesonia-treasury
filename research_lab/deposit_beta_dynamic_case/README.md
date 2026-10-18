# Deposit Beta Dynamic Case

A reproducible, 24-month synthetic bank case connecting deposits, loans, funding, credit costs, liquidity and equity.

## Read and run

- [Full economic narrative and equations](../../docs/methods/DEPOSIT_BETA_DYNAMIC_CASE.md)
- [LinkedIn article](../../publications/linkedin/Deposit_Beta_KESONIA_and_Bank_Risk_2026-10-16.md)
- [Case assumptions](assumptions.json)
- [Model](model.py)
- [Independent tests](../../tests/test_deposit_beta_dynamic_case.py)
- [Saved results](../../output/deposit_beta_dynamic_case_2026-10-18/scenario_summary.csv)

```text
python -B -m research_lab.deposit_beta_dynamic_case.run_case
python -B -m research_lab.deposit_beta_dynamic_case.build_publication
```

Run the commands from the repository root. The model and tests use the standard library and reuse existing `benchmark.py` and `operations.py`. Publication requires Pillow and python-docx, with Arial available. The model records deterministic expected-cohort cash, not sampled individual borrower defaults. The methods narrative specifies the synthetic contract timing, borrower-hazard mechanism, management allowance and internal capital proxy.

Copyright Nevil Maloba. Publication materials use Creative Commons Attribution NonCommercial ShareAlike 4.0, consistent with the research series. https://creativecommons.org/licenses/by-nc-sa/4.0/

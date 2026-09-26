# KESONIA Compounding, the Term Structure and the Funding Curve

Close, but one distinction matters: compounded KESONIA is not itself a term structure. It aggregates the daily overnight observations over one accrual period and converts them into the period's realised effective benchmark rate. That lets the lender calculate interest consistently from the published overnight rates.

A term structure instead compares rates across different future maturities at one valuation date. KESONIA can anchor such a curve, but the curve additionally needs instruments or assumptions across tenors. So:

- Nominal daily KESONIA observations → compounding → realised effective rate for the contract period.
- KESONIA-based market instruments and expectations → curve construction → term structure across maturities.
- Institution-specific funding spreads added to that curve → internal funding curve used for FTP.

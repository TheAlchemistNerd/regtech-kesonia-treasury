import glob
import os

replacements = {
    r"$$CCR = \left\lbrack \prod_{i = 1}^{d_{b}}\left( 1 + \frac{KESONIA_{i} \cdot n_{i}}{365} \right) - 1 \right\rbrack \times \frac{365}{d}$$": "CCR = [ ∏ (1 + (KESONIAᵢ × nᵢ) / 365) - 1 ] × (365 / d)",
    r"$$R_{t} = CCR_{t} + K(PD,LGD,EAD)$$": "Rₜ = CCRₜ + K(PD,LGD,EAD)",
    r"$$K = \frac{EL + CoC + OpEx}{1 - EL}$$": "K = (EL + CoC + OpEx) / (1 - EL)",
    r"$R_{t} = CCR_{t} + K$": "Rₜ = CCRₜ + K",
    r"$R_{t} = CCR + K$": "Rₜ = CCR + K",
    r"$CCR_{t}$": "CCRₜ",
    r"$R_{t}$": "Rₜ",
    r"$KESONIA_{i}$": "KESONIAᵢ",
    r"$n_{i}$": "nᵢ",
    r"$d_{b}$": "d_b",
    r"$p_{t}$": "pₜ",
    r"$K$": "K",
    r"$d$": "d",
    r"$PD \times LGD \times EAD$": "PD × LGD × EAD",
    r"$PD$": "PD",
    r"$LGD$": "LGD",
    r"$EAD$": "EAD",
    r"$\prod$": "∏",
    r"$\frac{365}{d}$": "365/d",
    r"$CCR$": "CCR"
}

files = glob.glob('linkedin/Part*.md')

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed {len(files)} files.")

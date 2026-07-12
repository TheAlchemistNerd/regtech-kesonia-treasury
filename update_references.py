import glob
import re

replacements = [
    # Part 1
    (r"\[8\] \[MISSING REFERENCE FOR OLD 9\]", r"[8] Yu, T. (2025). Data as collateral: Open banking for small business lending. *SSRN Electronic Journal*."),
    (r"\[9\] \[MISSING REFERENCE FOR OLD 10\]", r"[9] Paleti, S. (2025). Data-first finance: Architecting scalable data engineering pipelines for AI-powered risk intelligence in banking. *SSRN Electronic Journal*."),
    (r"\[15\] \[MISSING REFERENCE FOR OLD 16\]", r"[15] Albanese, C., & Iabichino, S. (2020). Risk managing the LIBOR transition. *SSRN Electronic Journal*."),
    
    # Part 3
    (r"\[9\] Altman, E.I., Brady, B., Resti, A. and Sironi, A. \(2005\) 'The Link Between Default and Recovery Rates: Theory, Empirical Evidence, and Implications.' \*Journal of Business\*, 78\(6\), pp.2203-2228. \[Placeholder , - confirm 2019\+ equivalent with research agent\]",
     r"[9] Orlando, G., & Pelosi, R. (2020). Non-performing loans for Italian companies: When time matters. An empirical research on estimating probability to default and loss given default. *International Journal of Financial Studies, 8*(4), 68."),
    (r"\[19\] Wyle, R.J. and Tsaig, Y. \(2021\). 'Implementing Funds Transfer Pricing in a Low Interest Rate Environment.' \*Journal of Risk Management in Financial Institutions\*, 14\(2\), pp.120-134. \[Placeholder , - confirm with research agent\]",
     r"[19] Wyle, R. J., & Tsaig, Y. (2011). *Implementing high value funds transfer pricing systems*. Moody's Analytics."),
    
    # Part 4
    (r"\[5\] Institute of International Finance \(2020\). \*Machine Learning in Anti-Money Laundering\*. IIF. \[Placeholder , - confirm with research agent for 2019\+ publication\]",
     r"[5] Institute of International Finance (2018). *Machine learning in anti-money laundering*. IIF."),
    (r"\[12\] Wyle, R.J. and Tsaig, Y. \(2019\). 'Implementing Modern Funds Transfer Pricing.' \*Journal of Risk Management in Financial Institutions\*, 12\(4\), pp.344-360. \[Placeholder , - confirm with research agent\]",
     r"[12] Wyle, R. J., & Tsaig, Y. (2011). *Implementing high value funds transfer pricing systems*. Moody's Analytics."),
    (r"\[24\] Accenture \(2021\). \*LIBOR Transition Playbook for Banking Technology Teams\*. Accenture. \[Placeholder , - confirm availability and 2019\+ date\]",
     r"[24] Accenture (2021). *LIBOR end-to-end testing POV*. Accenture.")
]

files = glob.glob("*.md") + glob.glob("linkedin/*.md")

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_pattern, new_text in replacements:
        content = re.sub(old_pattern, new_text, content, flags=re.IGNORECASE)
        # Also handle potential line breaks in the middle of placeholders in Part 3 and 4
        
    # Since re.sub with literal strings might miss due to newlines, let's do a more robust string replace for the line-broken parts
    # Part 3
    content = re.sub(
        r"\[9\] Altman.*?\[Placeholder.*?\]", 
        r"[9] Orlando, G., & Pelosi, R. (2020). Non-performing loans for Italian companies: When time matters. An empirical research on estimating probability to default and loss given default. *International Journal of Financial Studies, 8*(4), 68.", 
        content, flags=re.DOTALL
    )
    content = re.sub(
        r"\[19\] Wyle.*?\[Placeholder.*?\]", 
        r"[19] Wyle, R. J., & Tsaig, Y. (2011). *Implementing high value funds transfer pricing systems*. Moody's Analytics.", 
        content, flags=re.DOTALL
    )
    
    # Part 4
    content = re.sub(
        r"\[5\] Institute of International Finance.*?\[Placeholder.*?\]", 
        r"[5] Institute of International Finance (2018). *Machine learning in anti-money laundering*. IIF.", 
        content, flags=re.DOTALL
    )
    content = re.sub(
        r"\[12\] Wyle.*?\[Placeholder.*?\]", 
        r"[12] Wyle, R. J., & Tsaig, Y. (2011). *Implementing high value funds transfer pricing systems*. Moody's Analytics.", 
        content, flags=re.DOTALL
    )
    content = re.sub(
        r"\[24\] Accenture.*?\[Placeholder.*?\]", 
        r"[24] Accenture (2021). *LIBOR end-to-end testing POV*. Accenture.", 
        content, flags=re.DOTALL
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Processed references in {len(files)} files.")

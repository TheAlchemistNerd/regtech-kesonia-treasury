"""Reproduce the reference cases; never submits transactions or regulatory returns."""
from pathlib import Path
import hashlib
import json
from .benchmark import benchmark_examples
from .curves import curve_examples
from .pricing import pricing_examples
from .scenarios import scenario_examples
from .operations import operations_examples
from .lifecycle_cases import lifecycle_examples
from .option_cases import option_examples
from .regulatory_cases import regulatory_examples
from .accounting_cases import accounting_examples
from .connected_cases import connected_examples


def main():
    package = Path(__file__).resolve().parent
    results = {
        'edition': '2026-10-01',
        'evidence': 'One historical benchmark/index check; all other portfolios, quotes, holidays, forecasts and transactions are synthetic.',
        'scope': 'Research reference, not an institution-specific contract engine, empirical model, accounting policy or regulatory return.',
        'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(package.glob('*.py'))},
        'data_sha256': {p.relative_to(package).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted((package / 'data').glob('*.json'))},
        'benchmark': benchmark_examples(),
        'curves': curve_examples(),
        'pricing': pricing_examples(),
        'scenarios': scenario_examples(),
        'operations': operations_examples(),
        'lifecycle': lifecycle_examples(),
        'options': option_examples(),
        'regulatory': regulatory_examples(),
        'accounting': accounting_examples(),
        'connected': connected_examples(),
    }
    destination = package / 'results' / 'checked_examples.json'
    destination.parent.mkdir(exist_ok=True)
    destination.write_bytes((json.dumps(results, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(f'Reproduced reference cases: {destination}')


if __name__ == '__main__':
    main()

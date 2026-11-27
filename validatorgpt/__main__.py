import argparse
import json
from pathlib import Path
from .core import run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, help='Optional input file; default: examples/input.json')
    parser.add_argument('--output', type=Path, default=Path('results/report.json'))
    args = parser.parse_args()
    data = json.loads((args.data or Path('examples/input.json')).read_text(encoding='utf-8'))
    report = run(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2, allow_nan=False))

if __name__ == '__main__':
    main()

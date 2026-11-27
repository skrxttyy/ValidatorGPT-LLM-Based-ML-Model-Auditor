# ValidatorGPT

Deterministic classifier audit evidence and a concise findings report; optional LLM report drafting.

```bash
python -m venv .venv
# Activate the environment, then:
python -m pip install -r requirements.txt
python -m validatorgpt
python -m unittest discover -s tests -v
```

`--data path.json` accepts the schema in `examples/input.json`.
`--output path.json` sets the report location (default: `results/report.json`).
Source: `validatorgpt/core.py`; checks: `tests/`; inputs: `examples/`.

The default report is deterministic. Optional `python -m validatorgpt.draft results/report.json` uses an OpenAI-compatible endpoint via `LLM_BASE_URL`, `LLM_API_KEY`, and `LLM_MODEL`. It sends only the report, with a 600-token output budget. No LLM call is needed for the demo; that optional integration has not been exercised against a live service.

The checked-in report is an executed demonstration, not a real-world benchmark.
Seed: 42 where randomness is used. Python 3.12.

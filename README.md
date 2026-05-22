# human‑delta

A **single‑file** Python CLI that turns two timestamps into a friendly, human‑readable phrase.

![GitHub Actions CI](https://github.com/your‑username/human-delta/workflows/CI/badge.svg)

## Features

- Zero‑dependency runtime (only **click** for the command‑line interface).
- Works with ISO‑8601 strings, Unix timestamps, or any format accepted by `dateutil.parser`.
- Supports past and future dates ("3 days ago" / "in 2 weeks").
- Fully typed, linted, and tested with GitHub Actions CI.

## Installation

```bash
# Clone and install in editable mode (development)
git clone https://github.com/your-username/human-delta.git
cd human-delta
pip install -e .
```

Or install the entry‑point directly from PyPI (once published):

```bash
pip install human-delta
```

## Usage

```bash
# Show the difference between now and a given date
human-delta "2024-12-31T23:59:59Z"
# => "in 8 months"

# Compare two explicit dates
human-delta "2023-01-01" "2023-01-10"
# => "9 days ago"
```

## Development

```bash
# Install development dependencies
pip install -r requirements.txt
# Run the test suite
pytest -q
# Run linting
flake8 .
```

## CI / CD

The repository uses **GitHub Actions** to automatically:
- Lint the code with **flake8**.
- Run the test suite with **pytest**.
- Build a distribution package on tag pushes.

See `.github/workflows/ci.yml` for the full workflow definition.

## License

MIT – see [LICENSE](LICENSE) for details.

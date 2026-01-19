# LLN Explorer (Lite)

A CLI tool for visualizing the Law of Large Numbers through interactive simulations and plots.

## Overview

LLN Explorer generates visualizations that demonstrate two fundamental theorems in probability theory:

- **Strong Law of Large Numbers (SLLN)**: Sample averages converge almost surely to the expected value
- **Weak Law of Large Numbers (WLLN)**: Sample averages converge in probability to the expected value

The tool produces three types of visualizations:
1. **Sample Path Convergence** - Shows multiple sample paths converging toward the theoretical mean
2. **Deviation Probability Decay** - Shows P(|X_n - mu| > epsilon) decreasing with sample size
3. **Variance Decay** - Compares empirical variance with theoretical sigma^2/n

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/vickyvicky122/test_claudeskills.git
cd test_claudeskills/lln_explorer

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

Run with default settings (Normal distribution, 100 paths, 10000 samples):

```bash
python lln_explorer.py
```

This generates three PNG files in the `./output` directory.

## Usage

### Basic Command

```bash
python lln_explorer.py [OPTIONS]
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `--dist` | `normal` | Distribution: `normal`, `bernoulli`, or `uniform` |
| `--M` | `100` | Number of sample paths (realizations) |
| `--N` | `10000` | Maximum sample size per path |
| `--eps` | `0.1` | Epsilon threshold for deviation probability |
| `--output` | `./output` | Output directory for generated plots |
| `--p` | `0.5` | Bernoulli probability parameter |
| `--mu` | `0.0` | Normal distribution mean |
| `--sigma` | `1.0` | Normal distribution standard deviation |

### Examples

**Normal Distribution** (default):
```bash
python lln_explorer.py --dist normal --mu 0 --sigma 1 --M 100 --N 10000
```

**Bernoulli Distribution** (coin flips):
```bash
python lln_explorer.py --dist bernoulli --p 0.7 --M 50 --N 5000
```

**Uniform Distribution**:
```bash
python lln_explorer.py --dist uniform --M 100 --N 10000
```

**Custom epsilon** (tighter convergence threshold):
```bash
python lln_explorer.py --eps 0.05 --M 200 --N 20000
```

**Quick test run** (faster execution):
```bash
python lln_explorer.py --M 10 --N 1000
```

## Sample Output

```
LLN Explorer Configuration:
  Distribution: normal (mu=0.0, sigma=1.0)
  Theoretical mean: 0.0
  Theoretical variance: 1.0
  Sample paths (M): 100
  Max samples (N): 10000
  Epsilon: 0.1
  Output directory: /path/to/output

Running simulation...
Simulation completed in 1.23 seconds

Summary Statistics:
  Empirical mean (final): 0.000234
  Theoretical mean: 0.000000
  Empirical variance (final): 0.000098
  Theoretical variance (sigma^2/N): 0.000100
  Deviation probability (final): 0.0000

Figures saved to: /path/to/output/
Generating visualizations...
  Sample paths: normal_sample_paths.png
  Deviation probability: normal_deviation.png
  Variance decay: normal_variance.png
```

## Output Files

The tool generates three visualization files per run:

| File | Description |
|------|-------------|
| `{dist}_sample_paths.png` | Multiple sample paths showing convergence to mean |
| `{dist}_deviation.png` | P(\|X_n - mu\| > epsilon) vs sample size |
| `{dist}_variance.png` | Empirical vs theoretical variance decay |

## Supported Distributions

### Normal Distribution
- Parameters: `--mu` (mean), `--sigma` (standard deviation)
- Theoretical mean: mu
- Theoretical variance: sigma^2

### Bernoulli Distribution
- Parameter: `--p` (success probability)
- Theoretical mean: p
- Theoretical variance: p(1-p)

### Uniform Distribution
- Fixed range: [0, 1]
- Theoretical mean: 0.5
- Theoretical variance: 1/12

## Project Structure

```
lln_explorer/
├── lln_explorer.py    # Main script
├── requirements.txt   # Dependencies (numpy, matplotlib)
├── output/           # Generated visualizations
├── tests/            # Test suite
└── README.md         # This file
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments |
| 2 | Runtime error |

## License

MIT License

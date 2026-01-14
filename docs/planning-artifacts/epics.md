---
stepsCompleted: [step-01-validate-prerequisites, step-02-design-epics, step-03-create-stories]
inputDocuments:
  - path: "docs/planning-artifacts/prd.md"
    type: "prd"
    description: "LLN Explorer (Lite) - Product Requirements Document"
  - path: "docs/planning-artifacts/architecture.md"
    type: "architecture"
    description: "LLN Explorer (Lite) - Architecture Decision Document"
---

# LLN Explorer (Lite) - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for LLN Explorer (Lite), decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

- FR1: User can select Bernoulli distribution with configurable probability parameter p
- FR2: User can select Uniform(0,1) distribution
- FR3: User can select Normal distribution with configurable mean μ and standard deviation σ
- FR4: System provides known theoretical mean and variance for each distribution
- FR5: System can generate M independent sample paths of length N
- FR6: System can compute running averages X̄ₙ for each sample path at each n
- FR7: System can estimate deviation probability P(|X̄ₙ - μ| > ε) across sample paths
- FR8: System can compute empirical variance of X̄ₙ across sample paths at each n
- FR9: User can view multiple sample path trajectories on a single plot
- FR10: System displays horizontal reference line at theoretical mean μ
- FR11: Plot shows running average X̄ₙ vs sample size n for each path
- FR12: User can view deviation probability P(|X̄ₙ - μ| > ε) as a function of n
- FR13: User can configure deviation tolerance ε
- FR14: Plot shows empirical deviation probability decreasing with n
- FR15: User can view empirical variance of X̄ₙ as a function of n
- FR16: System overlays theoretical variance decay curve σ²/n
- FR17: Plot enables visual comparison of empirical vs theoretical decay
- FR18: System exports sample path plot as PNG file
- FR19: System exports deviation probability plot as PNG file
- FR20: System exports variance decay plot as PNG file
- FR21: System prints summary statistics to console (mean, variance, distribution info)
- FR22: Output files use predictable naming convention
- FR23: User can run tool with sensible defaults (no arguments required)
- FR24: User can override default parameters via command-line arguments
- FR25: User can specify output directory for generated figures
- FR26: System returns exit code 0 on success, non-zero on error

### NonFunctional Requirements

- NFR1: Full simulation completes in < 30 seconds for M=100, N=10,000
- NFR2: Memory usage remains reasonable (< 500MB) for typical parameters
- NFR3: Figure generation completes without user-perceived delay after simulation
- NFR4: Runs on Python 3.8+ without modification
- NFR5: Works on Windows, macOS, and Linux
- NFR6: Only requires NumPy and Matplotlib (standard scientific Python stack)
- NFR7: Single-file implementation (or minimal module structure)
- NFR8: Code is readable without extensive comments
- NFR9: No complex dependencies or build steps

### Additional Requirements

**From Architecture:**

- Python 3.14 required (architecture decision overrides PRD's 3.8+)
- No starter template needed — standalone Python script from scratch
- Dictionary-based distribution abstraction pattern for extensibility
- Chunked simulation for memory efficiency (process M paths in chunks)
- Single-file implementation with top-down organization:
  1. Imports
  2. Constants (DEFAULT_M, DEFAULT_N, etc.)
  3. Distribution dictionary (DISTRIBUTIONS)
  4. Simulation functions (simulate_chunked, compute_stats)
  5. Plot functions (plot_sample_paths, plot_deviation, plot_variance)
  6. CLI setup (parse_args, validate_args)
  7. Main orchestration (main)
  8. Entry point (if __name__ == '__main__')
- PEP 8 naming conventions enforced (snake_case functions/variables, UPPER_CASE constants)
- Fail-fast error handling with validation before computation
- Exit codes: 0 = success, 1 = invalid arguments, 2 = runtime error
- Output file naming: `{dist}_sample_paths.png`, `{dist}_deviation.png`, `{dist}_variance.png`
- Consistent figure styling (clean axes, labels, legends, uniform font sizes)
- argparse for CLI (stdlib, no external deps)

**Project Structure (from Architecture):**
```
lln_explorer/
├── lln_explorer.py          # Main script (single file)
├── requirements.txt         # numpy, matplotlib
├── README.md                # Usage documentation
├── LICENSE                  # MIT or chosen license
├── .gitignore               # Python gitignore
├── output/                  # Default output directory (gitignored)
│   └── .gitkeep
└── tests/                   # Optional test directory
    └── test_lln_explorer.py # pytest tests
```

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR1 | Epic 2 | Bernoulli distribution with configurable p |
| FR2 | Epic 2 | Uniform(0,1) distribution |
| FR3 | Epic 2 | Normal distribution with configurable μ, σ |
| FR4 | Epic 2 | Theoretical mean/variance for each distribution |
| FR5 | Epic 2 | Generate M independent sample paths of length N |
| FR6 | Epic 2 | Compute running averages X̄ₙ |
| FR7 | Epic 2 | Estimate deviation probability P(\|X̄ₙ - μ\| > ε) |
| FR8 | Epic 2 | Compute empirical variance of X̄ₙ |
| FR9 | Epic 3 | Multiple sample paths on single plot |
| FR10 | Epic 3 | Horizontal reference line at μ |
| FR11 | Epic 3 | Running average vs sample size n |
| FR12 | Epic 3 | Deviation probability vs n plot |
| FR13 | Epic 3 | Configurable deviation tolerance ε |
| FR14 | Epic 3 | Empirical deviation probability decreasing with n |
| FR15 | Epic 3 | Empirical variance vs n plot |
| FR16 | Epic 3 | Theoretical σ²/n overlay |
| FR17 | Epic 3 | Visual comparison empirical vs theoretical |
| FR18 | Epic 3 | Export sample path plot as PNG |
| FR19 | Epic 3 | Export deviation probability plot as PNG |
| FR20 | Epic 3 | Export variance decay plot as PNG |
| FR21 | Epic 3 | Console summary statistics |
| FR22 | Epic 1 | Predictable output file naming |
| FR23 | Epic 1 | Run with sensible defaults |
| FR24 | Epic 1 | Override defaults via CLI arguments |
| FR25 | Epic 1 | Specify output directory |
| FR26 | Epic 1 | Exit code 0 on success, non-zero on error |

## Epic List

### Epic 1: Project Setup & CLI Foundation
Users can install the tool, run it with defaults, and see usage help. The foundation is in place.
**FRs covered:** FR22, FR23, FR24, FR25, FR26

### Epic 2: Distribution Support & Simulation Engine
Users can select distributions and generate simulation data. The mathematical engine works.
**FRs covered:** FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8

### Epic 3: Complete Visualization Suite
Users can see all three LLN visualizations (sample paths, deviation probability, variance decay) with exports and summary statistics. Tool is complete.
**FRs covered:** FR9, FR10, FR11, FR12, FR13, FR14, FR15, FR16, FR17, FR18, FR19, FR20, FR21

---

## Epic 1: Project Setup & CLI Foundation

Users can install the tool, run it with defaults, and see usage help. The foundation is in place.

### Story 1.1: Project Initialization & Basic Script

**GitHub Issue:** [#2](https://github.com/vickyvicky122/test_claudeskills/issues/2)

As a **developer**,
I want to **set up the project structure with dependencies**,
So that **I have a working foundation to build upon**.

**Acceptance Criteria:**

**Given** an empty directory
**When** I run the initialization commands
**Then** the project structure exists:
- `lln_explorer.py` (main script)
- `requirements.txt` (numpy, matplotlib)
- `output/` directory with `.gitkeep`
- `.gitignore` (Python standard)
**And** `pip install -r requirements.txt` succeeds

---

### Story 1.2: CLI Argument Parsing with Defaults

**GitHub Issue:** [#3](https://github.com/vickyvicky122/test_claudeskills/issues/3)

As a **user**,
I want to **run the tool with sensible defaults or custom arguments**,
So that **I can use the tool immediately or configure it for my needs**.

**Acceptance Criteria:**

**Given** the script is installed
**When** I run `python lln_explorer.py --help`
**Then** I see all available options with descriptions

**Given** no arguments provided
**When** I run `python lln_explorer.py`
**Then** defaults are used: dist=normal, M=100, N=10000, eps=0.1, output=./output

**Given** custom arguments
**When** I run `python lln_explorer.py --dist bernoulli --M 50 --N 5000 --eps 0.05 --output ./custom`
**Then** those values are used instead of defaults

**Given** invalid arguments (e.g., --M -5)
**When** I run the script
**Then** exit code is 1 and error message is displayed

**Given** output directory doesn't exist
**When** I run the script
**Then** the directory is created automatically

---

## Epic 2: Distribution Support & Simulation Engine

Users can select distributions and generate simulation data. The mathematical engine works.

### Story 2.1: Distribution Dictionary Implementation

**GitHub Issue:** [#4](https://github.com/vickyvicky122/test_claudeskills/issues/4)

As a **user**,
I want to **select from Bernoulli, Uniform, or Normal distributions**,
So that **I can explore LLN behavior with different probability distributions**.

**Acceptance Criteria:**

**Given** the DISTRIBUTIONS dictionary is implemented
**When** I select `--dist bernoulli --p 0.5`
**Then** samples are drawn from Bernoulli(p=0.5) with mean=p, var=p(1-p)

**Given** `--dist uniform`
**When** the simulation runs
**Then** samples are drawn from Uniform(0,1) with mean=0.5, var=1/12

**Given** `--dist normal --mu 0 --sigma 1`
**When** the simulation runs
**Then** samples are drawn from Normal(μ, σ) with mean=μ, var=σ²

**And** each distribution provides theoretical mean and variance values

---

### Story 2.2: Simulation Engine with Chunked Processing

**GitHub Issue:** [#5](https://github.com/vickyvicky122/test_claudeskills/issues/5)

As a **user**,
I want to **generate M sample paths of length N efficiently**,
So that **I can analyze LLN convergence without memory issues**.

**Acceptance Criteria:**

**Given** parameters M=100, N=10000
**When** the simulation runs
**Then** 100 independent sample paths of length 10000 are generated

**Given** each sample path
**When** running averages are computed
**Then** X̄ₙ is calculated for each n from 1 to N

**Given** all sample paths
**When** deviation probability is computed
**Then** P(|X̄ₙ - μ| > ε) is estimated at each n

**Given** all sample paths
**When** empirical variance is computed
**Then** Var(X̄ₙ) is calculated at each n

**Given** M=100, N=10000 on standard hardware
**When** simulation completes
**Then** total time is < 30 seconds (NFR1)
**And** memory usage is < 500MB (NFR2)

---

## Epic 3: Complete Visualization Suite

Users can see all three LLN visualizations (sample paths, deviation probability, variance decay) with exports and summary statistics. Tool is complete.

### Story 3.1: Sample Path Visualization (Strong LLN)

**GitHub Issue:** [#6](https://github.com/vickyvicky122/test_claudeskills/issues/6)

As a **student or lecturer**,
I want to **see multiple sample paths converging toward the mean**,
So that **I can visualize Strong LLN (pathwise convergence)**.

**Acceptance Criteria:**

**Given** simulation data with M paths
**When** the sample path plot is generated
**Then** all M trajectories are displayed on a single plot

**Given** the theoretical mean μ
**When** the plot renders
**Then** a horizontal reference line at μ is displayed

**Given** each path
**When** plotted
**Then** running average X̄ₙ vs sample size n is shown

**Given** plot is complete
**When** export runs
**Then** `{dist}_sample_paths.png` is saved to output directory

---

### Story 3.2: Deviation Probability Visualization (Weak LLN)

**GitHub Issue:** [#7](https://github.com/vickyvicky122/test_claudeskills/issues/7)

As a **student or lecturer**,
I want to **see the probability of deviation shrinking with n**,
So that **I can visualize Weak LLN (convergence in probability)**.

**Acceptance Criteria:**

**Given** simulation data and ε value
**When** the deviation probability plot is generated
**Then** P(|X̄ₙ - μ| > ε) vs n is displayed

**Given** ε configured via CLI (default 0.1)
**When** probability is computed
**Then** the configured ε value is used

**Given** the plot
**When** rendered
**Then** the curve shows decreasing probability with increasing n

**Given** plot is complete
**When** export runs
**Then** `{dist}_deviation.png` is saved to output directory

---

### Story 3.3: Variance Decay Visualization & Console Summary

**GitHub Issue:** [#8](https://github.com/vickyvicky122/test_claudeskills/issues/8)

As a **self-learner or lecturer**,
I want to **see empirical variance decay with theory overlay and summary stats**,
So that **I can understand convergence rate and verify the simulation**.

**Acceptance Criteria:**

**Given** simulation data
**When** variance decay plot is generated
**Then** empirical Var(X̄ₙ) vs n is displayed

**Given** theoretical variance σ²
**When** plot renders
**Then** theoretical decay curve σ²/n is overlaid

**Given** both curves
**When** viewing the plot
**Then** visual comparison of empirical vs theoretical is clear

**Given** plot is complete
**When** export runs
**Then** `{dist}_variance.png` is saved to output directory

**Given** simulation completes
**When** results are ready
**Then** console displays:
```
Distribution: {dist} (params)
Paths: M, Samples: N, ε: eps

Empirical mean: X.XXXXX
Empirical variance: X.XXXXX
Theoretical variance: X.XXXXX

Figures saved to: ./output/
```

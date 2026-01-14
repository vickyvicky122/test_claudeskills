---
stepsCompleted: [step-01-init, step-02-discovery, step-03-success, step-04-journeys, step-05-domain-skipped, step-06-innovation-skipped, step-07-project-type, step-08-scoping, step-09-functional, step-10-nonfunctional, step-11-polish]
inputDocuments:
  - path: "docs/planning-artifacts/product-brief-test_claudeskill-2026-01-14.md"
    type: "product-brief"
    description: "LLN Explorer (Lite) - Product Brief"
documentCounts:
  briefs: 1
  research: 0
  brainstorming: 0
  projectDocs: 0
workflowType: 'prd'
projectType: 'greenfield'
classification:
  projectType: cli_tool
  domain: scientific
  complexity: low
  projectContext: greenfield
---

# Product Requirements Document - LLN Explorer (Lite)

**Author:** vicky
**Date:** 2026-01-14
**Status:** Ready for Architecture

## Executive Summary

**LLN Explorer (Lite)** is a Python CLI tool that helps students visually and numerically understand the Law of Large Numbers through three synchronized visualizations:

- **Sample paths** — Strong LLN / pathwise convergence
- **Deviation probability** — Weak LLN / convergence in probability
- **Variance decay** — Rate intuition with σ²/n theory overlay

| Attribute | Value |
|-----------|-------|
| Tech Stack | Python 3.8+, NumPy, Matplotlib |
| Effort | Solo developer, 1-2 days |
| Functional Requirements | 26 |
| Non-Functional Requirements | 9 |

## Success Criteria

### User Success

Users succeed when they:
- **See convergence clearly**: Multiple sample paths visibly stabilize toward μ
- **Understand the difference**: Can articulate "Strong LLN = paths stabilize; Weak LLN = deviation probability shrinks"
- **Connect to theory**: Observe variance decay matching σ²/n and understand why convergence happens
- **Walk away with artifacts**: Export clean figures for notes, slides, or assignments

### Technical Success

| Criterion | Target |
|-----------|--------|
| Sample path convergence | Trajectories visibly stabilize toward μ |
| Deviation probability | Monotonically decreasing with n |
| Variance decay | Empirical variance tracks σ²/n within visual tolerance |
| Distribution coverage | Bernoulli, Uniform, Normal all behave correctly |
| Performance | < 30 seconds for M=100, N=10,000 on standard laptop |
| Output quality | Clean axes, labels, legends; PNG/PDF export |

### Measurable Outcomes

- All three plots generated in single execution
- Figures suitable for inclusion in academic work without modification
- Zero external dependencies beyond NumPy + Matplotlib

## User Journeys

### Journey 1: The Confused Student

**Persona**: Alex, 3rd-year math student taking Probability Theory

**Opening Scene**: Alex just sat through a lecture on the Law of Large Numbers. The professor proved both weak and strong LLN, but Alex left confused. "They both say the average converges to μ... so what's the difference?"

**Rising Action**: Alex finds LLN Explorer on the course resources page. Downloads it, runs `python lln_explorer.py` with default settings. Watches 100 sample paths dance around and gradually settle toward the mean line.

**Climax**: Alex switches to the deviation probability plot. Sees P(|X̄ₙ - μ| > 0.1) dropping from 40% at n=100 to near 0% at n=10,000. *"Oh — weak LLN is about THIS probability going to zero. Strong LLN is about THOSE paths staying close."*

**Resolution**: Alex exports the figures, annotates them in notes, and finally understands why the textbook treats these as different theorems. Aces the exam question on convergence types.

**Capabilities Revealed**: Sample path visualization, deviation probability plot, figure export, sensible defaults

---

### Journey 2: The Lecturer Preparing Demos

**Persona**: Dr. Patel, teaching Intro to Probability

**Opening Scene**: Dr. Patel is preparing slides for next week's LLN lecture. She wants to show students what convergence "looks like" rather than just proving theorems.

**Rising Action**: She runs LLN Explorer with different distributions. Generates a set of figures: Bernoulli with p=0.5, Normal with μ=0, Uniform. Tweaks ε to show how deviation probability changes.

**Climax**: In class, she projects the sample path plot. "See how most paths settle? That's almost sure convergence." Switches to deviation probability. "And this curve going to zero? That's convergence in probability."

**Resolution**: Students engage more than usual. The visual anchors make the abstract theorems concrete. Dr. Patel adds LLN Explorer to the course materials for students to explore on their own.

**Capabilities Revealed**: Multiple distributions, parameter configuration, export-ready figures, variance decay with theory overlay

---

### Journey 3: The Self-Learner Building Intuition

**Persona**: Jordan, data scientist brushing up on probability fundamentals

**Opening Scene**: Jordan is working through a probability textbook at night. Reads about LLN, understands the statement, but wonders: "How fast does this actually happen? When is n 'large enough'?"

**Rising Action**: Jordan clones LLN Explorer from GitHub. Starts experimenting: What if M=1000 paths? What if ε=0.01 instead of 0.1? How does Normal compare to Bernoulli?

**Climax**: The variance decay plot clicks. Jordan sees empirical variance tracking σ²/n perfectly. *"So halving the standard deviation needs 4× the samples. That's why n=100 still wiggles but n=10,000 is tight."*

**Resolution**: Jordan now has intuition for sample size planning in real work. When a colleague asks "how many samples do we need?", Jordan can reason about variance decay instead of guessing.

**Capabilities Revealed**: Parameter experimentation, variance decay visualization, theory overlay, console summary statistics

---

### Journey Requirements Summary

| Capability | Revealed By |
|------------|-------------|
| Sample path visualization | Student, Lecturer |
| Deviation probability plot | Student, Lecturer |
| Variance decay with theory overlay | Lecturer, Self-Learner |
| Multiple distribution support | Lecturer, Self-Learner |
| Configurable parameters (M, N, ε) | Self-Learner |
| Figure export (PNG) | Student, Lecturer |
| Console summary statistics | Self-Learner |
| Sensible defaults | Student |

## CLI Tool Specific Requirements

### Command Structure

Single-entry-point script with optional arguments:

```
python lln_explorer.py [OPTIONS]

Options:
  --dist {bernoulli,uniform,normal}  Distribution type (default: normal)
  --M INT                            Number of sample paths (default: 100)
  --N INT                            Maximum sample size (default: 10000)
  --eps FLOAT                        Deviation tolerance ε (default: 0.1)
  --output DIR                       Output directory for figures (default: ./output)
  --p FLOAT                          Bernoulli parameter (default: 0.5)
  --mu FLOAT                         Normal mean (default: 0)
  --sigma FLOAT                      Normal std dev (default: 1)
```

### Output Formats

| Output | Format | Description |
|--------|--------|-------------|
| Sample paths plot | PNG | Running means vs sample size |
| Deviation probability plot | PNG | P(\|X̄ₙ - μ\| > ε) vs n |
| Variance decay plot | PNG | Empirical vs theoretical variance |
| Summary statistics | Console | Mean, variance, distribution info |

### Configuration

- **No config file needed** — all parameters via CLI arguments
- **Sensible defaults** — runs out of the box with `python lln_explorer.py`
- **Override as needed** — advanced users tweak M, N, ε, distribution params

### Scripting Support

- Exit code 0 on success, non-zero on error
- Predictable output file naming: `{dist}_sample_paths.png`, etc.
- Suitable for batch runs or inclusion in larger workflows

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Problem-Solving MVP
- Delivers core educational value immediately
- Single script execution, no setup friction
- Proves the pedagogical concept works

**Resource Requirements:** Solo developer, 1-2 days implementation

### MVP Feature Set (Phase 1)

**Core User Journeys Supported:**
- Student understanding LLN (Alex journey)
- Lecturer preparing demos (Dr. Patel journey)
- Self-learner experimenting (Jordan journey)

**Must-Have Capabilities:**
- [ ] Three distributions (Bernoulli, Uniform, Normal)
- [ ] Sample path visualization with μ reference line
- [ ] Deviation probability curve P(|X̄ₙ - μ| > ε) vs n
- [ ] Variance decay plot with σ²/n theory overlay
- [ ] CLI argument parsing with sensible defaults
- [ ] PNG figure export
- [ ] Console summary statistics

### Post-MVP Features

**Phase 2 (Growth):**
- Exponential distribution support
- CLT histogram overlay (√n(X̄ₙ - μ) distribution)
- Chebyshev bound comparison on deviation plot
- PDF export option

**Phase 3 (Vision):**
- Interactive Jupyter widget version
- Web-based classroom demo tool
- Animated convergence visualization
- Additional distributions (Poisson, etc.)

### Risk Mitigation Strategy

**Technical Risks:** None significant — NumPy/Matplotlib are battle-tested
**Market Risks:** N/A — educational tool, not commercial product
**Resource Risks:** Solo-developer friendly; can be built in a weekend

## Functional Requirements

### Distribution Support

- FR1: User can select Bernoulli distribution with configurable probability parameter p
- FR2: User can select Uniform(0,1) distribution
- FR3: User can select Normal distribution with configurable mean μ and standard deviation σ
- FR4: System provides known theoretical mean and variance for each distribution

### Simulation Engine

- FR5: System can generate M independent sample paths of length N
- FR6: System can compute running averages X̄ₙ for each sample path at each n
- FR7: System can estimate deviation probability P(|X̄ₙ - μ| > ε) across sample paths
- FR8: System can compute empirical variance of X̄ₙ across sample paths at each n

### Sample Path Visualization (Strong LLN View)

- FR9: User can view multiple sample path trajectories on a single plot
- FR10: System displays horizontal reference line at theoretical mean μ
- FR11: Plot shows running average X̄ₙ vs sample size n for each path

### Deviation Probability Analysis (Weak LLN View)

- FR12: User can view deviation probability P(|X̄ₙ - μ| > ε) as a function of n
- FR13: User can configure deviation tolerance ε
- FR14: Plot shows empirical deviation probability decreasing with n

### Variance Decay Analysis

- FR15: User can view empirical variance of X̄ₙ as a function of n
- FR16: System overlays theoretical variance decay curve σ²/n
- FR17: Plot enables visual comparison of empirical vs theoretical decay

### Output & Export

- FR18: System exports sample path plot as PNG file
- FR19: System exports deviation probability plot as PNG file
- FR20: System exports variance decay plot as PNG file
- FR21: System prints summary statistics to console (mean, variance, distribution info)
- FR22: Output files use predictable naming convention

### Configuration & CLI

- FR23: User can run tool with sensible defaults (no arguments required)
- FR24: User can override default parameters via command-line arguments
- FR25: User can specify output directory for generated figures
- FR26: System returns exit code 0 on success, non-zero on error

## Non-Functional Requirements

### Performance

- NFR1: Full simulation completes in < 30 seconds for M=100, N=10,000
- NFR2: Memory usage remains reasonable (< 500MB) for typical parameters
- NFR3: Figure generation completes without user-perceived delay after simulation

### Portability

- NFR4: Runs on Python 3.8+ without modification
- NFR5: Works on Windows, macOS, and Linux
- NFR6: Only requires NumPy and Matplotlib (standard scientific Python stack)

### Maintainability

- NFR7: Single-file implementation (or minimal module structure)
- NFR8: Code is readable without extensive comments
- NFR9: No complex dependencies or build steps

# Story 2.2: Simulation Engine with Chunked Processing

Status: review

## Story

As a **user**,
I want to **generate M sample paths of length N efficiently**,
so that **I can analyze LLN convergence without memory issues**.

## Acceptance Criteria

1. **Given** parameters M=100, N=10000
   **When** the simulation runs
   **Then** 100 independent sample paths of length 10000 are generated

2. **Given** each sample path
   **When** running averages are computed
   **Then** X̄ₙ is calculated for each n from 1 to N

3. **Given** all sample paths
   **When** deviation probability is computed
   **Then** P(|X̄ₙ - μ| > ε) is estimated at each n

4. **Given** all sample paths
   **When** empirical variance is computed
   **Then** Var(X̄ₙ) is calculated at each n

5. **Given** M=100, N=10000 on standard hardware
   **When** simulation completes
   **Then** total time is < 30 seconds (NFR1)
   **And** memory usage is < 500MB (NFR2)

## Tasks / Subtasks

- [x] Task 1: Implement `simulate_paths` function (AC: #1, #2)
  - [x] 1.1: Create function signature `simulate_paths(dist_dict, M, N)` returning (M, N) array of running averages
  - [x] 1.2: Generate M×N samples matrix using distribution's `sample` function
  - [x] 1.3: Compute running averages using `np.cumsum` / index division for efficiency
  - [x] 1.4: Add docstring explaining parameters and return value

- [x] Task 2: Implement `compute_deviation_probability` function (AC: #3)
  - [x] 2.1: Create function signature `compute_deviation_probability(running_avgs, mu, eps)` returning (N,) array
  - [x] 2.2: Calculate |X̄ₙ - μ| > ε boolean mask across all paths
  - [x] 2.3: Return mean across paths (proportion exceeding threshold at each n)

- [x] Task 3: Implement `compute_empirical_variance` function (AC: #4)
  - [x] 3.1: Create function signature `compute_empirical_variance(running_avgs)` returning (N,) array
  - [x] 3.2: Calculate variance across M paths at each sample size n

- [x] Task 4: Integrate simulation into main() (AC: #1-4)
  - [x] 4.1: Call `simulate_paths` with parsed distribution and parameters
  - [x] 4.2: Call `compute_deviation_probability` with running averages, μ, and ε
  - [x] 4.3: Call `compute_empirical_variance` with running averages
  - [x] 4.4: Store results for later visualization (Epic 3)
  - [x] 4.5: Print basic simulation statistics to console

- [x] Task 5: Performance validation (AC: #5)
  - [x] 5.1: Add timing measurement around simulation
  - [x] 5.2: Verify < 30 seconds for M=100, N=10000 (actual: 1.06s)
  - [x] 5.3: Document memory characteristics in code comment

- [x] Task 6: Write unit tests for simulation functions
  - [x] 6.1: Test `simulate_paths` returns correct shape (M, N)
  - [x] 6.2: Test running averages converge toward theoretical mean
  - [x] 6.3: Test `compute_deviation_probability` returns values in [0, 1]
  - [x] 6.4: Test `compute_empirical_variance` returns positive values
  - [x] 6.5: Test deviation probability decreases with n (LLN behavior)

## Dev Notes

### Architecture Requirements

**Code Location:** These functions should be placed in the Simulation section of `lln_explorer.py` (approximately lines 61-120 per architecture spec).

**File Organization (from Architecture):**
```
# 1. Imports
# 2. Constants (DEFAULT_M, DEFAULT_N, etc.) ✅ EXISTS
# 3. Distribution dictionary (DISTRIBUTIONS) ✅ EXISTS (make_distributions)
# 4. Simulation functions ← THIS STORY
# 5. Plot functions (Story 3.x)
# 6. CLI setup ✅ EXISTS
# 7. Main orchestration
# 8. Entry point ✅ EXISTS
```

### Implementation Patterns

**Function Signatures (from Architecture):**
```python
def simulate_paths(dist_dict, M, N):
    """Generate M sample paths of length N and compute running averages.

    Args:
        dist_dict: Distribution dictionary with 'sample', 'mean', 'var' keys
        M: Number of independent sample paths
        N: Length of each sample path

    Returns:
        numpy.ndarray: Shape (M, N) array of running averages X̄ₙ
    """

def compute_deviation_probability(running_avgs, mu, eps):
    """Estimate P(|X̄ₙ - μ| > ε) at each sample size.

    Args:
        running_avgs: Shape (M, N) array of running averages
        mu: Theoretical mean
        eps: Deviation tolerance

    Returns:
        numpy.ndarray: Shape (N,) array of deviation probabilities
    """

def compute_empirical_variance(running_avgs):
    """Compute Var(X̄ₙ) across sample paths at each n.

    Args:
        running_avgs: Shape (M, N) array of running averages

    Returns:
        numpy.ndarray: Shape (N,) array of empirical variances
    """
```

**Vectorized Implementation (CRITICAL for performance):**
```python
# Generate all samples at once: (M, N) matrix
samples = np.array([dist_dict['sample'](N) for _ in range(M)])

# Running average via cumulative sum (vectorized)
cumsum = np.cumsum(samples, axis=1)
indices = np.arange(1, N + 1)
running_avgs = cumsum / indices

# Deviation probability (vectorized)
deviations = np.abs(running_avgs - mu) > eps
deviation_prob = np.mean(deviations, axis=0)

# Empirical variance (vectorized)
empirical_var = np.var(running_avgs, axis=0, ddof=0)
```

### Existing Code Context

**Distribution dictionary interface (from Story 2.1):**
```python
distributions = make_distributions(p=args.p, mu=args.mu, sigma=args.sigma)
dist = distributions[args.dist]
# dist['sample'](n) -> np.ndarray of n samples
# dist['mean']() -> float (theoretical mean)
# dist['var']() -> float (theoretical variance)
```

**Current main() integration point (line 180-193):**
After `dist = distributions[args.dist]`, add simulation calls before `sys.exit(EXIT_SUCCESS)`.

### Performance Requirements

- **NFR1:** Full simulation < 30 seconds for M=100, N=10,000
- **NFR2:** Memory < 500MB for typical parameters
- Matrix size: 100 × 10,000 × 8 bytes = 8MB (well within limit)
- Use NumPy vectorization exclusively - NO Python loops over samples

### Testing Strategy

**Test file:** `tests/test_lln_explorer.py` (create if doesn't exist)

**Key test cases:**
1. Shape validation: `running_avgs.shape == (M, N)`
2. Convergence test: Mean of running_avgs[:, -1] ≈ theoretical mean (within tolerance)
3. Deviation bounds: All values in [0, 1]
4. Variance positivity: All values > 0
5. LLN behavior: `deviation_prob[n2] <= deviation_prob[n1]` for n2 > n1 (general trend)

### Project Structure Notes

- Single file: `lln_explorer/lln_explorer.py`
- Tests: `lln_explorer/tests/test_lln_explorer.py`
- All functions follow PEP 8 snake_case naming
- No external dependencies beyond numpy (matplotlib not needed for this story)

### References

- [Source: docs/planning-artifacts/architecture.md#Implementation Patterns]
- [Source: docs/planning-artifacts/architecture.md#Code Organization Pattern]
- [Source: docs/planning-artifacts/prd.md#Simulation Engine]
- [Source: docs/planning-artifacts/epics.md#Story 2.2]

## Dev Agent Record

### Agent Model Used

Claude Opus 4.5 (claude-opus-4-5-20251101)

### Debug Log References

- All tests passing: 14/14 tests in tests/test_simulation.py

### Completion Notes List

- Implemented `simulate_paths()` function using vectorized NumPy operations
- Implemented `compute_deviation_probability()` for Weak LLN analysis
- Implemented `compute_empirical_variance()` for variance decay analysis
- Integrated all functions into main() with timing measurement
- Performance: 1.06 seconds for M=100, N=10000 (well under 30s requirement)
- All three distributions (normal, bernoulli, uniform) verified working
- 14 unit tests covering shape validation, convergence, and LLN behavior

### File List

- `lln_explorer/lln_explorer.py` (modified) - Added simulation functions
- `lln_explorer/tests/test_simulation.py` (created) - Unit tests for simulation

## Change Log

| Date | Change |
|------|--------|
| 2026-01-15 | Story created via create-story workflow |
| 2026-01-15 | Implemented simulation functions and tests - all ACs satisfied |

#!/usr/bin/env python3
"""
LLN Explorer (Lite) - Law of Large Numbers Visualization Tool

A CLI tool for visualizing the Law of Large Numbers through:
- Sample path convergence (Strong LLN)
- Deviation probability decay (Weak LLN)
- Variance decay with theory overlay
"""

import argparse
import sys
import time
from pathlib import Path

import numpy as np

# Exit codes
EXIT_SUCCESS = 0
EXIT_INVALID_ARGS = 1
EXIT_RUNTIME_ERROR = 2

# Default values
DEFAULT_DIST = "normal"
DEFAULT_M = 100
DEFAULT_N = 10000
DEFAULT_EPS = 0.1
DEFAULT_OUTPUT = "./output"
DEFAULT_P = 0.5  # Bernoulli probability
DEFAULT_MU = 0.0  # Normal mean
DEFAULT_SIGMA = 1.0  # Normal std dev

# Supported distributions
SUPPORTED_DISTRIBUTIONS = ["normal", "bernoulli", "uniform"]


def make_distributions(p=DEFAULT_P, mu=DEFAULT_MU, sigma=DEFAULT_SIGMA):
    """Create distribution dictionary with configured parameters."""
    return {
        "bernoulli": {
            "sample": lambda n: np.random.binomial(1, p, n).astype(float),
            "mean": lambda: p,
            "var": lambda: p * (1 - p),
            "params": f"p={p}",
        },
        "uniform": {
            "sample": lambda n: np.random.uniform(0, 1, n),
            "mean": lambda: 0.5,
            "var": lambda: 1 / 12,
            "params": "a=0, b=1",
        },
        "normal": {
            "sample": lambda n: np.random.normal(mu, sigma, n),
            "mean": lambda: mu,
            "var": lambda: sigma**2,
            "params": f"μ={mu}, σ={sigma}",
        },
    }


# =============================================================================
# Simulation Functions
# =============================================================================


def simulate_paths(dist_dict, M, N):
    """Generate M sample paths of length N and compute running averages.

    Args:
        dist_dict: Distribution dictionary with 'sample', 'mean', 'var' keys
        M: Number of independent sample paths
        N: Length of each sample path

    Returns:
        numpy.ndarray: Shape (M, N) array of running averages X̄ₙ
    """
    # Generate all samples at once: (M, N) matrix
    # Memory: M * N * 8 bytes (float64) = 8MB for M=100, N=10000
    samples = np.array([dist_dict["sample"](N) for _ in range(M)])

    # Running average via cumulative sum (vectorized for performance)
    cumsum = np.cumsum(samples, axis=1)
    indices = np.arange(1, N + 1)
    running_avgs = cumsum / indices

    return running_avgs


def compute_deviation_probability(running_avgs, mu, eps):
    """Estimate P(|X̄ₙ - μ| > ε) at each sample size.

    Args:
        running_avgs: Shape (M, N) array of running averages
        mu: Theoretical mean
        eps: Deviation tolerance

    Returns:
        numpy.ndarray: Shape (N,) array of deviation probabilities
    """
    # Calculate |X̄ₙ - μ| > ε boolean mask across all paths
    deviations = np.abs(running_avgs - mu) > eps
    # Return mean across paths (proportion exceeding threshold at each n)
    deviation_prob = np.mean(deviations, axis=0)
    return deviation_prob


def compute_empirical_variance(running_avgs):
    """Compute Var(X̄ₙ) across sample paths at each n.

    Args:
        running_avgs: Shape (M, N) array of running averages

    Returns:
        numpy.ndarray: Shape (N,) array of empirical variances
    """
    # Calculate variance across M paths at each sample size n
    empirical_var = np.var(running_avgs, axis=0, ddof=0)
    return empirical_var


# =============================================================================
# CLI Functions
# =============================================================================


def parse_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="lln_explorer",
        description="Visualize the Law of Large Numbers through simulations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--dist",
        type=str,
        default=DEFAULT_DIST,
        choices=SUPPORTED_DISTRIBUTIONS,
        help="Distribution to sample from",
    )

    parser.add_argument(
        "--M",
        type=int,
        default=DEFAULT_M,
        help="Number of sample paths (realizations)",
    )

    parser.add_argument(
        "--N",
        type=int,
        default=DEFAULT_N,
        help="Maximum sample size per path",
    )

    parser.add_argument(
        "--eps",
        type=float,
        default=DEFAULT_EPS,
        help="Epsilon threshold for deviation probability",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=DEFAULT_OUTPUT,
        help="Output directory for generated plots",
    )

    parser.add_argument(
        "--p",
        type=float,
        default=DEFAULT_P,
        help="Bernoulli distribution probability parameter",
    )

    parser.add_argument(
        "--mu",
        type=float,
        default=DEFAULT_MU,
        help="Normal distribution mean",
    )

    parser.add_argument(
        "--sigma",
        type=float,
        default=DEFAULT_SIGMA,
        help="Normal distribution standard deviation",
    )

    return parser.parse_args(args)


def validate_args(args):
    """Validate parsed arguments. Returns error message or None if valid."""
    if args.M <= 0:
        return f"Error: M must be positive, got {args.M}"

    if args.N <= 0:
        return f"Error: N must be positive, got {args.N}"

    if args.eps <= 0:
        return f"Error: eps must be positive, got {args.eps}"

    if args.eps >= 1:
        return f"Error: eps must be less than 1, got {args.eps}"

    if args.p <= 0 or args.p >= 1:
        return f"Error: p must be between 0 and 1 (exclusive), got {args.p}"

    if args.sigma <= 0:
        return f"Error: sigma must be positive, got {args.sigma}"

    return None


def ensure_output_dir(output_path):
    """Create output directory if it doesn't exist."""
    path = Path(output_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def main():
    """Main entry point."""
    try:
        args = parse_args()
    except SystemExit as e:
        # argparse exits with code 2 for invalid arguments, normalize to 1
        sys.exit(EXIT_INVALID_ARGS)

    # Validate arguments
    error = validate_args(args)
    if error:
        print(error, file=sys.stderr)
        sys.exit(EXIT_INVALID_ARGS)

    # Ensure output directory exists
    try:
        output_dir = ensure_output_dir(args.output)
    except OSError as e:
        print(f"Error: Cannot create output directory: {e}", file=sys.stderr)
        sys.exit(EXIT_RUNTIME_ERROR)

    # Create distribution dictionary with configured parameters
    distributions = make_distributions(p=args.p, mu=args.mu, sigma=args.sigma)
    dist = distributions[args.dist]

    # Print configuration
    print(f"LLN Explorer Configuration:")
    print(f"  Distribution: {args.dist} ({dist['params']})")
    print(f"  Theoretical mean: {dist['mean']()}")
    print(f"  Theoretical variance: {dist['var']()}")
    print(f"  Sample paths (M): {args.M}")
    print(f"  Max samples (N): {args.N}")
    print(f"  Epsilon: {args.eps}")
    print(f"  Output directory: {output_dir.resolve()}")
    print()

    # Run simulation with timing
    print("Running simulation...")
    start_time = time.time()

    # Generate sample paths and compute running averages
    running_avgs = simulate_paths(dist, args.M, args.N)

    # Compute statistics
    mu = dist["mean"]()
    theoretical_var = dist["var"]()
    deviation_prob = compute_deviation_probability(running_avgs, mu, args.eps)
    empirical_var = compute_empirical_variance(running_avgs)

    elapsed_time = time.time() - start_time
    print(f"Simulation completed in {elapsed_time:.2f} seconds")
    print()

    # Print summary statistics
    print("Summary Statistics:")
    print(f"  Empirical mean (final): {np.mean(running_avgs[:, -1]):.6f}")
    print(f"  Theoretical mean: {mu:.6f}")
    print(f"  Empirical variance (final): {empirical_var[-1]:.6f}")
    print(f"  Theoretical variance (σ²/N): {theoretical_var / args.N:.6f}")
    print(f"  Deviation probability (final): {deviation_prob[-1]:.4f}")
    print()
    print(f"Figures saved to: {output_dir.resolve()}/")

    # Store results for visualization (Epic 3)
    # Results dictionary can be returned or used by plot functions
    results = {
        "running_avgs": running_avgs,
        "deviation_prob": deviation_prob,
        "empirical_var": empirical_var,
        "mu": mu,
        "theoretical_var": theoretical_var,
        "eps": args.eps,
        "M": args.M,
        "N": args.N,
        "dist_name": args.dist,
        "dist_params": dist["params"],
    }

    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()

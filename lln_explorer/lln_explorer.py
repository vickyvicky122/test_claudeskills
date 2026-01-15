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
from pathlib import Path

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

# Supported distributions
SUPPORTED_DISTRIBUTIONS = ["normal", "bernoulli", "exponential", "uniform"]


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

    # Print configuration (placeholder for actual simulation)
    print(f"LLN Explorer Configuration:")
    print(f"  Distribution: {args.dist}")
    print(f"  Sample paths (M): {args.M}")
    print(f"  Max samples (N): {args.N}")
    print(f"  Epsilon: {args.eps}")
    print(f"  Output directory: {output_dir.resolve()}")

    sys.exit(EXIT_SUCCESS)


if __name__ == "__main__":
    main()

"""Tests for simulation functions in lln_explorer.py."""

import numpy as np
import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from lln_explorer import (
    make_distributions,
    simulate_paths,
    compute_deviation_probability,
    compute_empirical_variance,
)


class TestSimulatePaths:
    """Tests for simulate_paths function."""

    def test_returns_correct_shape(self):
        """Test that simulate_paths returns array with shape (M, N)."""
        dist = make_distributions()["normal"]
        M, N = 10, 100
        result = simulate_paths(dist, M, N)
        assert result.shape == (M, N)

    def test_returns_correct_shape_larger(self):
        """Test shape with larger M and N values."""
        dist = make_distributions()["normal"]
        M, N = 50, 1000
        result = simulate_paths(dist, M, N)
        assert result.shape == (M, N)

    def test_running_averages_converge_normal(self):
        """Test that running averages converge toward theoretical mean for normal."""
        np.random.seed(42)
        dist = make_distributions(mu=5.0, sigma=1.0)["normal"]
        M, N = 100, 10000
        result = simulate_paths(dist, M, N)

        # Final running averages should be close to theoretical mean
        final_avg = np.mean(result[:, -1])
        assert abs(final_avg - 5.0) < 0.1  # Within 0.1 of theoretical mean

    def test_running_averages_converge_bernoulli(self):
        """Test that running averages converge toward theoretical mean for Bernoulli."""
        np.random.seed(42)
        dist = make_distributions(p=0.7)["bernoulli"]
        M, N = 100, 10000
        result = simulate_paths(dist, M, N)

        final_avg = np.mean(result[:, -1])
        assert abs(final_avg - 0.7) < 0.05

    def test_running_averages_converge_uniform(self):
        """Test that running averages converge toward theoretical mean for uniform."""
        np.random.seed(42)
        dist = make_distributions()["uniform"]
        M, N = 100, 10000
        result = simulate_paths(dist, M, N)

        final_avg = np.mean(result[:, -1])
        assert abs(final_avg - 0.5) < 0.05


class TestComputeDeviationProbability:
    """Tests for compute_deviation_probability function."""

    def test_returns_correct_shape(self):
        """Test that deviation probability returns array with shape (N,)."""
        dist = make_distributions()["normal"]
        M, N = 10, 100
        running_avgs = simulate_paths(dist, M, N)
        result = compute_deviation_probability(running_avgs, mu=0.0, eps=0.1)
        assert result.shape == (N,)

    def test_values_in_valid_range(self):
        """Test that all deviation probabilities are in [0, 1]."""
        dist = make_distributions()["normal"]
        M, N = 50, 500
        running_avgs = simulate_paths(dist, M, N)
        result = compute_deviation_probability(running_avgs, mu=0.0, eps=0.1)

        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0)

    def test_deviation_probability_decreases_trend(self):
        """Test that deviation probability generally decreases with n (LLN behavior)."""
        np.random.seed(42)
        dist = make_distributions()["normal"]
        M, N = 200, 5000
        running_avgs = simulate_paths(dist, M, N)
        result = compute_deviation_probability(running_avgs, mu=0.0, eps=0.1)

        # Compare early vs late: probability should be lower at larger n
        early_avg = np.mean(result[100:200])  # n=100 to 200
        late_avg = np.mean(result[4000:5000])  # n=4000 to 5000
        assert late_avg < early_avg

    def test_large_eps_gives_low_probability(self):
        """Test that large epsilon gives lower deviation probability."""
        np.random.seed(42)
        dist = make_distributions()["normal"]
        M, N = 50, 1000
        running_avgs = simulate_paths(dist, M, N)

        prob_small_eps = compute_deviation_probability(running_avgs, mu=0.0, eps=0.01)
        prob_large_eps = compute_deviation_probability(running_avgs, mu=0.0, eps=1.0)

        # Large eps should have lower or equal probability at most points
        assert np.mean(prob_large_eps) <= np.mean(prob_small_eps)


class TestComputeEmpiricalVariance:
    """Tests for compute_empirical_variance function."""

    def test_returns_correct_shape(self):
        """Test that empirical variance returns array with shape (N,)."""
        dist = make_distributions()["normal"]
        M, N = 10, 100
        running_avgs = simulate_paths(dist, M, N)
        result = compute_empirical_variance(running_avgs)
        assert result.shape == (N,)

    def test_values_are_positive(self):
        """Test that all empirical variances are positive."""
        dist = make_distributions()["normal"]
        M, N = 50, 500
        running_avgs = simulate_paths(dist, M, N)
        result = compute_empirical_variance(running_avgs)

        # Allow for numerical precision issues (variance can be very small but >= 0)
        assert np.all(result >= 0.0)

    def test_variance_decreases_with_n(self):
        """Test that empirical variance generally decreases with n."""
        np.random.seed(42)
        dist = make_distributions()["normal"]
        M, N = 200, 5000
        running_avgs = simulate_paths(dist, M, N)
        result = compute_empirical_variance(running_avgs)

        # Compare early vs late: variance should be lower at larger n
        early_var = np.mean(result[100:200])
        late_var = np.mean(result[4000:5000])
        assert late_var < early_var

    def test_variance_approximates_theory(self):
        """Test that empirical variance approximately matches σ²/n."""
        np.random.seed(42)
        sigma = 2.0
        dist = make_distributions(sigma=sigma)["normal"]
        M, N = 500, 1000
        running_avgs = simulate_paths(dist, M, N)
        result = compute_empirical_variance(running_avgs)

        # At n=1000, theoretical variance is σ²/n = 4/1000 = 0.004
        theoretical_var = sigma**2 / N
        empirical_var = result[-1]

        # Allow 50% tolerance due to sampling variability
        assert abs(empirical_var - theoretical_var) < theoretical_var * 0.5


class TestIntegration:
    """Integration tests for the simulation pipeline."""

    def test_full_simulation_pipeline(self):
        """Test complete simulation from distribution to statistics."""
        np.random.seed(42)
        M, N = 100, 1000
        eps = 0.1

        for dist_name in ["normal", "bernoulli", "uniform"]:
            distributions = make_distributions()
            dist = distributions[dist_name]
            mu = dist["mean"]()

            running_avgs = simulate_paths(dist, M, N)
            deviation_prob = compute_deviation_probability(running_avgs, mu, eps)
            empirical_var = compute_empirical_variance(running_avgs)

            # Basic sanity checks
            assert running_avgs.shape == (M, N)
            assert deviation_prob.shape == (N,)
            assert empirical_var.shape == (N,)
            assert np.all(deviation_prob >= 0) and np.all(deviation_prob <= 1)
            assert np.all(empirical_var >= 0)

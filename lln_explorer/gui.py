#!/usr/bin/env python3
"""
LLN Explorer GUI - Streamlit-based interface for Law of Large Numbers visualization.

Run with: streamlit run lln_explorer/gui.py
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Import simulation functions from CLI module
from lln_explorer import (
    compute_deviation_probability,
    compute_empirical_variance,
    make_distributions,
    simulate_paths,
)

# Page configuration
st.set_page_config(
    page_title="LLN Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Supported distributions
SUPPORTED_DISTRIBUTIONS = ["normal", "bernoulli", "uniform"]

# Default values (matching CLI defaults)
DEFAULT_DIST = "normal"
DEFAULT_M = 100
DEFAULT_N = 10000
DEFAULT_EPS = 0.1
DEFAULT_P = 0.5
DEFAULT_MU = 0.0
DEFAULT_SIGMA = 1.0


def init_session_state():
    """Initialize session state with default values."""
    defaults = {
        "dist": DEFAULT_DIST,
        "M": DEFAULT_M,
        "N": DEFAULT_N,
        "eps": DEFAULT_EPS,
        "p": DEFAULT_P,
        "mu": DEFAULT_MU,
        "sigma": DEFAULT_SIGMA,
        "simulation_run": False,
        "running_avgs": None,
        "log_scale_x": True,
        "log_scale_deviation": True,
        "show_chebyshev": True,
        "log_scale_variance": True,
        "show_theoretical_variance": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    """Render sidebar with all parameter controls."""
    st.sidebar.header("Simulation Parameters")

    # Distribution selector
    dist = st.sidebar.selectbox(
        "Distribution",
        options=SUPPORTED_DISTRIBUTIONS,
        index=SUPPORTED_DISTRIBUTIONS.index(st.session_state.dist),
        help="Select the probability distribution to sample from",
        key="dist_select",
    )
    st.session_state.dist = dist

    st.sidebar.divider()

    # General parameters
    st.sidebar.subheader("Sample Configuration")

    M = st.sidebar.slider(
        "Number of Sample Paths (M)",
        min_value=10,
        max_value=500,
        value=st.session_state.M,
        step=10,
        help="Number of independent sample paths to generate",
        key="M_slider",
    )
    st.session_state.M = M

    N = st.sidebar.slider(
        "Max Sample Size (N)",
        min_value=1000,
        max_value=50000,
        value=st.session_state.N,
        step=1000,
        help="Maximum number of samples per path",
        key="N_slider",
    )
    st.session_state.N = N

    eps = st.sidebar.slider(
        "Epsilon Threshold (ε)",
        min_value=0.01,
        max_value=0.5,
        value=st.session_state.eps,
        step=0.01,
        format="%.2f",
        help="Deviation threshold for P(|X̄ₙ - μ| > ε)",
        key="eps_slider",
    )
    st.session_state.eps = eps

    st.sidebar.divider()

    # Distribution-specific parameters
    st.sidebar.subheader("Distribution Parameters")

    if dist == "normal":
        mu = st.sidebar.number_input(
            "Mean (μ)",
            value=st.session_state.mu,
            step=0.1,
            format="%.2f",
            help="Mean of the normal distribution",
            key="mu_input",
        )
        st.session_state.mu = mu

        sigma = st.sidebar.number_input(
            "Standard Deviation (σ)",
            min_value=0.01,
            value=st.session_state.sigma,
            step=0.1,
            format="%.2f",
            help="Standard deviation of the normal distribution",
            key="sigma_input",
        )
        st.session_state.sigma = sigma

        st.sidebar.info(f"X ~ N({mu}, {sigma}²)")

    elif dist == "bernoulli":
        p = st.sidebar.slider(
            "Success Probability (p)",
            min_value=0.01,
            max_value=0.99,
            value=st.session_state.p,
            step=0.01,
            format="%.2f",
            help="Probability of success (1) in each trial",
            key="p_slider",
        )
        st.session_state.p = p

        st.sidebar.info(f"X ~ Bernoulli({p})")

    elif dist == "uniform":
        st.sidebar.info("X ~ Uniform(0, 1)")
        st.sidebar.caption("Fixed parameters: a=0, b=1")

    st.sidebar.divider()

    # Run simulation button
    run_clicked = st.sidebar.button(
        "Run Simulation",
        type="primary",
        use_container_width=True,
        help="Run the simulation with current parameters",
    )

    if run_clicked:
        st.session_state.simulation_run = True
        # Clear cached results to force recomputation
        st.session_state.running_avgs = None

    return run_clicked


def get_distribution_info():
    """Get theoretical mean and variance for current distribution."""
    dist = st.session_state.dist

    if dist == "normal":
        mu = st.session_state.mu
        sigma = st.session_state.sigma
        return {
            "name": "Normal",
            "params": f"μ={mu}, σ={sigma}",
            "mean": mu,
            "variance": sigma**2,
        }
    elif dist == "bernoulli":
        p = st.session_state.p
        return {
            "name": "Bernoulli",
            "params": f"p={p}",
            "mean": p,
            "variance": p * (1 - p),
        }
    elif dist == "uniform":
        return {
            "name": "Uniform",
            "params": "a=0, b=1",
            "mean": 0.5,
            "variance": 1 / 12,
        }


def run_simulation():
    """Run the LLN simulation and cache results in session state."""
    if st.session_state.running_avgs is None:
        # Create distribution with current parameters
        distributions = make_distributions(
            p=st.session_state.p,
            mu=st.session_state.mu,
            sigma=st.session_state.sigma,
        )
        dist = distributions[st.session_state.dist]

        # Run simulation with progress indicator
        progress_text = "Running simulation..."
        progress_bar = st.progress(0, text=progress_text)

        # Simulate in chunks to show progress
        M = st.session_state.M
        N = st.session_state.N
        chunk_size = max(1, M // 10)  # 10 progress updates
        running_avgs_list = []

        for i in range(0, M, chunk_size):
            chunk_m = min(chunk_size, M - i)
            chunk_avgs = simulate_paths(dist, chunk_m, N)
            running_avgs_list.append(chunk_avgs)
            progress = min((i + chunk_m) / M, 1.0)
            progress_bar.progress(progress, text=f"Simulating paths... {int(progress * 100)}%")

        # Combine chunks
        running_avgs = np.vstack(running_avgs_list)
        st.session_state.running_avgs = running_avgs
        progress_bar.empty()

    return st.session_state.running_avgs


def plot_sample_paths(running_avgs, mu, dist_name, log_scale=True, compact=False):
    """Create sample paths plot showing Strong LLN convergence.

    Args:
        running_avgs: Shape (M, N) array of running averages
        mu: Theoretical mean
        dist_name: Name of the distribution
        log_scale: Whether to use log scale for x-axis
        compact: Whether to create a smaller plot for dashboard

    Returns:
        matplotlib figure
    """
    M, N = running_avgs.shape
    n_values = np.arange(1, N + 1)

    figsize = (5, 3.5) if compact else (10, 6)
    fig, ax = plt.subplots(figsize=figsize)

    # Plot all M sample paths with low alpha for visibility
    for i in range(M):
        ax.plot(n_values, running_avgs[i], alpha=0.3, linewidth=0.5)

    # Add horizontal reference line at theoretical mean
    ax.axhline(y=mu, color="red", linestyle="--", linewidth=2, label=f"μ = {mu:.4f}")

    # Configure axes
    fontsize_label = 9 if compact else 12
    fontsize_title = 10 if compact else 14
    fontsize_legend = 8 if compact else 10
    ax.set_xlabel("Sample size (n)", fontsize=fontsize_label)
    ax.set_ylabel("Running average X̄ₙ", fontsize=fontsize_label)
    title = "Sample Paths (Strong LLN)" if compact else (
        f"Sample Path Convergence - {dist_name.capitalize()} Distribution\n"
        f"({M} paths, Strong LLN)"
    )
    ax.set_title(title, fontsize=fontsize_title)
    ax.legend(loc="upper right", fontsize=fontsize_legend)
    ax.grid(True, alpha=0.3)

    # Use log scale for x-axis if enabled
    if log_scale:
        ax.set_xscale("log")

    plt.tight_layout()
    return fig


def render_sample_paths_tab():
    """Render the Sample Path Convergence tab with visualization and education."""
    dist_info = get_distribution_info()

    # Run simulation if needed
    running_avgs = run_simulation()

    # Visualization controls
    col1, col2 = st.columns([3, 1])
    with col2:
        log_scale = st.checkbox(
            "Log scale (x-axis)",
            value=st.session_state.log_scale_x,
            help="Use logarithmic scale for sample size axis",
            key="log_scale_sample_paths",
        )
        st.session_state.log_scale_x = log_scale

    # Create and display the plot
    fig = plot_sample_paths(
        running_avgs,
        dist_info["mean"],
        st.session_state.dist,
        log_scale=log_scale,
    )
    st.pyplot(fig)
    plt.close(fig)

    # Summary statistics
    st.subheader("Convergence Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        final_mean = np.mean(running_avgs[:, -1])
        st.metric(
            "Empirical Mean (final)",
            f"{final_mean:.6f}",
            delta=f"{final_mean - dist_info['mean']:.6f}",
        )
    with col2:
        st.metric("Theoretical Mean (μ)", f"{dist_info['mean']:.6f}")
    with col3:
        # Proportion of paths within epsilon of mu at final n
        within_eps = np.mean(np.abs(running_avgs[:, -1] - dist_info["mean"]) <= st.session_state.eps)
        st.metric(
            f"Paths within ε={st.session_state.eps}",
            f"{within_eps * 100:.1f}%",
        )

    st.divider()

    # Educational content
    render_strong_lln_education()


def render_strong_lln_education():
    """Render educational content about the Strong Law of Large Numbers."""
    st.subheader("Understanding the Strong Law of Large Numbers")

    # Main theorem statement
    st.markdown("""
    The **Strong Law of Large Numbers (SLLN)** is a fundamental theorem in probability theory
    that describes how sample averages converge to the expected value.
    """)

    # Formal statement with LaTeX
    with st.expander("Formal Statement", expanded=True):
        st.markdown("**Theorem (Strong Law of Large Numbers):**")
        st.markdown("""
        Let $X_1, X_2, X_3, \\ldots$ be a sequence of independent and identically distributed
        (i.i.d.) random variables with finite expected value $\\mu = E[X_i]$.
        """)

        st.markdown("Then the sample mean converges **almost surely** to $\\mu$:")

        st.latex(r"P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1")

        st.markdown("where the sample mean is defined as:")

        st.latex(r"\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i = \frac{X_1 + X_2 + \cdots + X_n}{n}")

    # Intuitive explanation
    with st.expander("Intuitive Explanation", expanded=True):
        st.markdown("""
        **What does "almost surely" mean?**

        The Strong LLN says that with probability 1 (i.e., almost surely), the running average
        of your samples will converge to the true mean $\\mu$.

        **In practical terms:**
        - As you collect more data, your sample average gets closer to the true population mean
        - The convergence is not just "likely" — it happens with probability 1
        - For almost every possible infinite sequence of outcomes, the average will eventually
          settle near $\\mu$ and stay there

        **What you see in the plot:**
        - Each colored line is one "sample path" — a sequence of running averages
        - Early on (small n), paths vary widely
        - As n increases, all paths converge toward the red dashed line (μ)
        - The "funnel" shape shows convergence: paths get increasingly concentrated around μ
        """)

    # Key formulas reference
    with st.expander("Key Formulas", expanded=False):
        st.markdown("**Sample Mean:**")
        st.latex(r"\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i")

        st.markdown("**Strong LLN Convergence:**")
        st.latex(r"\bar{X}_n \xrightarrow{a.s.} \mu \quad \text{as } n \to \infty")

        st.markdown("**Equivalent Statement:**")
        st.latex(r"P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1")

        st.markdown("**For this simulation:**")
        dist_info = get_distribution_info()
        if st.session_state.dist == "normal":
            st.latex(rf"\mu = {dist_info['mean']:.4f}, \quad \sigma^2 = {dist_info['variance']:.4f}")
        elif st.session_state.dist == "bernoulli":
            p = st.session_state.p
            st.latex(rf"\mu = p = {p:.4f}, \quad \sigma^2 = p(1-p) = {dist_info['variance']:.4f}")
        else:  # uniform
            st.latex(rf"\mu = \frac{{a+b}}{{2}} = 0.5, \quad \sigma^2 = \frac{{(b-a)^2}}{{12}} = {dist_info['variance']:.4f}")

    # Comparison with Weak LLN
    with st.expander("Strong vs Weak LLN", expanded=False):
        st.markdown("""
        | Property | Strong LLN | Weak LLN |
        |----------|-----------|----------|
        | **Convergence Type** | Almost sure | In probability |
        | **Statement** | $P(\\lim \\bar{X}_n = \\mu) = 1$ | $\\lim P(|\\bar{X}_n - \\mu| > \\varepsilon) = 0$ |
        | **Strength** | Stronger (implies Weak LLN) | Weaker |
        | **Interpretation** | Path-by-path convergence | Probabilistic convergence |

        The Strong LLN implies the Weak LLN, but not vice versa. The Strong LLN makes a
        statement about individual sample paths, while the Weak LLN makes a statement about
        the probability distribution of $\\bar{X}_n$.
        """)


def plot_deviation_probability(deviation_prob, eps, variance, dist_name, log_scale=True, show_chebyshev=True, compact=False):
    """Create deviation probability plot showing Weak LLN convergence.

    Args:
        deviation_prob: Shape (N,) array of P(|X̄ₙ - μ| > ε) at each n
        eps: Epsilon threshold used
        variance: Theoretical variance σ² of the distribution
        dist_name: Name of the distribution
        log_scale: Whether to use log scale for x-axis
        show_chebyshev: Whether to show Chebyshev bound overlay
        compact: Whether to create a smaller plot for dashboard

    Returns:
        matplotlib figure
    """
    N = len(deviation_prob)
    n_values = np.arange(1, N + 1)

    figsize = (5, 3.5) if compact else (10, 6)
    fig, ax = plt.subplots(figsize=figsize)

    # Plot empirical deviation probability
    ax.plot(
        n_values,
        deviation_prob,
        color="blue",
        linewidth=1.5,
        label=f"Empirical P(|X̄ₙ - μ| > {eps})",
    )

    # Plot Chebyshev bound if enabled
    if show_chebyshev:
        # Chebyshev bound: P(|X̄ₙ - μ| > ε) ≤ σ²/(nε²)
        chebyshev_bound = variance / (n_values * eps**2)
        # Clip to [0, 1] since it's a probability bound
        chebyshev_bound = np.clip(chebyshev_bound, 0, 1)
        ax.plot(
            n_values,
            chebyshev_bound,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Chebyshev bound: σ²/(nε²)",
        )

    # Configure axes
    fontsize_label = 9 if compact else 12
    fontsize_title = 10 if compact else 14
    fontsize_legend = 8 if compact else 10
    ax.set_xlabel("Sample size (n)", fontsize=fontsize_label)
    ax.set_ylabel("Deviation probability", fontsize=fontsize_label)
    title = "Deviation Probability (Weak LLN)" if compact else (
        f"Deviation Probability Decay - {dist_name.capitalize()} Distribution\n"
        f"(ε = {eps}, Weak LLN)"
    )
    ax.set_title(title, fontsize=fontsize_title)
    ax.legend(loc="upper right", fontsize=fontsize_legend)
    ax.grid(True, alpha=0.3)

    # Use log scale for x-axis if enabled
    if log_scale:
        ax.set_xscale("log")

    # Set y-axis limits
    ax.set_ylim(0, 1.05)

    # Add epsilon annotation (skip in compact mode)
    if not compact:
        ax.axhline(y=0, color="gray", linestyle="-", linewidth=0.5)
        ax.annotate(
            f"ε = {eps}",
            xy=(n_values[-1], 0.02),
            fontsize=10,
            color="darkblue",
            ha="right",
        )

    plt.tight_layout()
    return fig


def render_deviation_probability_tab():
    """Render the Deviation Probability tab with visualization and education."""
    dist_info = get_distribution_info()

    # Run simulation if needed
    running_avgs = run_simulation()

    # Compute deviation probability
    deviation_prob = compute_deviation_probability(
        running_avgs, dist_info["mean"], st.session_state.eps
    )

    # Visualization controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        log_scale = st.checkbox(
            "Log scale (x-axis)",
            value=st.session_state.log_scale_deviation,
            help="Use logarithmic scale for sample size axis",
            key="log_scale_deviation_checkbox",
        )
        st.session_state.log_scale_deviation = log_scale
    with col3:
        show_chebyshev = st.checkbox(
            "Show Chebyshev bound",
            value=st.session_state.show_chebyshev,
            help="Overlay theoretical Chebyshev upper bound",
            key="show_chebyshev_checkbox",
        )
        st.session_state.show_chebyshev = show_chebyshev

    # Create and display the plot
    fig = plot_deviation_probability(
        deviation_prob,
        st.session_state.eps,
        dist_info["variance"],
        st.session_state.dist,
        log_scale=log_scale,
        show_chebyshev=show_chebyshev,
    )
    st.pyplot(fig)
    plt.close(fig)

    # Summary statistics
    st.subheader("Deviation Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            f"P(|X̄ₙ - μ| > {st.session_state.eps}) at n={st.session_state.N}",
            f"{deviation_prob[-1]:.4f}",
        )
    with col2:
        # Chebyshev bound at final n
        chebyshev_final = min(1.0, dist_info["variance"] / (st.session_state.N * st.session_state.eps**2))
        st.metric(
            "Chebyshev bound (final)",
            f"{chebyshev_final:.4f}",
        )
    with col3:
        # Find n where deviation prob first drops below 0.05
        below_threshold = np.where(deviation_prob < 0.05)[0]
        if len(below_threshold) > 0:
            n_convergence = below_threshold[0] + 1
            st.metric("n where P < 0.05", f"{n_convergence:,}")
        else:
            st.metric("n where P < 0.05", "Not reached")

    st.divider()

    # Educational content
    render_weak_lln_education()


def render_weak_lln_education():
    """Render educational content about the Weak Law of Large Numbers."""
    st.subheader("Understanding the Weak Law of Large Numbers")

    # Main theorem statement
    st.markdown("""
    The **Weak Law of Large Numbers (WLLN)** describes convergence in probability —
    the probability of the sample mean being far from μ goes to zero.
    """)

    # Formal statement with LaTeX
    with st.expander("Formal Statement", expanded=True):
        st.markdown("**Theorem (Weak Law of Large Numbers):**")
        st.markdown("""
        Let $X_1, X_2, X_3, \\ldots$ be a sequence of independent and identically distributed
        (i.i.d.) random variables with finite expected value $\\mu = E[X_i]$ and finite variance $\\sigma^2$.
        """)

        st.markdown("Then for any $\\varepsilon > 0$, the sample mean converges **in probability** to $\\mu$:")

        st.latex(r"\lim_{n \to \infty} P\left(|\bar{X}_n - \mu| > \varepsilon\right) = 0")

        st.markdown("This is equivalent to saying:")

        st.latex(r"\bar{X}_n \xrightarrow{P} \mu \quad \text{as } n \to \infty")

    # Chebyshev's Inequality
    with st.expander("Chebyshev's Inequality", expanded=True):
        st.markdown("**Chebyshev's Inequality** provides an upper bound on the deviation probability:")

        st.latex(r"P\left(|\bar{X}_n - \mu| > \varepsilon\right) \leq \frac{\text{Var}(\bar{X}_n)}{\varepsilon^2} = \frac{\sigma^2}{n\varepsilon^2}")

        st.markdown("""
        **Key insights:**
        - The bound decays as $O(1/n)$ — doubling n halves the bound
        - The bound is often loose (empirical probability decays faster)
        - It proves the Weak LLN: as $n \\to \\infty$, the bound $\\to 0$
        """)

        # Show current values
        dist_info = get_distribution_info()
        eps = st.session_state.eps
        st.markdown(f"**For this simulation** (ε = {eps}, σ² = {dist_info['variance']:.4f}):")
        st.latex(rf"P(|\bar{{X}}_n - \mu| > {eps}) \leq \frac{{{dist_info['variance']:.4f}}}{{n \cdot {eps}^2}} = \frac{{{dist_info['variance']:.4f}}}{{{eps**2:.4f} \cdot n}}")

    # Intuitive explanation
    with st.expander("Intuitive Explanation", expanded=True):
        st.markdown("""
        **What does "convergence in probability" mean?**

        The Weak LLN says that as n grows, it becomes increasingly unlikely for the sample
        mean to be far from the true mean.

        **In practical terms:**
        - Pick any tolerance ε (how far is "far enough")
        - The probability of exceeding this tolerance shrinks toward zero
        - Unlike Strong LLN, this doesn't guarantee path-by-path convergence

        **What you see in the plot:**
        - Blue line: Empirical probability P(|X̄ₙ - μ| > ε) computed from simulations
        - Red dashed line: Chebyshev's theoretical upper bound
        - Both decay to zero, confirming the Weak LLN
        - The empirical curve is typically below the Chebyshev bound (the bound is conservative)
        """)

    # Key formulas reference
    with st.expander("Key Formulas", expanded=False):
        st.markdown("**Weak LLN Convergence:**")
        st.latex(r"\lim_{n \to \infty} P\left(|\bar{X}_n - \mu| > \varepsilon\right) = 0")

        st.markdown("**Chebyshev's Inequality:**")
        st.latex(r"P\left(|\bar{X}_n - \mu| > \varepsilon\right) \leq \frac{\sigma^2}{n\varepsilon^2}")

        st.markdown("**Variance of Sample Mean:**")
        st.latex(r"\text{Var}(\bar{X}_n) = \frac{\sigma^2}{n}")

        st.markdown("**For this simulation:**")
        dist_info = get_distribution_info()
        eps = st.session_state.eps
        if st.session_state.dist == "normal":
            st.latex(rf"\sigma^2 = {dist_info['variance']:.4f}, \quad \varepsilon = {eps}")
        elif st.session_state.dist == "bernoulli":
            p = st.session_state.p
            st.latex(rf"\sigma^2 = p(1-p) = {dist_info['variance']:.4f}, \quad \varepsilon = {eps}")
        else:  # uniform
            st.latex(rf"\sigma^2 = \frac{{(b-a)^2}}{{12}} = {dist_info['variance']:.4f}, \quad \varepsilon = {eps}")

    # Comparison with Strong LLN
    with st.expander("Weak vs Strong LLN", expanded=False):
        st.markdown("""
        | Property | Weak LLN | Strong LLN |
        |----------|----------|-----------|
        | **Convergence Type** | In probability | Almost sure |
        | **Statement** | $\\lim P(|\\bar{X}_n - \\mu| > \\varepsilon) = 0$ | $P(\\lim \\bar{X}_n = \\mu) = 1$ |
        | **Strength** | Weaker | Stronger (implies Weak LLN) |
        | **What it says** | Unlikely to be far from μ | Will converge to μ |
        | **Proof tool** | Chebyshev inequality | More advanced techniques |

        **Key difference:** The Strong LLN implies the Weak LLN, but not vice versa.
        The Strong LLN guarantees that each individual sequence converges, while the
        Weak LLN only guarantees that the probability of being far from μ vanishes.
        """)


def plot_variance_decay(empirical_var, theoretical_var, dist_name, log_scale=True, show_theoretical=True, compact=False):
    """Create variance decay plot showing Var(X̄ₙ) = σ²/n.

    Args:
        empirical_var: Shape (N,) array of Var(X̄ₙ) at each n
        theoretical_var: Theoretical variance σ² of the distribution
        dist_name: Name of the distribution
        log_scale: Whether to use log-log scale
        show_theoretical: Whether to show theoretical σ²/n overlay
        compact: Whether to create a smaller plot for dashboard

    Returns:
        matplotlib figure
    """
    N = len(empirical_var)
    n_values = np.arange(1, N + 1)

    figsize = (5, 3.5) if compact else (10, 6)
    fig, ax = plt.subplots(figsize=figsize)

    # Plot empirical variance
    ax.plot(
        n_values,
        empirical_var,
        color="blue",
        linewidth=1.5,
        label="Empirical Var(X̄ₙ)",
    )

    # Plot theoretical variance decay if enabled
    if show_theoretical:
        theoretical_decay = theoretical_var / n_values
        ax.plot(
            n_values,
            theoretical_decay,
            color="red",
            linestyle="--",
            linewidth=2,
            label="Theoretical σ²/n",
        )

    # Configure axes
    fontsize_label = 9 if compact else 12
    fontsize_title = 10 if compact else 14
    fontsize_legend = 8 if compact else 10
    ax.set_xlabel("Sample size (n)", fontsize=fontsize_label)
    ax.set_ylabel("Variance of sample mean", fontsize=fontsize_label)
    title = "Variance Decay (σ²/n)" if compact else (
        f"Variance Decay - {dist_name.capitalize()} Distribution\n"
        f"(σ² = {theoretical_var:.4f})"
    )
    ax.set_title(title, fontsize=fontsize_title)
    ax.legend(loc="upper right", fontsize=fontsize_legend)
    ax.grid(True, alpha=0.3)

    # Use log-log scale if enabled (shows linear decay)
    if log_scale:
        ax.set_xscale("log")
        ax.set_yscale("log")

    plt.tight_layout()
    return fig


def render_variance_decay_tab():
    """Render the Variance Decay tab with visualization and education."""
    dist_info = get_distribution_info()

    # Run simulation if needed
    running_avgs = run_simulation()

    # Compute empirical variance
    empirical_var = compute_empirical_variance(running_avgs)

    # Visualization controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        log_scale = st.checkbox(
            "Log-log scale",
            value=st.session_state.log_scale_variance,
            help="Use logarithmic scale for both axes (shows 1/n decay as linear)",
            key="log_scale_variance_checkbox",
        )
        st.session_state.log_scale_variance = log_scale
    with col3:
        show_theoretical = st.checkbox(
            "Show σ²/n curve",
            value=st.session_state.show_theoretical_variance,
            help="Overlay theoretical variance decay curve",
            key="show_theoretical_variance_checkbox",
        )
        st.session_state.show_theoretical_variance = show_theoretical

    # Create and display the plot
    fig = plot_variance_decay(
        empirical_var,
        dist_info["variance"],
        st.session_state.dist,
        log_scale=log_scale,
        show_theoretical=show_theoretical,
    )
    st.pyplot(fig)
    plt.close(fig)

    # Summary statistics
    st.subheader("Variance Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Distribution Variance (σ²)",
            f"{dist_info['variance']:.6f}",
        )
    with col2:
        theoretical_final = dist_info["variance"] / st.session_state.N
        st.metric(
            f"Theoretical Var(X̄ₙ) at n={st.session_state.N}",
            f"{theoretical_final:.6f}",
        )
    with col3:
        st.metric(
            "Empirical Var(X̄ₙ) (final)",
            f"{empirical_var[-1]:.6f}",
            delta=f"{empirical_var[-1] - theoretical_final:.2e}",
        )

    # Additional statistics row
    col1, col2, col3 = st.columns(3)
    with col1:
        se_theoretical = np.sqrt(dist_info["variance"] / st.session_state.N)
        st.metric(
            "Standard Error (σ/√n)",
            f"{se_theoretical:.6f}",
        )
    with col2:
        se_empirical = np.sqrt(empirical_var[-1])
        st.metric(
            "Empirical SE (final)",
            f"{se_empirical:.6f}",
        )
    with col3:
        # Ratio of empirical to theoretical variance
        ratio = empirical_var[-1] / theoretical_final if theoretical_final > 0 else 0
        st.metric(
            "Empirical/Theoretical Ratio",
            f"{ratio:.4f}",
        )

    st.divider()

    # Educational content
    render_variance_decay_education()


def render_variance_decay_education():
    """Render educational content about variance decay and standard error."""
    st.subheader("Understanding Variance Decay")

    # Main concept
    st.markdown("""
    The **Variance of the Sample Mean** decreases as $1/n$ — this is why larger samples
    give more reliable estimates of the population mean.
    """)

    # Variance of Sample Mean
    with st.expander("Variance of Sample Mean", expanded=True):
        st.markdown("**Theorem:**")
        st.markdown("""
        For independent, identically distributed (i.i.d.) random variables
        $X_1, X_2, \\ldots, X_n$ with variance $\\sigma^2$:
        """)

        st.latex(r"\text{Var}(\bar{X}_n) = \text{Var}\left(\frac{1}{n}\sum_{i=1}^{n} X_i\right) = \frac{\sigma^2}{n}")

        st.markdown("**Derivation:**")
        st.latex(r"\text{Var}(\bar{X}_n) = \text{Var}\left(\frac{X_1 + X_2 + \cdots + X_n}{n}\right)")
        st.latex(r"= \frac{1}{n^2} \text{Var}(X_1 + X_2 + \cdots + X_n)")
        st.latex(r"= \frac{1}{n^2} \cdot n \cdot \sigma^2 \quad \text{(independence)}")
        st.latex(r"= \frac{\sigma^2}{n}")

        # Show current values
        dist_info = get_distribution_info()
        st.markdown(f"**For this simulation** (σ² = {dist_info['variance']:.4f}):")
        st.latex(rf"\text{{Var}}(\bar{{X}}_n) = \frac{{{dist_info['variance']:.4f}}}{{n}}")

    # Standard Error
    with st.expander("Standard Error", expanded=True):
        st.markdown("**Definition:**")
        st.markdown("""
        The **Standard Error (SE)** is the standard deviation of the sample mean:
        """)

        st.latex(r"\text{SE}(\bar{X}_n) = \sqrt{\text{Var}(\bar{X}_n)} = \frac{\sigma}{\sqrt{n}}")

        st.markdown("""
        **Interpretation:**
        - The SE quantifies the "typical" deviation of $\\bar{X}_n$ from the true mean $\\mu$
        - It decreases as $1/\\sqrt{n}$ — to halve the SE, you need 4× the sample size
        - Used to construct confidence intervals: $\\bar{X}_n \\pm z_{\\alpha/2} \\cdot \\text{SE}$
        """)

        # Show current SE
        dist_info = get_distribution_info()
        sigma = np.sqrt(dist_info["variance"])
        N = st.session_state.N
        se = sigma / np.sqrt(N)
        st.markdown(f"**For this simulation** (σ = {sigma:.4f}, n = {N}):")
        st.latex(rf"\text{{SE}}(\bar{{X}}_n) = \frac{{{sigma:.4f}}}{{\sqrt{{{N}}}}} = {se:.6f}")

    # Why this matters
    with st.expander("Why Variance Decay Matters", expanded=True):
        st.markdown("""
        **Practical Implications:**

        1. **Larger samples → More reliable estimates**
           - As n increases, Var($\\bar{X}_n$) decreases
           - The sample mean becomes a more precise estimator of μ

        2. **The 1/n decay rate is fundamental**
           - This rate appears throughout statistics
           - It's why "more data is better" has mathematical backing

        3. **Log-log plot shows linear relationship**
           - In log-log scale: $\\log(\\text{Var}) = \\log(\\sigma^2) - \\log(n)$
           - Slope of -1 confirms the 1/n decay

        4. **Diminishing returns**
           - To halve the variance, you need 2× the data
           - To halve the SE, you need 4× the data
        """)

    # Key formulas
    with st.expander("Key Formulas", expanded=False):
        st.markdown("**Variance of Sample Mean:**")
        st.latex(r"\text{Var}(\bar{X}_n) = \frac{\sigma^2}{n}")

        st.markdown("**Standard Error:**")
        st.latex(r"\text{SE}(\bar{X}_n) = \frac{\sigma}{\sqrt{n}}")

        st.markdown("**Log-log relationship:**")
        st.latex(r"\log(\text{Var}(\bar{X}_n)) = \log(\sigma^2) - \log(n)")

        st.markdown("**Scaling relationships:**")
        st.markdown("""
        | To achieve... | You need... |
        |---------------|-------------|
        | Half the variance | 2× sample size |
        | Half the SE | 4× sample size |
        | 1/10 the variance | 10× sample size |
        | 1/10 the SE | 100× sample size |
        """)

        st.markdown("**For this simulation:**")
        dist_info = get_distribution_info()
        if st.session_state.dist == "normal":
            sigma = st.session_state.sigma
            st.latex(rf"\sigma^2 = {sigma}^2 = {dist_info['variance']:.4f}")
        elif st.session_state.dist == "bernoulli":
            p = st.session_state.p
            st.latex(rf"\sigma^2 = p(1-p) = {p}(1-{p}) = {dist_info['variance']:.4f}")
        else:  # uniform
            st.latex(rf"\sigma^2 = \frac{{(b-a)^2}}{{12}} = \frac{{1}}{{12}} = {dist_info['variance']:.4f}")

    # Connection to LLN
    with st.expander("Connection to Law of Large Numbers", expanded=False):
        st.markdown("""
        **Why variance decay proves the Weak LLN:**

        Chebyshev's inequality states:
        """)
        st.latex(r"P(|\bar{X}_n - \mu| > \varepsilon) \leq \frac{\text{Var}(\bar{X}_n)}{\varepsilon^2} = \frac{\sigma^2}{n\varepsilon^2}")

        st.markdown("""
        Since $\\text{Var}(\\bar{X}_n) = \\sigma^2/n \\to 0$ as $n \\to \\infty$:
        - The Chebyshev bound → 0
        - Therefore $P(|\\bar{X}_n - \\mu| > \\varepsilon) \\to 0$
        - This proves the Weak Law of Large Numbers!

        **The chain of reasoning:**
        1. Variance decays as 1/n
        2. Chebyshev bound uses variance
        3. Bound → 0 proves convergence in probability
        """)


def render_dashboard_tab():
    """Render the Dashboard tab with all three visualizations in a grid layout."""
    dist_info = get_distribution_info()
    running_avgs = run_simulation()

    # Compute derived data
    deviation_prob = compute_deviation_probability(
        running_avgs, dist_info["mean"], st.session_state.eps
    )
    empirical_var = compute_empirical_variance(running_avgs)

    # Summary statistics panel at top
    st.subheader("Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        final_mean = np.mean(running_avgs[:, -1])
        st.metric(
            "Empirical Mean",
            f"{final_mean:.4f}",
            delta=f"{final_mean - dist_info['mean']:.4f}",
        )
    with col2:
        st.metric("Theoretical Mean (μ)", f"{dist_info['mean']:.4f}")
    with col3:
        within_eps = np.mean(np.abs(running_avgs[:, -1] - dist_info["mean"]) <= st.session_state.eps)
        st.metric(f"Paths within ε", f"{within_eps * 100:.1f}%")
    with col4:
        st.metric("Final Deviation P", f"{deviation_prob[-1]:.4f}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Variance (σ²)", f"{dist_info['variance']:.4f}")
    with col2:
        theoretical_var_final = dist_info["variance"] / st.session_state.N
        st.metric("Var(X̄ₙ) theoretical", f"{theoretical_var_final:.2e}")
    with col3:
        st.metric("Var(X̄ₙ) empirical", f"{empirical_var[-1]:.2e}")
    with col4:
        se = np.sqrt(dist_info["variance"] / st.session_state.N)
        st.metric("Standard Error", f"{se:.4f}")

    st.divider()

    # Three plots in a row
    st.subheader("Visualizations")
    col1, col2, col3 = st.columns(3)

    with col1:
        fig1 = plot_sample_paths(
            running_avgs,
            dist_info["mean"],
            st.session_state.dist,
            log_scale=True,
            compact=True,
        )
        st.pyplot(fig1)
        plt.close(fig1)
        st.caption("Sample paths converging to μ")

    with col2:
        fig2 = plot_deviation_probability(
            deviation_prob,
            st.session_state.eps,
            dist_info["variance"],
            st.session_state.dist,
            log_scale=True,
            show_chebyshev=True,
            compact=True,
        )
        st.pyplot(fig2)
        plt.close(fig2)
        st.caption("P(|X̄ₙ - μ| > ε) decay")

    with col3:
        fig3 = plot_variance_decay(
            empirical_var,
            dist_info["variance"],
            st.session_state.dist,
            log_scale=True,
            show_theoretical=True,
            compact=True,
        )
        st.pyplot(fig3)
        plt.close(fig3)
        st.caption("Var(X̄ₙ) = σ²/n decay")

    # Convergence metrics
    st.divider()
    st.subheader("Convergence Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Strong LLN**")
        max_deviation = np.max(np.abs(running_avgs[:, -1] - dist_info["mean"]))
        st.write(f"Max deviation at n={st.session_state.N}: {max_deviation:.6f}")
        st.write(f"All paths within ε: {'Yes' if within_eps == 1.0 else 'No'}")
    with col2:
        st.markdown("**Weak LLN**")
        chebyshev_final = min(1.0, dist_info["variance"] / (st.session_state.N * st.session_state.eps**2))
        st.write(f"Empirical P(deviation > ε): {deviation_prob[-1]:.4f}")
        st.write(f"Chebyshev bound: {chebyshev_final:.4f}")
    with col3:
        st.markdown("**Variance Decay**")
        ratio = empirical_var[-1] / theoretical_var_final if theoretical_var_final > 0 else 0
        st.write(f"Empirical/Theoretical ratio: {ratio:.4f}")
        st.write(f"SE(X̄ₙ): {np.sqrt(empirical_var[-1]):.6f}")


def render_learn_tab():
    """Render the Learn tab with comprehensive educational content."""
    st.subheader("Learn: Law of Large Numbers")

    st.markdown("""
    Welcome to the **LLN Explorer Learning Guide**. This section provides a structured
    journey through the Law of Large Numbers and related concepts.
    """)

    # Table of contents
    sections = [
        "Introduction to LLN",
        "Distribution Properties",
        "Strong vs Weak LLN",
        "Mathematical Prerequisites",
        "Key Formulas Reference",
    ]

    selected = st.radio("Select a topic:", sections, horizontal=True)

    st.divider()

    if selected == "Introduction to LLN":
        render_learn_introduction()
    elif selected == "Distribution Properties":
        render_learn_distributions()
    elif selected == "Strong vs Weak LLN":
        render_learn_comparison()
    elif selected == "Mathematical Prerequisites":
        render_learn_prerequisites()
    elif selected == "Key Formulas Reference":
        render_learn_formulas()


def render_learn_introduction():
    """Render introduction to LLN educational content."""
    st.markdown("## Introduction to the Law of Large Numbers")

    st.markdown("""
    The **Law of Large Numbers (LLN)** is one of the most fundamental theorems in probability
    and statistics. It describes the result of performing the same experiment many times.

    ### The Core Idea

    When you repeat a random experiment many times, the average of the results gets closer
    and closer to the expected value.
    """)

    st.info("""
    **Example:** If you flip a fair coin many times, the proportion of heads will get
    closer to 0.5 as you flip more times.
    """)

    st.markdown("""
    ### Why It Matters

    The LLN is the mathematical foundation for:
    - **Polling and surveys**: Why larger samples give more accurate results
    - **Insurance**: Why insurers can predict claims accurately with enough customers
    - **Casino profits**: Why the house always wins in the long run
    - **Quality control**: Why sampling can reliably detect defects
    - **Scientific experiments**: Why repeated measurements improve precision

    ### Two Versions

    There are two main versions of the LLN:

    1. **Strong Law (SLLN)**: The sample average *converges almost surely* to the expected value
    2. **Weak Law (WLLN)**: The probability of the sample average being far from the expected
       value *goes to zero*

    The Strong LLN is a stronger result (it implies the Weak LLN), but both are important
    in different contexts.
    """)

    st.latex(r"\text{Strong LLN: } P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1")
    st.latex(r"\text{Weak LLN: } \lim_{n \to \infty} P\left(|\bar{X}_n - \mu| > \varepsilon\right) = 0")


def render_learn_distributions():
    """Render distribution properties educational content."""
    st.markdown("## Distribution Properties")

    st.markdown("""
    Understanding the properties of different probability distributions is essential
    for applying the LLN. Here are the three distributions available in this explorer:
    """)

    # Normal Distribution
    with st.expander("Normal Distribution", expanded=True):
        st.markdown("### Normal (Gaussian) Distribution")
        st.latex(r"X \sim \mathcal{N}(\mu, \sigma^2)")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parameters:**")
            st.markdown("- μ (mu): Mean / location parameter")
            st.markdown("- σ (sigma): Standard deviation / scale parameter")

            st.markdown("**Properties:**")
            st.markdown(f"- Mean: E[X] = μ")
            st.markdown(f"- Variance: Var(X) = σ²")
            st.markdown("- Symmetric about μ")
            st.markdown("- 68-95-99.7 rule applies")

        with col2:
            st.markdown("**Probability Density Function (PDF):**")
            st.latex(r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)")

            st.markdown("**Standard Normal:**")
            st.latex(r"Z = \frac{X - \mu}{\sigma} \sim \mathcal{N}(0, 1)")

    # Bernoulli Distribution
    with st.expander("Bernoulli Distribution", expanded=True):
        st.markdown("### Bernoulli Distribution")
        st.latex(r"X \sim \text{Bernoulli}(p)")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parameters:**")
            st.markdown("- p: Probability of success (0 < p < 1)")

            st.markdown("**Properties:**")
            st.markdown("- Mean: E[X] = p")
            st.markdown("- Variance: Var(X) = p(1-p)")
            st.markdown("- Takes values 0 or 1 only")
            st.markdown("- Maximum variance at p = 0.5")

        with col2:
            st.markdown("**Probability Mass Function (PMF):**")
            st.latex(r"P(X = k) = p^k (1-p)^{1-k}, \quad k \in \{0, 1\}")

            st.markdown("**Connection to Binomial:**")
            st.markdown("Sum of n Bernoulli trials = Binomial(n, p)")

    # Uniform Distribution
    with st.expander("Uniform Distribution", expanded=True):
        st.markdown("### Uniform Distribution")
        st.latex(r"X \sim \text{Uniform}(a, b)")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parameters:**")
            st.markdown("- a: Lower bound")
            st.markdown("- b: Upper bound (b > a)")
            st.markdown("- This explorer uses a=0, b=1")

            st.markdown("**Properties:**")
            st.markdown("- Mean: E[X] = (a+b)/2")
            st.markdown("- Variance: Var(X) = (b-a)²/12")
            st.markdown("- All values equally likely")

        with col2:
            st.markdown("**Probability Density Function (PDF):**")
            st.latex(r"f(x) = \frac{1}{b-a}, \quad a \leq x \leq b")

            st.markdown("**For Uniform(0,1):**")
            st.latex(r"\mu = 0.5, \quad \sigma^2 = \frac{1}{12} \approx 0.0833")

    # Current distribution info
    st.divider()
    st.markdown("### Current Simulation Distribution")
    dist_info = get_distribution_info()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Distribution", dist_info["name"])
    with col2:
        st.metric("Mean (μ)", f"{dist_info['mean']:.4f}")
    with col3:
        st.metric("Variance (σ²)", f"{dist_info['variance']:.4f}")


def render_learn_comparison():
    """Render Strong vs Weak LLN comparison."""
    st.markdown("## Strong vs Weak Law of Large Numbers")

    st.markdown("""
    Both laws describe convergence, but they differ in the *type* of convergence
    and what guarantees they provide.
    """)

    # Comparison table
    st.markdown("### Comparison Table")
    st.markdown("""
    | Aspect | Strong LLN | Weak LLN |
    |--------|-----------|----------|
    | **Convergence Type** | Almost sure (a.s.) | In probability |
    | **Mathematical Statement** | P(lim X̄ₙ = μ) = 1 | lim P(\\|X̄ₙ - μ\\| > ε) = 0 |
    | **Interpretation** | Each sequence converges | Unlikely to be far from μ |
    | **Strength** | Stronger (implies Weak) | Weaker |
    | **Requirements** | Finite mean (weaker versions exist) | Finite variance |
    | **Proof Technique** | Borel-Cantelli lemma | Chebyshev's inequality |
    """)

    # Strong LLN
    with st.expander("Strong Law - Detailed", expanded=True):
        st.markdown("### Strong Law of Large Numbers")

        st.markdown("""
        **Statement:** With probability 1, the sample mean converges to the true mean.
        """)

        st.latex(r"P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1")

        st.markdown("""
        **What "almost surely" means:**
        - Consider all possible infinite sequences of random outcomes
        - The set of sequences where X̄ₙ doesn't converge to μ has probability 0
        - For any single realization, convergence is guaranteed

        **Visual interpretation:**
        - In the Sample Paths tab, each colored line is one realization
        - Every line converges to μ (the red dashed line)
        - The "funnel" shape shows all paths concentrating around μ
        """)

    # Weak LLN
    with st.expander("Weak Law - Detailed", expanded=True):
        st.markdown("### Weak Law of Large Numbers")

        st.markdown("""
        **Statement:** The probability of deviating from μ by more than ε goes to zero.
        """)

        st.latex(r"\lim_{n \to \infty} P\left(|\bar{X}_n - \mu| > \varepsilon\right) = 0")

        st.markdown("""
        **What "convergence in probability" means:**
        - Pick any tolerance ε > 0
        - As n increases, the chance of exceeding this tolerance vanishes
        - Doesn't guarantee any particular sequence converges

        **Proven via Chebyshev's inequality:**
        """)
        st.latex(r"P(|\bar{X}_n - \mu| > \varepsilon) \leq \frac{\sigma^2}{n\varepsilon^2} \to 0")

        st.markdown("""
        **Visual interpretation:**
        - In the Deviation Probability tab, see P(|X̄ₙ - μ| > ε) decay
        - The Chebyshev bound (red dashed line) also decays
        - Empirical probability typically decays faster than the bound
        """)

    # Key insight
    st.info("""
    **Key Insight:** The Strong LLN implies the Weak LLN, but not vice versa.

    If every sequence converges (Strong), then certainly the probability of being
    far from μ goes to zero (Weak). But sequences could have low probability of
    large deviations without each individual sequence converging.
    """)


def render_learn_prerequisites():
    """Render mathematical prerequisites content."""
    st.markdown("## Mathematical Prerequisites")

    st.markdown("""
    To fully understand the LLN, it helps to be familiar with these concepts:
    """)

    with st.expander("Expected Value (Mean)", expanded=True):
        st.markdown("### Expected Value")
        st.markdown("""
        The **expected value** E[X] is the long-run average of a random variable.
        """)

        st.markdown("**For discrete random variables:**")
        st.latex(r"E[X] = \sum_{x} x \cdot P(X = x)")

        st.markdown("**For continuous random variables:**")
        st.latex(r"E[X] = \int_{-\infty}^{\infty} x \cdot f(x) \, dx")

        st.markdown("**Properties:**")
        st.markdown("- Linearity: E[aX + b] = a·E[X] + b")
        st.markdown("- E[X + Y] = E[X] + E[Y] (always)")
        st.markdown("- E[XY] = E[X]·E[Y] (if independent)")

    with st.expander("Variance", expanded=True):
        st.markdown("### Variance")
        st.markdown("""
        **Variance** measures the spread of a distribution around its mean.
        """)

        st.latex(r"\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2")

        st.markdown("**Properties:**")
        st.markdown("- Var(X) ≥ 0 always")
        st.markdown("- Var(aX + b) = a²·Var(X)")
        st.markdown("- Var(X + Y) = Var(X) + Var(Y) (if independent)")

        st.markdown("**Standard deviation:**")
        st.latex(r"\sigma = \sqrt{\text{Var}(X)}")

    with st.expander("Independence", expanded=True):
        st.markdown("### Independence")
        st.markdown("""
        Random variables X and Y are **independent** if knowing X tells you nothing about Y.
        """)

        st.markdown("**Formal definition:**")
        st.latex(r"P(X \in A, Y \in B) = P(X \in A) \cdot P(Y \in B)")

        st.markdown("**Consequences:**")
        st.markdown("- E[XY] = E[X]·E[Y]")
        st.markdown("- Var(X + Y) = Var(X) + Var(Y)")
        st.markdown("- Covariance = 0")

        st.markdown("""
        **i.i.d. (independent and identically distributed):**
        The LLN requires samples to be i.i.d. — each drawn independently from
        the same distribution.
        """)

    with st.expander("Chebyshev's Inequality", expanded=True):
        st.markdown("### Chebyshev's Inequality")
        st.markdown("""
        A fundamental bound on how far a random variable can deviate from its mean.
        """)

        st.latex(r"P(|X - \mu| \geq k\sigma) \leq \frac{1}{k^2}")

        st.markdown("**Equivalent form:**")
        st.latex(r"P(|X - \mu| > \varepsilon) \leq \frac{\text{Var}(X)}{\varepsilon^2}")

        st.markdown("""
        **Why it matters for LLN:**
        - Provides the key tool for proving the Weak LLN
        - Applied to X̄ₙ with Var(X̄ₙ) = σ²/n
        - Bound decays as 1/n, proving convergence
        """)


def render_learn_formulas():
    """Render key formulas reference."""
    st.markdown("## Key Formulas Reference")

    st.markdown("### Sample Mean")
    st.latex(r"\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i")

    st.markdown("### Variance of Sample Mean")
    st.latex(r"\text{Var}(\bar{X}_n) = \frac{\sigma^2}{n}")

    st.markdown("### Standard Error")
    st.latex(r"\text{SE}(\bar{X}_n) = \frac{\sigma}{\sqrt{n}}")

    st.markdown("### Chebyshev Bound for Sample Mean")
    st.latex(r"P(|\bar{X}_n - \mu| > \varepsilon) \leq \frac{\sigma^2}{n\varepsilon^2}")

    st.divider()

    st.markdown("### Strong Law of Large Numbers")
    st.latex(r"P\left(\lim_{n \to \infty} \bar{X}_n = \mu\right) = 1")

    st.markdown("### Weak Law of Large Numbers")
    st.latex(r"\lim_{n \to \infty} P(|\bar{X}_n - \mu| > \varepsilon) = 0 \quad \forall \varepsilon > 0")

    st.divider()

    st.markdown("### Distribution Formulas")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Normal(μ, σ²)**")
        st.latex(r"E[X] = \mu")
        st.latex(r"\text{Var}(X) = \sigma^2")

    with col2:
        st.markdown("**Bernoulli(p)**")
        st.latex(r"E[X] = p")
        st.latex(r"\text{Var}(X) = p(1-p)")

    with col3:
        st.markdown("**Uniform(a, b)**")
        st.latex(r"E[X] = \frac{a+b}{2}")
        st.latex(r"\text{Var}(X) = \frac{(b-a)^2}{12}")

    st.divider()

    # Quick reference card
    st.markdown("### Quick Reference Card")
    st.markdown("""
    | Quantity | Formula | Description |
    |----------|---------|-------------|
    | Sample mean | X̄ₙ = (1/n)ΣXᵢ | Average of n observations |
    | Var(X̄ₙ) | σ²/n | Variance decreases with n |
    | SE(X̄ₙ) | σ/√n | Standard error |
    | Chebyshev | P(\\|X̄ₙ-μ\\|>ε) ≤ σ²/(nε²) | Probability bound |
    | To halve SE | Need 4× samples | Diminishing returns |
    | To halve Var | Need 2× samples | Linear scaling |
    """)


def render_main_content():
    """Render main content area with visualizations."""
    st.title("LLN Explorer")
    st.markdown("**Interactive Law of Large Numbers Visualization & Learning Tool**")

    # Current configuration display
    dist_info = get_distribution_info()

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Distribution", dist_info["name"])
    with col2:
        st.metric("Mean (μ)", f"{dist_info['mean']:.4f}")
    with col3:
        st.metric("Variance (σ²)", f"{dist_info['variance']:.4f}")
    with col4:
        st.metric("Paths (M)", st.session_state.M)
    with col5:
        st.metric("Max n (N)", f"{st.session_state.N:,}")

    st.divider()

    # Visualization tabs - 5 tabs including Dashboard and Learn
    if st.session_state.simulation_run:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Dashboard", "Sample Paths", "Deviation Probability", "Variance Decay", "Learn"]
        )

        with tab1:
            render_dashboard_tab()

        with tab2:
            render_sample_paths_tab()

        with tab3:
            render_deviation_probability_tab()

        with tab4:
            render_variance_decay_tab()

        with tab5:
            render_learn_tab()

        # Parameter summary
        with st.expander("Current Parameters", expanded=False):
            st.json(
                {
                    "distribution": st.session_state.dist,
                    "M": st.session_state.M,
                    "N": st.session_state.N,
                    "epsilon": st.session_state.eps,
                    "distribution_params": dist_info["params"],
                    "theoretical_mean": dist_info["mean"],
                    "theoretical_variance": dist_info["variance"],
                }
            )
    else:
        # Show Learn tab even before simulation
        tab_welcome, tab_learn = st.tabs(["Welcome", "Learn"])

        with tab_welcome:
            st.info(
                "Configure parameters in the sidebar and click **Run Simulation** to start."
            )

            # Welcome content
            st.markdown(
                """
            ### Welcome to LLN Explorer

            This interactive tool helps you visualize and understand the **Law of Large Numbers**:

            **Visualizations:**
            - **Dashboard**: All three visualizations at a glance with summary statistics
            - **Sample Paths**: See paths converging to μ (Strong LLN)
            - **Deviation Probability**: Watch P(|X̄ₙ - μ| > ε) decay (Weak LLN)
            - **Variance Decay**: Observe Var(X̄ₙ) = σ²/n

            **Learning:**
            - Explore the **Learn** tab for comprehensive educational content
            - Distribution formulas, theorem statements, and prerequisites
            - Available even before running a simulation!

            **To get started:**
            1. Select a probability distribution in the sidebar
            2. Configure simulation parameters (M paths, N samples)
            3. Click **Run Simulation** to generate visualizations
            """
            )

            # Quick start suggestions
            st.markdown("### Quick Start Suggestions")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Try Normal**")
                st.caption("Classic bell curve, μ=0, σ=1")
            with col2:
                st.markdown("**Try Bernoulli**")
                st.caption("Coin flips, p=0.5")
            with col3:
                st.markdown("**Try Uniform**")
                st.caption("Equal probability, [0,1]")

        with tab_learn:
            render_learn_tab()


def main():
    """Main entry point for the Streamlit GUI."""
    init_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()

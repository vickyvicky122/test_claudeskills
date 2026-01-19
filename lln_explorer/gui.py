#!/usr/bin/env python3
"""
LLN Explorer GUI - Streamlit-based interface for Law of Large Numbers visualization.

Run with: streamlit run lln_explorer/gui.py
"""

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Import simulation functions from CLI module
from lln_explorer import compute_deviation_probability, make_distributions, simulate_paths

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

        # Run simulation
        with st.spinner("Running simulation..."):
            running_avgs = simulate_paths(dist, st.session_state.M, st.session_state.N)
            st.session_state.running_avgs = running_avgs

    return st.session_state.running_avgs


def plot_sample_paths(running_avgs, mu, dist_name, log_scale=True):
    """Create sample paths plot showing Strong LLN convergence.

    Args:
        running_avgs: Shape (M, N) array of running averages
        mu: Theoretical mean
        dist_name: Name of the distribution
        log_scale: Whether to use log scale for x-axis

    Returns:
        matplotlib figure
    """
    M, N = running_avgs.shape
    n_values = np.arange(1, N + 1)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot all M sample paths with low alpha for visibility
    for i in range(M):
        ax.plot(n_values, running_avgs[i], alpha=0.3, linewidth=0.5)

    # Add horizontal reference line at theoretical mean
    ax.axhline(y=mu, color="red", linestyle="--", linewidth=2, label=f"μ = {mu:.4f}")

    # Configure axes
    ax.set_xlabel("Sample size (n)", fontsize=12)
    ax.set_ylabel("Running average X̄ₙ", fontsize=12)
    ax.set_title(
        f"Sample Path Convergence - {dist_name.capitalize()} Distribution\n"
        f"({M} paths, Strong LLN)",
        fontsize=14,
    )
    ax.legend(loc="upper right", fontsize=10)
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


def plot_deviation_probability(deviation_prob, eps, variance, dist_name, log_scale=True, show_chebyshev=True):
    """Create deviation probability plot showing Weak LLN convergence.

    Args:
        deviation_prob: Shape (N,) array of P(|X̄ₙ - μ| > ε) at each n
        eps: Epsilon threshold used
        variance: Theoretical variance σ² of the distribution
        dist_name: Name of the distribution
        log_scale: Whether to use log scale for x-axis
        show_chebyshev: Whether to show Chebyshev bound overlay

    Returns:
        matplotlib figure
    """
    N = len(deviation_prob)
    n_values = np.arange(1, N + 1)

    fig, ax = plt.subplots(figsize=(10, 6))

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
    ax.set_xlabel("Sample size (n)", fontsize=12)
    ax.set_ylabel("Deviation probability", fontsize=12)
    ax.set_title(
        f"Deviation Probability Decay - {dist_name.capitalize()} Distribution\n"
        f"(ε = {eps}, Weak LLN)",
        fontsize=14,
    )
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(True, alpha=0.3)

    # Use log scale for x-axis if enabled
    if log_scale:
        ax.set_xscale("log")

    # Set y-axis limits
    ax.set_ylim(0, 1.05)

    # Add epsilon annotation
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


def render_main_content():
    """Render main content area with visualizations."""
    st.title("LLN Explorer")
    st.markdown("**Interactive Law of Large Numbers Visualization**")

    # Current configuration display
    dist_info = get_distribution_info()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Distribution", dist_info["name"])
    with col2:
        st.metric("Theoretical Mean (μ)", f"{dist_info['mean']:.4f}")
    with col3:
        st.metric("Theoretical Variance (σ²)", f"{dist_info['variance']:.4f}")
    with col4:
        st.metric("Sample Paths (M)", st.session_state.M)

    st.divider()

    # Visualization tabs
    if st.session_state.simulation_run:
        tab1, tab2, tab3 = st.tabs(
            ["Sample Paths (Strong LLN)", "Deviation Probability (Weak LLN)", "Variance Decay"]
        )

        with tab1:
            render_sample_paths_tab()

        with tab2:
            render_deviation_probability_tab()

        with tab3:
            st.subheader("Variance Decay")
            st.caption("Story 4.4: Will show Var(X̄ₙ) = σ²/n")
            st.info("This visualization will be implemented in Story 4.4.")

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
        st.info(
            "Configure parameters in the sidebar and click **Run Simulation** to start."
        )

        # Welcome content
        st.markdown(
            """
        ### Welcome to LLN Explorer

        This interactive tool helps you visualize and understand the **Law of Large Numbers**:

        - **Strong LLN**: Sample paths converge almost surely to the mean
        - **Weak LLN**: Deviation probability decays to zero
        - **Variance Decay**: Sample mean variance decreases as σ²/n

        Use the sidebar to configure:
        1. Select a probability distribution
        2. Set the number of sample paths (M)
        3. Set the maximum sample size (N)
        4. Adjust the epsilon threshold for deviation analysis
        5. Configure distribution-specific parameters

        Then click **Run Simulation** to generate visualizations.
        """
        )


def main():
    """Main entry point for the Streamlit GUI."""
    init_session_state()
    render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()

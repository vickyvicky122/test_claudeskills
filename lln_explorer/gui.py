#!/usr/bin/env python3
"""
LLN Explorer GUI - Streamlit-based interface for Law of Large Numbers visualization.

Run with: streamlit run lln_explorer/gui.py
"""

import streamlit as st

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


def render_main_content():
    """Render main content area with visualization placeholders."""
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

    # Visualization placeholders
    if st.session_state.simulation_run:
        st.info(
            "Simulation parameters updated. Visualization will be implemented in Stories 4.2-4.5."
        )

        # Placeholder tabs for future visualizations
        tab1, tab2, tab3 = st.tabs(
            ["Sample Paths (Strong LLN)", "Deviation Probability (Weak LLN)", "Variance Decay"]
        )

        with tab1:
            st.subheader("Sample Path Convergence")
            st.caption("Story 4.2: Will show M sample paths converging to μ")
            st.empty()

        with tab2:
            st.subheader("Deviation Probability Decay")
            st.caption("Story 4.3: Will show P(|X̄ₙ - μ| > ε) → 0")
            st.empty()

        with tab3:
            st.subheader("Variance Decay")
            st.caption("Story 4.4: Will show Var(X̄ₙ) = σ²/n")
            st.empty()

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
    run_clicked = render_sidebar()
    render_main_content()


if __name__ == "__main__":
    main()

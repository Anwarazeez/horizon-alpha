# pyrefly: ignore [missing-import]
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Horizon-Alpha",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: white;
}

[data-testid="stMetric"] {
    background-color: #111827;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🚀 Horizon-Alpha")
st.markdown("### Predictive Business Simulation Engine")

# ---------------------------------------------------
# SIDEBAR INPUTS
# ---------------------------------------------------

with st.sidebar:

    st.header("Simulation Controls")

    initial_cash = st.number_input(
        "Starting Capital (₹)",
        value=500000
    )

    monthly_revenue = st.number_input(
        "Monthly Revenue (₹)",
        value=100000
    )

    monthly_expenses = st.number_input(
        "Monthly Expenses (₹)",
        value=70000
    )

    growth_rate = st.slider(
        "Monthly Growth Rate (%)",
        0,
        50,
        10
    )

    marketing_spend = st.number_input(
        "Marketing Spend (₹)",
        value=30000
    )

    volatility = st.slider(
        "Market Volatility",
        0.0,
        0.5,
        0.10
    )

    simulations = st.slider(
        "Simulation Runs",
        10,
        500,
        100
    )

# ---------------------------------------------------
# MONTE CARLO SIMULATION
# ---------------------------------------------------

months = 12

all_runs = []

rng = np.random.default_rng(42)

for s in range(simulations):

    cash_flow = [initial_cash]

    current_revenue = monthly_revenue

    for month in range(months):

        noise = rng.uniform(-volatility, volatility)

        marketing_boost = (
            marketing_spend *
            rng.uniform(0.00001, 0.00005)
        )

        growth_multiplier = (
            1
            + (growth_rate / 100)
            + noise
            + marketing_boost
        )

        current_revenue *= growth_multiplier

        net_change = (
            current_revenue - monthly_expenses
        )

        new_balance = (
            cash_flow[-1] + net_change
        )

        cash_flow.append(max(0, new_balance))

    all_runs.append(cash_flow)

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------

average_run = np.mean(all_runs, axis=0)

best_case = np.max(all_runs, axis=0)

worst_case = np.min(all_runs, axis=0)

failure_count = sum(
    1 for run in all_runs if run[-1] <= 0
)

failure_rate = (
    failure_count / simulations
) * 100

final_balance = average_run[-1]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Projected Balance",
    f"₹{final_balance:,.0f}"
)

col2.metric(
    "Growth Rate",
    f"{growth_rate}%"
)

col3.metric(
    "Risk Level",
    f"{volatility*100:.0f}%"
)

col4.metric(
    "Failure Probability",
    f"{failure_rate:.1f}%"
)

# ---------------------------------------------------
# PLOTLY GRAPH
# ---------------------------------------------------

fig = go.Figure()

# All simulations
for run in all_runs:

    fig.add_trace(
        go.Scatter(
            x=list(range(months + 1)),
            y=run,
            mode='lines',
            line=dict(width=1),
            opacity=0.15,
            showlegend=False
        )
    )

# Average line
fig.add_trace(
    go.Scatter(
        x=list(range(months + 1)),
        y=average_run,
        mode='lines+markers',
        name='Average Projection',
        line=dict(
            color='#00D1FF',
            width=4
        )
    )
)

# Best case
fig.add_trace(
    go.Scatter(
        x=list(range(months + 1)),
        y=best_case,
        mode='lines',
        name='Best Case',
        line=dict(
            color='green',
            dash='dash'
        )
    )
)

# Worst case
fig.add_trace(
    go.Scatter(
        x=list(range(months + 1)),
        y=worst_case,
        mode='lines',
        name='Worst Case',
        line=dict(
            color='red',
            dash='dash'
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    title="12-Month Financial Projection",
    xaxis_title="Months",
    yaxis_title="Cash Balance (₹)",
    height=600,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# AI-STYLE INSIGHTS
# ---------------------------------------------------

st.subheader("AI Insights")

if final_balance <= initial_cash:

    st.error(
        "⚠️ High probability of runway contraction detected."
    )

elif final_balance >= initial_cash * 2:

    st.success(
        "✅ Strong growth trajectory predicted."
    )

else:

    st.warning(
        "📈 Moderate growth with manageable volatility."
    )

st.info(
    f"""
    Based on {simulations} Monte Carlo simulations,
    the projected average balance after 12 months
    is ₹{final_balance:,.0f}.
    """
)

# ---------------------------------------------------
# DATA TABLE
# ---------------------------------------------------

df = pd.DataFrame({
    "Month": list(range(months + 1)),
    "Average Projection": average_run,
    "Best Case": best_case,
    "Worst Case": worst_case
})

st.subheader("Projection Data")

st.dataframe(df)

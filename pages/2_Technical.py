"""
Technical Page - Statistical Analysis
=====================================

Detailed methodology, statistical tests, and effect sizes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from pathlib import Path

st.set_page_config(
    page_title="Technical | SM & Mental Wellbeing",
    page_icon="📈",
    layout="wide",
)

# Load data
@st.cache_data
def load_data():
    data_path = Path("data/processed/v1/smmh_clean.csv")
    df = pd.read_csv(data_path)
    df = df[df["include_in_analysis"] == True].copy()
    return df

df = load_data()

# Header
st.title("Technical Analysis")
st.markdown("""
This page presents the statistical methodology and detailed test results.
All tests use α = 0.05 as the significance threshold.
""")

st.divider()

# Hypothesis Tests Summary
st.subheader("Hypothesis Test Results")

st.markdown("""
We tested five pre-registered hypotheses about associations between social media behaviours
and wellbeing indicators. All tests found statistically significant associations.
""")

# Create results table
test_results = pd.DataFrame({
    "ID": ["H1", "H2", "H3", "H4", "H5"],
    "Predictor": [
        "Daily time band",
        "Purposeless use",
        "Compare to successful",
        "Seek validation",
        "Restless without SM",
    ],
    "Outcome": [
        "Low mood freq",
        "Low mood freq",
        "Low mood freq",
        "Low mood freq",
        "Sleep issues",
    ],
    "Test": [
        "Kruskal-Wallis H",
        "Spearman rho",
        "Spearman rho",
        "Spearman rho",
        "Spearman rho",
    ],
    "Statistic": ["H = 53.7", "rho = 0.29", "rho = 0.40", "rho = 0.26", "rho = 0.16"],
    "p-value": ["< 0.001", "< 0.001", "< 0.001", "< 0.001", "< 0.001"],
    "Effect Size": ["Moderate", "Small", "Moderate", "Small", "Small"],
    "Significant": ["Yes", "Yes", "Yes", "Yes", "Yes"],
})

st.dataframe(test_results, use_container_width=True, hide_index=True)

st.divider()

# Effect Size Interpretation
st.subheader("Understanding Effect Sizes")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Spearman's rho interpretation (Cohen's guidelines):**

    | rho | Interpretation |
    |-----|----------------|
    | 0.10 - 0.29 | Small |
    | 0.30 - 0.49 | Moderate |
    | 0.50+ | Large |

    The strongest association (H3: comparison → low mood) has rho = 0.40,
    which is a **moderate** effect size.
    """)

with col2:
    st.markdown("""
    **What this means practically:**

    - These are real, statistically significant patterns
    - But social media behaviour explains only a **portion** of wellbeing variance
    - Many other factors influence mental wellbeing
    - Effect sizes are typical for social science research
    """)

st.divider()

# Correlation Matrix
st.subheader("Correlation Matrix: Behaviour vs Wellbeing")

behaviour_cols = [
    "purposeless_use",
    "distracted_when_busy",
    "restless_without_sm",
    "compare_to_successful",
    "seek_validation",
]

wellbeing_cols = [
    "low_mood_freq",
    "sleep_issues",
    "worries_bother",
    "difficulty_concentrating",
    "interest_fluctuation",
]

# Calculate Spearman correlations
corr_matrix = pd.DataFrame(index=behaviour_cols, columns=wellbeing_cols, dtype=float)

for b_col in behaviour_cols:
    for w_col in wellbeing_cols:
        rho, _ = stats.spearmanr(df[b_col], df[w_col])
        corr_matrix.loc[b_col, w_col] = rho

# Clean up labels
corr_matrix.index = [
    "Purposeless use",
    "Distracted when busy",
    "Restless without SM",
    "Compare to successful",
    "Seek validation",
]
corr_matrix.columns = [
    "Low mood",
    "Sleep issues",
    "Worries",
    "Concentration",
    "Interest fluctuation",
]

fig_corr = px.imshow(
    corr_matrix.values.astype(float),
    x=corr_matrix.columns.tolist(),
    y=corr_matrix.index.tolist(),
    color_continuous_scale="RdBu_r",
    zmin=-0.5,
    zmax=0.5,
    text_auto=".2f",
    aspect="auto",
)
fig_corr.update_layout(height=400)
st.plotly_chart(fig_corr, use_container_width=True)

st.caption("""
Spearman correlation coefficients. Red = positive association, Blue = negative association.
Darker colours indicate stronger correlations.
""")

st.divider()

# Detailed Test: H1 (Time vs Mood)
st.subheader("Deep Dive: Daily Time vs Low Mood (H1)")

col1, col2 = st.columns([2, 1])

with col1:
    time_order = [
        "Less than an Hour",
        "Between 1 and 2 hours",
        "Between 2 and 3 hours",
        "Between 3 and 4 hours",
        "Between 4 and 5 hours",
        "More than 5 hours",
    ]

    fig_box = px.box(
        df,
        x="daily_time_band",
        y="low_mood_freq",
        category_orders={"daily_time_band": time_order},
        color="daily_time_band",
        color_discrete_sequence=px.colors.sequential.Blues,
    )
    fig_box.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400,
        xaxis_title="Daily Time Spent",
        yaxis_title="Low Mood Frequency (1-5)",
    )
    st.plotly_chart(fig_box, use_container_width=True)

with col2:
    st.markdown("""
    **Test details:**

    - **Test:** Kruskal-Wallis H
    - **Why:** Non-parametric; doesn't assume normality
    - **H statistic:** 53.7
    - **p-value:** < 0.001
    - **Conclusion:** Significant differences in low mood across time bands

    **Post-hoc observation:**

    The jump from "2-3 hours" to "3-4 hours" shows
    a notable increase in median low mood.
    """)

st.divider()

# Scatter plot: Comparison vs Mood
st.subheader("Deep Dive: Social Comparison vs Low Mood (H3)")

col1, col2 = st.columns([2, 1])

with col1:
    # Add jitter for visibility
    df_plot = df.copy()
    df_plot["compare_jitter"] = df_plot["compare_to_successful"] + np.random.uniform(-0.2, 0.2, len(df_plot))
    df_plot["mood_jitter"] = df_plot["low_mood_freq"] + np.random.uniform(-0.2, 0.2, len(df_plot))

    fig_scatter = px.scatter(
        df_plot,
        x="compare_jitter",
        y="mood_jitter",
        opacity=0.5,
        trendline="ols",
        labels={
            "compare_jitter": "Compare to Successful (1-5)",
            "mood_jitter": "Low Mood Frequency (1-5)",
        },
    )
    fig_scatter.update_layout(height=400)
    fig_scatter.update_traces(marker=dict(size=8))
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    st.markdown("""
    **Test details:**

    - **Test:** Spearman correlation
    - **Why:** Ordinal data; robust to outliers
    - **rho:** 0.40
    - **p-value:** < 0.001
    - **Effect size:** Moderate

    **Interpretation:**

    This is the strongest predictor of low mood
    in our dataset. The positive slope shows
    that higher comparison frequency associates
    with more frequent low mood.

    *(Points jittered for visibility)*
    """)

st.divider()

# Assumptions and Limitations
st.subheader("Methodology Notes")

st.markdown("""
**Test selection rationale:**

- **Spearman correlation** used for Likert scale variables (ordinal, non-normal)
- **Kruskal-Wallis H** used for comparing groups with ordinal outcomes
- **No parametric tests** (Pearson, ANOVA) due to non-normal distributions

**Limitations:**

1. **Cross-sectional design:** Cannot establish temporal ordering or causation
2. **Self-report bias:** All measures are self-reported and subject to recall/social desirability effects
3. **Sample composition:** Predominantly university students aged 18-24; may not generalise
4. **Multiple testing:** 5 hypotheses tested; some findings may be inflated by chance
5. **Confounding:** Unmeasured variables (e.g., pre-existing mental health conditions) could explain associations
""")

st.info("""
**For researchers:**
The full analysis code is available in the `jupyter_notebooks/02_EDA_and_Tests.ipynb` notebook.
Raw correlation matrices and test outputs are documented in `reports/eda_summary.md`.
""")

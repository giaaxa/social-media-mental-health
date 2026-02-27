"""
Interactive Dashboard
=====================

Plotly-powered interactive charts with filters for exploration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from pathlib import Path

st.set_page_config(
    page_title="Dashboard | SM & Mental Wellbeing",
    page_icon="📊",
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
st.title("Interactive Dashboard")
st.markdown("Explore the data with filters and interactive charts.")

st.divider()

# Sidebar filters
st.sidebar.header("Filters")

# Age filter
age_options = ["All"] + sorted(df["age_band"].unique().tolist(), key=lambda x: (x != "<18", x))
selected_age = st.sidebar.selectbox("Age Band", age_options)

# Gender filter
gender_options = ["All"] + sorted(df["gender_grouped"].unique().tolist())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Time band filter
time_order = [
    "Less than an Hour",
    "Between 1 and 2 hours",
    "Between 2 and 3 hours",
    "Between 3 and 4 hours",
    "Between 4 and 5 hours",
    "More than 5 hours",
]
time_options = ["All"] + time_order
selected_time = st.sidebar.selectbox("Daily Time Spent", time_options)

# Occupation filter
occupation_options = ["All"] + sorted(df["occupation_status"].unique().tolist())
selected_occupation = st.sidebar.selectbox("Occupation", occupation_options)

# Apply filters
df_filtered = df.copy()

if selected_age != "All":
    df_filtered = df_filtered[df_filtered["age_band"] == selected_age]

if selected_gender != "All":
    df_filtered = df_filtered[df_filtered["gender_grouped"] == selected_gender]

if selected_time != "All":
    df_filtered = df_filtered[df_filtered["daily_time_band"] == selected_time]

if selected_occupation != "All":
    df_filtered = df_filtered[df_filtered["occupation_status"] == selected_occupation]

# Show filter summary
st.sidebar.divider()
st.sidebar.metric("Filtered Sample Size", f"{len(df_filtered):,}")

if len(df_filtered) < 30:
    st.sidebar.warning("Small sample size — interpret with caution")

st.sidebar.divider()
st.sidebar.markdown("**Reset filters** by selecting 'All' for each option.")

# Main dashboard content
if len(df_filtered) == 0:
    st.error("No data matches the selected filters. Please adjust your selections.")
else:
    # Row 1: Key metrics for filtered data
    st.subheader("Summary Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Sample Size", f"{len(df_filtered):,}")

    with col2:
        avg_mood = df_filtered["low_mood_freq"].mean()
        st.metric("Avg Low Mood Score", f"{avg_mood:.2f}")

    with col3:
        avg_comparison = df_filtered["compare_to_successful"].mean()
        st.metric("Avg Comparison Score", f"{avg_comparison:.2f}")

    with col4:
        avg_time = df_filtered["daily_hours_midpoint"].mean()
        st.metric("Avg Daily Hours", f"{avg_time:.1f}h")

    st.divider()

    # Row 2: Correlation heatmap and box plot
    st.subheader("Behaviour vs Wellbeing")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Correlation Heatmap**")

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
        ]

        # Calculate correlations for filtered data
        corr_data = []
        for b_col in behaviour_cols:
            row = []
            for w_col in wellbeing_cols:
                if len(df_filtered) >= 10:
                    rho, _ = stats.spearmanr(df_filtered[b_col], df_filtered[w_col])
                    row.append(rho)
                else:
                    row.append(np.nan)
            corr_data.append(row)

        corr_matrix = pd.DataFrame(
            corr_data,
            index=["Purposeless", "Distracted", "Restless", "Comparison", "Validation"],
            columns=["Low Mood", "Sleep", "Worries", "Concentration"],
        )

        fig_heatmap = px.imshow(
            corr_matrix.values,
            x=corr_matrix.columns.tolist(),
            y=corr_matrix.index.tolist(),
            color_continuous_scale="RdBu_r",
            zmin=-0.6,
            zmax=0.6,
            text_auto=".2f",
            aspect="auto",
        )
        fig_heatmap.update_layout(height=350, coloraxis_colorbar_title="rho")
        st.plotly_chart(fig_heatmap, use_container_width=True)

    with col2:
        st.markdown("**Low Mood by Time Spent**")

        if len(df_filtered["daily_time_band"].unique()) > 1:
            fig_box = px.box(
                df_filtered,
                x="daily_time_band",
                y="low_mood_freq",
                category_orders={"daily_time_band": time_order},
                color="daily_time_band",
                color_discrete_sequence=px.colors.sequential.Blues,
            )
            fig_box.update_layout(
                xaxis_tickangle=-45,
                showlegend=False,
                height=350,
                xaxis_title="Daily Time Spent",
                yaxis_title="Low Mood (1-5)",
            )
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("Select 'All' for Daily Time Spent to see this chart.")

    st.divider()

    # Row 3: Scatter plots
    st.subheader("Relationship Explorer")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Social Comparison vs Low Mood**")

        df_plot = df_filtered.copy()
        df_plot["compare_jitter"] = df_plot["compare_to_successful"] + np.random.uniform(-0.15, 0.15, len(df_plot))
        df_plot["mood_jitter"] = df_plot["low_mood_freq"] + np.random.uniform(-0.15, 0.15, len(df_plot))

        fig_scatter1 = px.scatter(
            df_plot,
            x="compare_jitter",
            y="mood_jitter",
            opacity=0.6,
            trendline="ols" if len(df_filtered) >= 10 else None,
            color_discrete_sequence=["#e74c3c"],
        )
        fig_scatter1.update_layout(
            height=320,
            xaxis_title="Comparison Frequency (1-5)",
            yaxis_title="Low Mood Frequency (1-5)",
        )
        fig_scatter1.update_traces(marker=dict(size=8))
        st.plotly_chart(fig_scatter1, use_container_width=True)

    with col2:
        st.markdown("**Purposeless Use vs Low Mood**")

        df_plot2 = df_filtered.copy()
        df_plot2["purpose_jitter"] = df_plot2["purposeless_use"] + np.random.uniform(-0.15, 0.15, len(df_plot2))
        df_plot2["mood_jitter"] = df_plot2["low_mood_freq"] + np.random.uniform(-0.15, 0.15, len(df_plot2))

        fig_scatter2 = px.scatter(
            df_plot2,
            x="purpose_jitter",
            y="mood_jitter",
            opacity=0.6,
            trendline="ols" if len(df_filtered) >= 10 else None,
            color_discrete_sequence=["#3498db"],
        )
        fig_scatter2.update_layout(
            height=320,
            xaxis_title="Purposeless Use (1-5)",
            yaxis_title="Low Mood Frequency (1-5)",
        )
        fig_scatter2.update_traces(marker=dict(size=8))
        st.plotly_chart(fig_scatter2, use_container_width=True)

    st.divider()

    # Row 4: Distributions
    st.subheader("Distributions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Platform Usage**")

        platform_cols = [col for col in df_filtered.columns if col.startswith("platform_") and col != "platform_count"]
        platform_usage = {col.replace("platform_", "").title(): df_filtered[col].sum() for col in platform_cols}
        platform_df = pd.DataFrame(list(platform_usage.items()), columns=["Platform", "Users"])
        platform_df = platform_df.sort_values("Users", ascending=True)

        fig_platform = px.bar(
            platform_df,
            x="Users",
            y="Platform",
            orientation="h",
            color="Users",
            color_continuous_scale="Greens",
        )
        fig_platform.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=320,
        )
        st.plotly_chart(fig_platform, use_container_width=True)

    with col2:
        st.markdown("**Low Mood Distribution**")

        mood_counts = df_filtered["low_mood_freq"].value_counts().sort_index().reset_index()
        mood_counts.columns = ["Score", "Count"]

        fig_mood = px.bar(
            mood_counts,
            x="Score",
            y="Count",
            color="Count",
            color_continuous_scale="Reds",
        )
        fig_mood.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=320,
            xaxis_title="Low Mood Score (1-5)",
        )
        st.plotly_chart(fig_mood, use_container_width=True)

    with col3:
        st.markdown("**Comparison Distribution**")

        comp_counts = df_filtered["compare_to_successful"].value_counts().sort_index().reset_index()
        comp_counts.columns = ["Score", "Count"]

        fig_comp = px.bar(
            comp_counts,
            x="Score",
            y="Count",
            color="Count",
            color_continuous_scale="Purples",
        )
        fig_comp.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            height=320,
            xaxis_title="Comparison Score (1-5)",
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    st.divider()

    # Footer note
    st.caption("""
    **Note:** Charts update based on your filter selections.
    Small sample sizes (n < 30) may produce unreliable patterns.
    Scatter plots include jitter to show overlapping points.
    """)

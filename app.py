"""
Social Media & Mental Wellbeing Insights - Streamlit App
=========================================================

Main entry point and Overview page for the analytics dashboard.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Social Media & Mental Wellbeing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load data
@st.cache_data
def load_data():
    """Load the cleaned dataset."""
    data_path = Path("data/processed/v1/smmh_clean.csv")
    df = pd.read_csv(data_path)
    # Filter to social media users only
    df = df[df["include_in_analysis"] == True].copy()
    return df

df = load_data()

# Header
st.title("Social Media & Mental Wellbeing Insights")
st.markdown("""
This app explores how social media usage patterns relate to **self-reported wellbeing indicators**
in a public survey dataset.

**This is for educational purposes only.** It does not diagnose, predict, or treat mental health conditions.
""")

st.divider()

# Key metrics row
st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Respondents", f"{len(df):,}")

with col2:
    avg_time = df["daily_hours_midpoint"].mean()
    st.metric("Avg Daily Hours", f"{avg_time:.1f}h")

with col3:
    avg_platforms = df["platform_count"].mean()
    st.metric("Avg Platforms Used", f"{avg_platforms:.1f}")

with col4:
    pct_high_use = (df["daily_time_band"].isin(["Between 4 and 5 hours", "More than 5 hours"])).mean() * 100
    st.metric("High Usage (4+ hrs)", f"{pct_high_use:.0f}%")

st.divider()

# Two column layout for distributions
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Daily Time Spent on Social Media")

    # Order the time bands properly
    time_order = [
        "Less than an Hour",
        "Between 1 and 2 hours",
        "Between 2 and 3 hours",
        "Between 3 and 4 hours",
        "Between 4 and 5 hours",
        "More than 5 hours",
    ]

    time_counts = df["daily_time_band"].value_counts().reindex(time_order).reset_index()
    time_counts.columns = ["Time Band", "Count"]

    fig_time = px.bar(
        time_counts,
        x="Time Band",
        y="Count",
        color="Count",
        color_continuous_scale="Blues",
    )
    fig_time.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        xaxis_tickangle=-45,
        height=350,
    )
    st.plotly_chart(fig_time, use_container_width=True)

    st.caption("Most respondents spend 3+ hours daily on social media.")

with col_right:
    st.subheader("Platform Usage")

    # Calculate platform usage
    platform_cols = [col for col in df.columns if col.startswith("platform_") and col != "platform_count"]
    platform_usage = {col.replace("platform_", "").title(): df[col].sum() for col in platform_cols}
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
        height=350,
    )
    st.plotly_chart(fig_platform, use_container_width=True)

    st.caption("YouTube, Facebook, and Instagram are the most commonly used platforms.")

st.divider()

# Demographics section
st.subheader("Who's in the Dataset?")

col_demo1, col_demo2, col_demo3 = st.columns(3)

with col_demo1:
    st.markdown("**Age Distribution**")
    age_order = ["<18", "18-24", "25-34", "35-44", "45+"]
    age_counts = df["age_band"].value_counts().reindex(age_order).reset_index()
    age_counts.columns = ["Age Band", "Count"]

    fig_age = px.pie(
        age_counts,
        values="Count",
        names="Age Band",
        color_discrete_sequence=px.colors.sequential.Blues_r,
    )
    fig_age.update_layout(height=280)
    st.plotly_chart(fig_age, use_container_width=True)

with col_demo2:
    st.markdown("**Gender Distribution**")
    gender_counts = df["gender_grouped"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]

    fig_gender = px.pie(
        gender_counts,
        values="Count",
        names="Gender",
        color_discrete_sequence=px.colors.sequential.Purples_r,
    )
    fig_gender.update_layout(height=280)
    st.plotly_chart(fig_gender, use_container_width=True)

with col_demo3:
    st.markdown("**Occupation Status**")
    occ_counts = df["occupation_status"].value_counts().reset_index()
    occ_counts.columns = ["Occupation", "Count"]

    fig_occ = px.pie(
        occ_counts,
        values="Count",
        names="Occupation",
        color_discrete_sequence=px.colors.sequential.Oranges_r,
    )
    fig_occ.update_layout(height=280)
    st.plotly_chart(fig_occ, use_container_width=True)

st.info("""
**Note on sample composition:** This dataset is dominated by university students aged 18-24.
Findings may not generalise to other populations.
""")

st.divider()

# Navigation guide
st.subheader("Explore the App")
st.markdown("""
Use the sidebar to navigate between pages:

- **Insights** — Plain-English takeaways from the data
- **Technical** — Statistical tests, effect sizes, and methodology
- **Ethics** — Privacy, governance, and limitations
- **Dashboard** — Interactive charts with filters for exploration
""")

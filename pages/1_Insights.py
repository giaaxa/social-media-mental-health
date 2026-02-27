"""
Insights Page 
=======================================

Non-technical summary of key findings from the data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Insights | SM & Mental Wellbeing",
    page_icon="💡",
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
st.title("Key Insights")
st.markdown("""
These are the main patterns we found in the data. Remember: **these are associations, not causes**.
We cannot say social media *causes* low mood — only that they tend to occur together in this dataset.
""")

st.divider()

# Insight 1: Social Comparison
st.subheader("1. Social Comparison is Strongly Linked to Low Mood")

col1, col2 = st.columns([2, 1])

with col1:
    # Create binned comparison chart
    df["comparison_level"] = pd.cut(
        df["compare_to_successful"],
        bins=[0, 2, 3, 5],
        labels=["Low (1-2)", "Medium (3)", "High (4-5)"],
    )

    comparison_mood = df.groupby("comparison_level", observed=True)["low_mood_freq"].mean().reset_index()
    comparison_mood.columns = ["Comparison Level", "Avg Low Mood Score"]

    fig1 = px.bar(
        comparison_mood,
        x="Comparison Level",
        y="Avg Low Mood Score",
        color="Avg Low Mood Score",
        color_continuous_scale="Reds",
        text=comparison_mood["Avg Low Mood Score"].round(2),
    )
    fig1.update_layout(
        yaxis_range=[0, 5],
        showlegend=False,
        coloraxis_showscale=False,
        height=300,
    )
    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("""
    **What this means:**

    People who frequently compare themselves to successful others on social media
    report feeling down more often.

    - **Low comparers:** avg mood score ~2.5
    - **High comparers:** avg mood score ~3.5

    This was the strongest association we found (rho = 0.40).
    """)

st.divider()

# Insight 2: Purposeless Scrolling
st.subheader("2. Purposeless Scrolling Correlates with Lower Wellbeing")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
    **What this means:**

    Using social media "just because" — without a specific goal — is associated
    with higher low mood frequency.

    People who scroll purposelessly more often tend to report:
    - More frequent low mood
    - More distraction issues
    - More sleep problems

    This suggests *how* you use social media may matter as much as *how long*.
    """)

with col2:
    df["purposeless_level"] = pd.cut(
        df["purposeless_use"],
        bins=[0, 2, 3, 5],
        labels=["Low (1-2)", "Medium (3)", "High (4-5)"],
    )

    purposeless_mood = df.groupby("purposeless_level", observed=True)["low_mood_freq"].mean().reset_index()
    purposeless_mood.columns = ["Purposeless Use Level", "Avg Low Mood Score"]

    fig2 = px.bar(
        purposeless_mood,
        x="Purposeless Use Level",
        y="Avg Low Mood Score",
        color="Avg Low Mood Score",
        color_continuous_scale="Oranges",
        text=purposeless_mood["Avg Low Mood Score"].round(2),
    )
    fig2.update_layout(
        yaxis_range=[0, 5],
        showlegend=False,
        coloraxis_showscale=False,
        height=300,
    )
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# Insight 3: Time Spent
st.subheader("3. More Time on Social Media = Higher Low Mood (On Average)")

time_order = [
    "Less than an Hour",
    "Between 1 and 2 hours",
    "Between 2 and 3 hours",
    "Between 3 and 4 hours",
    "Between 4 and 5 hours",
    "More than 5 hours",
]

time_mood = df.groupby("daily_time_band")["low_mood_freq"].agg(["mean", "count"]).reset_index()
time_mood.columns = ["Time Band", "Avg Low Mood", "Count"]
time_mood["Time Band"] = pd.Categorical(time_mood["Time Band"], categories=time_order, ordered=True)
time_mood = time_mood.sort_values("Time Band")

fig3 = px.bar(
    time_mood,
    x="Time Band",
    y="Avg Low Mood",
    color="Avg Low Mood",
    color_continuous_scale="Blues",
    text=time_mood["Avg Low Mood"].round(2),
)
fig3.update_layout(
    yaxis_range=[0, 5],
    xaxis_tickangle=-45,
    showlegend=False,
    coloraxis_showscale=False,
    height=350,
)
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **What this means:**

    There's a general trend: people who spend more time on social media
    tend to report feeling down more frequently.

    However, the relationship isn't perfectly linear — there's a lot of
    individual variation.
    """)

with col2:
    st.warning("""
    **Important caveat:**

    We can't tell which comes first. Do people feel low *because* they
    use social media a lot? Or do they use social media more *because*
    they're feeling low? This data can't answer that question.
    """)

st.divider()

# Summary box
st.subheader("Summary")

st.success("""
**Three key takeaways:**

1. **Social comparison** shows the strongest link to low mood — consider limiting comparison-focused activities
2. **Purposeless scrolling** is associated with poorer wellbeing — intentional use may be healthier
3. **Time spent** matters, but *how* you spend it may matter more

These patterns are consistent with broader research on digital wellbeing, but remember:
this is one survey dataset and cannot establish causation.
""")

"""
Ethics & Governance Page
========================

Privacy decisions, legal/social implications, bias and harm mitigation.
"""

import streamlit as st

st.set_page_config(
    page_title="Ethics | SM & Mental Wellbeing",
    page_icon="⚖️",
    layout="wide",
)

# Header
st.title("Ethics & Governance")
st.markdown("""
This project involves self-reported wellbeing data. While the dataset is publicly available,
responsible handling of such data requires careful consideration of privacy, bias, and potential harms.
""")

st.divider()

# Privacy Section
st.subheader("Privacy & Data Protection")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Risks identified:**

    - **Re-identification risk:** Combining age, gender, occupation, and
      specific response patterns could potentially identify individuals
    - **Sensitive data:** Wellbeing indicators touch on mental health,
      which requires heightened protection
    - **Secondary use concerns:** Original survey participants may not
      have anticipated this specific use
    """)

with col2:
    st.markdown("""
    **Mitigations applied:**

    - **Timestamp dropped:** Removed from processed dataset to reduce
      re-identification risk
    - **Age banding:** Exact ages grouped into bands (<18, 18-24, etc.)
    - **Gender aggregation:** Small groups combined into "Non-binary & Other"
      to prevent identification
    - **No row-level display:** App shows only aggregated statistics,
      never individual responses
    - **Suppression:** Groups with n < 10 excluded from some analyses
    """)

st.divider()

# Bias Section
st.subheader("Bias & Representativeness")

st.warning("""
**Critical limitation:** This dataset is not representative of the general population.

- 64% of respondents are aged 18-24
- Predominantly university students
- Self-selected survey participants (response bias)
- Unknown geographic distribution
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **What this means:**

    - Findings may not apply to older adults, non-students,
      or different cultural contexts
    - People who chose to respond may differ systematically
      from those who didn't
    - The "average" patterns we show are averages for
      *this sample*, not universal truths
    """)

with col2:
    st.markdown("""
    **How we've addressed this:**

    - Clear documentation of sample composition on Overview page
    - Explicit "may not generalise" warnings throughout
    - Segment comparisons available in Dashboard to explore
      whether patterns differ by group
    - No claims about causation or universal applicability
    """)

st.divider()

# Harm Mitigation Section
st.subheader("Potential Harms & Mitigations")

st.markdown("""
Analytics about mental wellbeing can cause harm if misinterpreted or misused.
We've taken steps to reduce these risks:
""")

harm_table = """
| Potential Harm | Mitigation |
|----------------|------------|
| **Stigmatisation:** Presenting social media users as "unhealthy" | We emphasise associations, not judgments. Correlations don't mean social media is bad. |
| **Self-diagnosis:** Users applying findings to themselves | Prominent disclaimers that this is not clinical advice. No individual-level predictions. |
| **Oversimplification:** "Just use social media less" messaging | We highlight that *how* you use it may matter more than *how long*. |
| **Causal claims:** "Social media causes depression" | Repeated emphasis that these are associations only. Cross-sectional data cannot establish causation. |
| **Platform blame:** Singling out specific platforms | We don't make claims about individual platforms being "worse" — sample sizes don't support this. |
"""

st.markdown(harm_table)

st.divider()

# Legal & Social Implications
st.subheader("Legal & Social Considerations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Legal context:**

    - **Data source:** Publicly available Kaggle dataset
    - **Lawful basis:** Educational/research use of anonymised public data
    - **GDPR note:** If this were operational with EU data, Article 9
      (special categories) would apply to health-related inferences
    - **No profiling:** We don't make predictions about individuals
      or automate decisions affecting people
    """)

with col2:
    st.markdown("""
    **Social responsibility:**

    - **Transparency:** Methods and limitations clearly documented
    - **Accessibility:** Plain-English explanations alongside technical details
    - **No commercial exploitation:** Educational project only
    - **Source attribution:** Dataset and methods fully cited
    """)

st.divider()

# Governance Practices
st.subheader("Governance Practices in This Project")

st.markdown("""
**Documentation:**
- Data dictionary with all variable definitions
- ETL report showing all transformations applied
- Jupyter notebooks with full analysis code

**Reproducibility:**
- Versioned datasets (`data/processed/v1/`)
- Pinned package versions in requirements.txt
- All code available in repository

**Quality controls:**
- Validation checks in ETL pipeline (Likert ranges, data types)
- Pre-registered hypotheses tested in EDA notebook
- Effect sizes reported alongside p-values
""")

st.divider()

# Responsible Use
st.subheader("Guidance for Users")

st.info("""
**If you're exploring this app for personal insight:**

- This data represents group-level patterns, not individual diagnoses
- Your experience may differ significantly from the averages shown
- If you're concerned about your mental wellbeing, please speak to a qualified professional
- Consider the insights as conversation starters, not conclusions

**If you're using this for research or policy:**

- Review the methodology limitations on the Technical page
- Do not generalise beyond the sample population without additional evidence
- Cite the original data source and acknowledge limitations
- Consider replication with more representative samples
""")

st.divider()

# Resources
st.subheader("Mental Health Resources")

st.markdown("""
If you or someone you know is struggling with mental health:

- **UK:** Samaritans — 116 123 (free, 24/7)
- **US:** National Suicide Prevention Lifeline — 988
- **International:** [findahelpline.com](https://findahelpline.com/)

This app is not a substitute for professional support.
""")

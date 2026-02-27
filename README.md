# Social Media & Mental Wellbeing Insights

A data app that explores how social media usage patterns (time spent, distraction, comparison, validation-seeking) relate to **self-reported wellbeing indicators** (low mood, sleep issues, worry, concentration) in a public survey dataset.

This project is for learning and communication of data insights. It is **not medical advice** and does **not** diagnose, predict, or treat mental health conditions.

# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

---

## Live Links
- Streamlit App: *(coming soon)*

---

## Project Purpose
People often *feel* that social media affects their wellbeing, but it’s hard to pinpoint which behaviours are most associated with negative outcomes (e.g., purposeless scrolling, distraction, constant comparison).

This project provides a **clear, ethical, non-clinical** analytics view of those associations, with:
- plain-English takeaways for non-technical users
- transparent methods for technical reviewers
- governance and harm-reduction decisions documented throughout

### Target audience
- Digital wellbeing / student support / community wellbeing stakeholders (non-clinical)
- Product teams exploring “healthy use” features (high-level insights only)
- Individuals curious about patterns (educational use)

---

## Dataset
**Source:** Kaggle — *“Social Media and Mental Health”* (`smmh.csv`)  
**Rows / Columns:** 481 rows × 21 columns  
**Type:** Self-reported survey responses

### What’s in the data (high level)
- **Demographics:** age, gender, relationship status, occupation status, organisation affiliation
- **Usage:** social media usage (Yes/No), platforms used, daily time spent (time bands)
- **Behaviour (Likert / frequency):** purposeless use, distraction, restlessness, validation-seeking, comparison
- **Wellbeing indicators (Likert):** low mood frequency, sleep issues, worry, concentration difficulty, interest fluctuation

---

## Data Handling & Cleaning (ETL)
Because the dataset includes wellbeing-related survey responses, the project follows a **data minimisation** approach and avoids unnecessary personal data exposure.

Key ETL steps (Python):
- Rename long survey questions into short, readable feature names (data dictionary generated)
- Standardise categorical values (e.g., gender variants, consistent casing)
- Convert Likert responses to numeric (1–5) and validate ranges
- Parse the multi-select platforms field into platform flags (e.g., `uses_instagram = 0/1`)
- Handle missing values (organisation affiliation → `Unknown`)
- Filter or flag the small number of respondents who answered **“No”** to using social media (so comparisons aren’t misleading)
- **Drop `Timestamp`** from the processed dataset to reduce re-identification risk
- Save cleaned data to `data/processed/v1/`

Outputs produced:
- `data/processed/v1/smmh_clean.csv`
- `docs/data_dictionary.md`

---

## Business Requirements (What the App Must Answer)
1. **Usage Overview**
   - How much time do respondents spend on social media daily?
   - Which platforms are most commonly used?
2. **Wellbeing Overview**
   - What is the distribution of self-reported wellbeing indicators (low mood, sleep issues, worry, etc.)?
3. **Key Associations**
   - Which usage behaviours are most strongly associated with negative wellbeing indicators *in this dataset*?
4. **Segment Comparisons**
   - Do patterns differ by age band, gender (carefully aggregated), occupation status, etc.?
5. **Evidence**
   - Provide statistical tests + effect sizes where appropriate, with plain-English interpretation.
6. **Predictive Prototype (Optional, Non-clinical)**
   - A simple model that estimates the likelihood of **higher self-reported low mood frequency** based on usage behaviours.
   - Shown as an educational prototype only (not for decisions or profiling).

---

## Hypotheses Tested (Association, Not Causation)
> These tests evaluate relationships in the dataset only. They do not establish causation.

**Primary outcome used for several tests:** `low_mood_freq` (survey Q18, 1–5)

**H1:** Higher daily time spent is associated with higher low mood frequency.  
- Test: Kruskal–Wallis (time bands vs low mood) + effect size  
- Visual: box/violin by daily time band

**H2:** More purposeless use is associated with higher low mood frequency.  
- Test: Spearman correlation + effect size  
- Visual: binned trend or scatter

**H3:** Higher comparison frequency is associated with higher low mood frequency.  
- Test: Spearman correlation  
- Visual: binned bars or scatter

**H4:** Validation-seeking is associated with higher low mood frequency.  
- Test: Spearman correlation  
- Visual: box/violin or binned % high outcome

**H5:** Distraction / restlessness is associated with sleep issues.  
- Test: Spearman correlation + group comparison  
- Visual: grouped bars or scatter

(Additional hypotheses are included only if they directly support a business requirement.)

---

## Streamlit App Structure

The Streamlit app provides a user-friendly experience with interactive visualisations:

- **Page 1 — Overview**
  - Dataset context, who it represents, headline KPIs and distributions
- **Page 2 — Insights (Non-technical)**
  - 2–3 plain-English takeaways with supportive visuals
- **Page 3 — Deep Dive (Technical)**
  - Statistical tests, assumptions, effect sizes, and limitations
- **Page 4 — Ethics & Governance**
  - Privacy decisions, legal/social implications, bias and harm mitigation
- **Page 5 — Interactive Dashboard**
  - Plotly-powered interactive charts with filters for exploration
  - Bar charts, heatmaps, box plots, and scatter plots
  - Filters for time band, age band, gender, occupation status

---

## Ethics, Privacy & Governance (LO1)
This project includes self-reported wellbeing indicators. In real-world use, this type of data can be **sensitive** and requires stronger governance.

### Key ethical risks and mitigations
- **Privacy & re-identification risk**
  - Mitigation: drop timestamps, avoid row-level displays, report aggregates, suppress very small groups.
- **Stigma / harm from misinterpretation**
  - Mitigation: avoid diagnostic language, present associations not “effects”, include limitations prominently.
- **Bias & representativeness**
  - Mitigation: document sampling limitations (survey skew), avoid broad generalisations, compare patterns across segments carefully.
- **Automated profiling risk (if modelling is included)**
  - Mitigation: the prototype is educational only, clearly labelled, and not intended for decisions about individuals.

### Governance practices used in this repo
- Data minimisation and clear purpose
- Documented feature definitions (data dictionary)
- Versioned datasets (`v1`, `v2`, …) to support reproducibility
- Clear attribution of dataset and sources

---

## Legal & Social Implications (LO1)
- **Legal:** wellbeing-related data requires careful handling in real deployments (lawful basis, additional safeguards, access controls). This project is published as educational analytics and avoids individual-level outputs.
- **Social:** dashboards can unintentionally reinforce stigma or “one-size-fits-all” narratives. This project uses careful wording, avoids causal claims, and focuses on patterns at group level.

---

## Communication Strategy (LO2)
To make insights accessible to both technical and non-technical audiences:
- Each key visual includes a **plain-English “What this means”** explanation.
- The app separates:
  - **Insights layer:** simple summaries + actionable interpretations
  - **Methods layer:** test choice, assumptions, effect sizes, caveats
- Documentation is structured and consistent (README + data dictionary + notebook commentary).

---

## Project Plan (LO3)

### Implementation
- ETL + validation → processed dataset
- EDA + hypothesis testing notebooks
- Streamlit app with interactive Plotly dashboard
- UX + accessibility pass (labels, readable layout, clear navigation)

### Maintenance (If this were a real app)
- Refresh cadence: monthly/quarterly
- Data validation checks: schema, value ranges (Likert 1–5), missingness thresholds
- Versioning approach: `data/processed/v2/` etc.

### Updates
- Improve platform feature engineering (multi-platform intensity)
- Stronger segment checks (age bands, gender standardisation)
- Better explanatory text and annotations based on feedback

### Evaluation
- Lightweight user testing (3–5 users)
- Success criteria:
  - Non-technical users can explain 2 key insights correctly
  - Users understand limitations (association ≠ causation)
  - Navigation and labels are intuitive

---

## Tools Used
- Python: pandas, numpy
- Stats: scipy.stats / statsmodels
- Visuals: plotly (interactive charts)
- App UI: streamlit

---

## How to Run Locally
1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

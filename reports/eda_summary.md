# EDA Summary Report

**Generated:** 2026-02-26 19:31
**Dataset:** smmh_clean.csv (n=478 social media users)

## Key Findings

1. **Social comparison is strongly associated with low mood.** Respondents who frequently compare themselves to successful people on social media report higher low mood frequency (rho=0.40, p<0.001).

2. **Purposeless scrolling correlates with low mood.** Those who use social media without specific purpose more often report higher low mood frequency (rho=0.29, p<0.001).

3. **Validation-seeking behaviour shows a moderate association with low mood.** Respondents who more frequently seek validation through social media features also report higher low mood (rho=0.26, p<0.001).

## Hypothesis Test Results

| ID | Predictor | Outcome | Statistic | Effect Size | Significant? |
|----|-----------|---------|-----------|-------------|--------------|
| H1 | daily_time_band | low_mood_freq | H=53.7 | moderate | Yes |
| H2 | purposeless_use | low_mood_freq | rho=0.29 | small | Yes |
| H3 | compare_to_successful | low_mood_freq | rho=0.40 | moderate | Yes |
| H4 | seek_validation | low_mood_freq | rho=0.26 | small | Yes |
| H5 | restless_without_sm | sleep_issues | rho=0.16 | small | Yes |

## Notable Distributions

- **Daily time:** Most common is "More than 5 hours" (116 respondents)
- **Platforms:** YouTube (86%), Facebook (85%), Instagram (75%)
- **Demographics:** 18-24 age band dominates (308 respondents, 64%)

## Limitations

1. **Cross-sectional data:** Cannot determine causality. Associations may be bidirectional.
2. **Self-reported measures:** Subject to recall bias and social desirability effects.
3. **Sample composition:** Dominated by university students aged 18-24.
4. **Small subgroups:** Non-binary & Other group excluded from gender comparison (n<10).

## Next Steps (Tableau/Streamlit)

1. Create interactive filters for age_band, gender_grouped, daily_time_band
2. Build dashboard with key visualisations
3. Add plain-English interpretation panels
4. Include prominent "association ≠ causation" disclaimers

# ETL Report

**Generated:** 2026-02-23 17:07

## Dataset Shape

| Metric | Before | After |
|--------|--------|-------|
| Rows | 481 | 481 |
| Columns | 21 | 40 |
| Duplicate rows | 0 | 0 |

## Columns Added/Removed

- **Dropped:** `timestamp` (privacy/re-identification risk)
- **Added:** `age_band`, `gender_clean`, `gender_grouped`, `daily_hours_midpoint`, platform flags, affiliation flags, `include_in_analysis`

## Missingness Summary

| Column | Missing Count | % |
|--------|---------------|---|
| `org_affiliations_raw` | 30 | 6.24% |

## Gender Distribution

### Cleaned

| Gender | Count | % |
|--------|-------|---|
| Female | 263 | 54.7% |
| Male | 211 | 43.9% |
| Non-binary | 4 | 0.8% |
| Unsure | 1 | 0.2% |
| Trans | 1 | 0.2% |
| Other | 1 | 0.2% |

### Grouped

| Gender Group | Count | % |
|--------------|-------|---|
| Female | 263 | 54.7% |
| Male | 211 | 43.9% |
| Non-binary & Other | 7 | 1.5% |

## Platform Usage

| Platform | Users | % |
|----------|-------|---|
| Facebook | 407 | 84.6% |
| Twitter | 131 | 27.2% |
| Instagram | 359 | 74.6% |
| YouTube | 412 | 85.7% |
| Snapchat | 181 | 37.6% |
| Discord | 198 | 41.2% |
| Reddit | 126 | 26.2% |
| Pinterest | 145 | 30.1% |
| TikTok | 94 | 19.5% |

## Social Media Usage

- **Uses social media:** 478 (99.4%)
- **Does not use SM:** 3 (0.6%)

## Analysis Inclusion

- **Included (`include_in_analysis=True`):** 478 rows
- **Excluded (`include_in_analysis=False`):** 3 rows

Excluded rows are respondents who answered 'No' to using social media. They are retained in the dataset but should be filtered out for SM-behaviour analysis.

## Data Quality

- All Likert columns validated: values in range 1-5
- No duplicate rows
- Timestamp dropped for privacy

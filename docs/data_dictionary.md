# Data Dictionary

**Dataset:** smmh_clean.csv
**Generated:** 2026-02-23 17:07
**Rows:** 481
**Columns:** 40

## Column Reference

| Cleaned Name | Type | Allowed Values | Description | Original Column |
|--------------|------|----------------|-------------|-----------------|
| `age` | numeric | 1-100+ | Respondent age in years | 1. What is your age? |
| `age_band` | categorical | <18, 18-24, 25-34, 35-44, 45+, Unknown | Age grouped into bands for privacy | — |
| `gender_clean` | categorical | Male, Female, Non-binary, Trans, Unsure, Other, Prefer not to say | Standardised gender response | — |
| `gender_grouped` | categorical | Male, Female, Non-binary & Other, Prefer not to say | Aggregated gender for small-group privacy | — |
| `relationship_status` | categorical | Single, In a relationship, Married, Divorced | Relationship status | 3. Relationship Status |
| `occupation_status` | categorical | University Student, School Student, Salaried Worker, Retired | Current occupation | 4. Occupation Status |
| `uses_social_media` | boolean | True, False | Whether respondent uses social media | 6. Do you use social media? |
| `daily_time_band` | ordinal | Less than an Hour to More than 5 hours | Original time band response | 8. What is the average time you spend on social me... |
| `daily_hours_midpoint` | numeric | 0.5-5.5 | Numeric midpoint of time band for analysis | — |
| `platform_facebook` | boolean | 0, 1 | Uses Facebook (derived from platforms_raw) | — |
| `platform_twitter` | boolean | 0, 1 | Uses Twitter (derived from platforms_raw) | — |
| `platform_instagram` | boolean | 0, 1 | Uses Instagram (derived from platforms_raw) | — |
| `platform_youtube` | boolean | 0, 1 | Uses YouTube (derived from platforms_raw) | — |
| `platform_snapchat` | boolean | 0, 1 | Uses Snapchat (derived from platforms_raw) | — |
| `platform_discord` | boolean | 0, 1 | Uses Discord (derived from platforms_raw) | — |
| `platform_reddit` | boolean | 0, 1 | Uses Reddit (derived from platforms_raw) | — |
| `platform_pinterest` | boolean | 0, 1 | Uses Pinterest (derived from platforms_raw) | — |
| `platform_tiktok` | boolean | 0, 1 | Uses TikTok (derived from platforms_raw) | — |
| `platform_count` | numeric | 0-9 | Count of platforms used | — |
| `affil_university` | boolean | 0, 1 | Affiliated with University | — |
| `affil_school` | boolean | 0, 1 | Affiliated with School | — |
| `affil_company` | boolean | 0, 1 | Affiliated with Company | — |
| `affil_private` | boolean | 0, 1 | Affiliated with Private organisation | — |
| `affil_government` | boolean | 0, 1 | Affiliated with Government | — |
| `affil_na` | boolean | 0, 1 | Affiliated with No affiliation / N/A | — |
| `purposeless_use` | ordinal | 1-5 | Frequency of using SM without specific purpose | 9. How often do you find yourself using Social med... |
| `distracted_when_busy` | ordinal | 1-5 | Frequency of SM distraction when busy | 10. How often do you get distracted by Social medi... |
| `restless_without_sm` | ordinal | 1-5 | Restlessness when not using SM | 11. Do you feel restless if you haven't used Socia... |
| `easily_distracted` | ordinal | 1-5 | General distractibility (1=low, 5=high) | 12. On a scale of 1 to 5, how easily distracted ar... |
| `worries_bother` | ordinal | 1-5 | How much worries bother respondent | 13. On a scale of 1 to 5, how much are you bothere... |
| `difficulty_concentrating` | ordinal | 1-5 | Difficulty concentrating on things | 14. Do you find it difficult to concentrate on thi... |
| `compare_to_successful` | ordinal | 1-5 | Frequency of comparing to successful people via SM | 15. On a scale of 1-5, how often do you compare yo... |
| `comparison_feelings` | ordinal | 1-5 | How comparisons make respondent feel | 16. Following the previous question, how do you fe... |
| `seek_validation` | ordinal | 1-5 | Frequency of seeking validation from SM | 17. How often do you look to seek validation from ... |
| `low_mood_freq` | ordinal | 1-5 | Frequency of feeling depressed or down | 18. How often do you feel depressed or down? |
| `interest_fluctuation` | ordinal | 1-5 | How often interest in activities fluctuates | 19. On a scale of 1 to 5, how frequently does your... |
| `sleep_issues` | ordinal | 1-5 | Frequency of sleep issues | 20. On a scale of 1 to 5, how often do you face is... |
| `platforms_raw` | text | Multi-select list | Original platforms response (retained for reference) | 7. What social media platforms do you commonly use... |
| `org_affiliations_raw` | text | Free text | Original affiliation response (retained for reference) | 5. What type of organizations are you affiliated w... |
| `include_in_analysis` | boolean | True, False | True if uses_social_media=True; default filter for Tableau | — |

## Notes

- **Likert scales (1-5):** Higher values generally indicate higher frequency/intensity
- **Privacy:** Timestamp dropped; age banded; gender grouped for small-n protection
- **Analysis flag:** `include_in_analysis=True` filters to SM users only (default for dashboards)
- **Platform/Affiliation flags:** Binary (0/1) derived from multi-select fields

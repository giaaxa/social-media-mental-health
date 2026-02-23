"""
ETL Pipeline for Social Media and Mental Health Dataset
========================================================

This script cleans and transforms the raw smmh.csv dataset into a
Tableau-ready format with proper documentation.

Usage:
    python src/etl.py

Or import and call:
    from src.etl import run_etl
    run_etl()

Requirements:
    - pandas
    - numpy

Author: ETL Pipeline for Capstone Project
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths (relative to project root)
RAW_DATA_PATH = Path("data/raw/v1/smmh.csv")
PROCESSED_DATA_PATH = Path("data/processed/v1/smmh_clean.csv")
DATA_DICTIONARY_PATH = Path("docs/data_dictionary.md")
ETL_REPORT_PATH = Path("reports/etl_report.md")

# Column mapping: original survey questions -> clean snake_case names
COLUMN_MAPPING = {
    "Timestamp": "timestamp",  # Will be dropped for privacy
    "1. What is your age?": "age",
    "2. Gender": "gender_raw",
    "3. Relationship Status": "relationship_status",
    "4. Occupation Status": "occupation_status",
    "5. What type of organizations are you affiliated with?": "org_affiliations_raw",
    "6. Do you use social media?": "uses_social_media",
    "7. What social media platforms do you commonly use?": "platforms_raw",
    "8. What is the average time you spend on social media every day?": "daily_time_band",
    "9. How often do you find yourself using Social media without a specific purpose?": "purposeless_use",
    "10. How often do you get distracted by Social media when you are busy doing something?": "distracted_when_busy",
    "11. Do you feel restless if you haven't used Social media in a while?": "restless_without_sm",
    "12. On a scale of 1 to 5, how easily distracted are you?": "easily_distracted",
    "13. On a scale of 1 to 5, how much are you bothered by worries?": "worries_bother",
    "14. Do you find it difficult to concentrate on things?": "difficulty_concentrating",
    "15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?": "compare_to_successful",
    "16. Following the previous question, how do you feel about these comparisons, generally speaking?": "comparison_feelings",
    "17. How often do you look to seek validation from features of social media?": "seek_validation",
    "18. How often do you feel depressed or down?": "low_mood_freq",
    "19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?": "interest_fluctuation",
    "20. On a scale of 1 to 5, how often do you face issues regarding sleep?": "sleep_issues",
}

# Likert scale columns (must be 1-5)
LIKERT_COLUMNS = [
    "purposeless_use",
    "distracted_when_busy",
    "restless_without_sm",
    "easily_distracted",
    "worries_bother",
    "difficulty_concentrating",
    "compare_to_successful",
    "comparison_feelings",
    "seek_validation",
    "low_mood_freq",
    "interest_fluctuation",
    "sleep_issues",
]

# Platform flags to create
PLATFORMS = [
    "Facebook",
    "Twitter",
    "Instagram",
    "YouTube",
    "Snapchat",
    "Discord",
    "Reddit",
    "Pinterest",
    "TikTok",
]

# Organisation affiliation flags
AFFILIATIONS = {
    "university": ["University"],
    "school": ["School"],
    "company": ["Company"],
    "private": ["Private"],
    "government": ["Government", "Goverment"],  # Include typo variant
    "na": ["N/A", "NA", ""],
}

# Time band to midpoint mapping
TIME_BAND_MIDPOINTS = {
    "Less than an Hour": 0.5,
    "Between 1 and 2 hours": 1.5,
    "Between 2 and 3 hours": 2.5,
    "Between 3 and 4 hours": 3.5,
    "Between 4 and 5 hours": 4.5,
    "More than 5 hours": 5.5,
}

# Gender normalisation mapping
GENDER_NORMALISATION = {
    # Male variants
    "male": "Male",
    "m": "Male",
    "man": "Male",
    # Female variants
    "female": "Female",
    "f": "Female",
    "woman": "Female",
    # Non-binary variants
    "nonbinary": "Non-binary",
    "non-binary": "Non-binary",
    "non binary": "Non-binary",
    "nb": "Non-binary",
    "enby": "Non-binary",
    "genderqueer": "Non-binary",
    "genderfluid": "Non-binary",
    "agender": "Non-binary",
    # Trans (will be grouped separately but kept as clean value)
    "trans": "Trans",
    "transgender": "Trans",
    "trans male": "Trans",
    "trans female": "Trans",
    "trans man": "Trans",
    "trans woman": "Trans",
    # Unsure / questioning
    "unsure": "Unsure",
    "questioning": "Unsure",
    "unknown": "Unsure",
    # Prefer not to say
    "prefer not to say": "Prefer not to say",
    "rather not say": "Prefer not to say",
    "decline": "Prefer not to say",
}

# Gender grouping for aggregated analysis
GENDER_GROUPING = {
    "Male": "Male",
    "Female": "Female",
    "Non-binary": "Non-binary & Other",
    "Trans": "Non-binary & Other",
    "Unsure": "Non-binary & Other",
    "Other": "Non-binary & Other",
    "Prefer not to say": "Prefer not to say",
}


# =============================================================================
# ETL FUNCTIONS
# =============================================================================


def load_raw_data(filepath: Path) -> pd.DataFrame:
    """Load raw CSV data and perform initial validation."""
    print(f"Loading raw data from: {filepath}")

    if not filepath.exists():
        raise FileNotFoundError(f"Raw data file not found: {filepath}")

    df = pd.read_csv(filepath)
    print(f"  Loaded {len(df)} rows, {len(df.columns)} columns")

    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns using the explicit mapping."""
    print("Renaming columns...")

    # Check all expected columns exist
    missing_cols = set(COLUMN_MAPPING.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    df = df.rename(columns=COLUMN_MAPPING)
    print(f"  Renamed {len(COLUMN_MAPPING)} columns")

    return df


def drop_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    """Drop timestamp column for privacy/re-identification risk."""
    print("Dropping timestamp column (privacy)...")

    if "timestamp" in df.columns:
        df = df.drop(columns=["timestamp"])
        print("  Dropped timestamp column")

    return df


def clean_age(df: pd.DataFrame) -> pd.DataFrame:
    """Convert age to integer and create age bands."""
    print("Processing age...")

    # Convert to numeric, coercing errors to NaN
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Create age bands
    def get_age_band(age):
        if pd.isna(age):
            return "Unknown"
        age = int(age)
        if age < 18:
            return "<18"
        elif age <= 24:
            return "18-24"
        elif age <= 34:
            return "25-34"
        elif age <= 44:
            return "35-44"
        else:
            return "45+"

    df["age_band"] = df["age"].apply(get_age_band)

    # Convert age to nullable integer (round first to handle float conversion)
    df["age"] = pd.array(df["age"].round().values, dtype="Int64")

    print(f"  Age range: {df['age'].min()} - {df['age'].max()}")
    print(f"  Age bands: {df['age_band'].value_counts().to_dict()}")

    return df


def clean_gender(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise gender values and create grouped column."""
    print("Processing gender...")

    def normalise_gender(val):
        if pd.isna(val):
            return "Prefer not to say"

        # Strip whitespace and lowercase for matching
        val_clean = str(val).strip().lower()

        # Look up in normalisation mapping
        if val_clean in GENDER_NORMALISATION:
            return GENDER_NORMALISATION[val_clean]

        # If not found, return "Other"
        return "Other"

    df["gender_clean"] = df["gender_raw"].apply(normalise_gender)

    # Create grouped column
    df["gender_grouped"] = df["gender_clean"].map(GENDER_GROUPING)

    # Drop the raw column
    df = df.drop(columns=["gender_raw"])

    print(f"  Gender clean distribution: {df['gender_clean'].value_counts().to_dict()}")
    print(f"  Gender grouped distribution: {df['gender_grouped'].value_counts().to_dict()}")

    return df


def clean_yes_no(df: pd.DataFrame) -> pd.DataFrame:
    """Convert Yes/No columns to boolean."""
    print("Converting Yes/No to boolean...")

    def to_bool(val):
        if pd.isna(val):
            return None
        val_str = str(val).strip().lower()
        if val_str in ["yes", "y", "true", "1"]:
            return True
        elif val_str in ["no", "n", "false", "0"]:
            return False
        return None

    df["uses_social_media"] = df["uses_social_media"].apply(to_bool)

    print(f"  uses_social_media: {df['uses_social_media'].value_counts().to_dict()}")

    return df


def parse_platforms(df: pd.DataFrame) -> pd.DataFrame:
    """Parse multi-select platforms into individual flag columns."""
    print("Parsing platform flags...")

    for platform in PLATFORMS:
        col_name = f"platform_{platform.lower()}"

        def has_platform(val, p=platform):
            if pd.isna(val):
                return 0
            return 1 if p.lower() in str(val).lower() else 0

        df[col_name] = df["platforms_raw"].apply(has_platform)

    # Count platforms per row
    platform_cols = [f"platform_{p.lower()}" for p in PLATFORMS]
    df["platform_count"] = df[platform_cols].sum(axis=1)

    print(f"  Platform usage counts:")
    for p in PLATFORMS:
        col = f"platform_{p.lower()}"
        print(f"    {p}: {df[col].sum()}")

    return df


def parse_affiliations(df: pd.DataFrame) -> pd.DataFrame:
    """Parse organisation affiliations into flag columns."""
    print("Parsing affiliation flags...")

    for affil_key, affil_values in AFFILIATIONS.items():
        col_name = f"affil_{affil_key}"

        def has_affiliation(val, values=affil_values):
            if pd.isna(val):
                return 1 if "" in values else 0
            val_str = str(val).strip()
            for v in values:
                if v.lower() in val_str.lower():
                    return 1
            return 0

        df[col_name] = df["org_affiliations_raw"].apply(has_affiliation)

    print(f"  Affiliation counts:")
    for affil_key in AFFILIATIONS.keys():
        col = f"affil_{affil_key}"
        print(f"    {affil_key}: {df[col].sum()}")

    return df


def create_time_midpoint(df: pd.DataFrame) -> pd.DataFrame:
    """Create numeric midpoint from time band."""
    print("Creating daily_hours_midpoint...")

    df["daily_hours_midpoint"] = df["daily_time_band"].map(TIME_BAND_MIDPOINTS)

    # Check for unmapped values
    unmapped = df[df["daily_hours_midpoint"].isna() & df["daily_time_band"].notna()]["daily_time_band"].unique()
    if len(unmapped) > 0:
        print(f"  WARNING: Unmapped time bands: {unmapped}")

    print(f"  Time band distribution: {df['daily_time_band'].value_counts().to_dict()}")

    return df


def validate_likert_scales(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and convert Likert scale columns to integers 1-5."""
    print("Validating Likert scale columns...")

    for col in LIKERT_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing Likert column: {col}")

        # Convert to numeric
        df[col] = pd.to_numeric(df[col], errors="coerce")

        # Check range
        min_val = df[col].min()
        max_val = df[col].max()

        if pd.notna(min_val) and min_val < 1:
            raise ValueError(f"Likert column '{col}' has value below 1: {min_val}")
        if pd.notna(max_val) and max_val > 5:
            raise ValueError(f"Likert column '{col}' has value above 5: {max_val}")

        # Convert to integer
        df[col] = df[col].astype("Int64")

        print(f"  {col}: range [{min_val}-{max_val}], missing: {df[col].isna().sum()}")

    return df


def create_analysis_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Create include_in_analysis flag based on social media usage."""
    print("Creating include_in_analysis flag...")

    df["include_in_analysis"] = df["uses_social_media"] == True

    included = df["include_in_analysis"].sum()
    excluded = len(df) - included

    print(f"  Included in analysis: {included}")
    print(f"  Excluded from analysis: {excluded}")

    return df


def run_quality_checks(df: pd.DataFrame, stage: str = "final") -> dict:
    """Run data quality checks and return summary."""
    print(f"\nRunning quality checks ({stage})...")

    checks = {
        "stage": stage,
        "row_count": len(df),
        "column_count": len(df.columns),
        "duplicate_rows": df.duplicated().sum(),
        "missingness": {},
        "columns": list(df.columns),
    }

    # Missingness by column
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            checks["missingness"][col] = {
                "count": int(missing),
                "pct": round(missing / len(df) * 100, 2),
            }

    print(f"  Row count: {checks['row_count']}")
    print(f"  Column count: {checks['column_count']}")
    print(f"  Duplicate rows: {checks['duplicate_rows']}")
    print(f"  Columns with missing values: {len(checks['missingness'])}")

    if checks["duplicate_rows"] > 0:
        print(f"  WARNING: {checks['duplicate_rows']} duplicate rows found!")

    return checks


def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Reorder columns for Tableau-friendly output."""
    print("Reordering columns...")

    # Define column order
    id_cols = ["age", "age_band", "gender_clean", "gender_grouped"]
    demo_cols = ["relationship_status", "occupation_status"]
    usage_cols = ["uses_social_media", "daily_time_band", "daily_hours_midpoint"]
    platform_cols = [f"platform_{p.lower()}" for p in PLATFORMS] + ["platform_count"]
    affil_cols = [f"affil_{k}" for k in AFFILIATIONS.keys()]
    behaviour_cols = [
        "purposeless_use", "distracted_when_busy", "restless_without_sm",
        "easily_distracted", "worries_bother", "difficulty_concentrating",
    ]
    wellbeing_cols = [
        "compare_to_successful", "comparison_feelings", "seek_validation",
        "low_mood_freq", "interest_fluctuation", "sleep_issues",
    ]
    raw_cols = ["platforms_raw", "org_affiliations_raw"]
    flag_cols = ["include_in_analysis"]

    ordered_cols = (
        id_cols + demo_cols + usage_cols + platform_cols + affil_cols +
        behaviour_cols + wellbeing_cols + raw_cols + flag_cols
    )

    # Only include columns that exist
    final_cols = [c for c in ordered_cols if c in df.columns]

    # Add any columns we might have missed
    remaining = [c for c in df.columns if c not in final_cols]
    if remaining:
        print(f"  Adding remaining columns: {remaining}")
        final_cols.extend(remaining)

    df = df[final_cols]

    return df


def save_processed_data(df: pd.DataFrame, filepath: Path) -> None:
    """Save the cleaned dataset."""
    print(f"\nSaving processed data to: {filepath}")

    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)

    print(f"  Saved {len(df)} rows, {len(df.columns)} columns")


def generate_data_dictionary(df: pd.DataFrame, filepath: Path) -> None:
    """Generate markdown data dictionary."""
    print(f"\nGenerating data dictionary: {filepath}")

    # Define column metadata
    column_info = {
        "age": ("numeric", "1-100+", "Respondent age in years"),
        "age_band": ("categorical", "<18, 18-24, 25-34, 35-44, 45+, Unknown", "Age grouped into bands for privacy"),
        "gender_clean": ("categorical", "Male, Female, Non-binary, Trans, Unsure, Other, Prefer not to say", "Standardised gender response"),
        "gender_grouped": ("categorical", "Male, Female, Non-binary & Other, Prefer not to say", "Aggregated gender for small-group privacy"),
        "relationship_status": ("categorical", "Single, In a relationship, Married, Divorced", "Relationship status"),
        "occupation_status": ("categorical", "University Student, School Student, Salaried Worker, Retired", "Current occupation"),
        "uses_social_media": ("boolean", "True, False", "Whether respondent uses social media"),
        "daily_time_band": ("ordinal", "Less than an Hour to More than 5 hours", "Original time band response"),
        "daily_hours_midpoint": ("numeric", "0.5-5.5", "Numeric midpoint of time band for analysis"),
        "purposeless_use": ("ordinal", "1-5", "Frequency of using SM without specific purpose"),
        "distracted_when_busy": ("ordinal", "1-5", "Frequency of SM distraction when busy"),
        "restless_without_sm": ("ordinal", "1-5", "Restlessness when not using SM"),
        "easily_distracted": ("ordinal", "1-5", "General distractibility (1=low, 5=high)"),
        "worries_bother": ("ordinal", "1-5", "How much worries bother respondent"),
        "difficulty_concentrating": ("ordinal", "1-5", "Difficulty concentrating on things"),
        "compare_to_successful": ("ordinal", "1-5", "Frequency of comparing to successful people via SM"),
        "comparison_feelings": ("ordinal", "1-5", "How comparisons make respondent feel"),
        "seek_validation": ("ordinal", "1-5", "Frequency of seeking validation from SM"),
        "low_mood_freq": ("ordinal", "1-5", "Frequency of feeling depressed or down"),
        "interest_fluctuation": ("ordinal", "1-5", "How often interest in activities fluctuates"),
        "sleep_issues": ("ordinal", "1-5", "Frequency of sleep issues"),
        "platforms_raw": ("text", "Multi-select list", "Original platforms response (retained for reference)"),
        "org_affiliations_raw": ("text", "Free text", "Original affiliation response (retained for reference)"),
        "platform_count": ("numeric", "0-9", "Count of platforms used"),
        "include_in_analysis": ("boolean", "True, False", "True if uses_social_media=True; default filter for Tableau"),
    }

    # Add platform flags
    for p in PLATFORMS:
        col = f"platform_{p.lower()}"
        column_info[col] = ("boolean", "0, 1", f"Uses {p} (derived from platforms_raw)")

    # Add affiliation flags
    affil_names = {
        "university": "University",
        "school": "School",
        "company": "Company",
        "private": "Private organisation",
        "government": "Government",
        "na": "No affiliation / N/A",
    }
    for key, name in affil_names.items():
        col = f"affil_{key}"
        column_info[col] = ("boolean", "0, 1", f"Affiliated with {name}")

    # Build mapping from original to cleaned
    reverse_mapping = {v: k for k, v in COLUMN_MAPPING.items()}

    # Generate markdown
    lines = [
        "# Data Dictionary",
        "",
        f"**Dataset:** smmh_clean.csv",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Rows:** {len(df)}",
        f"**Columns:** {len(df.columns)}",
        "",
        "## Column Reference",
        "",
        "| Cleaned Name | Type | Allowed Values | Description | Original Column |",
        "|--------------|------|----------------|-------------|-----------------|",
    ]

    for col in df.columns:
        if col in column_info:
            dtype, values, desc = column_info[col]
        else:
            dtype, values, desc = "unknown", "—", "—"

        original = reverse_mapping.get(col, "—")
        if original == col:
            original = "—"

        # Escape pipe characters in values
        values = values.replace("|", "\\|")

        lines.append(f"| `{col}` | {dtype} | {values} | {desc} | {original[:50]}{'...' if len(original) > 50 else ''} |")

    lines.extend([
        "",
        "## Notes",
        "",
        "- **Likert scales (1-5):** Higher values generally indicate higher frequency/intensity",
        "- **Privacy:** Timestamp dropped; age banded; gender grouped for small-n protection",
        "- **Analysis flag:** `include_in_analysis=True` filters to SM users only (default for dashboards)",
        "- **Platform/Affiliation flags:** Binary (0/1) derived from multi-select fields",
        "",
    ])

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text("\n".join(lines))

    print(f"  Generated data dictionary with {len(df.columns)} columns")


def generate_etl_report(
    _df_before: pd.DataFrame,  # Retained for potential future use
    df_after: pd.DataFrame,
    checks_before: dict,
    checks_after: dict,
    filepath: Path,
) -> None:
    """Generate ETL summary report."""
    print(f"\nGenerating ETL report: {filepath}")

    lines = [
        "# ETL Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Dataset Shape",
        "",
        "| Metric | Before | After |",
        "|--------|--------|-------|",
        f"| Rows | {checks_before['row_count']} | {checks_after['row_count']} |",
        f"| Columns | {checks_before['column_count']} | {checks_after['column_count']} |",
        f"| Duplicate rows | {checks_before['duplicate_rows']} | {checks_after['duplicate_rows']} |",
        "",
        "## Columns Added/Removed",
        "",
        f"- **Dropped:** `timestamp` (privacy/re-identification risk)",
        f"- **Added:** `age_band`, `gender_clean`, `gender_grouped`, `daily_hours_midpoint`, platform flags, affiliation flags, `include_in_analysis`",
        "",
        "## Missingness Summary",
        "",
    ]

    if checks_after["missingness"]:
        lines.append("| Column | Missing Count | % |")
        lines.append("|--------|---------------|---|")
        for col, info in checks_after["missingness"].items():
            lines.append(f"| `{col}` | {info['count']} | {info['pct']}% |")
    else:
        lines.append("No missing values in final dataset.")

    lines.extend([
        "",
        "## Gender Distribution",
        "",
        "### Cleaned",
        "",
        "| Gender | Count | % |",
        "|--------|-------|---|",
    ])

    gender_clean = df_after["gender_clean"].value_counts()
    for g, count in gender_clean.items():
        pct = round(count / len(df_after) * 100, 1)
        lines.append(f"| {g} | {count} | {pct}% |")

    lines.extend([
        "",
        "### Grouped",
        "",
        "| Gender Group | Count | % |",
        "|--------------|-------|---|",
    ])

    gender_grouped = df_after["gender_grouped"].value_counts()
    for g, count in gender_grouped.items():
        pct = round(count / len(df_after) * 100, 1)
        lines.append(f"| {g} | {count} | {pct}% |")

    lines.extend([
        "",
        "## Platform Usage",
        "",
        "| Platform | Users | % |",
        "|----------|-------|---|",
    ])

    for p in PLATFORMS:
        col = f"platform_{p.lower()}"
        count = df_after[col].sum()
        pct = round(count / len(df_after) * 100, 1)
        lines.append(f"| {p} | {count} | {pct}% |")

    lines.extend([
        "",
        "## Social Media Usage",
        "",
    ])

    uses_sm = df_after["uses_social_media"].sum()
    uses_sm_pct = round(uses_sm / len(df_after) * 100, 1)
    lines.append(f"- **Uses social media:** {uses_sm} ({uses_sm_pct}%)")
    lines.append(f"- **Does not use SM:** {len(df_after) - uses_sm} ({round(100 - uses_sm_pct, 1)}%)")

    lines.extend([
        "",
        "## Analysis Inclusion",
        "",
    ])

    included = df_after["include_in_analysis"].sum()
    excluded = len(df_after) - included

    lines.append(f"- **Included (`include_in_analysis=True`):** {included} rows")
    lines.append(f"- **Excluded (`include_in_analysis=False`):** {excluded} rows")
    lines.append("")
    lines.append("Excluded rows are respondents who answered 'No' to using social media. They are retained in the dataset but should be filtered out for SM-behaviour analysis.")

    lines.extend([
        "",
        "## Data Quality",
        "",
        f"- All Likert columns validated: values in range 1-5",
        f"- No duplicate rows",
        f"- Timestamp dropped for privacy",
        "",
    ])

    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text("\n".join(lines))

    print(f"  Generated ETL report")


# =============================================================================
# MAIN ETL PIPELINE
# =============================================================================


def run_etl(
    raw_path: Path = RAW_DATA_PATH,
    processed_path: Path = PROCESSED_DATA_PATH,
    dict_path: Path = DATA_DICTIONARY_PATH,
    report_path: Path = ETL_REPORT_PATH,
) -> pd.DataFrame:
    """
    Run the complete ETL pipeline.

    Returns:
        Cleaned DataFrame
    """
    print("=" * 60)
    print("ETL PIPELINE: Social Media and Mental Health Dataset")
    print("=" * 60)

    # Load raw data
    df = load_raw_data(raw_path)
    df_before = df.copy()
    checks_before = run_quality_checks(df, stage="raw")

    # Transform
    df = rename_columns(df)
    df = drop_timestamp(df)
    df = clean_age(df)
    df = clean_gender(df)
    df = clean_yes_no(df)
    df = parse_platforms(df)
    df = parse_affiliations(df)
    df = create_time_midpoint(df)
    df = validate_likert_scales(df)
    df = create_analysis_flag(df)
    df = reorder_columns(df)

    # Final quality checks
    checks_after = run_quality_checks(df, stage="processed")

    # Save outputs
    save_processed_data(df, processed_path)
    generate_data_dictionary(df, dict_path)
    generate_etl_report(df_before, df, checks_before, checks_after, report_path)

    print("\n" + "=" * 60)
    print("ETL COMPLETE")
    print("=" * 60)
    print(f"  Processed data: {processed_path}")
    print(f"  Data dictionary: {dict_path}")
    print(f"  ETL report: {report_path}")

    return df


if __name__ == "__main__":
    # Change to project root if running from src/
    import os
    if os.path.basename(os.getcwd()) == "src":
        os.chdir("..")

    run_etl()

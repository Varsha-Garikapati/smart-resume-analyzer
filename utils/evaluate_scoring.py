import os
import re
import pandas as pd

from resume_parser import extract_contact_info
from section_extractor import extract_sections
from resume_scorer import calculate_resume_score


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = os.path.join(
    "data",
    "job_resume_fit.csv"
)

OUTPUT_PATH = os.path.join(
    "data",
    "scoring_evaluation_results.csv"
)

SAMPLE_SIZE = 100


# ============================================================
# LOAD DATASET
# ============================================================

def load_dataset():
    print("\nLoading dataset...")

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset not found at: {DATASET_PATH}\n"
            "Make sure job_resume_fit.csv is inside the data folder."
        )

    df = pd.read_csv(DATASET_PATH)

    print(
        f"Dataset loaded successfully: "
        f"{len(df)} rows"
    )

    return df


# ============================================================
# SELECT REPRESENTATIVE SAMPLE
# ============================================================

def select_evaluation_sample(df):
    """
    Select a diverse evaluation subset.

    We do not simply take the first 100 rows.

    The sample contains:
    - different job categories
    - low, medium and high matching examples
    """

    if len(df) <= SAMPLE_SIZE:
        return df.copy()

    selected_parts = []

    # --------------------------------------------------------
    # Step 1: Sort within categories by AI match score
    # --------------------------------------------------------

    df_sorted = df.sort_values(
        ["category", "ai_match_score"]
    )

    categories = df["category"].dropna().unique()

    # Try to take approximately 3 examples from each
    # category: low, medium and high.
    for category in categories:

        category_df = df_sorted[
            df_sorted["category"] == category
        ]

        if len(category_df) == 0:
            continue

        # Low-match example
        low_index = 0

        # Middle example
        middle_index = len(category_df) // 2

        # High-match example
        high_index = len(category_df) - 1

        indices = list(
            dict.fromkeys([
                low_index,
                middle_index,
                high_index
            ])
        )

        selected_parts.append(
            category_df.iloc[indices]
        )

    if selected_parts:
        sample = pd.concat(
            selected_parts,
            ignore_index=True
        )
    else:
        sample = df.sample(
            n=SAMPLE_SIZE,
            random_state=42
        )

    # --------------------------------------------------------
    # Step 2: If fewer than 100, fill remaining rows
    # --------------------------------------------------------

    if len(sample) < SAMPLE_SIZE:

        remaining = df[
            ~df["ID"].isin(sample["ID"])
        ]

        remaining_needed = (
            SAMPLE_SIZE - len(sample)
        )

        if len(remaining) > 0:

            extra = remaining.sample(
                n=min(
                    remaining_needed,
                    len(remaining)
                ),
                random_state=42
            )

            sample = pd.concat(
                [sample, extra],
                ignore_index=True
            )

    # --------------------------------------------------------
    # Step 3: If somehow over 100, sample down
    # --------------------------------------------------------

    if len(sample) > SAMPLE_SIZE:

        sample = sample.sample(
            n=SAMPLE_SIZE,
            random_state=42
        )

    return sample.reset_index(drop=True)

def prepare_dataset_resume(text):
    """
    Prepare dataset resumes for section extraction.

    The dataset often stores the entire resume as one
    continuous line, so we insert line breaks before
    recognizable section headings.
    """

    if not isinstance(text, str):
        return ""

    section_headings = [
        "Education",
        "Skills",
        "Projects",
        "Experience",
        "Certifications",
        "Achievements"
    ]

    prepared_text = text

    for heading in section_headings:
        prepared_text = re.sub(
            rf"\s+{re.escape(heading)}\s+",
            f"\n\n{heading}\n",
            prepared_text,
            flags=re.IGNORECASE
        )

    return prepared_text
# ============================================================
# ANALYZE ONE RESUME
# ============================================================

def analyze_resume(resume_text):
    """
    Run our current resume-quality pipeline on
    one dataset resume.

    This deliberately does NOT use:
    - job_text
    - ai_match_score
    - JD match
    - semantic score

    Therefore this evaluates the intrinsic resume
    quality scorer independently.
    """

    if not isinstance(resume_text, str):
        resume_text = ""

    if not resume_text.strip():
        return {
            "total_score": 0,
            "profile_type": "unknown",
            "breakdown": {}
        }

    try:

        # ---------------------------------------------
        # Contact information
        # ---------------------------------------------

        contact_info = extract_contact_info(
            resume_text
        )
        prepared_text = prepare_dataset_resume(resume_text)
        section_content = extract_sections(prepared_text)

        sections = {
            section: bool(content.strip())
            for section, content in section_content.items()
        }

        # ---------------------------------------------
        # Resume quality score
        # ---------------------------------------------

        result = calculate_resume_score(
            contact_info,
            sections,
            section_content,
            resume_text
        )

        return result

    except Exception as error:

        print(
            f"Error analyzing resume: {error}"
        )

        return {
            "total_score": 0,
            "profile_type": "error",
            "breakdown": {}
        }


# ============================================================
# RUN EVALUATION
# ============================================================

def run_evaluation(df):
    """
    Run the resume scorer across the evaluation sample.
    """

    results = []

    total = len(df)

    print(
        f"\nEvaluating {total} resumes..."
    )

    for index, row in df.iterrows():

        resume_text = row.get(
            "resume_text",
            ""
        )

        result = analyze_resume(
            resume_text
        )

        breakdown = result.get(
            "breakdown",
            {}
        )

        results.append({

            # Dataset information
            "ID": row.get("ID"),
            "category": row.get("category"),

            # Dataset's reference matching signals
            "dataset_ai_match_score": row.get(
                "ai_match_score"
            ),

            "dataset_skill_match_score": row.get(
                "skill_string_match_score"
            ),

            "dataset_fuzzy_match_score": row.get(
                "fuzzy_match_score"
            ),

            # Our score
            "our_resume_score": result.get(
                "total_score",
                0
            ),

            "profile_type": result.get(
                "profile_type",
                "unknown"
            ),

            # Our breakdown
            "content_impact": breakdown.get(
                "content_impact",
                0
            ),

            "structure": breakdown.get(
                "structure",
                0
            ),

            "skills": breakdown.get(
                "skills",
                0
            ),

            "projects_experience": breakdown.get(
                "projects_experience",
                0
            ),

            "education": breakdown.get(
                "education",
                0
            ),

            "formatting": breakdown.get(
                "formatting",
                0
            ),

            "contact": breakdown.get(
                "contact",
                0
            ),

            # Basic dataset information
            "resume_word_count": len(
                str(resume_text).split()
            ),

            "job_category": row.get(
                "category"
            )
        })

        # Progress
        if (
            (index + 1) % 10 == 0
            or index + 1 == total
        ):
            print(
                f"Processed {index + 1}/{total}"
            )

    return pd.DataFrame(results)


# ============================================================
# PRINT SUMMARY
# ============================================================

def print_summary(results):
    """
    Print useful statistics so we can inspect whether
    the new scoring system behaves sensibly.
    """

    print("\n")
    print("=" * 60)
    print("SCORING EVALUATION SUMMARY")
    print("=" * 60)

    # --------------------------------------------------------
    # Overall statistics
    # --------------------------------------------------------

    scores = results[
        "our_resume_score"
    ]

    print("\nOur Resume Quality Score:")
    print(
        f"Minimum : {scores.min():.2f}"
    )
    print(
        f"Maximum : {scores.max():.2f}"
    )
    print(
        f"Mean    : {scores.mean():.2f}"
    )
    print(
        f"Median  : {scores.median():.2f}"
    )

    # --------------------------------------------------------
    # Score distribution
    # --------------------------------------------------------

    excellent = (
        scores >= 80
    ).sum()

    good = (
        (scores >= 60)
        & (scores < 80)
    ).sum()

    weak = (
        (scores >= 40)
        & (scores < 60)
    ).sum()

    poor = (
        scores < 40
    ).sum()

    print("\nScore Distribution:")
    print(
        f"80-100 : {excellent}"
    )
    print(
        f"60-79  : {good}"
    )
    print(
        f"40-59  : {weak}"
    )
    print(
        f"0-39   : {poor}"
    )

    # --------------------------------------------------------
    # Profile distribution
    # --------------------------------------------------------

    print("\nProfile Types:")

    print(
        results["profile_type"]
        .value_counts()
        .to_string()
    )

    # --------------------------------------------------------
    # Average breakdown
    # --------------------------------------------------------

    breakdown_columns = [
        "content_impact",
        "structure",
        "skills",
        "projects_experience",
        "education",
        "formatting",
        "contact"
    ]

    print("\nAverage Score Breakdown:")

    for column in breakdown_columns:

        print(
            f"{column:25s}: "
            f"{results[column].mean():.2f}"
        )

    # --------------------------------------------------------
    # Average score by category
    # --------------------------------------------------------

    print("\nAverage Score by Job Category:")

    category_scores = (
        results
        .groupby("category")[
            "our_resume_score"
        ]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    print(
        category_scores
        .round(2)
        .to_string()
    )
    # --------------------------------------------------------
    # Compare our score with dataset matching score
    # --------------------------------------------------------

    print("\nOur Resume Quality vs Dataset Match Score:")

    comparison = results[
        [
            "our_resume_score",
            "dataset_ai_match_score"
        ]
    ].dropna()

    if len(comparison) > 1:

        correlation = comparison[
            "our_resume_score"
        ].corr(
            comparison[
                "dataset_ai_match_score"
            ]
        )

        print(
            f"Correlation: {correlation:.3f}"
        )

        print(
            "\nNote: This correlation is only "
            "diagnostic because the two scores "
            "measure different things."
        )
    print("\n")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    # Load complete dataset
    df = load_dataset()

    # Select evaluation subset
    sample = select_evaluation_sample(
        df
    )

    print(
        f"\nSelected "
        f"{len(sample)} representative resumes "
        f"for evaluation."
    )

    # Run our scorer
    results = run_evaluation(
        sample
    )

    # Save results
    results.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(
        f"\nEvaluation results saved to:\n"
        f"{OUTPUT_PATH}"
    )

    # Display summary
    print_summary(
        results
    )


if __name__ == "__main__":
    main()
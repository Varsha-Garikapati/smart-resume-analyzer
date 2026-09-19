import re


ROLE_SKILLS = {
    "AI Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "natural language processing",
        "computer vision",
        "docker",
        "git"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "scikit-learn",
        "tensorflow",
        "pytorch",
        "pandas",
        "numpy",
        "data structures",
        "git"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "machine learning",
        "scikit-learn",
        "pandas",
        "numpy",
        "statistics",
        "data visualization"
    ],

    "Software Developer": [
        "python",
        "java",
        "c++",
        "data structures",
        "algorithms",
        "object oriented programming",
        "git",
        "sql",
        "rest api",
        "docker"
    ]
}


# Different ways a skill can appear in a resume
SKILL_ALIASES = {
    "python": [
        "python"
    ],

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "deep learning": [
        "deep learning"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch",
        "py torch"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy",
        "num py"
    ],

    "data structures": [
        "data structures",
        "data structures and algorithms"
    ],

    "git": [
        "git"
    ],

    "sql": [
        "sql"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "algorithms": [
        "algorithms",
        "algorithm"
    ],

    "object oriented programming": [
        "object oriented programming",
        "object-oriented programming",
        "oop"
    ],

    "rest api": [
        "rest api",
        "restful api"
    ],

    "docker": [
        "docker"
    ],

    "statistics": [
        "statistics",
        "statistical"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "computer vision": [
        "computer vision"
    ]
}


def skill_exists_in_resume(resume_text, skill):
    text = resume_text.lower()

    aliases = SKILL_ALIASES.get(
        skill.lower(),
        [skill]
    )

    for alias in aliases:
        alias = alias.lower().strip()

        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            return True

    return False


def count_action_verbs(text):
    action_verbs = [
        "developed",
        "built",
        "implemented",
        "designed",
        "created",
        "optimized",
        "analyzed",
        "integrated",
        "deployed",
        "trained",
        "achieved",
        "contributed",
        "engineered"
    ]

    text_lower = text.lower()
    count = 0

    for verb in action_verbs:
        if re.search(
            r"\b" + re.escape(verb) + r"\b",
            text_lower
        ):
            count += 1

    return count


def count_quantified_content(text):
    patterns = [
        r"\b\d+%",
        r"\b\d+\+",
        r"\b\d+(?:\.\d+)?\s*(?:accuracy|users|projects|models|datasets|samples)\b",
        r"\b\d+(?:\.\d+)?\b"
    ]

    matches = []

    for pattern in patterns:
        matches.extend(
            re.findall(
                pattern,
                text,
                re.IGNORECASE
            )
        )

    return len(matches)


def check_dates(text):
    patterns = [
        r"\b20\d{2}\b",
        r"\b\d{4}\s*-\s*\d{4}\b",
        r"\b\d{4}\s*-\s*(?:present|current)\b",
        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+20\d{2}\b"
    ]

    for pattern in patterns:
        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return True

    return False


def check_role_alignment(resume_text, selected_role):
    """
    Checks whether the resume explicitly contains
    a relevant role or role-related phrase.

    This is kept separate from skill matching so
    role alignment does not duplicate keyword scoring.
    """

    text = resume_text.lower()
    role = selected_role.lower()

    role_aliases = {
        "ai engineer": [
            "ai engineer",
            "artificial intelligence engineer",
            "machine learning engineer",
            "ml engineer"
        ],

        "machine learning engineer": [
            "machine learning engineer",
            "ml engineer",
            "machine learning"
        ],

        "data scientist": [
            "data scientist",
            "data science"
        ],

        "software developer": [
            "software developer",
            "software engineer",
            "software development"
        ]
    }

    aliases = role_aliases.get(
        role,
        [role]
    )

    for alias in aliases:
        pattern = (
            r"(?<!\w)"
            + re.escape(alias)
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            return 5

    return 0


def analyze_ats(
    resume_text,
    selected_role,
    contact_info=None,
    sections=None
):

    if contact_info is None:
        contact_info = {
            "email": None,
            "phone": None,
            "linkedin": None,
            "github": None
        }

    if sections is None:
        sections = {
            "education": False,
            "skills": False,
            "projects": False,
            "experience": False,
            "certifications": False
        }

    # =========================================================
    # 1. KEYWORD MATCH - 60
    # =========================================================

    role_skills = ROLE_SKILLS.get(
        selected_role,
        []
    )

    matched_skills = []
    missing_skills = []

    for skill in role_skills:

        if skill_exists_in_resume(
            resume_text,
            skill
        ):
            matched_skills.append(skill)

        else:
            missing_skills.append(skill)

    if role_skills:
        keyword_score = (
            len(matched_skills)
            / len(role_skills)
        ) * 60

    else:
        keyword_score = 0


    # =========================================================
    # 2. SECTION STRUCTURE - 10
    # =========================================================

    section_score = 0

    if sections.get("education"):
        section_score += 3

    if sections.get("skills"):
        section_score += 3

    if sections.get("projects"):
        section_score += 2

    if sections.get("experience"):
        section_score += 1

    if sections.get("certifications"):
        section_score += 1

    section_score = min(
        section_score,
        10
    )


    # =========================================================
    # 3. CONTACT INFORMATION - 5
    # =========================================================

    contact_score = 0

    if contact_info.get("email"):
        contact_score += 2

    if contact_info.get("phone"):
        contact_score += 1

    if contact_info.get("linkedin"):
        contact_score += 1

    if contact_info.get("github"):
        contact_score += 1


    # =========================================================
    # 4. ATS PARSING QUALITY - 10
    # =========================================================

    parsing_score = 0

    text_length = len(
        resume_text.strip()
    )

    if text_length >= 500:
        parsing_score += 3

    elif text_length >= 250:
        parsing_score += 2


    detected_sections = sum(
        1
        for value in sections.values()
        if value
    )

    if detected_sections >= 4:
        parsing_score += 4

    elif detected_sections >= 3:
        parsing_score += 3

    elif detected_sections >= 2:
        parsing_score += 2


    word_count = len(
        resume_text.split()
    )

    if word_count >= 150:
        parsing_score += 3

    elif word_count >= 80:
        parsing_score += 2

    parsing_score = min(
        parsing_score,
        10
    )


    # =========================================================
    # 5. DATES & CONSISTENCY - 5
    # =========================================================

    consistency_score = 0

    if check_dates(resume_text):
        consistency_score += 2


    lines = resume_text.split("\n")

    long_lines = 0

    for line in lines:

        if len(line.strip()) > 250:
            long_lines += 1

    if long_lines <= 3:
        consistency_score += 3

    elif long_lines <= 6:
        consistency_score += 2


    # =========================================================
    # 6. CONTENT QUALITY - 5
    # =========================================================

    content_score = 0

    action_count = count_action_verbs(
        resume_text
    )

    if action_count >= 6:
        content_score += 3

    elif action_count >= 3:
        content_score += 2

    elif action_count >= 1:
        content_score += 1


    quantified_count = count_quantified_content(
        resume_text
    )

    if quantified_count >= 4:
        content_score += 2

    elif quantified_count >= 2:
        content_score += 1


    # =========================================================
    # 7. ROLE ALIGNMENT - 5
    # =========================================================

    alignment_score = check_role_alignment(
        resume_text,
        selected_role
    )


    # =========================================================
    # FINAL ATS SCORE
    # =========================================================

    total_score = round(
        min(
            keyword_score
            + section_score
            + contact_score
            + parsing_score
            + consistency_score
            + content_score
            + alignment_score,
            100
        )
    )


    # =========================================================
    # ISSUES / FEEDBACK
    # =========================================================

    issues = []

    if missing_skills:
        issues.append(
            "Some important skills for the selected role are missing."
        )

    if not contact_info.get("linkedin"):
        issues.append(
            "LinkedIn profile was not detected."
        )

    if not contact_info.get("github"):
        issues.append(
            "GitHub or portfolio link was not detected."
        )

    if not sections.get("experience"):
        issues.append(
            "Experience section was not detected."
        )

    if not check_dates(resume_text):
        issues.append(
            "No recognizable date information was detected."
        )

    if action_count < 3:
        issues.append(
            "Use stronger action verbs in project and experience descriptions."
        )

    if quantified_count < 2:
        issues.append(
            "Add more measurable outcomes where possible."
        )


    # =========================================================
    # RETURN RESULT
    # =========================================================

    return {
        "ats_score": total_score,

        "selected_role": selected_role,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "breakdown": {
            "keyword_match": round(keyword_score),
            "section_structure": section_score,
            "contact_information": contact_score,
            "ats_parsing": parsing_score,
            "dates_consistency": consistency_score,
            "content_quality": content_score,
            "role_alignment": alignment_score
        },

        "issues": issues
    }
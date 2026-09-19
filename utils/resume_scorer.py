import re


# ============================================================
# CONFIGURATION
# ============================================================

ACTION_VERBS = [
    "developed",
    "implemented",
    "built",
    "designed",
    "created",
    "engineered",
    "optimized",
    "improved",
    "analyzed",
    "evaluated",
    "integrated",
    "trained",
    "tested",
    "collaborated",
    "contributed",
    "deployed",
    "managed",
    "automated",
    "led",
    "created",
    "configured",
    "processed",
    "developed",
    "achieved",
    "reduced",
    "increased",
    "streamlined",
    "delivered"
]


# Canonical skill names with aliases.
# This prevents things such as React + React.js being
# counted as two different skills.
SKILL_ALIASES = {
    # Programming
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": [r"\bc\b"],
    "sql": ["sql"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],

    # AI / ML
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "computer vision": ["computer vision"],
    "natural language processing": [
        "natural language processing",
        "nlp"
    ],
    "cnn": ["cnn", "convolutional neural network"],
    "rnn": ["rnn", "recurrent neural network"],

    # Data
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "data analysis": ["data analysis"],
    "data visualization": ["data visualization"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],

    # AI systems
    "generative ai": [
        "generative ai",
        "generative artificial intelligence"
    ],
    "rag": ["rag", "retrieval augmented generation"],
    "embeddings": ["embeddings"],
    "langchain": ["langchain"],
    "langgraph": ["langgraph"],
    "ai agents": ["ai agents", "artificial intelligence agents"],

    # Software
    "react": ["react", "react.js"],
    "rest api": ["rest api", "restful api"],
    "git": [r"\bgit\b"],
    "github": ["github"],
    "docker": ["docker"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],

    # Tools
    "streamlit": ["streamlit"],
    "jupyter": ["jupyter", "jupyter notebook"],
    "linux": ["linux"],
    "aws": ["aws", "amazon web services"],
    "vs code": ["vs code", "visual studio code"],

    # Databases
    "mysql": ["mysql"],
    "mongodb": ["mongodb"],
    "postgresql": ["postgresql"],
    "firebase": ["firebase"]
}


PROJECT_TECHNOLOGIES = [
    "python",
    "java",
    "c++",
    "sql",
    "javascript",
    "typescript",
    "react",
    "html",
    "css",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "opencv",
    "flask",
    "fastapi",
    "streamlit",
    "docker",
    "aws",
    "git",
    "github",
    "mysql",
    "mongodb",
    "postgresql",
    "firebase",
    "langchain",
    "langgraph",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text):
    """
    Normalize text for reliable matching.
    """

    if not text:
        return ""

    text = text.lower()

    # Normalize common separators
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Collapse repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_term(text, term):
    """
    Safely check whether a term exists in text.

    Uses word boundaries for short/simple terms so that
    'c' does not match every word containing the letter c.
    """

    text_lower = normalize_text(text)

    # Regex-style term
    if term.startswith(r"\b"):
        return re.search(term, text_lower) is not None

    # Multi-word or special terms
    escaped = re.escape(term)

    return re.search(
        r"(?<!\w)" + escaped + r"(?!\w)",
        text_lower
    ) is not None


def count_action_verbs(text):
    """
    Count unique strong action verbs used in the content.

    Recognizes common resume verb forms such as:
    develop, developed, developing
    analyze, analyzed, analyzing
    contribute, contributed, contributing
    """

    if not text:
        return 0

    text_lower = normalize_text(text)

    found = set()

    ACTION_VERB_FORMS = {
        "develop": [
            "develop",
            "developed",
            "developing"
        ],
        "implement": [
            "implement",
            "implemented",
            "implementing"
        ],
        "build": [
            "build",
            "built",
            "building"
        ],
        "design": [
            "design",
            "designed",
            "designing"
        ],
        "create": [
            "create",
            "created",
            "creating"
        ],
        "engineer": [
            "engineer",
            "engineered",
            "engineering"
        ],
        "optimize": [
            "optimize",
            "optimized",
            "optimizing"
        ],
        "improve": [
            "improve",
            "improved",
            "improving"
        ],
        "analyze": [
            "analyze",
            "analyzed",
            "analyzing"
        ],
        "evaluate": [
            "evaluate",
            "evaluated",
            "evaluating"
        ],
        "integrate": [
            "integrate",
            "integrated",
            "integrating"
        ],
        "train": [
            "train",
            "trained",
            "training"
        ],
        "test": [
            "test",
            "tested",
            "testing"
        ],
        "collaborate": [
            "collaborate",
            "collaborated",
            "collaborating"
        ],
        "contribute": [
            "contribute",
            "contributed",
            "contributing"
        ],
        "deploy": [
            "deploy",
            "deployed",
            "deploying"
        ],
        "manage": [
            "manage",
            "managed",
            "managing"
        ],
        "automate": [
            "automate",
            "automated",
            "automating"
        ],
        "lead": [
            "lead",
            "led",
            "leading"
        ],
        "configure": [
            "configure",
            "configured",
            "configuring"
        ],
        "process": [
            "process",
            "processed",
            "processing"
        ],
        "achieve": [
            "achieve",
            "achieved",
            "achieving"
        ],
        "reduce": [
            "reduce",
            "reduced",
            "reducing"
        ],
        "increase": [
            "increase",
            "increased",
            "increasing"
        ],
        "streamline": [
            "streamline",
            "streamlined",
            "streamlining"
        ],
        "deliver": [
            "deliver",
            "delivered",
            "delivering"
        ]
    }

    for base_verb, forms in ACTION_VERB_FORMS.items():

        for form in forms:

            if re.search(
                r"\b" + re.escape(form) + r"\b",
                text_lower
            ):
                found.add(base_verb)
                break

    return len(found)


def count_quantified_achievements(text):
    """
    Detect meaningful measurable evidence.

    Examples:
    - 93%
    - 20% improvement
    - 100+ users
    - 500 images
    - 3 models
    - 10 projects

    Years and standalone academic numbers are not
    automatically treated as achievements.
    """

    if not text:
        return 0

    patterns = [
        # Percentages
        r"\b\d+(?:\.\d+)?\s*%",

        # Numbers followed by +
        r"\b\d[\d,]*(?:\.\d+)?\s*\+",

        # Numbers followed by meaningful units
        r"\b\d[\d,]*(?:\.\d+)?\s+"
        r"(?:users|images|projects|models|"
        r"datasets|samples|records|"
        r"problems|features|classes|"
        r"patients|experiments|"
        r"applications|applications|"
        r"years|months|days)\b",

        # Explicit improvement/result language
        r"\b(?:improved|increased|reduced|"
        r"achieved|boosted|decreased|"
        r"optimized)\b[^.\n]{0,60}"
        r"\b\d+(?:\.\d+)?\s*%"
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

    # Remove duplicate exact matches
    return len(set(matches))


def count_recognized_skills(text):
    """
    Count unique recognized skills.

    Uses canonical skills + aliases to avoid duplicate
    counting such as:
        React + React.js
        NLP + Natural Language Processing
    """

    if not text:
        return 0

    matched_skills = set()

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_term(text, alias):
                matched_skills.add(canonical_skill)
                break

    return len(matched_skills)


def get_recognized_skills(text):
    """
    Return the canonical recognized skills.
    """

    if not text:
        return []

    matched_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if contains_term(text, alias):
                matched_skills.append(canonical_skill)
                break

    return matched_skills


def estimate_project_count(text):
    """
    Estimate project count using several signals.

    Project titles may be written as:
        Project Name
        Project Name — Description
        Project Name | Technologies
        Project Name - Technologies

    This is intentionally conservative to avoid counting
    every bullet point as a project.
    """

    if not text or not text.strip():
        return 0

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return 0

    project_count = 0

    # Strong title indicators
    for line in lines:

        if len(line) > 120:
            continue

        lower = line.lower()

        # Separator commonly used between project title
        # and technology/description
        if "|" in line:
            project_count += 1
            continue

        if "—" in line:
            project_count += 1
            continue

        # Hyphen with reasonable title length
        if " - " in line and len(line) < 100:
            project_count += 1
            continue

        # Lines that explicitly look like project titles
        project_words = [
            "project",
            "classifier",
            "system",
            "platform",
            "application",
            "analyzer",
            "interface",
            "model",
            "prediction",
            "dashboard"
        ]

        if (
            len(line.split()) <= 8
            and any(
                word in lower
                for word in project_words
            )
        ):
            project_count += 1

    return min(project_count, 6)


def count_project_technologies(text):
    """
    Count unique technologies mentioned in projects.
    """

    if not text:
        return 0

    matched = set()

    for technology in PROJECT_TECHNOLOGIES:

        if contains_term(text, technology):
            matched.add(technology)

    return len(matched)


def count_meaningful_bullets(text):
    """
    Estimate the number of meaningful bullet-style
    statements in a section.
    """

    if not text:
        return 0

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    meaningful = 0

    for line in lines:

        # Remove common bullet markers
        cleaned = re.sub(
            r"^[•●▪◦\-*]\s*",
            "",
            line
        ).strip()

        if len(cleaned.split()) >= 6:
            meaningful += 1

    return meaningful


def detect_dates(text):
    """
    Detect common resume date formats.

    Examples:
        2024
        2022 - 2024
        Jan 2024
        Jan 2024 - Mar 2025
        Present
    """

    if not text:
        return []

    patterns = [
        r"\b(?:19|20)\d{2}\b",

        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|"
        r"sep|oct|nov|dec)[a-z]*\s+"
        r"(?:19|20)\d{2}\b",

        r"\b(?:19|20)\d{2}\s*[-–]\s*"
        r"(?:19|20)\d{2}\b",

        r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|"
        r"sep|oct|nov|dec)[a-z]*\s+"
        r"(?:19|20)\d{2}\s*[-–]\s*"
        r"(?:present|current|now|"
        r"(?:jan|feb|mar|apr|may|jun|jul|aug|"
        r"sep|oct|nov|dec)[a-z]*\s+(?:19|20)\d{2})\b"
    ]

    dates = []

    for pattern in patterns:
        dates.extend(
            re.findall(
                pattern,
                text,
                re.IGNORECASE
            )
        )

    return list(set(dates))


def estimate_resume_length_quality(resume_text):
    """
    Estimate whether the resume contains a reasonable
    amount of content.

    This is only a small component of quality.
    Length alone should never dominate the score.
    """

    word_count = len(resume_text.split())

    if 250 <= word_count <= 900:
        return 3

    if 150 <= word_count < 250:
        return 2

    if 900 < word_count <= 1200:
        return 2

    if word_count >= 100:
        return 1

    return 0


def detect_fresher_profile(sections, section_content):
    """
    Determine whether the resume appears to be a
    student/fresher profile.

    A fresher profile is identified mainly by the
    absence of a formal experience section and the
    presence of education/projects.

    This is intentionally simple and explainable.
    """

    has_experience = bool(
        section_content.get("experience", "").strip()
    )

    has_education = bool(
        section_content.get("education", "").strip()
    )

    has_projects = bool(
        section_content.get("projects", "").strip()
    )

    if not has_experience and (
        has_education or has_projects
    ):
        return True

    return False


# ============================================================
# SECTION SCORING HELPERS
# ============================================================

def calculate_content_impact_score(
    resume_text,
    section_content,
    is_fresher
):
    """
    Content & Impact — 25 points.

    Measures:
    - meaningful content
    - action-oriented writing
    - measurable achievements
    """

    score = 0

    projects_text = section_content.get(
        "projects",
        ""
    )

    experience_text = section_content.get(
        "experience",
        ""
    )

    relevant_text = (
        projects_text + "\n" + experience_text
    ).strip()

    if not relevant_text:
        return 0

    # Meaningful bullet/content presence — 8 points
    bullet_count = count_meaningful_bullets(
        relevant_text
    )

    if bullet_count >= 8:
        score += 8
    elif bullet_count >= 5:
        score += 6
    elif bullet_count >= 3:
        score += 4
    elif bullet_count >= 1:
        score += 2

    # Action-oriented language — 8 points
    action_count = count_action_verbs(
        relevant_text
    )

    if action_count >= 8:
        score += 8
    elif action_count >= 6:
        score += 7
    elif action_count >= 4:
        score += 5
    elif action_count >= 2:
        score += 3
    elif action_count >= 1:
        score += 1

    # Measurable evidence — 9 points
    quantified_count = count_quantified_achievements(
        relevant_text
    )

    if quantified_count >= 5:
        score += 9
    elif quantified_count >= 3:
        score += 7
    elif quantified_count >= 2:
        score += 5
    elif quantified_count >= 1:
        score += 3

    return min(score, 25)


def calculate_structure_score(
    sections,
    section_content,
    is_fresher
):
    """
    Structure & Completeness — 20 points.

    For freshers, Projects are considered a core section.
    For experienced candidates, Experience is prioritized.
    """

    score = 0

    has_education = bool(
        sections.get("education")
    )

    has_skills = bool(
        sections.get("skills")
    )

    has_projects = bool(
        sections.get("projects")
    )

    has_experience = bool(
        sections.get("experience")
    )

    has_certifications = bool(
        sections.get("certifications")
    )

    # Education — 5 points
    if has_education:
        score += 5

    # Skills — 5 points
    if has_skills:
        score += 5

    # Projects / Experience — 6 points
    if is_fresher:

        if has_projects:
            score += 6

        elif has_experience:
            score += 4

    else:

        if has_experience:
            score += 6

        elif has_projects:
            score += 3

    # Certifications — 2 points
    if has_certifications:
        score += 2

    # Additional completeness — 2 points
    # Resume has at least 3 meaningful sections.
    important_sections = [
        has_education,
        has_skills,
        has_projects or has_experience
    ]

    if sum(important_sections) >= 3:
        score += 2

    return min(score, 20)


def calculate_skills_score(
    section_content,
    project_content
):
    """
    Skills & Technical Evidence — 15 points.

    Measures both:
    - breadth of recognized skills
    - evidence that technologies are actually used
      in projects.
    """

    skills_text = section_content.get(
        "skills",
        ""
    )

    if not skills_text.strip():
        return 0

    recognized_skills = count_recognized_skills(
        skills_text
    )

    project_technologies = count_project_technologies(
        project_content
    )

    score = 0

    # Skill breadth — 9 points
    if recognized_skills >= 15:
        score += 9
    elif recognized_skills >= 10:
        score += 8
    elif recognized_skills >= 7:
        score += 6
    elif recognized_skills >= 4:
        score += 4
    elif recognized_skills >= 1:
        score += 2

    # Technical evidence through projects — 6 points
    if project_technologies >= 8:
        score += 6
    elif project_technologies >= 5:
        score += 5
    elif project_technologies >= 3:
        score += 3
    elif project_technologies >= 1:
        score += 2

    return min(score, 15)


def calculate_project_experience_score(
    section_content,
    is_fresher
):
    """
    Projects / Experience Quality — 15 points.

    Adaptive for early-career resumes:
        - Freshers: projects are the primary evidence.
        - Early-career candidates: experience and projects
          both contribute meaningfully.
        - Experienced candidates: experience is prioritized.
    """

    projects_text = section_content.get(
        "projects",
        ""
    )

    experience_text = section_content.get(
        "experience",
        ""
    )

    score = 0

    # --------------------------------------------------------
    # FRESHER: PROJECT-FOCUSED
    # --------------------------------------------------------

    if is_fresher:

        if projects_text.strip():

            project_count = estimate_project_count(
                projects_text
            )

            # Project count — 5 points
            if project_count >= 4:
                score += 5
            elif project_count == 3:
                score += 4
            elif project_count == 2:
                score += 3
            elif project_count == 1:
                score += 2

            # Project depth — 5 points
            action_count = count_action_verbs(
                projects_text
            )

            technology_count = count_project_technologies(
                projects_text
            )

            depth = 0

            if action_count >= 4:
                depth += 3
            elif action_count >= 2:
                depth += 2
            elif action_count >= 1:
                depth += 1

            if technology_count >= 5:
                depth += 2
            elif technology_count >= 2:
                depth += 1

            score += min(depth, 5)

            # Measurable outcomes — 5 points
            quantified = count_quantified_achievements(
                projects_text
            )

            if quantified >= 4:
                score += 5
            elif quantified >= 3:
                score += 4
            elif quantified >= 2:
                score += 3
            elif quantified >= 1:
                score += 2

    # --------------------------------------------------------
    # EARLY-CAREER / EXPERIENCED
    # --------------------------------------------------------

    else:

        has_experience = bool(
            experience_text.strip()
        )

        has_projects = bool(
            projects_text.strip()
        )

        # Experience contribution — 8 points
        if has_experience:

            # Presence and substantive experience
            experience_words = len(
                experience_text.split()
            )

            if experience_words >= 150:
                score += 4
            elif experience_words >= 80:
                score += 3
            elif experience_words >= 40:
                score += 2
            else:
                score += 1

            # Action-oriented experience
            action_count = count_action_verbs(
                experience_text
            )

            if action_count >= 6:
                score += 2
            elif action_count >= 3:
                score += 1

            # Measurable impact
            quantified = count_quantified_achievements(
                experience_text
            )

            if quantified >= 2:
                score += 2
            elif quantified >= 1:
                score += 1

        # Projects contribution — 7 points
        if has_projects:

            project_count = estimate_project_count(
                projects_text
            )

            # Project breadth — 3 points
            if project_count >= 4:
                score += 3
            elif project_count >= 3:
                score += 2
            elif project_count >= 1:
                score += 1

            # Technical depth — 2 points
            technology_count = count_project_technologies(
                projects_text
            )

            if technology_count >= 8:
                score += 2
            elif technology_count >= 4:
                score += 1

            # Measurable / evaluation evidence — 2 points
            quantified = count_quantified_achievements(
                projects_text
            )

            if quantified >= 3:
                score += 2
            elif quantified >= 1:
                score += 1

    return min(score, 15)


def calculate_education_score(section_content):
    """
    Education & Qualifications — 10 points.
    """

    education_text = section_content.get(
        "education",
        ""
    )

    if not education_text.strip():
        return 0

    score = 4

    education_lower = education_text.lower()

    degree_keywords = [
        "bachelor",
        "master",
        "b.tech",
        "m.tech",
        "b.e",
        "m.e",
        "b.sc",
        "m.sc",
        "phd",
        "doctorate",
        "degree"
    ]

    if any(
        keyword in education_lower
        for keyword in degree_keywords
    ):
        score += 3

    # Academic performance
    if re.search(
        r"\b(?:cgpa|gpa|percentage|percent)\b",
        education_lower
    ):
        score += 2

    # Institution / college information
    if (
        "university" in education_lower
        or "institute" in education_lower
        or "college" in education_lower
    ):
        score += 1

    return min(score, 10)


def calculate_format_readability_score(
    resume_text,
    sections,
    section_content
):
    """
    Formatting & Readability — 10 points.

    Since this scorer receives extracted text rather than
    the original visual document, this measures text-level
    structural signals only.

    It does NOT pretend to evaluate visual formatting perfectly.
    """

    score = 0

    # Reasonable overall length — 3 points
    score += estimate_resume_length_quality(
        resume_text
    )

    # Recognizable sections — 3 points
    section_count = sum(
        1
        for value in sections.values()
        if value
    )

    if section_count >= 5:
        score += 3
    elif section_count >= 4:
        score += 2
    elif section_count >= 3:
        score += 1

    # Reasonable section content — 2 points
    non_empty_sections = sum(
        1
        for content in section_content.values()
        if content and content.strip()
    )

    if non_empty_sections >= 5:
        score += 2
    elif non_empty_sections >= 3:
        score += 1

    # Avoid excessive repeated blank lines / malformed text
    # This is a small text extraction quality signal.
    repeated_spaces = len(
        re.findall(r"[ \t]{3,}", resume_text)
    )

    if repeated_spaces == 0:
        score += 1

    # Date presence — 1 point
    if detect_dates(resume_text):
        score += 1

    return min(score, 10)


def calculate_contact_score(contact_info):
    """
    Contact & Professional Details — 5 points.

    Email + phone are core.
    LinkedIn/GitHub are useful but should not dominate
    the intrinsic resume quality score.
    """

    score = 0

    if contact_info.get("email"):
        score += 2

    if contact_info.get("phone"):
        score += 2

    # One professional profile is enough for the final point.
    if (
        contact_info.get("linkedin")
        or contact_info.get("github")
    ):
        score += 1

    return min(score, 5)


# ============================================================
# MAIN RESUME SCORING FUNCTION
# ============================================================

def calculate_resume_score(
    contact_info,
    sections,
    section_content,
    resume_text
):
    """
    Calculate an overall resume quality score.

    IMPORTANT:
    This score evaluates the intrinsic quality of the resume.

    It does NOT use:
        - ATS role matching
        - Job description matching
        - Semantic similarity

    Those are intentionally kept as separate scores.
    """

    # Safety handling
    if not resume_text:
        resume_text = ""

    if not section_content:
        section_content = {}

    if not sections:
        sections = {}

    # --------------------------------------------------------
    # Determine candidate profile
    # --------------------------------------------------------

    is_fresher = detect_fresher_profile(
        sections,
        section_content
    )

    # --------------------------------------------------------
    # Calculate individual dimensions
    # --------------------------------------------------------

    content_impact_score = (
        calculate_content_impact_score(
            resume_text,
            section_content,
            is_fresher
        )
    )

    structure_score = (
        calculate_structure_score(
            sections,
            section_content,
            is_fresher
        )
    )

    skills_score = (
        calculate_skills_score(
            section_content,
            section_content.get("projects", "")
        )
    )

    project_experience_score = (
        calculate_project_experience_score(
            section_content,
            is_fresher
        )
    )

    education_score = (
        calculate_education_score(
            section_content
        )
    )

    formatting_score = (
        calculate_format_readability_score(
            resume_text,
            sections,
            section_content
        )
    )

    contact_score = (
        calculate_contact_score(
            contact_info
        )
    )

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    total_score = (
        content_impact_score
        + structure_score
        + skills_score
        + project_experience_score
        + education_score
        + formatting_score
        + contact_score
    )

    total_score = min(
        round(total_score),
        100
    )

    # --------------------------------------------------------
    # Breakdown
    # --------------------------------------------------------

    breakdown = {
        "content_impact": content_impact_score,
        "structure": structure_score,
        "skills": skills_score,
        "projects_experience": project_experience_score,
        "education": education_score,
        "formatting": formatting_score,
        "contact": contact_score
    }

    return {
        "total_score": total_score,
        "breakdown": breakdown,
        "profile_type": (
            "fresher"
            if is_fresher
            else "experienced"
        )
    }
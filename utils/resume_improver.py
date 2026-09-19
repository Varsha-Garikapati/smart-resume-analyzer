import re


# =========================================
# HELPER FUNCTIONS
# =========================================

def split_into_sentences(text):
    """
    Split resume content into meaningful lines
    or sentences for analysis.
    """

    lines = []

    for line in text.split("\n"):

        cleaned_line = line.strip()

        if cleaned_line:
            lines.append(cleaned_line)

    return lines


def has_action_verb(text):
    """
    Check whether a line starts with
    a strong action verb.
    """

    action_verbs = [
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
        "led"
    ]

    text_lower = text.lower().strip()

    return any(
        text_lower.startswith(verb)
        for verb in action_verbs
    )


def contains_measurement(text):
    """
    Detect measurable achievements such as:
    89%, 2,700+, 100 users, etc.
    """

    patterns = [
        r"\d+%",
        r"\d[\d,]*\+",
        r"\b\d+\s+(users|images|projects|models|problems|metrics)\b"
    ]

    for pattern in patterns:

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):
            return True

    return False


def contains_weak_phrase(text):
    """
    Detect commonly weak resume phrases.
    """

    weak_phrases = [
        "worked on",
        "responsible for",
        "helped with",
        "involved in",
        "participated in",
        "familiar with"
    ]

    text_lower = text.lower()

    return any(
        phrase in text_lower
        for phrase in weak_phrases
    )


# =========================================
# PROJECT ANALYSIS
# =========================================

def analyze_projects(projects_content):

    suggestions = []

    if not projects_content:

        suggestions.append(
            "Add at least one technical project demonstrating your skills."
        )

        return suggestions


    lines = split_into_sentences(
        projects_content
    )

    weak_action_count = 0
    measurement_count = 0


    for line in lines:

        # Ignore very short lines
        if len(line.split()) < 5:
            continue

        if not has_action_verb(line):
            weak_action_count += 1

        if contains_measurement(line):
            measurement_count += 1


    if weak_action_count >= 2:

        suggestions.append(
            "Strengthen project descriptions by starting bullet points "
            "with action verbs such as Developed, Built, Implemented, "
            "or Optimized."
        )


    if measurement_count == 0:

        suggestions.append(
            "Add measurable project outcomes such as accuracy, "
            "performance improvements, dataset size, or number of users."
        )


    if not suggestions:

        suggestions.append(
            "Your project descriptions use strong action language "
            "and measurable achievements."
        )


    return suggestions


# =========================================
# EXPERIENCE ANALYSIS
# =========================================

def analyze_experience(experience_content):

    suggestions = []

    if not experience_content:

        suggestions.append(
            "Add relevant internships, research experience, "
            "freelance work, or leadership experience."
        )

        return suggestions


    lines = split_into_sentences(
        experience_content
    )

    weak_phrases_found = 0
    weak_action_count = 0
    measurement_count = 0


    for line in lines:

        if len(line.split()) < 5:
            continue

        if contains_weak_phrase(line):
            weak_phrases_found += 1

        if not has_action_verb(line):
            weak_action_count += 1

        if contains_measurement(line):
            measurement_count += 1


    if weak_phrases_found > 0:

        suggestions.append(
            "Replace weak phrases such as 'Worked on' or "
            "'Responsible for' with stronger action verbs."
        )


    if weak_action_count >= 2:

        suggestions.append(
            "Start experience bullet points with strong action verbs "
            "such as Developed, Implemented, Built, or Optimized."
        )


    if measurement_count == 0:

        suggestions.append(
            "Add measurable impact to your experience where possible, "
            "such as performance improvements, users served, "
            "features delivered, or time saved."
        )


    if not suggestions:

        suggestions.append(
            "Your experience descriptions contain strong action language "
            "and measurable impact."
        )


    return suggestions


# =========================================
# SKILLS ANALYSIS
# =========================================

def analyze_skills(skills_content):

    suggestions = []

    if not skills_content:

        suggestions.append(
            "Add a dedicated technical skills section."
        )

        return suggestions


    skill_categories = {

        "Programming": [
            "python",
            "java",
            "c++",
            "sql",
            "javascript"
        ],

        "Machine Learning": [
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "scikit-learn"
        ],

        "Tools": [
            "git",
            "github",
            "docker",
            "linux",
            "aws"
        ]
    }


    skills_lower = skills_content.lower()

    missing_categories = []


    for category, skills in skill_categories.items():

        if not any(
            skill in skills_lower
            for skill in skills
        ):
            missing_categories.append(
                category
            )


    if missing_categories:

        suggestions.append(
            "Consider strengthening your skills section with "
            "relevant categories such as: "
            + ", ".join(missing_categories)
            + "."
        )

    else:

        suggestions.append(
            "Your skills section covers programming, technical tools, "
            "and machine learning technologies."
        )


    return suggestions


# =========================================
# MAIN RESUME IMPROVEMENT FUNCTION
# =========================================

def generate_resume_improvements(
    section_content
):
    """
    Generate personalized improvement suggestions
    based on the actual resume content.
    """

    projects_content = section_content.get(
        "projects",
        ""
    )

    experience_content = section_content.get(
        "experience",
        ""
    )

    skills_content = section_content.get(
        "skills",
        ""
    )


    improvements = {

        "projects": analyze_projects(
            projects_content
        ),

        "experience": analyze_experience(
            experience_content
        ),

        "skills": analyze_skills(
            skills_content
        )

    }


    return improvements

import re


# =========================================
# SKILL DATABASE WITH ALIASES
# =========================================

SKILL_DATABASE = {

    # Programming Languages
    "python": ["python"],
    "java": ["java"],
    "c++": ["c++", "cpp"],
    "c": ["c"],
    "sql": ["sql"],

    "javascript": [
        "javascript",
        "java script",
        "js"
    ],

    "typescript": [
        "typescript",
        "ts"
    ],


    # =====================================
    # MACHINE LEARNING / AI
    # =====================================

    "machine learning": [
        "machine learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "dl"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "tensorflow": [
        "tensorflow",
        "tensor flow"
    ],

    "pytorch": [
        "pytorch",
        "py torch"
    ],

    "scikit-learn": [
        "scikit-learn",
        "scikit learn",
        "sklearn"
    ],

    "computer vision": [
        "computer vision",
        "cv"
    ],

    "natural language processing": [
        "natural language processing",
        "nlp"
    ],

    "cnn": [
        "cnn",
        "convolutional neural network"
    ],

    "rnn": [
        "rnn",
        "recurrent neural network"
    ],

    "transformers": [
        "transformers",
        "transformer models"
    ],

    "generative ai": [
        "generative ai",
        "gen ai"
    ],

    "large language models": [
        "large language models",
        "llm"
    ],

    "rag": [
        "rag",
        "retrieval augmented generation"
    ],


    # =====================================
    # DATA SCIENCE
    # =====================================

    "pandas": ["pandas"],

    "numpy": ["numpy"],

    "matplotlib": ["matplotlib"],

    "seaborn": ["seaborn"],

    "data analysis": [
        "data analysis",
        "data analytics"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation"
    ],

    "statistics": [
        "statistics",
        "statistical analysis"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "tableau": ["tableau"],

    "excel": [
        "excel",
        "microsoft excel"
    ],


    # =====================================
    # WEB DEVELOPMENT
    # =====================================

    "html": ["html"],

    "css": ["css"],

    "react": [
        "react",
        "react.js",
        "reactjs"
    ],

    "node.js": [
        "node.js",
        "nodejs",
        "node"
    ],

    "flask": ["flask"],

    "django": ["django"],

    "fastapi": [
        "fastapi",
        "fast api"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "restful apis"
    ],


    # =====================================
    # TOOLS / DEVOPS
    # =====================================

    "git": ["git"],

    "github": ["github"],

    "docker": ["docker"],

    "kubernetes": [
        "kubernetes",
        "k8s"
    ],

    "linux": ["linux"],


    # =====================================
    # CLOUD
    # =====================================

    "aws": [
        "aws",
        "amazon web services"
    ],

    "azure": [
        "azure",
        "microsoft azure"
    ],

    "google cloud": [
        "google cloud",
        "gcp"
    ],


    # =====================================
    # DATABASES
    # =====================================

    "mysql": ["mysql"],

    "postgresql": [
        "postgresql",
        "postgres"
    ],

    "mongodb": [
        "mongodb",
        "mongo db"
    ],


    # =====================================
    # OTHER
    # =====================================

    "streamlit": ["streamlit"],

    "jupyter": [
        "jupyter",
        "jupyter notebook"
    ],

    "api": ["api", "apis"],

    "agile": ["agile"]
}


# =========================================
# HELPER FUNCTION
# =========================================

def skill_found_in_text(skill_aliases, text):
    """
    Check whether any alias of a skill
    is present in the given text.
    """

    for alias in skill_aliases:

        pattern = (
            r"(?<!\w)"
            + re.escape(alias.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):
            return True

    return False


# =========================================
# EXTRACT SKILLS FROM JOB DESCRIPTION
# =========================================

def extract_jd_skills(job_description):
    """
    Extract recognized technical skills
    from the Job Description using aliases.
    """

    job_description_lower = job_description.lower()

    found_skills = []

    for skill, aliases in SKILL_DATABASE.items():

        if skill_found_in_text(
            aliases,
            job_description_lower
        ):

            found_skills.append(skill)

    return sorted(set(found_skills))


# =========================================
# MAIN JD ANALYSIS FUNCTION
# =========================================

def analyze_job_description(
    resume_text,
    job_description
):
    """
    Compare resume skills with skills
    extracted from the Job Description.
    """

    # =====================================
    # CHECK IF JD WAS PROVIDED
    # =====================================

    if not job_description or not job_description.strip():

        return {
            "jd_provided": False,
            "jd_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "jd_match_score": None
        }


    # =====================================
    # EXTRACT SKILLS FROM JD
    # =====================================

    jd_skills = extract_jd_skills(
        job_description
    )


    # =====================================
    # PREPARE RESUME TEXT
    # =====================================

    resume_text_lower = resume_text.lower()


    # =====================================
    # MATCH SKILLS
    # =====================================

    matched_skills = []

    missing_skills = []


    for skill in jd_skills:

        aliases = SKILL_DATABASE[skill]

        if skill_found_in_text(
            aliases,
            resume_text_lower
        ):

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)


    # =====================================
    # CALCULATE JD MATCH SCORE
    # =====================================

    if jd_skills:

        jd_match_score = round(

            (
                len(matched_skills)
                / len(jd_skills)
            ) * 100

        )

    else:

        jd_match_score = 0


    # =====================================
    # RETURN RESULT
    # =====================================

    return {

        "jd_provided": True,

        "jd_skills": jd_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "jd_match_score": jd_match_score

    }
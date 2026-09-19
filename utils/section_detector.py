import re


SECTION_KEYWORDS = {
    "education": [
        "education",
        "academic background",
        "academic qualifications"
    ],

    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "technical expertise"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "internship",
        "internships"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "courses and certifications",
        "licenses"
    ]
}


ALL_HEADINGS = [
    "education",
    "academic background",
    "academic qualifications",

    "skills",
    "technical skills",
    "core competencies",
    "technical expertise",

    "projects",
    "academic projects",
    "personal projects",
    "project experience",

    "experience",
    "work experience",
    "professional experience",
    "internship",
    "internships",

    "certifications",
    "certificates",
    "courses and certifications",
    "licenses",

    "achievements",
    "awards",
    "accomplishments",
    "honors and awards",

    "summary",
    "profile",
    "professional summary",
    "objective",
    "career objective",
    "about me",
    "contact",
    "contact information",
    "languages",
    "interests",
    "publications",
    "positions of responsibility",
    "extracurricular activities"
]


def normalize_text(text):
    """Normalize text for heading comparison."""

    text = text.strip().lower()

    # Remove common heading punctuation
    text = re.sub(r"[:\-|]+$", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_section_from_heading(heading):
    """Return the analyzer section corresponding to a heading."""

    heading = normalize_text(heading)

    for section, keywords in SECTION_KEYWORDS.items():

        for keyword in keywords:

            if heading == keyword.lower():
                return section

    return None


def is_exact_heading(line):
    """
    Check whether the complete line is a known heading.

    Example:
        'EXPERIENCE' -> True

    But:
        'I have hands-on experience in machine learning'
        -> False
    """

    normalized_line = normalize_text(line)

    for heading in ALL_HEADINGS:

        if normalized_line == heading.lower():
            return heading

    return None


def detect_merged_headings(line):
    """
    Detect PDF extraction cases where two headings
    are joined together.

    Example:
        EDUCATIONABOUT ME

    This is interpreted as:
        EDUCATION
        ABOUT ME
    """

    text = normalize_text(line)

    headings = sorted(
        ALL_HEADINGS,
        key=len,
        reverse=True
    )

    for first_heading in headings:

        first = first_heading.lower()

        if not text.startswith(first):
            continue

        remaining = text[len(first):].strip()

        if not remaining:
            continue

        for second_heading in headings:

            second = second_heading.lower()

            if remaining == second:
                return [
                    first_heading,
                    second_heading
                ]

    return []


def detect_sections(text):
    """
    Detect actual resume section headings.

    The detector intentionally does NOT search for section
    words anywhere in the resume text. This prevents words
    such as 'experience' inside normal sentences from being
    incorrectly treated as section headings.
    """

    lines = text.split("\n")

    detected_sections = {
        "education": False,
        "skills": False,
        "projects": False,
        "experience": False,
        "certifications": False
    }

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        # ----------------------------------------------
        # Case 1: Normal heading
        # ----------------------------------------------

        heading = is_exact_heading(clean_line)

        if heading:

            section = get_section_from_heading(heading)

            if section:
                detected_sections[section] = True

            continue

        # ----------------------------------------------
        # Case 2: Merged PDF headings
        # Example: EDUCATIONABOUT ME
        # ----------------------------------------------

        merged = detect_merged_headings(clean_line)

        if merged:

            for heading in merged:

                section = get_section_from_heading(heading)

                if section:
                    detected_sections[section] = True

    return detected_sections
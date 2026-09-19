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
        "technical skills & tools",
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
    ],

    "achievements": [
        "achievements",
        "awards",
        "accomplishments",
        "honors and awards"
    ]
}


ALL_SECTION_HEADINGS = [
    "education",
    "academic background",
    "academic qualifications",

    "skills",
    "technical skills",
    "technical skills & tools",
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


def normalize_heading(text):
    """
    Normalize a possible heading for comparison.
    """

    text = text.strip().lower()

    # Remove common heading punctuation
    text = re.sub(r"[:\-|]+$", "", text).strip()

    return text


def get_section_name(heading):
    """
    Convert a heading into the internal section name.
    """

    heading = normalize_heading(heading)

    for section, keywords in SECTION_KEYWORDS.items():

        for keyword in keywords:

            if heading == keyword.lower():
                return section

    return None


def find_exact_heading(line):
    """
    Check whether the entire line is a known heading.
    """

    normalized_line = normalize_heading(line)

    for heading in sorted(
        ALL_SECTION_HEADINGS,
        key=len,
        reverse=True
    ):

        if normalized_line == heading.lower():
            return heading

    return None


def find_merged_headings(line):
    """
    Detect headings that have been merged together by PDF extraction.

    Example:

        EDUCATIONABOUT ME

    becomes:

        EDUCATION
        ABOUT ME

    IMPORTANT:
    We only allow this when the line STARTS with one known
    heading and the remaining text is another known heading.
    This prevents normal sentences containing words like
    'skills' or 'experience' from being treated as headings.
    """

    text = line.strip()
    text_lower = text.lower()

    headings = sorted(
        ALL_SECTION_HEADINGS,
        key=len,
        reverse=True
    )

    results = []

    # The first heading must start the line.
    for first_heading in headings:

        first_lower = first_heading.lower()

        if not text_lower.startswith(first_lower):
            continue

        remaining = text_lower[len(first_lower):].strip()

        if not remaining:
            continue

        # Check whether another heading immediately follows.
        for second_heading in headings:

            second_lower = second_heading.lower()

            if remaining.startswith(second_lower):

                leftover = remaining[len(second_lower):].strip()

                # The remainder must be empty.
                # This keeps the merged-heading rule strict.
                if not leftover:

                    results.append(
                        (first_heading, second_heading)
                    )

                break

        if results:
            break

    return results

def is_contact_line(line):
    """
    Check whether a line mainly contains contact information.
    """

    line_lower = line.lower().strip()

    # Phone number
    if re.search(r"(?:\+91[-\s]?)?[6-9]\d{9}", line):
        return True

    # Email
    if re.search(
        r"[A-Za-z0-9._%+-]+\s*@\s*[A-Za-z0-9.-]+\s*\.\s*[A-Za-z]{2,}",
        line
    ):
        return True

    # Contact labels that may appear after PDF extraction
    if line_lower in {
        "linkedin",
        "github",
        "email",
        "phone",
        "contact",
        "contact information"
    }:
        return True

    return False


def extract_sections(text):
    """
    Extract content belonging to important resume sections.

    Handles:
    1. Normal section headings.
    2. PDF-extracted merged headings such as
       'EDUCATIONABOUT ME'.

    It intentionally does NOT treat ordinary occurrences
    of words like 'skills' or 'experience' as headings.
    """

    lines = text.split("\n")

    extracted_sections = {
        "education": "",
        "skills": "",
        "projects": "",
        "experience": "",
        "certifications": "",
        "achievements": ""
    }

    current_section = None

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        # --------------------------------------------------
        # CASE 1: Entire line is a known heading
        # --------------------------------------------------

        exact_heading = find_exact_heading(clean_line)

        if exact_heading:

            section_name = get_section_name(exact_heading)

            if section_name:
                current_section = section_name
            else:
                # Non-extractable heading such as About Me,
                # Summary, Contact, etc. ends the previous section.
                current_section = None

            continue

        # --------------------------------------------------
        # CASE 2: PDF merged two headings together
        # Example: EDUCATIONABOUT ME
        # --------------------------------------------------

        merged_headings = find_merged_headings(clean_line)

        if merged_headings:

            first_heading, second_heading = merged_headings[0]

            first_section = get_section_name(first_heading)
            second_section = get_section_name(second_heading)

            # First heading starts a section
            if first_section:
                current_section = first_section
            #else:
                #current_section = None

            # Second heading immediately ends/changes it
            if second_section:
                current_section = second_section
            #else:
                #current_section = None

            continue

        # --------------------------------------------------
        # CASE 3: Normal content
        # --------------------------------------------------

        if current_section:

            if is_contact_line(clean_line):
                continue

            extracted_sections[current_section] += (
                clean_line + "\n"
            )

    return extracted_sections
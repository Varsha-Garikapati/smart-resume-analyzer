import os
import re
import fitz
from docx import Document


def _detect_column_split(blocks, page_width):
    """
    Analyse block x0 positions to determine whether the page has
    two distinct columns.

    Returns the x-coordinate of the gap between the columns if a
    two-column layout is detected, otherwise returns None.

    Strategy
    --------
    1. Collect the left edge (x0) of every text block.
    2. Build a histogram with ~10-point buckets across the page.
    3. If there are two clearly separated clusters of x0 values,
       the page is two-column.  The split point is the midpoint of
       the gap between the clusters.
    """

    if not blocks or page_width <= 0:
        return None

    x0_values = []
    for block in blocks:
        if block.get("type") != 0:
            continue
        bx0 = block["bbox"][0]
        x0_values.append(bx0)

    if len(x0_values) < 4:
        return None

    # Bucket width ~5 points
    bucket_size = 5
    n_buckets = max(1, int(page_width / bucket_size))
    buckets = [0] * n_buckets

    for x in x0_values:
        idx = min(int(x / bucket_size), n_buckets - 1)
        buckets[idx] = 1  # presence, not count

    # Find the leftmost and rightmost occupied buckets
    occupied = [i for i, v in enumerate(buckets) if v]
    if not occupied:
        return None

    left_edge = occupied[0] * bucket_size
    right_edge = occupied[-1] * bucket_size

    # If all blocks start within ~15 % of each other, it's single column
    span = right_edge - left_edge
    if span < page_width * 0.15:
        return None

    # Find the largest gap between consecutive occupied buckets
    # in the middle 80 % of the page (ignore margins)
    margin_left = page_width * 0.10
    margin_right = page_width * 0.90

    best_gap_size = 0
    best_gap_mid = None

    for k in range(len(occupied) - 1):
        a = occupied[k] * bucket_size
        b = occupied[k + 1] * bucket_size
        gap = b - a
        mid = (a + b) / 2

        if gap > best_gap_size and margin_left < mid < margin_right:
            best_gap_size = gap
            best_gap_mid = mid

    # Gap must be meaningful (at least 8 % of page width)
    if best_gap_mid is None or best_gap_size < page_width * 0.08:
        return None

    return best_gap_mid


def _extract_page_text_singlecol(blocks):
    """
    Original single-column extraction: sort all lines by (y0, x0).
    """
    lines = []
    for block in blocks:
        if block.get("type") != 0:
            continue
        for line in block["lines"]:
            line_text = "".join(s["text"] for s in line["spans"]).strip()
            if line_text:
                x0, y0, x1, y1 = line["bbox"]
                lines.append((y0, x0, line_text))

    lines.sort(key=lambda item: (round(item[0], 1), round(item[1], 1)))
    return "\n".join(t for _, _, t in lines)


def _extract_page_text_twocol(blocks, split_x):
    """
    Two-column extraction: separate blocks into left and right groups
    by their block-level x0, then sort each column top-to-bottom and
    concatenate (left column first, then right column).
    """
    left_lines = []
    right_lines = []

    for block in blocks:
        if block.get("type") != 0:
            continue

        block_x0 = block["bbox"][0]

        for line in block["lines"]:
            line_text = "".join(s["text"] for s in line["spans"]).strip()
            if not line_text:
                continue

            x0, y0, x1, y1 = line["bbox"]

            if block_x0 < split_x:
                left_lines.append((y0, x0, line_text))
            else:
                right_lines.append((y0, x0, line_text))

    left_lines.sort(key=lambda item: (round(item[0], 1), round(item[1], 1)))
    right_lines.sort(key=lambda item: (round(item[0], 1), round(item[1], 1)))

    left_text = "\n".join(t for _, _, t in left_lines)
    right_text = "\n".join(t for _, _, t in right_lines)

    parts = [p for p in [left_text, right_text] if p]
    return "\n\n".join(parts)


def extract_text_from_pdf(file_path):
    text = ""

    document = fitz.open(file_path)

    for page in document:

        page_dict = page.get_text("dict")
        page_width = page.rect.width
        blocks = page_dict["blocks"]

        # --------------------------------------------------
        # Detect whether this page is two-column
        # --------------------------------------------------
        split_x = _detect_column_split(blocks, page_width)

        if split_x is not None:
            page_text = _extract_page_text_twocol(blocks, split_x)
        else:
            page_text = _extract_page_text_singlecol(blocks)

        text += page_text + "\n\n"

    document.close()

    # ==================================================
    # CLEAN PDF EXTRACTION ARTIFACTS
    # ==================================================

    # Normalize spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # --------------------------------------------------
    # PUNCTUATION (SENTENCE SEPARATION)
    # --------------------------------------------------

    # Separate fused sentences without splitting technical terms,
    # abbreviations, domains, or file extensions.
    text = re.sub(
        r"(?<=[a-z])[.!?](?=[A-Z])",
        r"\g<0> ",
        text
    )

    # --------------------------------------------------
    # EMAILS
    # --------------------------------------------------

    text = re.sub(
        r"([A-Za-z0-9._%+-]+)"
        r"\s*@\s*"
        r"([A-Za-z0-9.-]+)"
        r"\s*\.\s*"
        r"([A-Za-z]{2,})",
        r"\1@\2.\3",
        text
    )

    # --------------------------------------------------
    # TECHNICAL TERMS
    # --------------------------------------------------

    text = re.sub(
        r"\bReact\s*\.\s*js\b",
        "React.js",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\bDeeplearning\s*\.\s*ai\b",
        "Deeplearning.ai",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # ABBREVIATIONS
    # --------------------------------------------------

    text = re.sub(
        r"\be\s*\.\s*g\s*\.",
        "e.g.",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # PRESENT
    # --------------------------------------------------

    text = re.sub(
        r"\bp\s*r\s*e\s*s\s*e\s*n\s*t\b",
        "present",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # DATE RANGES
    # --------------------------------------------------

    text = re.sub(
        r"(\d{4})\s*-\s*(present|current)",
        r"\1 - \2",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # ACCURACY
    # --------------------------------------------------

    text = re.sub(
        r"(\d+(?:\.\d+)?)\s*accuracy",
        r"\1% accuracy",
        text,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------
    # BLANK LINES
    # --------------------------------------------------

    text = re.sub(
        r"\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()
    


def extract_text_from_docx(file_path):
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_resume_text(file_path):
    """Detect the file type and extract resume text."""

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF or DOCX."
        )


def extract_contact_info(text):
    """Extract contact information from resume text."""

    # --------------------------------------------------
    # EMAIL
    # --------------------------------------------------

    email_pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"\s*@\s*"
        r"[A-Za-z0-9.-]+"
        r"\s*\.\s*"
        r"[A-Za-z]{2,}"
    )

    email_matches = re.findall(
        email_pattern,
        text
    )

    emails = []

    for email in email_matches:

        # Remove spaces introduced by PDF extraction
        email = re.sub(
            r"\s+",
            "",
            email
        )

        # PDF extraction may attach the next label to the email
        email = re.split(
            r"linkedin|github",
            email,
            flags=re.IGNORECASE
        )[0]

        if email not in emails:
            emails.append(email)

    # --------------------------------------------------
    # PHONE
    # --------------------------------------------------
    # Supports:
    # +91 98765 43210
    # +91-9876543210
    # +1 415 555 2671
    # +44 20 7946 0958
    # +61-412-345-678
    # 98765 43210
    #
    # First extract phone-like candidates, then keep only
    # candidates containing 8-15 digits.

    phone_candidates = re.findall(
        r"(?<!\w)\+?\d[\d\s().-]{7,20}\d(?!\w)",
        text
    )

    phones = []

    for phone in phone_candidates:

        # Count only actual digits
        digit_count = len(re.sub(r"\D", "", phone))

        if 8 <= digit_count <= 15:
            # Skip simple 4‑digit years (e.g., 2022)
            if digit_count == 4:
                continue
            # Clean excessive whitespace
            phone = re.sub(r"\s+", " ", phone).strip()
            if phone not in phones:
                phones.append(phone)

    # --------------------------------------------------
    # LINKEDIN
    # --------------------------------------------------

    linkedin_pattern = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"linkedin\.com/[A-Za-z0-9_./-]+"
    )

    linkedin = re.findall(
        linkedin_pattern,
        text,
        re.IGNORECASE
    )

    # If PDF extraction keeps only the visible "LinkedIn"
    # label, still mark LinkedIn as detected.
    if not linkedin:

        if re.search(
            r"\blinkedin\b",
            text,
            re.IGNORECASE
        ):
            linkedin = ["LinkedIn"]

    # --------------------------------------------------
    # GITHUB
    # --------------------------------------------------

    github_pattern = (
        r"(?:https?://)?"
        r"(?:www\.)?"
        r"github\.com/[A-Za-z0-9_./-]+"
    )

    github = re.findall(
        github_pattern,
        text,
        re.IGNORECASE
    )

    # --------------------------------------------------
    # RETURN CONTACT INFORMATION
    # --------------------------------------------------

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "linkedin": linkedin[0] if linkedin else None,
        "github": github[0] if github else None
    }
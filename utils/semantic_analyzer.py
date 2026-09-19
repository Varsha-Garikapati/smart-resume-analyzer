from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
import re


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def get_section_text(section_content, section_name):
    """
    Safely get text from a resume section.
    """

    if not section_content:
        return ""

    text = section_content.get(
        section_name,
        ""
    )

    if not text:
        return ""

    return text.strip()


def calculate_similarity(text1, text2):
    """
    Calculate semantic similarity between two pieces of text.
    """

    if not text1 or not text2:
        return 0

    embeddings = model.encode(
        [
            text1,
            text2
        ],
        convert_to_tensor=True
    )

    similarity = cos_sim(
        embeddings[0],
        embeddings[1]
    )

    return float(
        similarity.item()
    )


def split_into_chunks(text):
    if not text:
        return []

    lines = text.splitlines()
    chunks = []
    current_chunk = ""

    heading_patterns = [
        r"^what are we looking for\??\s*:?\s*$",
        r"^requirements\??\s*:?\s*$",
        r"^responsibilities\??\s*:?\s*$",
        r"^qualifications\??\s*:?\s*$",
        r"^skills\??\s*:?\s*$",
        r"^about the role\??\s*:?\s*$",
        r"^your role\s*[–—-]?\s*:?\s*$"
    ]

    for raw_line in lines:

        line = raw_line.strip()

        # Blank line = end of paragraph/chunk
        if not line:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            continue

        is_bullet = bool(
            re.match(
                r"^[•●▪◦\-–—]\s*",
                line
            )
        )

        # Remove bullet marker
        line = re.sub(
            r"^[•●▪◦\-–—]\s*",
            "",
            line
        )

        # Remove embedded "Your Role" heading
        line = re.sub(
            r"\s*(Your Role\s*[–—-]?)\s*$",
            "",
            line,
            flags=re.IGNORECASE
        )

        if not line:
            continue

        # Ignore standalone JD headings
        if any(
            re.match(
                pattern,
                line,
                re.IGNORECASE
            )
            for pattern in heading_patterns
        ):
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            continue

        # Each bullet starts a new chunk
        if is_bullet:

            if current_chunk:
                chunks.append(current_chunk.strip())

            current_chunk = line

        else:

            # Continue the current paragraph
            if current_chunk:
                current_chunk += " " + line
            else:
                current_chunk = line

    # Add final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Remove very short chunks
    chunks = [
        chunk
        for chunk in chunks
        if len(chunk.split()) >= 5
    ]

    return chunks


def find_semantic_insights(
    resume_text,
    job_description,
    section_content=None
):
    # -----------------------------
    # Prepare JD requirements
    # -----------------------------
    jd_chunks = split_into_chunks(
        job_description
    )

    # -----------------------------
    # Prepare resume evidence
    # Use meaningful resume sections
    # instead of the whole resume
    # -----------------------------

    resume_chunks = []

    if section_content:
        evidence_sections = [
            "projects",
            "experience"
        ]

        for section_name in evidence_sections:
            section_text = section_content.get(
                section_name,
                ""
            )

            if not section_text:
                continue

            # Normalize PDF line breaks while preserving
            # sentence boundaries.
            text = re.sub(
                r"\s+",
                " ",
                section_text
            ).strip()

            # Split into complete sentences.
            # This keeps multi-line PDF sentences together
            # while separating different resume bullets.
            chunks = re.split(
                r"(?<=[.!?])\s+(?=[A-Z])",
                text
            )

            for chunk in chunks:
                chunk = chunk.strip()

                if not chunk:
                    continue

                chunk = re.sub(
                    r"^[•●▪◦\-–—]\s*",
                    "",
                    chunk
                ).strip()

                if len(chunk.split()) >= 5:
                    resume_chunks.append(
                        chunk
                    )

    # -----------------------------
    # Fallback for cases where
    # section content is unavailable
    # -----------------------------

    if not resume_chunks:
        resume_lines = resume_text.splitlines()

        for line in resume_lines:
            line = line.strip()

            if not line:
                continue

            line = re.sub(
                r"^[•●▪◦\-–—]\s*",
                "",
                line
            )

            if len(line.split()) < 5:
                continue

            resume_chunks.append(line)

    if not resume_chunks or not jd_chunks:
        return {
            "strong_matches": [],
            "semantic_gaps": []
        }

    # -----------------------------
    # Generate embeddings
    # -----------------------------

    resume_embeddings = model.encode(
        resume_chunks,
        convert_to_tensor=True
    )

    jd_embeddings = model.encode(
        jd_chunks,
        convert_to_tensor=True
    )

    # -----------------------------
    # Compare JD requirements
    # with resume evidence
    # -----------------------------

    similarity_matrix = cos_sim(
        jd_embeddings,
        resume_embeddings
    )

    strong_matches = []
    semantic_gaps = []

    for i, jd_chunk in enumerate(
        jd_chunks
    ):

        similarities = similarity_matrix[i]

        best_score = float(
            similarities.max().item()
        )

        best_index = int(
            similarities.argmax().item()
        )

        best_resume_chunk = (
            resume_chunks[best_index]
        )

        percentage = round(
            best_score * 100
        )

        if percentage >= 55:
            strong_matches.append({
                "requirement": jd_chunk,
                "resume_match": best_resume_chunk,
                "score": percentage
            })

        elif percentage < 40:
            semantic_gaps.append({
                "requirement": jd_chunk,
                "score": percentage
            })

    # -----------------------------
    # Remove duplicate matches
    # -----------------------------

    unique_matches = []
    used_pairs = set()

    for match in sorted(
        strong_matches,
        key=lambda x: x["score"],
        reverse=True
    ):

        pair = (
            match["requirement"],
            match["resume_match"]
        )

        if pair not in used_pairs:
            unique_matches.append(match)
            used_pairs.add(pair)

    strong_matches = unique_matches[:5]

    # -----------------------------
    # Remove duplicate gaps
    # -----------------------------

    unique_gaps = []
    used_requirements = set()

    for gap in sorted(
        semantic_gaps,
        key=lambda x: x["score"]
    ):

        requirement = gap["requirement"]

        if requirement not in used_requirements:
            unique_gaps.append(gap)
            used_requirements.add(requirement)

    semantic_gaps = unique_gaps[:5]

    return {
        "strong_matches": strong_matches,
        "semantic_gaps": semantic_gaps
    }


def calculate_semantic_similarity(
    resume_text,
    job_description,
    section_content=None
):
    """
    Calculate semantic similarity between
    relevant resume sections and a job description.

    Skills and projects receive the highest importance
    because they provide the strongest evidence of
    technical alignment.
    """

    if (
        not job_description
        or not job_description.strip()
    ):
        return {
            "semantic_score": None,
            "semantic_similarity": None,
            "section_similarities": {},
            "semantic_insights": {
                "strong_matches": [],
                "semantic_gaps": []
            }
        }

    # --------------------------------------------------
    # Get relevant resume sections
    # --------------------------------------------------

    skills_text = get_section_text(
        section_content,
        "skills"
    )

    projects_text = get_section_text(
        section_content,
        "projects"
    )

    experience_text = get_section_text(
        section_content,
        "experience"
    )

    # --------------------------------------------------
    # Calculate section-wise similarities
    # --------------------------------------------------

    section_similarities = {}

    if skills_text:

        section_similarities["skills"] = (
            calculate_similarity(
                skills_text,
                job_description
            )
        )

    if projects_text:

        section_similarities["projects"] = (
            calculate_similarity(
                projects_text,
                job_description
            )
        )

    if experience_text:

        section_similarities["experience"] = (
            calculate_similarity(
                experience_text,
                job_description
            )
        )

    # --------------------------------------------------
    # Weighted semantic score
    # --------------------------------------------------

    weighted_score = 0
    total_weight = 0

    if skills_text:

        weighted_score += (
            section_similarities["skills"] * 0.40
        )

        total_weight += 0.40

    if projects_text:

        weighted_score += (
            section_similarities["projects"] * 0.40
        )

        total_weight += 0.40

    if experience_text:

        weighted_score += (
            section_similarities["experience"] * 0.20
        )

        total_weight += 0.20

    # --------------------------------------------------
    # Fallback
    # --------------------------------------------------

    if total_weight == 0:

        similarity = calculate_similarity(
            resume_text,
            job_description
        )

        weighted_similarity = similarity

    else:

        weighted_similarity = (
            weighted_score / total_weight
        )

    # --------------------------------------------------
    # Convert to percentage
    # --------------------------------------------------

    semantic_score = round(
        weighted_similarity * 100
    )

    semantic_score = max(
        0,
        min(
            semantic_score,
            100
        )
    )

    # --------------------------------------------------
    # Generate semantic insights
    # --------------------------------------------------

    semantic_insights = find_semantic_insights(
        resume_text,
        job_description,
        section_content
    )

    # --------------------------------------------------
    # Return result
    # --------------------------------------------------

    return {
        "semantic_score": semantic_score,

        "semantic_similarity": weighted_similarity,

        "section_similarities": {
            key: round(
                value * 100
            )
            for key, value
            in section_similarities.items()
        },

        "semantic_insights": semantic_insights
    }
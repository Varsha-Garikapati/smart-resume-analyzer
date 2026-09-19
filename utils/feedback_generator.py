def generate_feedback(
    contact_info,
    sections,
    score_result,
    ats_result
):
    strengths = []
    improvements = []
    recommendations = []

    # ---------------- CONTACT INFORMATION ----------------

    if contact_info.get("email"):
        strengths.append("Professional email address is present.")
    else:
        improvements.append("Add a professional email address.")

    if contact_info.get("phone"):
        strengths.append("Phone number is available.")
    else:
        improvements.append("Add a contact phone number.")

    if contact_info.get("linkedin"):
        strengths.append("LinkedIn profile is included.")
    else:
        recommendations.append("Consider adding a LinkedIn profile link.")
    if contact_info.get("github"):
        strengths.append("GitHub profile link is included.")
    else:
        recommendations.append(
            "No GitHub profile link was detected. "
            "Consider adding a clickable GitHub or portfolio URL to showcase your projects."
        )

    # ---------------- RESUME SECTIONS ----------------

    section_labels = {
        "education": "Education",
        "skills": "Skills",
        "projects": "Projects",
        "experience": "Experience",
        "certifications": "Certifications"
    }

    for section, label in section_labels.items():

        if not sections.get(section):

            if section == "experience":
                recommendations.append(
                    "No formal experience section was detected. "
                    "For a fresher, this is not necessarily a weakness. "
                    "Consider adding internships, research, freelance work, "
                    "or relevant leadership experience if available."
                )
            else:
                improvements.append(
                    f"Add an {label} section to improve resume completeness."
                )

    # ---------------- ATS ANALYSIS ----------------

    ats_score = ats_result.get("ats_score", 0)
    selected_role = ats_result.get(
        "selected_role",
        "the selected role"
    )

    missing_skills = ats_result.get("missing_skills", [])

    if ats_score >= 80:
        strengths.append(
            f"Strong ATS compatibility for the {selected_role} role."
        )

    elif ats_score >= 50:
        recommendations.append(
            f"Your resume has moderate ATS compatibility for the "
            f"{selected_role} role."
        )

    else:
        improvements.append(
            f"Your resume needs stronger alignment with the "
            f"{selected_role} role."
        )

    if missing_skills:
        skills_text = ", ".join(missing_skills[:5])

        recommendations.append(
            f"Consider adding relevant skills such as: {skills_text}."
        )
    else:
        strengths.append(
            "All key skills for the selected role were detected."
        )

    # ---------------- OVERALL RESUME SCORE ----------------

    total_score = score_result.get("total_score", 0)

    if total_score >= 80:

        strengths.append(
            "Your resume has a strong overall structure and content."
        )

    elif total_score >= 60:

        recommendations.append(
            "Your resume has a solid foundation. "
            "Focus on improving weaker sections and adding measurable impact."
        )

    else:

        improvements.append(
            "Improve resume completeness, structure, and content quality."
        )

    # ---------------- FALLBACK ----------------

    if not strengths:
        strengths.append(
            "Your resume contains relevant academic and technical content."
        )

    if not improvements:
        improvements.append(
            "No major structural issues were detected. "
            "Focus on tailoring the resume to the target role and strengthening measurable impact."
        )

    if not recommendations:
        recommendations.append(
            "Continue tailoring your resume to the specific job description."
        )

    return {
        "strengths": strengths,
        "improvements": improvements,
        "recommendations": recommendations
    }
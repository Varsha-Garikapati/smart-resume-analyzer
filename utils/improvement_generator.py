import re


def generate_improvements(section_content, ats_result):
    """
    Generate section-wise resume improvement suggestions.
    """

    improvements = {
        "projects": [],
        "skills": [],
        "experience": [],
        "education": [],
        "overall": []
    }

    # =====================================
    # PROJECT IMPROVEMENTS
    # =====================================

    projects_text = section_content.get("projects", "")

    if projects_text:

        # Check for numbers / measurable results
        if not re.search(r"\d+", projects_text):
            improvements["projects"].append(
                "Add measurable achievements such as accuracy, percentage improvement, dataset size, users, or performance metrics."
            )

        # Check for technology indicators
        technology_keywords = [
            "python", "java", "c++", "tensorflow",
            "pytorch", "react", "flask", "django",
            "streamlit", "sql", "aws"
        ]

        found_technologies = sum(
            keyword in projects_text.lower()
            for keyword in technology_keywords
        )

        if found_technologies < 2:
            improvements["projects"].append(
                "Mention the key technologies and tools used in each project."
            )

        if not improvements["projects"]:
            improvements["projects"].append(
                "Your projects include measurable results and relevant technologies. Consider adding stronger impact statements where possible."
            )

    else:

        improvements["projects"].append(
            "Add a Projects section with 2–4 relevant projects demonstrating your technical skills."
        )


    # =====================================
    # SKILLS IMPROVEMENTS
    # =====================================

    skills_text = section_content.get("skills", "")

    if not skills_text:

        improvements["skills"].append(
            "Add a dedicated Technical Skills section highlighting your strongest technologies and tools."
        )

    elif len(skills_text.split()) < 10:

        improvements["skills"].append(
            "Expand your skills section by including relevant programming languages, frameworks, tools, and technologies."
        )

    else:

        improvements["skills"].append(
            "Your skills section is well developed. Consider organizing skills into clear categories for better readability."
        )


    # =====================================
    # EXPERIENCE IMPROVEMENTS
    # =====================================

    experience_text = section_content.get("experience", "")

    if not experience_text:

        improvements["experience"].append(
            "No formal experience section was detected. "
            "For a fresher, this is not necessarily a weakness. "
            "Consider adding internships, research, freelance work, "
            "or relevant leadership experience if available."
        )

    else:

        # Check for measurable results
        if not re.search(r"\d+", experience_text):

            improvements["experience"].append(
                "Add measurable impact to your experience, such as performance improvements, users served, time saved, or project scale."
            )

        # Check for action verbs
        action_verbs = [
            "developed", "built", "implemented",
            "designed", "created", "optimized",
            "improved", "analyzed", "collaborated"
        ]

        found_action_verb = any(
            verb in experience_text.lower()
            for verb in action_verbs
        )

        if not found_action_verb:

            improvements["experience"].append(
                "Start experience bullet points with strong action verbs such as Developed, Built, Implemented, or Optimized."
            )

        if not improvements["experience"]:

            improvements["experience"].append(
                "Your experience descriptions are structured well. Consider adding more measurable impact where possible."
            )


    # =====================================
    # EDUCATION IMPROVEMENTS
    # =====================================

    education_text = section_content.get("education", "").strip()

    if not education_text:

        improvements["education"].append(
            "Add your degree, institution, graduation year, and relevant academic achievements."
        )

    else:

        improvements["education"].append(
            "Your education section is complete. Keep your degree, institution, graduation year, and academic achievements clearly formatted."
        )


    # =====================================
    # OVERALL / ATS IMPROVEMENTS
    # =====================================

    missing_skills = ats_result.get("missing_skills", [])

    if missing_skills:

        skills_list = ", ".join(missing_skills[:5])

        improvements["overall"].append(
            f"For the selected role, consider adding relevant skills such as: {skills_list}."
        )


    ats_score = ats_result.get("ats_score", 0)

    if ats_score < 50:

        improvements["overall"].append(
            "Your resume has low alignment with the selected role. "
            "Tailor your skills, projects, and experience to better match "
            "the job requirements."
        )

    elif ats_score < 75:

        improvements["overall"].append(
            "Your resume has moderate alignment with the selected role. "
            "Strengthening role-specific keywords could improve your ATS compatibility."
        )

    else:

        improvements["overall"].append(
            "Your resume has strong alignment with the selected role. "
            "Focus on improving clarity and demonstrating measurable impact."
        )


    return improvements
import os

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from utils.section_detector import detect_sections
from utils.section_extractor import extract_sections
from utils.resume_scorer import calculate_resume_score
from utils.ats_analyzer import analyze_ats
from utils.resume_parser import (
    extract_resume_text,
    extract_contact_info
)
from utils.feedback_generator import generate_feedback
from utils.improvement_generator import generate_improvements
from utils.resume_improver import generate_resume_improvements
from utils.jd_analyzer import analyze_job_description
from utils.semantic_analyzer import calculate_semantic_similarity

app = Flask(__name__)


# =========================================
# CONFIGURATION
# =========================================

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Create uploads folder if it does not exist
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================
# FILE VALIDATION
# =========================================

def allowed_file(filename):

    """
    Check whether the uploaded file
    has an allowed extension.
    """

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================
# UPLOAD AND ANALYZE RESUME
# =========================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_resume():

    # -------------------------------------
    # CHECK FILE
    # -------------------------------------

    if "resume" not in request.files:

        return "No file uploaded."


    file = request.files["resume"]
    selected_role = request.form.get("role")
    job_description = request.form.get("job_description", "")


    # -------------------------------------
    # VALIDATE FILE
    # -------------------------------------

    if file.filename == "":

        return "Please select a resume file."


    if not selected_role:

        return "Please select a target job role."


    if not allowed_file(
        file.filename
    ):

        return (
            "Only PDF and DOCX files "
            "are allowed."
        )


    # -------------------------------------
    # SAVE FILE
    # -------------------------------------

    filename = secure_filename(
        file.filename
    )


    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )


    file.save(
        file_path
    )


    try:

        # =================================
        # EXTRACT RESUME TEXT
        # =================================

        resume_text = extract_resume_text(
            file_path
        )


        # =================================
        # EXTRACT CONTACT INFORMATION
        # =================================

        contact_info = extract_contact_info(
            resume_text
        )


        # =================================
        # DETECT SECTIONS
        # =================================

        sections = detect_sections(
            resume_text
        )
        


        # =================================
        # EXTRACT SECTION CONTENT
        # =================================

        section_content = extract_sections(
            resume_text
        )
        # =================================
        # CALCULATE RESUME SCORE
        # =================================

        score_result = calculate_resume_score(
            contact_info,
            sections,
            section_content,
            resume_text
        )


        # =================================
        # ATS ANALYSIS
        # =================================

        ats_result = analyze_ats(
            resume_text,
            selected_role,
            contact_info,
            sections
        )
        jd_result = analyze_job_description(
            resume_text,
            job_description
        )
        # =================================
        # SEMANTIC AI ANALYSIS
        # =================================
        semantic_result = calculate_semantic_similarity(
            resume_text,
            job_description,
            section_content
        )

        # =================================
        # SMART RESUME FEEDBACK
        # =================================

        feedback = generate_feedback(
            contact_info,
            sections,
            score_result,
            ats_result
        )

        # =================================
        # GENERAL SECTION IMPROVEMENTS
        # =================================

        improvements = generate_improvements(
            section_content,
            ats_result
        )

        # =================================
        # PERSONALIZED RESUME IMPROVEMENTS
        # =================================

        resume_improvements = (
            generate_resume_improvements(
                section_content
            )
        )


        # =================================
        # RENDER RESULT PAGE
        # =================================

        return render_template(

            "result.html",
            resume_text=resume_text,
            contact_info=contact_info,
            sections=sections,
            section_content=section_content,
            score_result=score_result,
            ats_result=ats_result,
            jd_result=jd_result,
            semantic_result=semantic_result,
            feedback=feedback,
            improvements=improvements,
            resume_improvements=resume_improvements
        )


    except Exception as error:

        return (

            "Error processing resume: "

            f"{str(error)}"
        )


# =========================================
# RUN APPLICATION
# =========================================

if __name__ == "__main__":

    app.run(
        debug=False
    )
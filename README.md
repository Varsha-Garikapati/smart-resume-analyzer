# Smart AI Resume Analyzer

An AI-assisted resume analysis web application that evaluates resume quality, ATS compatibility, job-description alignment, and contextual semantic similarity.

## Features

- PDF and DOCX resume upload
- Resume text extraction
- Contact information extraction
- Automatic resume section detection
- Explainable overall resume scoring
- Role-specific ATS compatibility analysis
- Job Description (JD) keyword matching
- AI-based semantic similarity analysis
- Section-wise semantic analysis
- Strengths and improvement recommendations
- Project, skills, experience, and education improvement suggestions
- Responsive web interface

## Technology Stack

### Backend
- Python
- Flask

### Resume Processing
- PyMuPDF
- python-docx
- Regular expressions

### AI / NLP
- Sentence Transformers
- `all-MiniLM-L6-v2`
- Cosine similarity

### Frontend
- HTML
- CSS
- JavaScript
- Jinja2 templates

### Data
- Job-role skill configuration
- Resume-JD evaluation dataset

## System Workflow

1. User uploads a resume in PDF or DOCX format.
2. The application extracts the resume text.
3. Contact information and resume sections are detected.
4. The resume is evaluated using an explainable scoring system.
5. ATS compatibility is calculated for the selected target role.
6. If a Job Description is provided, explicit JD skill matching is performed.
7. Sentence Transformers calculate contextual semantic similarity between the resume and JD.
8. The system generates semantic insights and identifies areas of low contextual coverage.
9. Personalized feedback and resume improvement suggestions are displayed.

## Scoring

The overall resume quality score is divided into seven categories:

| Category | Weight |
|---|---:|
| Content & Impact | 25 |
| Structure & Completeness | 20 |
| Skills & Technical Evidence | 15 |
| Projects / Experience Quality | 15 |
| Education & Qualifications | 10 |
| Formatting & Readability | 10 |
| Contact & Professional Details | 5 |
| **Total** | **100** |

ATS compatibility separately evaluates factors such as:

- Required skill coverage
- Resume section structure
- Contact information
- ATS parsing readiness
- Dates and consistency
- Content quality
- Role alignment

## Semantic Matching

The application uses the pretrained Sentence Transformer model:

`all-MiniLM-L6-v2`

Semantic matching is different from keyword matching. It measures contextual similarity between resume content and Job Description requirements using sentence embeddings and cosine similarity.

Semantic similarity is therefore treated as a contextual alignment signal rather than proof that a candidate possesses a particular skill.

## Project Structure

```text
smart-resume-analyzer/
│
├── app.py
├── requirements.txt
│
├── data/
│   ├── job_resume_fit.csv
│   ├── job_roles.json
│   └── scoring_evaluation_...
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── index.html
│   └── result.html
│
├── uploads/
│
└── utils/
    ├── ats_analyzer.py
    ├── evaluate_scoring.py
    ├── feedback_generator.py
    ├── improvement_generator.py
    ├── jd_analyzer.py
    ├── resume_improver.py
    ├── resume_parser.py
    ├── resume_scorer.py
    ├── section_detector.py
    ├── section_extractor.py
    └── semantic_analyzer.py
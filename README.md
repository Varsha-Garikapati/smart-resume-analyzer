# Smart AI Resume Analyzer

An AI-assisted web application that analyzes resumes for overall quality, ATS compatibility, job-description alignment, and contextual semantic similarity.

The system combines deterministic resume parsing and explainable scoring with NLP-based semantic analysis to provide actionable feedback for improving a resume.

---

## Features

- PDF and DOCX resume upload
- Resume text extraction
- Contact information extraction
- Automatic resume section detection
- Explainable overall resume quality scoring
- Role-specific ATS compatibility analysis
- Job Description (JD) keyword matching
- AI-based semantic similarity analysis
- Section-wise semantic analysis
- Contextual matches and low-coverage insights
- Strengths and improvement recommendations
- Project, skills, experience, and education improvement suggestions
- Responsive web interface
- Web deployment using Render

---

## Technology Stack

### Backend

- Python
- Flask

### Resume Processing

- PyMuPDF
- python-docx
- Regular Expressions

### AI / NLP

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Sentence embeddings
- Cosine similarity

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 templates

### Data

- Job-role skill configuration
- Resume-JD evaluation dataset
- Scoring evaluation data

### Deployment

- Render
- Gunicorn

---

## How It Works

The application follows the following pipeline:

```text
Resume Upload
      ↓
Resume Text Extraction
      ↓
Contact & Section Detection
      ↓
Overall Resume Quality Scoring
      ↓
Role-Specific ATS Analysis
      ↓
Job Description Analysis
      ↓
Semantic Similarity Analysis
      ↓
Feedback & Improvement Suggestions
      ↓
Interactive Results Dashboard
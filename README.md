# SmartHire

SmartHire is a full-stack resume analysis platform designed to evaluate a resume's ATS readiness and measure its alignment with a specific job description.

The project analyzes resume structure, extracts job requirements, performs skill and requirement matching, identifies missing keywords, and generates explainable recommendations to help candidates improve their resumes for a target role.

> **Project Status:** Backend V1 is implemented and validated. Frontend development, end-to-end integration, advanced AI features, and production deployment are planned next.

---

## Features

### Resume Processing

- Upload resumes in PDF or DOCX format
- Extract text from uploaded resumes
- Parse candidate information
- Detect contact details
- Identify major resume sections
- Report parser confidence and limitations

### Job Description Analysis

- Parse job descriptions
- Extract the job title
- Detect required, preferred, and unclassified skills
- Extract experience requirements
- Detect education requirements
- Detect certification requirements
- Report parsing confidence for incomplete or vague job descriptions

### ATS Readiness Analysis

- Evaluate whether resume text can be successfully extracted
- Check for meaningful resume content
- Detect important contact information
- Recognize core resume sections
- Evaluate structural readability
- Provide ATS-related findings and suggestions

The ATS Readiness Score is an internal heuristic for structural and text-based readiness. It does not reproduce the proprietary scoring algorithm of any specific applicant tracking system.

### Job-Specific Resume Matching

- Compare resume skills with job requirements
- Distinguish required and preferred skills
- Detect matched and missing skills
- Evaluate education requirements
- Handle experience requirements conservatively when they cannot be reliably verified
- Check certification requirements
- Dynamically calculate a Resume Match Score using applicable job requirements
- Return `unable_to_score` when the job description does not contain enough scoreable requirements

### Keyword Analysis

- Analyze technical keywords
- Identify matched and missing job-related skills
- Analyze relevant action terminology
- Filter generic job-description words
- Avoid recommending irrelevant or misleading keywords

### Recommendations

- Generate prioritized recommendations
- Prioritize missing required skills over preferred skills
- Provide evidence for recommendations
- Avoid unnecessary recommendations when no meaningful improvement can be inferred

### Authentication

- Custom Django user model
- User registration
- JWT-based authentication
- Protected resume analysis API

---

## Tech Stack

### Backend

- Python
- Django
- Django REST Framework
- Simple JWT

### Resume Processing

- PyPDF
- python-docx

### Database

- SQLite for local development

### Frontend

- React — planned

### Production Database and Deployment

- PostgreSQL — planned for production
- Deployment configuration — planned

---

## Current Project Structure

```text
SmartHire/
├── backend/
│   ├── apps/
│   │   ├── resumes/
│   │   │   ├── migrations/
│   │   │   ├── analysis.py
│   │   │   ├── ats.py
│   │   │   ├── job_parser.py
│   │   │   ├── keywords.py
│   │   │   ├── models.py
│   │   │   ├── parser.py
│   │   │   ├── recommendations.py
│   │   │   ├── serializers.py
│   │   │   ├── skill_taxonomy.py
│   │   │   ├── tests.py
│   │   │   ├── urls.py
│   │   │   ├── utils.py
│   │   │   └── views.py
│   │   │
│   │   └── users/
│   │       ├── migrations/
│   │       ├── admin.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── urls.py
│   │       └── views.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   └── urls.py
│   │
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## Analysis Workflow

```text
Resume Upload + Job Description
              │
              ▼
      Resume Text Extraction
              │
              ▼
   Resume and Job Description Parsing
              │
              ▼
     ATS Readiness Analysis
              │
              ▼
    Job-Specific Resume Matching
              │
              ▼
        Keyword Analysis
              │
              ▼
   Prioritized Recommendations
              │
              ▼
      Structured API Response
```

---

## API Overview

### Authentication

The backend provides endpoints for user registration and JWT-based authentication.

### Resume Analysis

The protected resume analysis endpoint accepts:

- A resume file
- A job description

The API returns structured results containing:

- ATS Readiness Score
- Resume Match Score when sufficient requirements are available
- Parsed resume information
- Parsed job requirements
- Skill matching results
- Experience analysis
- Education analysis
- Certification analysis
- Keyword analysis
- Prioritized recommendations
- Parser confidence and limitations

---

## Backend Validation

The current backend analyzer has been manually validated against multiple scenarios.

### Test 1 — Required and Preferred Skills

Verified:

- Required skill classification
- Preferred skill classification
- Skill matching
- Missing skill detection
- Recommendation prioritization

### Test 2 — Skills, Experience, and Education

Verified:

- Job title extraction
- Experience requirement parsing
- Education requirement parsing
- Required and preferred skill matching
- Safe handling of experience that cannot be reliably verified

### Test 3 — Vague Job Description

Verified:

- No invented technical requirements
- No invented education requirements
- No invented experience requirements
- No misleading `0%` match score
- `unable_to_score` behavior when no meaningful scoring components are available
- Filtering of generic contextual terms

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Divakarkotikalapudi/SmartHire.git
cd SmartHire
```

### 2. Create a Virtual Environment

```bash
cd backend
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Set a Django secret key using the `DJANGO_SECRET_KEY` environment variable.

For local development, configure environment variables according to your operating system or development environment.

Never commit real secret keys, passwords, API keys, or other credentials to the repository.

### 6. Apply Database Migrations

```bash
python manage.py migrate
```

### 7. Run Django System Checks

```bash
python manage.py check
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

The backend will run locally at:

```text
http://127.0.0.1:8000/
```

---

## Security and Repository Practices

The repository excludes local and sensitive files such as:

- Virtual environments
- Python cache files
- Local SQLite databases
- Environment variable files
- IDE-specific files
- Node.js dependencies and build output

Secrets should be provided through environment variables and must not be committed to Git.

---

## Current Limitations

- ATS scoring is heuristic and does not reproduce any proprietary ATS algorithm
- Text extraction alone cannot reliably detect every visual formatting problem
- Experience duration is not guessed when it cannot be reliably verified
- Resume matching quality depends on the information available in the job description
- The current skill taxonomy is rule-based and will be expanded
- Frontend integration is not yet implemented
- Advanced AI-assisted recommendations are planned for a later phase

---

## Roadmap

- [x] Django backend setup
- [x] User authentication
- [x] Resume upload and text extraction
- [x] Resume parsing
- [x] Job description parsing
- [x] ATS readiness analysis
- [x] Job-specific resume matching
- [x] Keyword analysis
- [x] Prioritized recommendations
- [x] Backend validation with multiple test scenarios
- [ ] UI/UX design
- [ ] React frontend
- [ ] Frontend and backend integration
- [ ] End-to-end testing
- [ ] Advanced AI-assisted resume suggestions
- [ ] PostgreSQL production configuration
- [ ] Production hardening
- [ ] Deployment

---

## Disclaimer

SmartHire provides heuristic resume analysis and job-alignment guidance. Its scores and recommendations are intended to support resume improvement and should not be interpreted as predictions or guarantees of hiring outcomes, interview selection, or performance in any specific applicant tracking system.

---

## Author

**Divakar Kotikalapudi**

GitHub: `Divakarkotikalapudi`

---

## License

A license has not yet been selected for this project.

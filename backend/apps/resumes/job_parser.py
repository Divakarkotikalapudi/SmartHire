import re

from .skill_taxonomy import SKILL_ALIASES
from .utils import normalize_text


# ---------------------------------------------------------------------------
# JOB DESCRIPTION SECTION HEADINGS
# ---------------------------------------------------------------------------

SECTION_HEADINGS = {
    "required": {
        "requirements",
        "required skills",
        "required qualifications",
        "minimum qualifications",
        "must have",
        "must-have skills",
        "essential skills",
        "essential qualifications",
        "what you need",
        "what we are looking for",
    },

    "preferred": {
        "preferred skills",
        "preferred qualifications",
        "nice to have",
        "nice-to-have",
        "good to have",
        "bonus skills",
        "desirable skills",
        "additional qualifications",
    },

    "responsibilities": {
        "responsibilities",
        "job responsibilities",
        "key responsibilities",
        "role responsibilities",
        "what you will do",
        "what you'll do",
        "duties",
    },

    "experience": {
        "experience",
        "experience requirements",
        "required experience",
        "professional experience",
    },

    "education": {
        "education",
        "education requirements",
        "educational qualifications",
        "academic qualifications",
    },

    "certifications": {
        "certifications",
        "required certifications",
        "preferred certifications",
        "licenses and certifications",
    },
}


# ---------------------------------------------------------------------------
# REQUIREMENT LANGUAGE
# ---------------------------------------------------------------------------

REQUIRED_CONTEXT_PATTERNS = [
    r"\brequired\b",
    r"\brequirement(?:s)?\b",
    r"\bmust\s+have\b",
    r"\bmust\s+possess\b",
    r"\bneed(?:ed|s)?\b",
    r"\bessential\b",
    r"\bmandatory\b",
    r"\bminimum\s+qualification(?:s)?\b",
    r"\bproficien(?:t|cy)\s+(?:in|with)\b",
    r"\bexperience\s+(?:in|with|using)\b",
    r"\bknowledge\s+of\b",
    r"\bfamiliarity\s+with\b",
    r"\bstrong\s+(?:knowledge|experience|skills?)\s+(?:in|with|of)\b",
    r"\bhands[-\s]?on\s+experience\s+(?:in|with|using)\b",
]


PREFERRED_CONTEXT_PATTERNS = [
    r"\bpreferred\b",
    r"\bpreferably\b",
    r"\bnice\s+to\s+have\b",
    r"\bgood\s+to\s+have\b",
    r"\bbonus\b",
    r"\ba\s+plus\b",
    r"\bplus\b",
    r"\bdesirable\b",
    r"\badvantage(?:ous)?\b",
    r"\boptional\b",
]


# ---------------------------------------------------------------------------
# EXPERIENCE PATTERNS
# ---------------------------------------------------------------------------

EXPERIENCE_PATTERNS = [
    re.compile(
        r"\b(\d+)\s*\+\s*years?"
        r"(?:\s+of)?\s+experience\b",
        re.IGNORECASE,
    ),

    re.compile(
        r"\bminimum\s+(?:of\s+)?(\d+)"
        r"\s+years?(?:\s+of)?\s+experience\b",
        re.IGNORECASE,
    ),

    re.compile(
        r"\bat\s+least\s+(\d+)"
        r"\s+years?(?:\s+of)?\s+experience\b",
        re.IGNORECASE,
    ),

    re.compile(
        r"\b(\d+)\s*[-–]\s*(\d+)"
        r"\s+years?(?:\s+of)?\s+experience\b",
        re.IGNORECASE,
    ),

    re.compile(
        r"\b(\d+)\s+to\s+(\d+)"
        r"\s+years?(?:\s+of)?\s+experience\b",
        re.IGNORECASE,
    ),
]


ENTRY_LEVEL_PATTERNS = [
    r"\bentry[-\s]?level\b",
    r"\bfresher(?:s)?\b",
    r"\brecent graduate(?:s)?\b",
    r"\bgraduate role\b",
    r"\b0\s*[-–]\s*1\s+years?\b",
    r"\b0\s+to\s+1\s+years?\b",
]


# ---------------------------------------------------------------------------
# EDUCATION CONFIGURATION
# ---------------------------------------------------------------------------

DEGREE_ALIASES = {
    "bachelor": {
        "bachelor degree",
        "bachelor's degree",
        "bachelors degree",
        "bachelor of technology",
        "bachelor of engineering",
        "bachelor of science",
        "b.tech",
        "btech",
        "b.e.",
        "b.sc",
        "bsc",
    },

    "master": {
        "master degree",
        "master's degree",
        "masters degree",
        "master of technology",
        "master of engineering",
        "master of science",
        "master of business administration",
        "m.tech",
        "mtech",
        "m.e.",
        "m.sc",
        "msc",
        "mba",
    },

    "phd": {
        "phd",
        "ph.d.",
        "doctorate",
        "doctoral degree",
    },
}

EDUCATION_FIELDS = {
    "computer science": {
        "computer science",
        "computer engineering",
        "cs",
        "cse",
    },

    "information technology": {
        "information technology",
        "it",
    },

    "software engineering": {
        "software engineering",
    },

    "electronics and communication engineering": {
        "electronics and communication engineering",
        "electronics & communication engineering",
        "ece",
    },

    "engineering": {
        "engineering",
    },
}


# ---------------------------------------------------------------------------
# CERTIFICATION CONFIGURATION
# ---------------------------------------------------------------------------

CERTIFICATION_KEYWORDS = {
    "aws certified cloud practitioner",
    "aws certified solutions architect",
    "aws certified developer",
    "aws certified sysops administrator",
    "microsoft certified azure fundamentals",
    "azure fundamentals",
    "google cloud certification",
    "google professional cloud architect",
    "pmp",
    "project management professional",
    "cissp",
    "comptia a+",
    "comptia security+",
    "comptia network+",
    "ccna",
    "certified scrum master",
}


# ---------------------------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------------------------

def add_unique(items, value):
    if value and value not in items:
        items.append(value)


def clean_line(line):
    line = line.strip()

    line = re.sub(
        r"^[\s•●▪◦*-]+",
        "",
        line,
    )

    return line.strip()


def normalize_heading(line):
    heading = clean_line(line)

    heading = heading.lower()

    heading = heading.rstrip(":")

    heading = re.sub(
        r"\s+",
        " ",
        heading,
    )

    return heading.strip()


def contains_phrase(text, phrase):
    normalized_text = normalize_text(text)
    normalized_phrase = normalize_text(phrase)

    if not normalized_text or not normalized_phrase:
        return False

    pattern = (
        rf"(?<!\w)"
        rf"{re.escape(normalized_phrase)}"
        rf"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE,
        )
    )


def matches_any_pattern(
    text,
    patterns,
):
    return any(
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )
        for pattern in patterns
    )


def get_skill_aliases(skill):
    aliases = SKILL_ALIASES.get(
        skill,
        [],
    )

    result = []

    for alias in [
        skill,
        *aliases,
    ]:
        add_unique(
            result,
            alias,
        )

    return result


def skill_exists_in_text(
    text,
    skill,
):
    return any(
        contains_phrase(
            text,
            alias,
        )
        for alias in get_skill_aliases(
            skill
        )
    )


# ---------------------------------------------------------------------------
# SECTION DETECTION
# ---------------------------------------------------------------------------

def detect_section_heading(line):
    normalized_line = normalize_heading(
        line
    )

    for section, headings in (
        SECTION_HEADINGS.items()
    ):
        if normalized_line in headings:
            return section

    return None


def split_job_sections(
    job_description,
):
    sections = {
        "general": [],
        "required": [],
        "preferred": [],
        "responsibilities": [],
        "experience": [],
        "education": [],
        "certifications": [],
    }

    current_section = "general"

    for raw_line in (
        job_description.splitlines()
    ):
        line = clean_line(
            raw_line
        )

        if not line:
            continue

        detected_section = (
            detect_section_heading(
                line
            )
        )

        if detected_section:
            current_section = (
                detected_section
            )

            continue

        sections[
            current_section
        ].append(
            line
        )

    return {
        section: "\n".join(
            content
        ).strip()
        for section, content
        in sections.items()
    }


# ---------------------------------------------------------------------------
# SKILL DETECTION
# ---------------------------------------------------------------------------

def detect_all_skills(
    job_description,
):
    detected = []

    for skill in SKILL_ALIASES:
        if skill_exists_in_text(
            job_description,
            skill,
        ):
            add_unique(
                detected,
                skill,
            )

    return detected


def detect_skills_in_text(
    text,
    all_detected_skills,
):
    detected = []

    for skill in all_detected_skills:
        if skill_exists_in_text(
            text,
            skill,
        ):
            add_unique(
                detected,
                skill,
            )

    return detected


# ---------------------------------------------------------------------------
# SENTENCE AND CLAUSE EXTRACTION
# ---------------------------------------------------------------------------

def split_into_sentences(
    text,
):
    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text,
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_into_clauses(
    sentence,
):
    clauses = re.split(
        r"[;]|"
        r"\bbut\b|"
        r"\bhowever\b|"
        r"\bwhile\b",
        sentence,
        flags=re.IGNORECASE,
    )

    return [
        clause.strip()
        for clause in clauses
        if clause.strip()
    ]


# ---------------------------------------------------------------------------
# SKILL REQUIREMENT CLASSIFICATION
# ---------------------------------------------------------------------------

def classify_skill_from_sections(
    skill,
    sections,
):
    if skill_exists_in_text(
        sections.get(
            "required",
            "",
        ),
        skill,
    ):
        return "required"

    if skill_exists_in_text(
        sections.get(
            "preferred",
            "",
        ),
        skill,
    ):
        return "preferred"

    return None


def classify_skill_from_context(
    skill,
    job_description,
):
    sentences = split_into_sentences(
        job_description
    )

    for sentence in sentences:
        if not skill_exists_in_text(
            sentence,
            skill,
        ):
            continue

        clauses = split_into_clauses(
            sentence
        )

        relevant_clauses = [
            clause
            for clause in clauses
            if skill_exists_in_text(
                clause,
                skill,
            )
        ]

        if not relevant_clauses:
            relevant_clauses = [
                sentence
            ]

        for clause in relevant_clauses:
            if matches_any_pattern(
                clause,
                PREFERRED_CONTEXT_PATTERNS,
            ):
                return "preferred"

        for clause in relevant_clauses:
            if matches_any_pattern(
                clause,
                REQUIRED_CONTEXT_PATTERNS,
            ):
                return "required"

    return None


def classify_skills(
    job_description,
    sections,
    all_skills,
):
    required = []
    preferred = []
    unclassified = []

    for skill in all_skills:
        classification = (
            classify_skill_from_sections(
                skill,
                sections,
            )
        )

        if classification is None:
            classification = (
                classify_skill_from_context(
                    skill,
                    job_description,
                )
            )

        if classification == "required":
            add_unique(
                required,
                skill,
            )

        elif classification == "preferred":
            add_unique(
                preferred,
                skill,
            )

        else:
            add_unique(
                unclassified,
                skill,
            )

    return {
        "all": all_skills,
        "required": required,
        "preferred": preferred,
        "unclassified": unclassified,
    }


# ---------------------------------------------------------------------------
# RESPONSIBILITY EXTRACTION
# ---------------------------------------------------------------------------

def extract_responsibilities(
    sections,
):
    responsibilities_text = (
        sections.get(
            "responsibilities",
            "",
        )
    )

    if not responsibilities_text:
        return []

    responsibilities = []

    for line in (
        responsibilities_text.splitlines()
    ):
        line = clean_line(
            line
        )

        if line:
            add_unique(
                responsibilities,
                line,
            )

    return responsibilities


# ---------------------------------------------------------------------------
# EXPERIENCE EXTRACTION
# ---------------------------------------------------------------------------

def extract_experience_requirements(
    job_description,
):
    requirements = []

    minimum_years = None
    maximum_years = None

    for pattern in EXPERIENCE_PATTERNS:
        for match in pattern.finditer(
            job_description
        ):
            groups = match.groups()

            if len(groups) == 1:
                minimum = int(
                    groups[0]
                )

                maximum = None

            else:
                minimum = int(
                    groups[0]
                )

                maximum = int(
                    groups[1]
                )

            requirements.append(
                {
                    "text": (
                        match.group(0)
                    ),
                    "minimum_years": (
                        minimum
                    ),
                    "maximum_years": (
                        maximum
                    ),
                }
            )

            if (
                minimum_years is None
                or minimum
                > minimum_years
            ):
                minimum_years = (
                    minimum
                )

            if maximum is not None:
                if (
                    maximum_years is None
                    or maximum
                    > maximum_years
                ):
                    maximum_years = (
                        maximum
                    )

    entry_level = (
        matches_any_pattern(
            job_description,
            ENTRY_LEVEL_PATTERNS,
        )
    )

    return {
        "requirements": requirements,
        "minimum_years": minimum_years,
        "maximum_years": maximum_years,
        "entry_level": entry_level,
    }


# ---------------------------------------------------------------------------
# EDUCATION EXTRACTION
# ---------------------------------------------------------------------------

def extract_education_requirements(
    job_description,
    sections,
):
    education_text = (
        sections.get(
            "education",
            "",
        )
    )

    search_text = (
        education_text
        if education_text
        else job_description
    )

    degrees = []
    fields = []

    for degree, aliases in (
        DEGREE_ALIASES.items()
    ):
        for alias in aliases:
            if contains_phrase(
                search_text,
                alias,
            ):
                add_unique(
                    degrees,
                    degree,
                )

                break

    for field, aliases in (
        EDUCATION_FIELDS.items()
    ):
        for alias in aliases:
            if contains_phrase(
                search_text,
                alias,
            ):
                add_unique(
                    fields,
                    field,
                )

                break

    required = bool(
        degrees
        or fields
        or education_text
    )

    return {
        "required": required,
        "degrees": degrees,
        "fields": fields,
        "raw_text": education_text,
    }


# ---------------------------------------------------------------------------
# CERTIFICATION EXTRACTION
# ---------------------------------------------------------------------------

def extract_certification_requirements(
    job_description,
    sections,
):
    certification_text = (
        sections.get(
            "certifications",
            "",
        )
    )

    search_text = (
        certification_text
        if certification_text
        else job_description
    )

    certifications = []

    for certification in (
        CERTIFICATION_KEYWORDS
    ):
        if contains_phrase(
            search_text,
            certification,
        ):
            add_unique(
                certifications,
                certification,
            )

    return {
        "certifications": certifications,
        "raw_text": certification_text,
    }


# ---------------------------------------------------------------------------
# JOB TITLE EXTRACTION
# ---------------------------------------------------------------------------

def extract_job_title(
    job_description,
):
    patterns = [
        # Examples:
        # "We are looking for a Python Developer"
        # "We are seeking an ML Engineer"
        # "We are hiring a Python Developer"
        # "Hiring a Data Analyst"
        (
            r"\b(?:"
            r"(?:looking|seeking)\s+for|"
            r"hiring"
            r")\s+(?:an?\s+)?"
            r"([a-zA-Z0-9+#./ -]+?"
            r"(?:developer|engineer|analyst|"
            r"designer|manager|specialist|"
            r"consultant|architect))\b"
        ),

        # Example: "Job Title: Python Developer"
        (
            r"\bjob\s+title\s*:\s*"
            r"([^\n]+)"
        ),

        # Example: "Position: Backend Engineer"
        (
            r"\bposition\s*:\s*"
            r"([^\n]+)"
        ),

        # Example: "Role: Software Developer"
        (
            r"\brole\s*:\s*"
            r"([^\n]+)"
        ),
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            job_description,
            flags=re.IGNORECASE,
        )

        if match:
            return (
                match.group(1)
                .strip()
                .rstrip(".,;:")
            )

    return None
# ---------------------------------------------------------------------------
# PARSER CONFIDENCE
# ---------------------------------------------------------------------------

def build_parser_confidence(
    job_description,
    sections,
    skills,
    responsibilities,
    experience,
    education,
):
    limitations = []

    word_count = len(
        job_description.split()
    )

    recognized_section_count = sum(
        1
        for section, content
        in sections.items()
        if (
            section != "general"
            and content
        )
    )

    if word_count < 40:
        limitations.append(
            "The job description is short, so "
            "some requirements may be missing "
            "or unclear."
        )

    if recognized_section_count == 0:
        limitations.append(
            "No explicit job-description "
            "sections were recognized."
        )

    if not responsibilities:
        limitations.append(
            "No explicit responsibilities "
            "section was detected."
        )

    if not (
        experience.get(
            "requirements"
        )
    ):
        limitations.append(
            "No explicit numeric experience "
            "requirement was detected."
        )

    if not education.get(
        "required"
    ):
        limitations.append(
            "No explicit education requirement "
            "was detected."
        )

    classified_skill_count = (
        len(
            skills.get(
                "required",
                [],
            )
        )
        + len(
            skills.get(
                "preferred",
                [],
            )
        )
    )

    if (
        skills.get(
            "all"
        )
        and classified_skill_count == 0
    ):
        limitations.append(
            "Detected skills could not be "
            "confidently classified as required "
            "or preferred."
        )

    if (
        word_count >= 100
        and recognized_section_count >= 2
    ):
        level = "high"

    elif (
        word_count >= 30
        or recognized_section_count >= 1
        or classified_skill_count > 0
    ):
        level = "moderate"

    else:
        level = "limited"

    return {
        "level": level,
        "limitations": limitations,
    }


# ---------------------------------------------------------------------------
# MAIN JOB DESCRIPTION PARSER
# ---------------------------------------------------------------------------

def parse_job_description(
    job_description,
):
    if not isinstance(
        job_description,
        str,
    ):
        raise ValueError(
            "Job description must be text."
        )

    job_description = (
        job_description.strip()
    )

    if not job_description:
        raise ValueError(
            "Job description cannot be empty."
        )

    sections = split_job_sections(
        job_description
    )

    all_skills = detect_all_skills(
        job_description
    )

    skills = classify_skills(
        job_description,
        sections,
        all_skills,
    )

    responsibilities = (
        extract_responsibilities(
            sections
        )
    )

    experience = (
        extract_experience_requirements(
            job_description
        )
    )

    education = (
        extract_education_requirements(
            job_description,
            sections,
        )
    )

    certifications = (
        extract_certification_requirements(
            job_description,
            sections,
        )
    )

    parser_confidence = (
        build_parser_confidence(
            job_description,
            sections,
            skills,
            responsibilities,
            experience,
            education,
        )
    )

    return {
        "job_title": (
            extract_job_title(
                job_description
            )
        ),

        "normalized_text": (
            normalize_text(
                job_description
            )
        ),

        "sections": sections,

        "skills": skills,

        "responsibilities": (
            responsibilities
        ),

        "experience": experience,

        "education": education,

        "certifications": (
            certifications
        ),

        "parser_confidence": (
            parser_confidence
        ),

        "metadata": {
            "word_count": len(
                job_description.split()
            ),

            "recognized_section_count": (
                sum(
                    1
                    for section, content
                    in sections.items()
                    if (
                        section != "general"
                        and content
                    )
                )
            ),
        },
    }
import re


# ---------------------------------------------------------------------------
# RESUME SECTION HEADINGS
# ---------------------------------------------------------------------------

SECTION_ALIASES = {
    "summary": [
        "summary",
        "professional summary",
        "career objective",
        "objective",
        "profile",
        "professional profile",
        "career summary",
        "about me",
    ],

    "skills": [
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "core competencies",
        "technical competencies",
        "technologies",
        "technology stack",
        "tech stack",
        "tools and technologies",
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "internship",
        "internships",
        "internship experience",
        "internships and experience",
        "professional experience and internships",
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "technical projects",
        "project experience",
        "key projects",
        "selected projects",
    ],

    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "educational qualifications",
        "qualifications",
        "education and qualifications",
    ],

    "certifications": [
        "certifications",
        "certification",
        "certificates",
        "professional certifications",
        "licenses and certifications",
        "courses and certifications",
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
        "awards and achievements",
        "honors",
        "honors and awards",
    ],

    "languages": [
        "languages",
        "language",
        "language proficiency",
        "languages known",
    ],

    "publications": [
        "publications",
        "research publications",
        "research papers",
        "published work",
    ],

    "volunteer_experience": [
        "volunteer experience",
        "volunteering",
        "volunteer work",
        "community involvement",
        "community service",
    ],
}


# ---------------------------------------------------------------------------
# CONTACT PATTERNS
# ---------------------------------------------------------------------------

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+"
    r"@[A-Za-z0-9.-]+"
    r"\.[A-Za-z]{2,}\b"
)


PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\+?\d{1,3}[\s.-]?)?"
    r"(?:\(?\d{2,5}\)?[\s.-]?)?"
    r"\d{3,5}[\s.-]?\d{4,6}"
    r"(?!\d)"
)


LINKEDIN_PATTERN = re.compile(
    r"(?:https?://)?"
    r"(?:www\.)?"
    r"linkedin\.com/in/"
    r"[A-Za-z0-9_-]+"
    r"/?",
    re.IGNORECASE,
)


GITHUB_PATTERN = re.compile(
    r"(?:https?://)?"
    r"(?:www\.)?"
    r"github\.com/"
    r"[A-Za-z0-9_-]+"
    r"/?",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------------------------

def normalize_heading(text):
    text = text.strip().lower()

    text = re.sub(
        r"^[\-\*\u2022\u25CF\u25AA\u25E6]+\s*",
        "",
        text,
    )

    text = re.sub(
        r"[:\-–—]+$",
        "",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def clean_content_line(line):
    return line.strip()


def add_unique(items, value):
    if value and value not in items:
        items.append(value)


# ---------------------------------------------------------------------------
# SECTION DETECTION
# ---------------------------------------------------------------------------

def detect_section_heading(line):
    normalized_line = normalize_heading(
        line
    )

    if not normalized_line:
        return None

    for section, aliases in SECTION_ALIASES.items():
        if normalized_line in aliases:
            return section

    return None


def initialize_sections():
    return {
        section: []
        for section in SECTION_ALIASES
    }


def extract_sections(resume_text):
    section_lines = initialize_sections()

    preamble_lines = []
    unknown_lines = []

    current_section = None

    for raw_line in resume_text.splitlines():
        line = clean_content_line(
            raw_line
        )

        if not line:
            continue

        detected_section = detect_section_heading(
            line
        )

        if detected_section:
            current_section = detected_section
            continue

        if current_section:
            section_lines[
                current_section
            ].append(line)

        else:
            preamble_lines.append(line)

    section_content = {
        section: "\n".join(
            lines
        ).strip()
        for section, lines
        in section_lines.items()
    }

    detected_sections = {
        section: bool(content)
        for section, content
        in section_content.items()
    }

    return {
        "sections": detected_sections,
        "section_content": section_content,
        "preamble": "\n".join(
            preamble_lines
        ).strip(),
        "unknown_content": "\n".join(
            unknown_lines
        ).strip(),
    }


# ---------------------------------------------------------------------------
# CONTACT INFORMATION
# ---------------------------------------------------------------------------

def extract_email(resume_text):
    match = EMAIL_PATTERN.search(
        resume_text
    )

    if match:
        return match.group(0)

    return None


def clean_phone_candidate(phone):
    phone = re.sub(
        r"\s+",
        " ",
        phone,
    ).strip()

    return phone


def is_probable_phone(phone):
    digits = re.sub(
        r"\D",
        "",
        phone,
    )

    return 10 <= len(digits) <= 15


def extract_phone(resume_text):
    matches = PHONE_PATTERN.findall(
        resume_text
    )

    for match in matches:
        candidate = clean_phone_candidate(
            match
        )

        if is_probable_phone(
            candidate
        ):
            return candidate

    return None


def extract_linkedin(resume_text):
    match = LINKEDIN_PATTERN.search(
        resume_text
    )

    if match:
        return match.group(0)

    return None


def extract_github(resume_text):
    match = GITHUB_PATTERN.search(
        resume_text
    )

    if match:
        return match.group(0)

    return None


def extract_contact_information(
    resume_text,
):
    return {
        "email": extract_email(
            resume_text
        ),
        "phone": extract_phone(
            resume_text
        ),
        "linkedin": extract_linkedin(
            resume_text
        ),
        "github": extract_github(
            resume_text
        ),
    }


# ---------------------------------------------------------------------------
# CANDIDATE NAME DETECTION
# ---------------------------------------------------------------------------

def is_possible_name(line):
    cleaned = line.strip()

    if not cleaned:
        return False

    if len(cleaned) > 80:
        return False

    if EMAIL_PATTERN.search(cleaned):
        return False

    if PHONE_PATTERN.search(cleaned):
        return False

    if LINKEDIN_PATTERN.search(cleaned):
        return False

    if GITHUB_PATTERN.search(cleaned):
        return False

    if detect_section_heading(cleaned):
        return False

    words = cleaned.split()

    if not 2 <= len(words) <= 6:
        return False

    alphabetic_words = sum(
        1
        for word in words
        if re.fullmatch(
            r"[A-Za-z.'-]+",
            word,
        )
    )

    return (
        alphabetic_words
        == len(words)
    )


def extract_candidate_name(
    resume_text,
):
    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    for line in lines[:8]:
        if is_possible_name(line):
            return line

    return None


# ---------------------------------------------------------------------------
# SECTION QUALITY INFORMATION
# ---------------------------------------------------------------------------

def analyze_section_quality(
    section_content,
):
    quality = {}

    for section, content in (
        section_content.items()
    ):
        word_count = len(
            content.split()
        )

        quality[section] = {
            "has_content": bool(
                content.strip()
            ),
            "word_count": word_count,
        }

    return quality


# ---------------------------------------------------------------------------
# PARSER CONFIDENCE
# ---------------------------------------------------------------------------

def calculate_parser_confidence(
    resume_text,
    contact,
    candidate_name,
    sections,
    section_content,
):
    signals = 0
    total_signals = 6
    limitations = []

    word_count = len(
        resume_text.split()
    )

    if word_count >= 100:
        signals += 1
    else:
        limitations.append(
            "The extracted resume text is short, so some content may not have been parsed."
        )

    if contact.get("email"):
        signals += 1
    else:
        limitations.append(
            "An email address could not be detected."
        )

    if contact.get("phone"):
        signals += 1
    else:
        limitations.append(
            "A phone number could not be detected."
        )

    if candidate_name:
        signals += 1
    else:
        limitations.append(
            "The candidate name could not be confidently detected."
        )

    core_sections = [
        "skills",
        "experience",
        "education",
        "projects",
    ]

    recognized_core_sections = sum(
        1
        for section in core_sections
        if sections.get(section)
    )

    if recognized_core_sections >= 3:
        signals += 1
    else:
        limitations.append(
            "Fewer than three core resume sections were confidently recognized."
        )

    meaningful_sections = sum(
        1
        for content
        in section_content.values()
        if len(content.split()) >= 5
    )

    if meaningful_sections >= 3:
        signals += 1
    else:
        limitations.append(
            "Limited structured section content was extracted."
        )

    confidence_ratio = (
        signals / total_signals
    )

    if confidence_ratio >= 0.8:
        level = "high"

    elif confidence_ratio >= 0.5:
        level = "moderate"

    else:
        level = "limited"

    return {
        "level": level,
        "limitations": limitations,
    }


# ---------------------------------------------------------------------------
# PARSING METADATA
# ---------------------------------------------------------------------------

def build_parser_metadata(
    resume_text,
    sections,
):
    detected_section_count = sum(
        1
        for detected in sections.values()
        if detected
    )

    return {
        "text_length": len(
            resume_text
        ),
        "word_count": len(
            resume_text.split()
        ),
        "line_count": len(
            [
                line
                for line
                in resume_text.splitlines()
                if line.strip()
            ]
        ),
        "detected_section_count": (
            detected_section_count
        ),
    }


# ---------------------------------------------------------------------------
# MAIN RESUME PARSER
# ---------------------------------------------------------------------------

def parse_resume(resume_text):
    if not isinstance(
        resume_text,
        str,
    ):
        raise ValueError(
            "Resume content must be text."
        )

    cleaned_resume_text = (
        resume_text.strip()
    )

    if not cleaned_resume_text:
        raise ValueError(
            "Resume text cannot be empty."
        )

    contact = extract_contact_information(
        cleaned_resume_text
    )

    candidate_name = (
        extract_candidate_name(
            cleaned_resume_text
        )
    )

    section_result = extract_sections(
        cleaned_resume_text
    )

    sections = section_result[
        "sections"
    ]

    section_content = section_result[
        "section_content"
    ]

    section_quality = (
        analyze_section_quality(
            section_content
        )
    )

    parser_confidence = (
        calculate_parser_confidence(
            cleaned_resume_text,
            contact,
            candidate_name,
            sections,
            section_content,
        )
    )

    metadata = build_parser_metadata(
        cleaned_resume_text,
        sections,
    )

    return {
        "candidate": {
            "name": candidate_name,
        },

        "contact": contact,

        "sections": sections,

        "section_content": (
            section_content
        ),

        "section_quality": (
            section_quality
        ),

        "preamble": section_result[
            "preamble"
        ],

        "parser_confidence": (
            parser_confidence
        ),

        "metadata": metadata,

        # Kept for compatibility with the current ATS engine.
        "text_length": metadata[
            "text_length"
        ],

        "word_count": metadata[
            "word_count"
        ],
    }
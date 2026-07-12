# ---------------------------------------------------------------------------
# ATS READINESS CONFIGURATION
# ---------------------------------------------------------------------------

CORE_SECTIONS = {
    "skills": 10,
    "experience": 10,
    "education": 10,
}


SUPPORTING_SECTIONS = {
    "projects": 5,
    "summary": 3,
    "certifications": 2,
}


MINIMUM_MEANINGFUL_WORDS = 80
RECOMMENDED_MINIMUM_WORDS = 200
RECOMMENDED_MAXIMUM_WORDS = 1200


# ---------------------------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------------------------

def clamp_score(score):
    return max(
        0.0,
        min(
            100.0,
            score,
        ),
    )


def round_score(score):
    return round(
        clamp_score(score),
        2,
    )


def create_check(
    category,
    name,
    status,
    points_earned,
    points_possible,
    message,
    severity=None,
):
    return {
        "category": category,
        "name": name,
        "status": status,
        "passed": status == "passed",
        "points_earned": round(
            points_earned,
            2,
        ),
        "points_possible": round(
            points_possible,
            2,
        ),
        "severity": severity,
        "message": message,
    }


# ---------------------------------------------------------------------------
# TEXT EXTRACTION CHECKS
# ---------------------------------------------------------------------------

def analyze_text_extraction(
    parsed_resume,
):
    checks = []

    metadata = parsed_resume.get(
        "metadata",
        {},
    )

    text_length = metadata.get(
        "text_length",
        parsed_resume.get(
            "text_length",
            0,
        ),
    )

    word_count = metadata.get(
        "word_count",
        parsed_resume.get(
            "word_count",
            0,
        ),
    )

    if text_length > 0:
        checks.append(
            create_check(
                category="parseability",
                name="text_extraction",
                status="passed",
                points_earned=15,
                points_possible=15,
                severity=None,
                message=(
                    "Resume text was successfully "
                    "extracted."
                ),
            )
        )

    else:
        checks.append(
            create_check(
                category="parseability",
                name="text_extraction",
                status="failed",
                points_earned=0,
                points_possible=15,
                severity="critical",
                message=(
                    "No extractable resume text "
                    "was detected."
                ),
            )
        )

    if word_count >= MINIMUM_MEANINGFUL_WORDS:
        checks.append(
            create_check(
                category="parseability",
                name="meaningful_content",
                status="passed",
                points_earned=10,
                points_possible=10,
                severity=None,
                message=(
                    "The resume contains enough "
                    "extractable text for "
                    "structured analysis."
                ),
            )
        )

    elif word_count > 0:
        checks.append(
            create_check(
                category="parseability",
                name="meaningful_content",
                status="warning",
                points_earned=5,
                points_possible=10,
                severity="medium",
                message=(
                    "The resume contains limited "
                    "extractable text. Important "
                    "content may be missing or "
                    "too brief."
                ),
            )
        )

    else:
        checks.append(
            create_check(
                category="parseability",
                name="meaningful_content",
                status="failed",
                points_earned=0,
                points_possible=10,
                severity="critical",
                message=(
                    "No meaningful resume content "
                    "could be analyzed."
                ),
            )
        )

    return checks


# ---------------------------------------------------------------------------
# CONTACT INFORMATION CHECKS
# ---------------------------------------------------------------------------

def analyze_contact_information(
    parsed_resume,
):
    checks = []

    contact = parsed_resume.get(
        "contact",
        {},
    )

    email = contact.get(
        "email"
    )

    phone = contact.get(
        "phone"
    )

    if email:
        checks.append(
            create_check(
                category="contact_information",
                name="email",
                status="passed",
                points_earned=8,
                points_possible=8,
                severity=None,
                message=(
                    "An email address was "
                    "successfully detected."
                ),
            )
        )

    else:
        checks.append(
            create_check(
                category="contact_information",
                name="email",
                status="failed",
                points_earned=0,
                points_possible=8,
                severity="high",
                message=(
                    "No email address was "
                    "detected."
                ),
            )
        )

    if phone:
        checks.append(
            create_check(
                category="contact_information",
                name="phone",
                status="passed",
                points_earned=7,
                points_possible=7,
                severity=None,
                message=(
                    "A phone number was "
                    "successfully detected."
                ),
            )
        )

    else:
        checks.append(
            create_check(
                category="contact_information",
                name="phone",
                status="failed",
                points_earned=0,
                points_possible=7,
                severity="high",
                message=(
                    "No phone number was "
                    "detected."
                ),
            )
        )

    return checks


# ---------------------------------------------------------------------------
# CORE SECTION CHECKS
# ---------------------------------------------------------------------------

def analyze_core_sections(
    parsed_resume,
):
    checks = []

    sections = parsed_resume.get(
        "sections",
        {},
    )

    section_content = parsed_resume.get(
        "section_content",
        {},
    )

    for section, points in (
        CORE_SECTIONS.items()
    ):
        detected = sections.get(
            section,
            False,
        )

        content = section_content.get(
            section,
            "",
        ).strip()

        if detected and content:
            checks.append(
                create_check(
                    category="core_sections",
                    name=section,
                    status="passed",
                    points_earned=points,
                    points_possible=points,
                    severity=None,
                    message=(
                        f"The {section} section "
                        f"was recognized and "
                        f"contains extractable "
                        f"content."
                    ),
                )
            )

        elif detected:
            checks.append(
                create_check(
                    category="core_sections",
                    name=section,
                    status="warning",
                    points_earned=(
                        points * 0.5
                    ),
                    points_possible=points,
                    severity="medium",
                    message=(
                        f"The {section} section "
                        f"was recognized but "
                        f"contains limited "
                        f"extractable content."
                    ),
                )
            )

        else:
            checks.append(
                create_check(
                    category="core_sections",
                    name=section,
                    status="failed",
                    points_earned=0,
                    points_possible=points,
                    severity="high",
                    message=(
                        f"The {section} section "
                        f"was not confidently "
                        f"recognized."
                    ),
                )
            )

    return checks


# ---------------------------------------------------------------------------
# SUPPORTING SECTION CHECKS
# ---------------------------------------------------------------------------

def analyze_supporting_sections(
    parsed_resume,
):
    checks = []

    sections = parsed_resume.get(
        "sections",
        {},
    )

    section_content = parsed_resume.get(
        "section_content",
        {},
    )

    for section, points in (
        SUPPORTING_SECTIONS.items()
    ):
        detected = sections.get(
            section,
            False,
        )

        content = section_content.get(
            section,
            "",
        ).strip()

        if detected and content:
            checks.append(
                create_check(
                    category="supporting_sections",
                    name=section,
                    status="passed",
                    points_earned=points,
                    points_possible=points,
                    severity=None,
                    message=(
                        f"The {section} section "
                        f"was recognized."
                    ),
                )
            )

        else:
            checks.append(
                create_check(
                    category="supporting_sections",
                    name=section,
                    status="not_present",
                    points_earned=0,
                    points_possible=points,
                    severity="low",
                    message=(
                        f"The {section} section "
                        f"was not detected. This "
                        f"may be acceptable "
                        f"depending on the "
                        f"candidate's background."
                    ),
                )
            )

    return checks


# ---------------------------------------------------------------------------
# STRUCTURE CHECKS
# ---------------------------------------------------------------------------

def analyze_structure(
    parsed_resume,
):
    checks = []

    metadata = parsed_resume.get(
        "metadata",
        {},
    )

    detected_section_count = (
        metadata.get(
            "detected_section_count",
            0,
        )
    )

    if detected_section_count >= 4:
        checks.append(
            create_check(
                category="structure",
                name="recognizable_structure",
                status="passed",
                points_earned=10,
                points_possible=10,
                severity=None,
                message=(
                    "The resume has a clearly "
                    "recognizable section "
                    "structure."
                ),
            )
        )

    elif detected_section_count >= 2:
        checks.append(
            create_check(
                category="structure",
                name="recognizable_structure",
                status="warning",
                points_earned=5,
                points_possible=10,
                severity="medium",
                message=(
                    "Only part of the resume "
                    "structure was confidently "
                    "recognized."
                ),
            )
        )

    else:
        checks.append(
            create_check(
                category="structure",
                name="recognizable_structure",
                status="failed",
                points_earned=0,
                points_possible=10,
                severity="high",
                message=(
                    "The resume structure was "
                    "difficult to recognize from "
                    "the extracted text."
                ),
            )
        )

    return checks


# ---------------------------------------------------------------------------
# RESUME LENGTH CHECK
# ---------------------------------------------------------------------------

def analyze_resume_length(
    parsed_resume,
):
    metadata = parsed_resume.get(
        "metadata",
        {},
    )

    word_count = metadata.get(
        "word_count",
        parsed_resume.get(
            "word_count",
            0,
        ),
    )

    if (
        RECOMMENDED_MINIMUM_WORDS
        <= word_count
        <= RECOMMENDED_MAXIMUM_WORDS
    ):
        return create_check(
            category="content_readability",
            name="resume_length",
            status="passed",
            points_earned=5,
            points_possible=5,
            severity=None,
            message=(
                "The amount of extracted text "
                "falls within the analyzer's "
                "general readability range."
            ),
        )

    if (
        MINIMUM_MEANINGFUL_WORDS
        <= word_count
        < RECOMMENDED_MINIMUM_WORDS
    ):
        return create_check(
            category="content_readability",
            name="resume_length",
            status="warning",
            points_earned=3,
            points_possible=5,
            severity="low",
            message=(
                "The resume is relatively brief. "
                "This is not automatically a "
                "problem, but important evidence "
                "may be limited."
            ),
        )

    if word_count > RECOMMENDED_MAXIMUM_WORDS:
        return create_check(
            category="content_readability",
            name="resume_length",
            status="warning",
            points_earned=3,
            points_possible=5,
            severity="low",
            message=(
                "The resume contains a large "
                "amount of extracted text. "
                "Review it for unnecessary or "
                "repetitive content."
            ),
        )

    return create_check(
        category="content_readability",
        name="resume_length",
        status="failed",
        points_earned=0,
        points_possible=5,
        severity="medium",
        message=(
            "The resume contains too little "
            "extractable text for reliable "
            "content analysis."
        ),
    )


# ---------------------------------------------------------------------------
# SCORE CALCULATION
# ---------------------------------------------------------------------------

def calculate_ats_score(
    checks,
):
    scored_checks = [
        check
        for check in checks
        if check["category"]
        != "supporting_sections"
    ]

    earned = sum(
        check["points_earned"]
        for check in scored_checks
    )

    possible = sum(
        check["points_possible"]
        for check in scored_checks
    )

    if possible == 0:
        return 0.0

    return round_score(
        (
            earned
            / possible
        )
        * 100
    )

# ---------------------------------------------------------------------------
# READINESS LEVEL
# ---------------------------------------------------------------------------

def get_readiness_level(
    score,
):
    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Good"

    if score >= 60:
        return "Needs Improvement"

    return "High Risk"


# ---------------------------------------------------------------------------
# FINDINGS
# ---------------------------------------------------------------------------

def build_findings(
    checks,
):
    strengths = []
    issues = []

    for check in checks:
        finding = {
            "category": check[
                "category"
            ],
            "name": check[
                "name"
            ],
            "message": check[
                "message"
            ],
        }

        if check["status"] == "passed":
            strengths.append(
                finding
            )

        elif check["status"] in {
            "failed",
            "warning",
        }:
            finding[
                "severity"
            ] = check[
                "severity"
            ]

            issues.append(
                finding
            )

    severity_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
        None: 4,
    }

    issues.sort(
        key=lambda item: (
            severity_order.get(
                item.get(
                    "severity"
                ),
                4,
            )
        )
    )

    return {
        "strengths": strengths,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# SUGGESTIONS
# ---------------------------------------------------------------------------

def build_ats_suggestions(
    checks,
):
    suggestions = []

    suggestion_messages = {
        "text_extraction": (
            "Use a text-based PDF or DOCX file "
            "and verify that resume text can be "
            "selected and copied."
        ),

        "meaningful_content": (
            "Ensure important resume content is "
            "present as extractable text rather "
            "than only inside images."
        ),

        "email": (
            "Add a professional email address "
            "in the main resume text."
        ),

        "phone": (
            "Add a valid phone number in the "
            "main resume text."
        ),

        "skills": (
            "Use a clearly labeled Skills or "
            "Technical Skills section."
        ),

        "experience": (
            "Use a clearly labeled Experience "
            "or Internship section when "
            "applicable."
        ),

        "education": (
            "Use a clearly labeled Education "
            "section."
        ),

        "recognizable_structure": (
            "Use conventional section headings "
            "and a clear reading order."
        ),

        "resume_length": (
            "Review the resume length and keep "
            "the content focused on relevant, "
            "specific evidence."
        ),
    }

    seen = set()

    for check in checks:
        if check["status"] not in {
            "failed",
            "warning",
        }:
            continue

        name = check[
            "name"
        ]

        suggestion = (
            suggestion_messages.get(
                name
            )
        )

        if (
            suggestion
            and suggestion not in seen
        ):
            seen.add(
                suggestion
            )

            suggestions.append(
                {
                    "priority": (
                        check[
                            "severity"
                        ]
                    ),
                    "related_check": name,
                    "suggestion": suggestion,
                }
            )

    return suggestions


# ---------------------------------------------------------------------------
# ANALYSIS LIMITATIONS
# ---------------------------------------------------------------------------

def build_limitations():
    return [
        (
            "The ATS Readiness Score estimates "
            "text extraction and structural "
            "readability. It does not reproduce "
            "the proprietary scoring algorithm "
            "of any specific applicant tracking "
            "system."
        ),
        (
            "Checks based only on extracted text "
            "cannot reliably detect every visual "
            "formatting issue, including complex "
            "columns, tables, text boxes, icons, "
            "headers, footers, or reading-order "
            "problems."
        ),
        (
            "A high ATS Readiness Score does not "
            "guarantee interview selection or "
            "successful ranking for a specific "
            "job."
        ),
    ]


# ---------------------------------------------------------------------------
# MAIN ATS ANALYZER
# ---------------------------------------------------------------------------

def analyze_ats(
    parsed_resume,
):
    if not isinstance(
        parsed_resume,
        dict,
    ):
        raise ValueError(
            "Parsed resume must be a dictionary."
        )

    checks = []

    checks.extend(
        analyze_text_extraction(
            parsed_resume
        )
    )

    checks.extend(
        analyze_contact_information(
            parsed_resume
        )
    )

    checks.extend(
        analyze_core_sections(
            parsed_resume
        )
    )

    checks.extend(
        analyze_supporting_sections(
            parsed_resume
        )
    )

    checks.extend(
        analyze_structure(
            parsed_resume
        )
    )

    checks.append(
        analyze_resume_length(
            parsed_resume
        )
    )

    ats_readiness_score = (
        calculate_ats_score(
            checks
        )
    )

    findings = build_findings(
        checks
    )

    suggestions = (
        build_ats_suggestions(
            checks
        )
    )

    return {
        "ats_readiness_score": (
            ats_readiness_score
        ),

        "readiness_level": (
            get_readiness_level(
                ats_readiness_score
            )
        ),

        "findings": findings,

        "suggestions": suggestions,

        "checks": checks,

        "limitations": (
            build_limitations()
        ),
    }
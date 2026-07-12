import re
from .utils import normalize_text
from .skill_taxonomy import SKILL_ALIASES


# ---------------------------------------------------------------------------
# MATCHING CONFIGURATION
# ---------------------------------------------------------------------------

EVIDENCE_STRENGTH = {
    "experience": 1.00,
    "projects": 0.90,
    "skills": 0.75,
    "certifications": 0.70,
    "summary": 0.50,
    "education": 0.40,
    "achievements": 0.40,
    "preamble": 0.30,
}


REQUIREMENT_WEIGHTS = {
    "required_skills": 1.00,
    "preferred_skills": 0.60,
    "unclassified_skills": 0.80,
}


MATCH_STATUS_VALUE = {
    "matched": 1.00,
    "partial": 0.50,
    "missing": 0.00,
    "not_applicable": None,
    "unable_to_verify": None,
}


# ---------------------------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------------------------

def normalize_text(text):
    if not text:
        return ""

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def contains_term(text, term):
    normalized_text = normalize_text(text)
    normalized_term = normalize_text(term)

    if not normalized_text or not normalized_term:
        return False

    pattern = (
        rf"(?<!\w)"
        rf"{re.escape(normalized_term)}"
        rf"(?!\w)"
    )

    return bool(
        re.search(
            pattern,
            normalized_text,
            flags=re.IGNORECASE,
        )
    )


def add_unique(items, value):
    if value and value not in items:
        items.append(value)


def round_score(value):
    return round(
        max(
            0.0,
            min(
                100.0,
                value,
            ),
        ),
        2,
    )


# ---------------------------------------------------------------------------
# SKILL EVIDENCE
# ---------------------------------------------------------------------------

def get_skill_aliases(skill):
    aliases = SKILL_ALIASES.get(
        skill,
        [],
    )

    all_aliases = [
        skill,
        *aliases,
    ]

    unique_aliases = []

    for alias in all_aliases:
        if alias not in unique_aliases:
            unique_aliases.append(alias)

    return unique_aliases


def skill_exists_in_text(
    text,
    skill,
):
    aliases = get_skill_aliases(
        skill
    )

    return any(
        contains_term(
            text,
            alias,
        )
        for alias in aliases
    )


def find_skill_evidence(
    skill,
    parsed_resume,
):
    evidence = []

    section_content = parsed_resume.get(
        "section_content",
        {},
    )

    for section, content in (
        section_content.items()
    ):
        if not content:
            continue

        if skill_exists_in_text(
            content,
            skill,
        ):
            evidence.append(
                {
                    "section": section,
                    "strength": (
                        EVIDENCE_STRENGTH.get(
                            section,
                            0.40,
                        )
                    ),
                }
            )

    preamble = parsed_resume.get(
        "preamble",
        "",
    )

    if (
        preamble
        and skill_exists_in_text(
            preamble,
            skill,
        )
    ):
        evidence.append(
            {
                "section": "preamble",
                "strength": (
                    EVIDENCE_STRENGTH[
                        "preamble"
                    ]
                ),
            }
        )

    evidence.sort(
        key=lambda item: item[
            "strength"
        ],
        reverse=True,
    )

    return evidence


def get_evidence_level(evidence):
    if not evidence:
        return "none"

    strongest = evidence[0][
        "strength"
    ]

    if strongest >= 0.90:
        return "strong"

    if strongest >= 0.70:
        return "moderate"

    return "limited"


def classify_skill_match(
    skill,
    parsed_resume,
):
    evidence = find_skill_evidence(
        skill,
        parsed_resume,
    )

    if not evidence:
        return {
            "skill": skill,
            "status": "missing",
            "evidence_level": "none",
            "evidence": [],
        }

    strongest_evidence = evidence[0][
        "strength"
    ]

    if strongest_evidence >= 0.70:
        status = "matched"

    else:
        status = "partial"

    return {
        "skill": skill,
        "status": status,
        "evidence_level": (
            get_evidence_level(
                evidence
            )
        ),
        "evidence": evidence,
    }


# ---------------------------------------------------------------------------
# SKILL REQUIREMENT MATCHING
# ---------------------------------------------------------------------------

def analyze_skill_group(
    skills,
    group_name,
    parsed_resume,
):
    results = []

    for skill in skills:
        result = classify_skill_match(
            skill,
            parsed_resume,
        )

        result[
            "requirement_type"
        ] = group_name

        results.append(
            result
        )

    return results


def analyze_skills(
    parsed_resume,
    parsed_job,
):
    job_skills = parsed_job.get(
        "skills",
        {},
    )

    required = analyze_skill_group(
        job_skills.get(
            "required",
            [],
        ),
        "required",
        parsed_resume,
    )

    preferred = analyze_skill_group(
        job_skills.get(
            "preferred",
            [],
        ),
        "preferred",
        parsed_resume,
    )

    unclassified = analyze_skill_group(
        job_skills.get(
            "unclassified",
            [],
        ),
        "unclassified",
        parsed_resume,
    )

    all_results = (
        required
        + preferred
        + unclassified
    )

    matched = [
        item
        for item in all_results
        if item["status"]
        == "matched"
    ]

    partial = [
        item
        for item in all_results
        if item["status"]
        == "partial"
    ]

    missing = [
        item
        for item in all_results
        if item["status"]
        == "missing"
    ]

    return {
        "required": required,
        "preferred": preferred,
        "unclassified": (
            unclassified
        ),
        "matched": matched,
        "partial": partial,
        "missing": missing,
    }


def calculate_skill_component(
    skill_analysis,
):
    weighted_earned = 0.0
    weighted_possible = 0.0

    group_mapping = {
        "required": (
            REQUIREMENT_WEIGHTS[
                "required_skills"
            ]
        ),
        "preferred": (
            REQUIREMENT_WEIGHTS[
                "preferred_skills"
            ]
        ),
        "unclassified": (
            REQUIREMENT_WEIGHTS[
                "unclassified_skills"
            ]
        ),
    }

    for group, weight in (
        group_mapping.items()
    ):
        for result in skill_analysis.get(
            group,
            [],
        ):
            weighted_possible += weight

            status_value = (
                MATCH_STATUS_VALUE[
                    result["status"]
                ]
            )

            weighted_earned += (
                status_value
                * weight
            )

    if weighted_possible == 0:
        return None

    return (
        weighted_earned
        / weighted_possible
    )


# ---------------------------------------------------------------------------
# EXPERIENCE REQUIREMENT MATCHING
# ---------------------------------------------------------------------------

def extract_resume_experience_years(
    parsed_resume,
):
    experience_text = (
        parsed_resume.get(
            "section_content",
            {},
        ).get(
            "experience",
            "",
        )
    )

    if not experience_text:
        return None

    patterns = [
        r"(\d+)\s*\+\s*years?",
        r"(\d+)\s*-\s*(\d+)\s+years?",
        r"(\d+)\s+to\s+(\d+)\s+years?",
    ]

    detected_years = []

    normalized_text = normalize_text(
        experience_text
    )

    for pattern in patterns:
        matches = re.finditer(
            pattern,
            normalized_text,
            flags=re.IGNORECASE,
        )

        for match in matches:
            groups = match.groups()

            numeric_values = [
                int(value)
                for value in groups
                if value is not None
            ]

            detected_years.extend(
                numeric_values
            )

    if not detected_years:
        return None

    return max(
        detected_years
    )


def analyze_experience_requirement(
    parsed_resume,
    parsed_job,
):
    job_experience = parsed_job.get(
        "experience",
        {},
    )

    minimum_years = (
        job_experience.get(
            "minimum_years"
        )
    )

    entry_level = (
        job_experience.get(
            "entry_level",
            False,
        )
    )

    has_requirement = bool(
        job_experience.get(
            "requirements"
        )
        or entry_level
        or minimum_years is not None
    )

    if not has_requirement:
        return {
            "applicable": False,
            "status": (
                "not_applicable"
            ),
            "required_minimum_years": (
                None
            ),
            "detected_resume_years": (
                None
            ),
            "message": (
                "No explicit experience "
                "requirement was detected "
                "in the job description."
            ),
        }

    if entry_level and (
        minimum_years is None
        or minimum_years == 0
    ):
        return {
            "applicable": True,
            "status": "matched",
            "required_minimum_years": 0,
            "detected_resume_years": (
                extract_resume_experience_years(
                    parsed_resume
                )
            ),
            "message": (
                "The job description "
                "indicates an entry-level "
                "or fresher opportunity."
            ),
        }

    resume_years = (
        extract_resume_experience_years(
            parsed_resume
        )
    )

    if resume_years is None:
        return {
            "applicable": True,
            "status": (
                "unable_to_verify"
            ),
            "required_minimum_years": (
                minimum_years
            ),
            "detected_resume_years": (
                None
            ),
            "message": (
                "An experience requirement "
                "was detected, but the "
                "resume does not provide "
                "enough reliable information "
                "to verify total years."
            ),
        }

    if (
        minimum_years is not None
        and resume_years
        >= minimum_years
    ):
        status = "matched"

    else:
        status = "missing"

    return {
        "applicable": True,
        "status": status,
        "required_minimum_years": (
            minimum_years
        ),
        "detected_resume_years": (
            resume_years
        ),
        "message": (
            "Experience requirement "
            "comparison completed using "
            "explicitly detected years."
        ),
    }


# ---------------------------------------------------------------------------
# EDUCATION MATCHING
# ---------------------------------------------------------------------------

def resume_contains_any_term(
    text,
    terms,
):
    return any(
        contains_term(
            text,
            term,
        )
        for term in terms
    )


def analyze_education_requirement(
    parsed_resume,
    parsed_job,
):
    job_education = parsed_job.get(
        "education",
        {},
    )

    if not job_education.get(
        "required",
        False,
    ):
        return {
            "applicable": False,
            "status": (
                "not_applicable"
            ),
            "matched_degrees": [],
            "matched_fields": [],
            "message": (
                "No explicit education "
                "requirement was detected."
            ),
        }

    resume_education = (
        parsed_resume.get(
            "section_content",
            {},
        ).get(
            "education",
            "",
        )
    )

    if not resume_education:
        return {
            "applicable": True,
            "status": "missing",
            "matched_degrees": [],
            "matched_fields": [],
            "message": (
                "The job description "
                "contains an education "
                "requirement, but no "
                "education section was "
                "detected in the resume."
            ),
        }

    required_degrees = (
        job_education.get(
            "degrees",
            [],
        )
    )

    required_fields = (
        job_education.get(
            "fields",
            [],
        )
    )

    degree_terms = {
        "bachelor": [
            "bachelor",
            "b.tech",
            "btech",
            "b.e",
            "b.e.",
            "b.s",
            "bs degree",
        ],

        "master": [
            "master",
            "m.tech",
            "mtech",
            "m.e",
            "m.e.",
            "m.s",
            "ms degree",
        ],

        "phd": [
            "phd",
            "ph.d",
            "doctorate",
        ],
    }

    field_terms = {
        "computer_science": [
            "computer science",
            "computer engineering",
        ],

        "information_technology": [
            "information technology",
            "information systems",
        ],

        "software_engineering": [
            "software engineering",
        ],

        "electronics": [
            "electronics",
            "electronics and communication",
            "electronics and communications",
        ],

        "engineering": [
            "engineering",
        ],

        "data_science": [
            "data science",
            "data analytics",
        ],

        "mathematics": [
            "mathematics",
            "statistics",
        ],

        "business": [
            "business administration",
            "business management",
            "mba",
        ],
    }

    matched_degrees = []

    for degree in required_degrees:
        terms = degree_terms.get(
            degree,
            [degree],
        )

        if resume_contains_any_term(
            resume_education,
            terms,
        ):
            add_unique(
                matched_degrees,
                degree,
            )

    matched_fields = []

    for field in required_fields:
        terms = field_terms.get(
            field,
            [field],
        )

        if resume_contains_any_term(
            resume_education,
            terms,
        ):
            add_unique(
                matched_fields,
                field,
            )

    degree_match = (
        not required_degrees
        or bool(matched_degrees)
    )

    field_match = (
        not required_fields
        or bool(matched_fields)
    )

    if (
        degree_match
        and field_match
    ):
        status = "matched"

    elif (
        degree_match
        or field_match
    ):
        status = "partial"

    else:
        status = "missing"

    return {
        "applicable": True,
        "status": status,
        "matched_degrees": (
            matched_degrees
        ),
        "matched_fields": (
            matched_fields
        ),
        "message": (
            "Education was compared only "
            "because an explicit education "
            "requirement was detected."
        ),
    }


# ---------------------------------------------------------------------------
# CERTIFICATION MATCHING
# ---------------------------------------------------------------------------

def analyze_certification_requirement(
    parsed_resume,
    parsed_job,
):
    job_certifications = (
        parsed_job.get(
            "certifications",
            {},
        ).get(
            "certifications",
            [],
        )
    )

    if not job_certifications:
        return {
            "applicable": False,
            "status": (
                "not_applicable"
            ),
            "matched": [],
            "missing": [],
            "message": (
                "No recognized "
                "certification requirement "
                "was detected."
            ),
        }

    certification_text = (
        parsed_resume.get(
            "section_content",
            {},
        ).get(
            "certifications",
            "",
        )
    )

    matched = []
    missing = []

    for certification in (
        job_certifications
    ):
        if contains_term(
            certification_text,
            certification,
        ):
            add_unique(
                matched,
                certification,
            )

        else:
            add_unique(
                missing,
                certification,
            )

    if (
        matched
        and not missing
    ):
        status = "matched"

    elif matched:
        status = "partial"

    else:
        status = "missing"

    return {
        "applicable": True,
        "status": status,
        "matched": matched,
        "missing": missing,
        "message": (
            "Recognized certification "
            "requirements were compared "
            "with the resume."
        ),
    }


# ---------------------------------------------------------------------------
# COMPONENT SCORING
# ---------------------------------------------------------------------------

def status_to_component_value(
    analysis_result,
):
    if not analysis_result.get(
        "applicable",
        False,
    ):
        return None

    status = analysis_result.get(
        "status"
    )

    return MATCH_STATUS_VALUE.get(
        status
    )


def calculate_dynamic_score(
    skill_component,
    experience_component,
    education_component,
    certification_component,
):
    components = []

    if skill_component is not None:
        components.append(
            {
                "name": "skills",
                "value": (
                    skill_component
                ),
                "base_weight": 0.60,
            }
        )

    if experience_component is not None:
        components.append(
            {
                "name": "experience",
                "value": (
                    experience_component
                ),
                "base_weight": 0.20,
            }
        )

    if education_component is not None:
        components.append(
            {
                "name": "education",
                "value": (
                    education_component
                ),
                "base_weight": 0.10,
            }
        )

    if certification_component is not None:
        components.append(
            {
                "name": (
                    "certifications"
                ),
                "value": (
                    certification_component
                ),
                "base_weight": 0.10,
            }
        )

    if not components:
        return {
            "score": None,
            "components_used": [],
            "score_status": "unable_to_score",
    }

    total_weight = sum(
        component[
            "base_weight"
        ]
        for component in components
    )

    weighted_score = 0.0
    components_used = []

    for component in components:
        normalized_weight = (
            component[
                "base_weight"
            ]
            / total_weight
        )

        weighted_score += (
            component["value"]
            * normalized_weight
        )

        components_used.append(
            component["name"]
        )

    return {
    "score": round_score(
        weighted_score
        * 100
    ),
    "components_used": (
        components_used
    ),
    "score_status": "scored",
}


# ---------------------------------------------------------------------------
# MATCH STATUS
# ---------------------------------------------------------------------------
def get_match_level(score):
    if score is None:
        return "unable_to_score"

    if score >= 85:
        return "strong_match"

    if score >= 70:
        return "good_match"

    if score >= 50:
        return "moderate_match"

    return "low_match"


# ---------------------------------------------------------------------------
# SUMMARY FINDINGS
# ---------------------------------------------------------------------------

def build_match_findings(
    skill_analysis,
    experience_analysis,
    education_analysis,
    certification_analysis,
):
    findings = []

    for item in skill_analysis[
        "matched"
    ]:
        findings.append(
            {
                "type": "matched_skill",
                "priority": "positive",
                "skill": item["skill"],
                "message": (
                    f"{item['skill']} was "
                    f"found with "
                    f"{item['evidence_level']} "
                    f"resume evidence."
                ),
            }
        )

    for item in skill_analysis[
        "partial"
    ]:
        findings.append(
            {
                "type": (
                    "partial_skill"
                ),
                "priority": "medium",
                "skill": item["skill"],
                "message": (
                    f"{item['skill']} was "
                    f"found only with limited "
                    f"resume evidence."
                ),
            }
        )

    for item in skill_analysis[
        "missing"
    ]:
        priority = (
            "high"
            if item[
                "requirement_type"
            ] == "required"
            else "medium"
        )

        findings.append(
            {
                "type": (
                    "missing_skill"
                ),
                "priority": priority,
                "skill": item["skill"],
                "message": (
                    f"No clear evidence of "
                    f"{item['skill']} was "
                    f"found in the resume."
                ),
            }
        )

    for name, result in [
        (
            "experience",
            experience_analysis,
        ),
        (
            "education",
            education_analysis,
        ),
        (
            "certification",
            certification_analysis,
        ),
    ]:
        if (
            result.get("applicable")
            and result.get("status")
            not in [
                "matched",
                "not_applicable",
            ]
        ):
            findings.append(
                {
                    "type": (
                        f"{name}_requirement"
                    ),
                    "priority": "high",
                    "message": result[
                        "message"
                    ],
                }
            )

    return findings


# ---------------------------------------------------------------------------
# MAIN RESUME MATCH ANALYZER
# ---------------------------------------------------------------------------

def analyze_resume_match(
    parsed_resume,
    parsed_job,
):
    skill_analysis = analyze_skills(
        parsed_resume,
        parsed_job,
    )

    experience_analysis = (
        analyze_experience_requirement(
            parsed_resume,
            parsed_job,
        )
    )

    education_analysis = (
        analyze_education_requirement(
            parsed_resume,
            parsed_job,
        )
    )

    certification_analysis = (
        analyze_certification_requirement(
            parsed_resume,
            parsed_job,
        )
    )

    skill_component = (
        calculate_skill_component(
            skill_analysis
        )
    )

    experience_component = (
        status_to_component_value(
            experience_analysis
        )
    )

    education_component = (
        status_to_component_value(
            education_analysis
        )
    )

    certification_component = (
        status_to_component_value(
            certification_analysis
        )
    )

    score_result = (
        calculate_dynamic_score(
            skill_component,
            experience_component,
            education_component,
            certification_component,
        )
    )

    resume_match_score = (
        score_result["score"]
    )

    findings = build_match_findings(
        skill_analysis,
        experience_analysis,
        education_analysis,
        certification_analysis,
    )

    return {
        "resume_match_score": (
            resume_match_score
        ),

        "match_level": get_match_level(
            resume_match_score
        ),

        "skills": skill_analysis,

        "experience": (
            experience_analysis
        ),

        "education": (
            education_analysis
        ),

        "certifications": (
            certification_analysis
        ),

        "findings": findings,

        "scoring_metadata": {
            "components_used": (
                score_result[
                    "components_used"
                ]
            ),
        },
    }

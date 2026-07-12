import re

from .skill_taxonomy import SKILL_ALIASES
from .utils import normalize_text


# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

GENERIC_JOB_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "that",
    "the",
    "their",
    "this",
    "to",
    "we",
    "will",
    "with",
    "you",
    "your",
    "looking",
    "seeking",
    "candidate",
    "candidates",
    "applicant",
    "applicants",
    "role",
    "position",
    "job",
    "team",
    "company",
    "organization",
    "work",
    "working",
    "include",
    "includes",
    "including",
    "nice",
    "would",
    "computer",
    "degree",
    "field",
    "hiring",
    "least",
    "must",
    "related",
    "science",
    "years",
    "exciting",
    "join",
    "motivated",
}


GENERIC_RECRUITING_TERMS = {
    "developer",
    "engineer",
    "experience",
    "experienced",
    "knowledge",
    "skills",
    "skill",
    "ability",
    "responsible",
    "responsibilities",
    "requirement",
    "requirements",
    "required",
    "preferred",
    "qualification",
    "qualifications",
    "strong",
    "good",
    "excellent",
}


ACTION_KEYWORDS = {
    "develop",
    "developed",
    "build",
    "built",
    "design",
    "designed",
    "implement",
    "implemented",
    "create",
    "created",
    "maintain",
    "maintained",
    "manage",
    "managed",
    "analyze",
    "analyzed",
    "analyse",
    "analysed",
    "optimize",
    "optimized",
    "improve",
    "improved",
    "integrate",
    "integrated",
    "deploy",
    "deployed",
    "test",
    "tested",
    "collaborate",
    "collaborated",
    "automate",
    "automated",
    "troubleshoot",
    "troubleshooting",
}


# ---------------------------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------------------------

def add_unique(items, value):
    if value and value not in items:
        items.append(value)


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


def tokenize(text):
    normalized_text = normalize_text(text)

    tokens = re.findall(
        r"[a-zA-Z][a-zA-Z0-9+#]*(?:[./-][a-zA-Z0-9+#]+)*",
        normalized_text,
    )

    return [
        token.strip("./-")
        for token in tokens
        if token.strip("./-")
    ]


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
        contains_term(
            text,
            alias,
        )
        for alias in get_skill_aliases(
            skill
        )
    )


# ---------------------------------------------------------------------------
# TECHNICAL KEYWORD ANALYSIS
# ---------------------------------------------------------------------------

def analyze_technical_keywords(
    resume_text,
    parsed_job,
):
    job_skills = parsed_job.get(
        "skills",
        {},
    )

    required_skills = job_skills.get(
        "required",
        [],
    )

    preferred_skills = job_skills.get(
        "preferred",
        [],
    )

    unclassified_skills = job_skills.get(
        "unclassified",
        [],
    )

    matched_required = []
    missing_required = []

    matched_preferred = []
    missing_preferred = []

    matched_unclassified = []
    missing_unclassified = []

    for skill in required_skills:
        if skill_exists_in_text(
            resume_text,
            skill,
        ):
            add_unique(
                matched_required,
                skill,
            )
        else:
            add_unique(
                missing_required,
                skill,
            )

    for skill in preferred_skills:
        if skill_exists_in_text(
            resume_text,
            skill,
        ):
            add_unique(
                matched_preferred,
                skill,
            )
        else:
            add_unique(
                missing_preferred,
                skill,
            )

    for skill in unclassified_skills:
        if skill_exists_in_text(
            resume_text,
            skill,
        ):
            add_unique(
                matched_unclassified,
                skill,
            )
        else:
            add_unique(
                missing_unclassified,
                skill,
            )

    return {
        "required": {
            "matched": matched_required,
            "missing": missing_required,
        },

        "preferred": {
            "matched": matched_preferred,
            "missing": missing_preferred,
        },

        "unclassified": {
            "matched": matched_unclassified,
            "missing": missing_unclassified,
        },
    }


# ---------------------------------------------------------------------------
# ACTION KEYWORD ANALYSIS
# ---------------------------------------------------------------------------

def extract_job_action_keywords(
    job_description,
):
    detected_actions = []

    for keyword in ACTION_KEYWORDS:
        if contains_term(
            job_description,
            keyword,
        ):
            add_unique(
                detected_actions,
                keyword,
            )

    return detected_actions


def analyze_action_keywords(
    resume_text,
    job_description,
):
    job_actions = (
        extract_job_action_keywords(
            job_description
        )
    )

    matched = []
    missing = []

    for action in job_actions:
        if contains_term(
            resume_text,
            action,
        ):
            add_unique(
                matched,
                action,
            )
        else:
            add_unique(
                missing,
                action,
            )

    return {
        "job_actions": job_actions,
        "matched": matched,
        "missing": missing,
    }


# ---------------------------------------------------------------------------
# IMPORTANT NON-SKILL TERMS
# ---------------------------------------------------------------------------

def extract_relevant_terms(
    job_description,
):
    tokens = tokenize(
        job_description
    )

    frequencies = {}

    for token in tokens:
        normalized_token = (
            token.lower()
        )

        if len(normalized_token) < 3:
            continue

        if (
            normalized_token
            in GENERIC_JOB_WORDS
        ):
            continue

        if (
            normalized_token
            in GENERIC_RECRUITING_TERMS
        ):
            continue

        if (
            normalized_token
            in ACTION_KEYWORDS
        ):
            continue

        frequencies[
            normalized_token
        ] = (
            frequencies.get(
                normalized_token,
                0,
            )
            + 1
        )

    sorted_terms = sorted(
        frequencies.items(),
        key=lambda item: (
            -item[1],
            item[0],
        ),
    )

    return [
        term
        for term, _ in sorted_terms
    ]


def remove_skill_related_terms(
    terms,
    parsed_job,
):
    all_job_skills = (
        parsed_job.get(
            "skills",
            {},
        ).get(
            "all",
            [],
        )
    )

    skill_terms = set()

    for skill in all_job_skills:
        for alias in get_skill_aliases(
            skill
        ):
            for token in tokenize(
                alias
            ):
                skill_terms.add(
                    token.lower()
                )

    return [
        term
        for term in terms
        if term not in skill_terms
    ]


def analyze_relevant_terms(
    resume_text,
    job_description,
    parsed_job,
):
    relevant_terms = (
        extract_relevant_terms(
            job_description
        )
    )

    relevant_terms = (
        remove_skill_related_terms(
            relevant_terms,
            parsed_job,
        )
    )

    matched = []
    missing = []

    for term in relevant_terms:
        if contains_term(
            resume_text,
            term,
        ):
            add_unique(
                matched,
                term,
            )
        else:
            add_unique(
                missing,
                term,
            )

    return {
        "matched": matched,
        "missing": missing,
    }


# ---------------------------------------------------------------------------
# KEYWORD SUGGESTIONS
# ---------------------------------------------------------------------------

def build_keyword_suggestions(
    technical_analysis,
    action_analysis,
    relevant_term_analysis,
):
    suggestions = []

    for skill in technical_analysis[
        "required"
    ][
        "missing"
    ]:
        suggestions.append(
            {
                "type": "required_skill",
                "priority": "high",
                "keyword": skill,
                "suggestion": (
                    f"The job description "
                    f"requires {skill}. Add it "
                    f"only if you genuinely "
                    f"have this skill and can "
                    f"support it with evidence."
                ),
            }
        )

    for skill in technical_analysis[
        "preferred"
    ][
        "missing"
    ]:
        suggestions.append(
            {
                "type": (
                    "preferred_skill"
                ),
                "priority": "medium",
                "keyword": skill,
                "suggestion": (
                    f"{skill} appears as a "
                    f"preferred skill. Include "
                    f"it only if it accurately "
                    f"reflects your experience."
                ),
            }
        )

    for skill in technical_analysis[
        "unclassified"
    ][
        "missing"
    ]:
        suggestions.append(
            {
                "type": (
                    "relevant_skill"
                ),
                "priority": "medium",
                "keyword": skill,
                "suggestion": (
                    f"{skill} is relevant to "
                    f"the job description. "
                    f"Consider mentioning it "
                    f"where appropriate only "
                    f"if you actually have "
                    f"experience with it."
                ),
            }
        )

    if action_analysis[
        "missing"
    ]:
        suggestions.append(
            {
                "type": (
                    "action_language"
                ),
                "priority": "low",
                "keywords": (
                    action_analysis[
                        "missing"
                    ][:5]
                ),
                "suggestion": (
                    "Where truthful and "
                    "natural, describe relevant "
                    "work using clear action "
                    "language aligned with the "
                    "job responsibilities."
                ),
            }
        )

    important_missing_terms = (
        relevant_term_analysis[
            "missing"
        ][:5]
    )

    if important_missing_terms:
        suggestions.append(
            {
                "type": (
                    "contextual_terms"
                ),
                "priority": "low",
                "keywords": (
                    important_missing_terms
                ),
                "suggestion": (
                    "Review these recurring "
                    "job-description terms and "
                    "use them naturally only "
                    "where they accurately "
                    "describe your background."
                ),
            }
        )

    return suggestions


# ---------------------------------------------------------------------------
# KEYWORD COVERAGE SUMMARY
# ---------------------------------------------------------------------------

def build_keyword_summary(
    technical_analysis,
):
    matched = []
    missing = []

    for group in [
        "required",
        "preferred",
        "unclassified",
    ]:
        for skill in technical_analysis[
            group
        ][
            "matched"
        ]:
            add_unique(
                matched,
                skill,
            )

        for skill in technical_analysis[
            group
        ][
            "missing"
        ]:
            add_unique(
                missing,
                skill,
            )

    return {
        "matched_skills": matched,
        "missing_skills": missing,
    }


# ---------------------------------------------------------------------------
# MAIN KEYWORD ANALYZER
# ---------------------------------------------------------------------------

def analyze_keywords(
    resume_text,
    job_description,
    parsed_job,
):
    if not isinstance(
        resume_text,
        str,
    ):
        raise ValueError(
            "Resume content must be text."
        )

    if not isinstance(
        job_description,
        str,
    ):
        raise ValueError(
            "Job description must be text."
        )

    if not resume_text.strip():
        raise ValueError(
            "Resume text cannot be empty."
        )

    if not job_description.strip():
        raise ValueError(
            "Job description cannot be empty."
        )

    technical_analysis = (
        analyze_technical_keywords(
            resume_text,
            parsed_job,
        )
    )

    action_analysis = (
        analyze_action_keywords(
            resume_text,
            job_description,
        )
    )

    relevant_term_analysis = (
        analyze_relevant_terms(
            resume_text,
            job_description,
            parsed_job,
        )
    )

    suggestions = (
        build_keyword_suggestions(
            technical_analysis,
            action_analysis,
            relevant_term_analysis,
        )
    )

    summary = build_keyword_summary(
        technical_analysis
    )

    return {
        "summary": summary,

        "technical_keywords": (
            technical_analysis
        ),

        "action_keywords": (
            action_analysis
        ),

        "contextual_terms": (
            relevant_term_analysis
        ),

        "suggestions": suggestions,
    }
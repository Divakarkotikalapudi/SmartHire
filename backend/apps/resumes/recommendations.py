# ---------------------------------------------------------------------------
# RECOMMENDATION CONFIGURATION
# ---------------------------------------------------------------------------

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


CATEGORY_ORDER = {
    "ats": 0,
    "required_skill": 1,
    "experience": 2,
    "education": 3,
    "certification": 4,
    "preferred_skill": 5,
    "relevant_skill": 6,
    "keyword": 7,
    "content": 8,
}


# ---------------------------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------------------------

def normalize_priority(priority):
    if priority in PRIORITY_ORDER:
        return priority

    return "medium"


def create_recommendation(
    category,
    priority,
    title,
    message,
    action,
    related_item=None,
    evidence=None,
):
    return {
        "category": category,
        "priority": normalize_priority(
            priority
        ),
        "title": title,
        "message": message,
        "action": action,
        "related_item": related_item,
        "evidence": evidence or [],
    }


def recommendation_key(
    recommendation,
):
    return (
        recommendation.get(
            "category",
            "",
        ).lower(),
        str(
            recommendation.get(
                "related_item",
                "",
            )
        ).lower(),
        recommendation.get(
            "title",
            "",
        ).lower(),
    )


def add_unique_recommendation(
    recommendations,
    recommendation,
    seen,
):
    key = recommendation_key(
        recommendation
    )

    if key not in seen:
        seen.add(key)

        recommendations.append(
            recommendation
        )


# ---------------------------------------------------------------------------
# ATS RECOMMENDATIONS
# ---------------------------------------------------------------------------

def build_ats_recommendations(
    ats_analysis,
):
    recommendations = []

    for suggestion in ats_analysis.get(
        "suggestions",
        [],
    ):
        related_check = suggestion.get(
            "related_check"
        )

        priority = suggestion.get(
            "priority",
            "medium",
        )

        message = suggestion.get(
            "suggestion",
            "",
        )

        title_mapping = {
            "text_extraction": (
                "Improve resume text extraction"
            ),

            "meaningful_content": (
                "Improve extractable resume content"
            ),

            "email": (
                "Add a detectable email address"
            ),

            "phone": (
                "Add a detectable phone number"
            ),

            "skills": (
                "Use a clear Skills section"
            ),

            "experience": (
                "Use a clear Experience section"
            ),

            "education": (
                "Use a clear Education section"
            ),

            "recognizable_structure": (
                "Improve resume structure"
            ),

            "resume_length": (
                "Review resume content length"
            ),
        }

        title = title_mapping.get(
            related_check,
            "Improve ATS readability",
        )

        recommendations.append(
            create_recommendation(
                category="ats",
                priority=priority,
                title=title,
                message=message,
                action=message,
                related_item=related_check,
            )
        )

    return recommendations


# ---------------------------------------------------------------------------
# SKILL RECOMMENDATIONS
# ---------------------------------------------------------------------------

def build_skill_recommendations(
    match_analysis,
):
    recommendations = []

    skill_analysis = match_analysis.get(
        "skills",
        {},
    )

    for item in skill_analysis.get(
        "required",
        [],
    ):
        if item.get("status") == "missing":
            skill = item.get(
                "skill"
            )

            recommendations.append(
                create_recommendation(
                    category=(
                        "required_skill"
                    ),
                    priority="high",
                    title=(
                        f"Address the required "
                        f"skill: {skill}"
                    ),
                    message=(
                        f"The job description "
                        f"identifies {skill} as a "
                        f"required skill, but no "
                        f"clear evidence was found "
                        f"in the resume."
                    ),
                    action=(
                        f"If you genuinely have "
                        f"experience with {skill}, "
                        f"show it in the most "
                        f"relevant Skills, Project, "
                        f"or Experience entry. "
                        f"Do not add it if you "
                        f"cannot support the claim."
                    ),
                    related_item=skill,
                )
            )

        elif item.get(
            "status"
        ) == "partial":
            skill = item.get(
                "skill"
            )

            recommendations.append(
                create_recommendation(
                    category=(
                        "required_skill"
                    ),
                    priority="high",
                    title=(
                        f"Strengthen evidence for "
                        f"{skill}"
                    ),
                    message=(
                        f"{skill} appears in the "
                        f"resume, but the available "
                        f"evidence is limited."
                    ),
                    action=(
                        f"If accurate, demonstrate "
                        f"how you used {skill} in a "
                        f"project, internship, or "
                        f"work experience instead "
                        f"of only listing the term."
                    ),
                    related_item=skill,
                    evidence=item.get(
                        "evidence",
                        [],
                    ),
                )
            )

    for item in skill_analysis.get(
        "preferred",
        [],
    ):
        if item.get(
            "status"
        ) == "missing":
            skill = item.get(
                "skill"
            )

            recommendations.append(
                create_recommendation(
                    category=(
                        "preferred_skill"
                    ),
                    priority="medium",
                    title=(
                        f"Review the preferred "
                        f"skill: {skill}"
                    ),
                    message=(
                        f"{skill} was identified "
                        f"as a preferred skill, but "
                        f"no clear resume evidence "
                        f"was found."
                    ),
                    action=(
                        f"Include {skill} only if "
                        f"you genuinely have the "
                        f"skill. When possible, "
                        f"support it with a concrete "
                        f"example."
                    ),
                    related_item=skill,
                )
            )

    for item in skill_analysis.get(
        "unclassified",
        [],
    ):
        if item.get(
            "status"
        ) == "missing":
            skill = item.get(
                "skill"
            )

            recommendations.append(
                create_recommendation(
                    category=(
                        "relevant_skill"
                    ),
                    priority="medium",
                    title=(
                        f"Review job-relevant "
                        f"skill: {skill}"
                    ),
                    message=(
                        f"{skill} appears relevant "
                        f"to the job description, "
                        f"but the employer's exact "
                        f"requirement level was not "
                        f"clear."
                    ),
                    action=(
                        f"If {skill} accurately "
                        f"reflects your background, "
                        f"mention it naturally with "
                        f"supporting evidence."
                    ),
                    related_item=skill,
                )
            )

    return recommendations


# ---------------------------------------------------------------------------
# EXPERIENCE RECOMMENDATIONS
# ---------------------------------------------------------------------------

def build_experience_recommendations(
    match_analysis,
):
    recommendations = []

    experience = match_analysis.get(
        "experience",
        {},
    )

    if not experience.get(
        "applicable",
        False,
    ):
        return recommendations

    status = experience.get(
        "status"
    )

    required_years = experience.get(
        "required_minimum_years"
    )

    if status == "missing":
        recommendations.append(
            create_recommendation(
                category="experience",
                priority="high",
                title=(
                    "Review the experience requirement"
                ),
                message=(
                    "The resume does not appear "
                    "to satisfy the explicitly "
                    "detected experience "
                    "requirement."
                ),
                action=(
                    "Do not inflate years of "
                    "experience. Instead, present "
                    "relevant internships, projects, "
                    "freelance work, or professional "
                    "experience accurately and "
                    "clearly."
                ),
                related_item=(
                    required_years
                ),
            )
        )

    elif status == "unable_to_verify":
        recommendations.append(
            create_recommendation(
                category="experience",
                priority="medium",
                title=(
                    "Clarify relevant experience"
                ),
                message=(
                    "The job description contains "
                    "an experience requirement, "
                    "but the resume does not "
                    "provide enough reliable "
                    "information to verify it."
                ),
                action=(
                    "Use clear organization or "
                    "project names, role titles, "
                    "and dates where applicable. "
                    "Keep all dates and experience "
                    "claims accurate."
                ),
                related_item=(
                    required_years
                ),
            )
        )

    return recommendations


# ---------------------------------------------------------------------------
# EDUCATION RECOMMENDATIONS
# ---------------------------------------------------------------------------

def build_education_recommendations(
    match_analysis,
):
    recommendations = []

    education = match_analysis.get(
        "education",
        {},
    )

    if not education.get(
        "applicable",
        False,
    ):
        return recommendations

    status = education.get(
        "status"
    )

    if status == "missing":
        recommendations.append(
            create_recommendation(
                category="education",
                priority="high",
                title=(
                    "Review the education requirement"
                ),
                message=(
                    "The job description contains "
                    "an education requirement that "
                    "was not clearly matched in "
                    "the resume."
                ),
                action=(
                    "Verify that your actual degree, "
                    "field of study, institution, "
                    "and education status are "
                    "clearly stated. Do not claim "
                    "a qualification you do not "
                    "hold."
                ),
                related_item="education",
            )
        )

    elif status == "partial":
        recommendations.append(
            create_recommendation(
                category="education",
                priority="medium",
                title=(
                    "Clarify education alignment"
                ),
                message=(
                    "The resume partially matches "
                    "the detected education "
                    "requirement."
                ),
                action=(
                    "Make your actual degree and "
                    "field of study explicit so "
                    "the qualification can be "
                    "interpreted correctly."
                ),
                related_item="education",
            )
        )

    return recommendations


# ---------------------------------------------------------------------------
# CERTIFICATION RECOMMENDATIONS
# ---------------------------------------------------------------------------

def build_certification_recommendations(
    match_analysis,
):
    recommendations = []

    certification = (
        match_analysis.get(
            "certifications",
            {},
        )
    )

    if not certification.get(
        "applicable",
        False,
    ):
        return recommendations

    missing = certification.get(
        "missing",
        [],
    )

    for item in missing:
        recommendations.append(
            create_recommendation(
                category="certification",
                priority="medium",
                title=(
                    f"Review certification "
                    f"requirement: {item}"
                ),
                message=(
                    f"The job description "
                    f"mentions {item}, but it "
                    f"was not detected in the "
                    f"resume."
                ),
                action=(
                    f"Add {item} only if you "
                    f"actually hold the "
                    f"certification. Otherwise, "
                    f"do not claim it."
                ),
                related_item=item,
            )
        )

    return recommendations


# ---------------------------------------------------------------------------
# KEYWORD RECOMMENDATIONS
# ---------------------------------------------------------------------------

def build_keyword_recommendations(
    keyword_analysis,
):
    recommendations = []

    for suggestion in keyword_analysis.get(
        "suggestions",
        [],
    ):
        suggestion_type = suggestion.get(
            "type"
        )

        # Skill recommendations are already
        # handled using the evidence-based
        # matching analysis. Skipping them here
        # prevents duplicate recommendations.
        if suggestion_type in {
            "required_skill",
            "preferred_skill",
            "relevant_skill",
        }:
            continue

        if suggestion_type == (
            "action_language"
        ):
            keywords = suggestion.get(
                "keywords",
                [],
            )

            recommendations.append(
                create_recommendation(
                    category="keyword",
                    priority="low",
                    title=(
                        "Improve action-oriented wording"
                    ),
                    message=(
                        "Some action language used "
                        "in the job description is "
                        "not reflected in the "
                        "resume."
                    ),
                    action=(
                        "Where truthful and natural, "
                        "describe relevant work with "
                        "clear action verbs. Do not "
                        "copy wording that does not "
                        "describe your actual work."
                    ),
                    related_item=(
                        "action_language"
                    ),
                    evidence=keywords,
                )
            )

        elif suggestion_type == (
            "contextual_terms"
        ):
            keywords = suggestion.get(
                "keywords",
                [],
            )

            recommendations.append(
                create_recommendation(
                    category="keyword",
                    priority="low",
                    title=(
                        "Review important job terminology"
                    ),
                    message=(
                        "Some recurring contextual "
                        "terms from the job "
                        "description were not found "
                        "in the resume."
                    ),
                    action=(
                        "Review these terms and use "
                        "them only where they "
                        "accurately describe your "
                        "skills, projects, or "
                        "experience."
                    ),
                    related_item=(
                        "contextual_terms"
                    ),
                    evidence=keywords,
                )
            )

    return recommendations


# ---------------------------------------------------------------------------
# RECOMMENDATION SORTING
# ---------------------------------------------------------------------------

def sort_recommendations(
    recommendations,
):
    return sorted(
        recommendations,
        key=lambda item: (
            PRIORITY_ORDER.get(
                item.get(
                    "priority"
                ),
                3,
            ),
            CATEGORY_ORDER.get(
                item.get(
                    "category"
                ),
                99,
            ),
            item.get(
                "title",
                "",
            ).lower(),
        ),
    )


# ---------------------------------------------------------------------------
# PRIORITY SUMMARY
# ---------------------------------------------------------------------------

def build_priority_summary(
    recommendations,
):
    summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for recommendation in recommendations:
        priority = recommendation.get(
            "priority",
            "medium",
        )

        if priority in summary:
            summary[priority] += 1

    return summary


# ---------------------------------------------------------------------------
# TOP ACTIONS
# ---------------------------------------------------------------------------

def build_top_actions(
    recommendations,
    limit=5,
):
    return [
        {
            "priority": item[
                "priority"
            ],
            "title": item[
                "title"
            ],
            "action": item[
                "action"
            ],
        }
        for item in recommendations[
            :limit
        ]
    ]


# ---------------------------------------------------------------------------
# MAIN RECOMMENDATION ENGINE
# ---------------------------------------------------------------------------

def generate_recommendations(
    match_analysis,
    ats_analysis,
    keyword_analysis,
):
    if not isinstance(
        match_analysis,
        dict,
    ):
        raise ValueError(
            "Match analysis must be a dictionary."
        )

    if not isinstance(
        ats_analysis,
        dict,
    ):
        raise ValueError(
            "ATS analysis must be a dictionary."
        )

    if not isinstance(
        keyword_analysis,
        dict,
    ):
        raise ValueError(
            "Keyword analysis must be a dictionary."
        )

    collected = []

    collected.extend(
        build_ats_recommendations(
            ats_analysis
        )
    )

    collected.extend(
        build_skill_recommendations(
            match_analysis
        )
    )

    collected.extend(
        build_experience_recommendations(
            match_analysis
        )
    )

    collected.extend(
        build_education_recommendations(
            match_analysis
        )
    )

    collected.extend(
        build_certification_recommendations(
            match_analysis
        )
    )

    collected.extend(
        build_keyword_recommendations(
            keyword_analysis
        )
    )

    recommendations = []
    seen = set()

    for recommendation in collected:
        add_unique_recommendation(
            recommendations,
            recommendation,
            seen,
        )

    recommendations = (
        sort_recommendations(
            recommendations
        )
    )

    return {
        "priority_summary": (
            build_priority_summary(
                recommendations
            )
        ),

        "top_actions": (
            build_top_actions(
                recommendations
            )
        ),

        "all_recommendations": (
            recommendations
        ),
    }
import {
  useEffect,
  useState,
} from "react";

import {
  Link,
  Navigate,
  useLocation,
  useParams,
} from "react-router-dom";

import {
  getAnalysisById,
} from "../api/resumes";

import "./Results.css";


function Results() {
  const location = useLocation();
  const { analysisId } = useParams();

  const stateAnalysisResult =
    location.state?.analysisResult;

  const [
    analysisResult,
    setAnalysisResult,
  ] = useState(
    stateAnalysisResult || null
  );

  const [loading, setLoading] =
    useState(
      !stateAnalysisResult &&
        Boolean(analysisId)
    );

  const [error, setError] =
    useState("");


  useEffect(() => {
    if (
      stateAnalysisResult ||
      !analysisId
    ) {
      return;
    }

    let isMounted = true;

    const loadSavedAnalysis =
      async () => {
        try {
          setLoading(true);
          setError("");

          const savedAnalysis =
            await getAnalysisById(
              analysisId
            );

          if (!isMounted) {
            return;
          }

          if (
            !savedAnalysis
              ?.analysis_result
          ) {
            throw new Error(
              "The saved analysis result is unavailable."
            );
          }

          setAnalysisResult(
            savedAnalysis
              .analysis_result
          );
        } catch (error) {
          if (!isMounted) {
            return;
          }

          setError(
            error.message ||
              "Unable to load this analysis."
          );
        } finally {
          if (isMounted) {
            setLoading(false);
          }
        }
      };

    loadSavedAnalysis();

    return () => {
      isMounted = false;
    };
  }, [
    analysisId,
    stateAnalysisResult,
  ]);


  if (loading) {
    return (
      <div className="results-page">
        <header className="results-navbar">
          <div className="results-nav-container">
            <Link
              to="/"
              className="results-logo"
            >
              SmartHire
            </Link>

            <nav className="results-nav-links">
              <Link
                to="/analyze"
                className="results-nav-link"
              >
                New Analysis
              </Link>

              <Link
                to="/history"
                className="results-account-button"
              >
                History
              </Link>
            </nav>
          </div>
        </header>

        <main className="results-main">
          <section className="results-loading-state">
            <div className="results-loading-spinner" />

            <h1>
              Loading your analysis
            </h1>

            <p>
              Retrieving your saved
              resume analysis.
            </p>
          </section>
        </main>
      </div>
    );
  }


  if (error) {
    return (
      <div className="results-page">
        <header className="results-navbar">
          <div className="results-nav-container">
            <Link
              to="/"
              className="results-logo"
            >
              SmartHire
            </Link>

            <nav className="results-nav-links">
              <Link
                to="/analyze"
                className="results-nav-link"
              >
                New Analysis
              </Link>

              <Link
                to="/history"
                className="results-account-button"
              >
                History
              </Link>
            </nav>
          </div>
        </header>

        <main className="results-main">
          <section className="results-error-state">
            <div className="results-error-icon">
              !
            </div>

            <h1>
              Unable to load analysis
            </h1>

            <p>{error}</p>

            <div className="results-error-actions">
              <Link
                to="/history"
                className="results-error-secondary-button"
              >
                View History
              </Link>

              <Link
                to="/analyze"
                className="results-error-primary-button"
              >
                New Analysis
                <span>→</span>
              </Link>
            </div>
          </section>
        </main>
      </div>
    );
  }


  if (!analysisResult) {
    return (
      <Navigate
        to="/analyze"
        replace
      />
    );
  }


  const {
    resume_name = "Resume",
    scores = {},
    summary = {},
    resume_analysis = {},
    match_analysis = {},
    keyword_analysis = {},
    ats_analysis = {},
    recommendations = {},
  } = analysisResult;


  const atsScore = normalizeScore(
    scores.ats_readiness_score
  );

  const matchScore = normalizeScore(
    scores.resume_match_score
  );


  const atsLevel =
    summary.ats_readiness_level ||
    ats_analysis.readiness_level ||
    "Not available";


  const matchLevel = formatLabel(
    summary.match_level ||
      match_analysis.match_level ||
      "Not available"
  );


  const candidate =
    resume_analysis.candidate || {};

  const contact =
    resume_analysis.contact || {};


  const skills =
    match_analysis.skills || {};


  const matchedSkills =
    Array.isArray(skills.matched)
      ? skills.matched
      : [];


  const partialSkills =
    Array.isArray(skills.partial)
      ? skills.partial
      : [];


  const missingSkills =
    Array.isArray(skills.missing)
      ? skills.missing
      : [];


  const keywordSummary =
    keyword_analysis.summary || {};


  const matchedKeywords =
    Array.isArray(
      keywordSummary.matched_skills
    )
      ? keywordSummary.matched_skills
      : [];


  const missingKeywords =
    Array.isArray(
      keywordSummary.missing_skills
    )
      ? keywordSummary.missing_skills
      : [];


  const atsFindings =
    ats_analysis.findings || {};


  const atsStrengths =
    Array.isArray(
      atsFindings.strengths
    )
      ? atsFindings.strengths
      : [];


  const atsIssues =
    Array.isArray(
      atsFindings.issues
    )
      ? atsFindings.issues
      : [];


  const topActions =
    Array.isArray(
      recommendations.top_actions
    )
      ? recommendations.top_actions
      : [];


  const allRecommendations =
    Array.isArray(
      recommendations
        .all_recommendations
    )
      ? recommendations
          .all_recommendations
      : [];


  const prioritySummary =
    recommendations
      .priority_summary || {};


  const experience =
    match_analysis.experience || {};

  const education =
    match_analysis.education || {};

  const certifications =
    match_analysis.certifications || {};


  return (
    <div className="results-page">
      <header className="results-navbar">
        <div className="results-nav-container">
          <Link
            to="/"
            className="results-logo"
          >
            SmartHire
          </Link>

          <nav className="results-nav-links">
            <Link
              to="/analyze"
              className="results-nav-link"
            >
              New Analysis
            </Link>

            <Link
              to="/history"
              className="results-account-button"
            >
              History
            </Link>
          </nav>
        </div>
      </header>


      <main className="results-main">
        <section className="results-header">
          <div>
            <span className="results-eyebrow">
              ANALYSIS COMPLETE
            </span>

            <h1>
              Your resume analysis
            </h1>

            <p>
              Review your ATS readiness,
              job alignment, skill gaps,
              keywords, and prioritized
              recommendations.
            </p>
          </div>

          <Link
            to="/analyze"
            className="new-analysis-button"
          >
            Analyze Another Resume
            <span>→</span>
          </Link>
        </section>


        <section className="results-resume-card">
          <div className="results-resume-icon">
            CV
          </div>

          <div className="results-resume-info">
            <span>
              ANALYZED RESUME
            </span>

            <strong>
              {resume_name}
            </strong>

            {getCandidateDisplay(
              candidate,
              contact
            ) && (
              <p>
                {getCandidateDisplay(
                  candidate,
                  contact
                )}
              </p>
            )}
          </div>

          <span className="analysis-complete-badge">
            Analysis Complete
          </span>
        </section>


        <section className="results-score-grid">
          <ScoreCard
            label="ATS READINESS"
            score={atsScore}
            level={atsLevel}
            description="An estimate of resume text extraction, structure, and ATS readability."
          />

          <ScoreCard
            label="RESUME MATCH"
            score={matchScore}
            level={matchLevel}
            description="How closely the evidence in your resume aligns with the detected job requirements."
          />
        </section>


        {topActions.length > 0 && (
          <section className="results-section">
            <SectionHeading
              eyebrow="PRIORITY ACTIONS"
              title="What to improve first"
              description="Start with the highest-priority actions identified by the analysis."
            />

            <div className="top-actions-list">
              {topActions.map(
                (item, index) => (
                  <article
                    className="top-action-card"
                    key={`${item.title}-${index}`}
                  >
                    <span className="top-action-number">
                      {String(
                        index + 1
                      ).padStart(
                        2,
                        "0"
                      )}
                    </span>

                    <div>
                      <PriorityBadge
                        priority={
                          item.priority
                        }
                      />

                      <h3>
                        {item.title}
                      </h3>

                      <p>
                        {item.action}
                      </p>
                    </div>
                  </article>
                )
              )}
            </div>
          </section>
        )}


        <section className="results-section">
          <SectionHeading
            eyebrow="SKILL ALIGNMENT"
            title="How your skills compare with the role"
            description="Skills are classified using evidence found in your resume sections."
          />

          <div className="skill-analysis-grid">
            <SkillCard
              title="Matched Skills"
              description="Skills supported by moderate or strong resume evidence."
              skills={matchedSkills}
              type="matched"
            />

            <SkillCard
              title="Partial Skills"
              description="Skills detected with limited supporting resume evidence."
              skills={partialSkills}
              type="partial"
            />

            <SkillCard
              title="Missing Skills"
              description="Job-related skills for which no clear resume evidence was detected."
              skills={missingSkills}
              type="missing"
            />
          </div>
        </section>


        <section className="results-section">
          <SectionHeading
            eyebrow="KEYWORD ANALYSIS"
            title="Technical keyword coverage"
            description="Review technical skills from the job description that were found or not found in your resume."
          />

          <div className="skill-analysis-grid">
            <KeywordCard
              title="Matched Keywords"
              description="Technical job keywords detected in your resume."
              keywords={
                matchedKeywords
              }
              type="matched"
            />

            <KeywordCard
              title="Missing Keywords"
              description="Technical job keywords not detected in your resume."
              keywords={
                missingKeywords
              }
              type="missing"
            />
          </div>
        </section>


        <section className="results-section">
          <SectionHeading
            eyebrow="ATS FINDINGS"
            title="Resume readiness findings"
            description="These checks focus on text extraction, contact information, recognizable sections, structure, and content length."
          />

          <div className="skill-analysis-grid">
            <FindingCard
              title="Strengths"
              findings={
                atsStrengths
              }
              type="strength"
            />

            <FindingCard
              title="Issues"
              findings={atsIssues}
              type="issue"
            />
          </div>
        </section>


        <section className="results-section">
          <SectionHeading
            eyebrow="REQUIREMENT ANALYSIS"
            title="Additional job requirements"
            description="Review experience, education, and certification requirements detected in the job description."
          />

          <div className="details-grid">
            <RequirementCard
              title="Experience"
              data={experience}
            />

            <RequirementCard
              title="Education"
              data={education}
            />

            <RequirementCard
              title="Certifications"
              data={
                certifications
              }
            />
          </div>
        </section>


        {allRecommendations.length >
          0 && (
          <section className="results-section">
            <SectionHeading
              eyebrow="RECOMMENDATIONS"
              title="Recommended improvements"
              description="These recommendations are prioritized by severity and are designed to avoid encouraging inaccurate resume claims."
            />

            <PrioritySummary
              summary={
                prioritySummary
              }
            />

            <div className="recommendations-list">
              {allRecommendations.map(
                (item, index) => (
                  <article
                    className="recommendation-card"
                    key={`${item.category}-${item.title}-${index}`}
                  >
                    <div className="recommendation-number">
                      {index + 1}
                    </div>

                    <div className="recommendation-content">
                      <div className="recommendation-meta">
                        <PriorityBadge
                          priority={
                            item.priority
                          }
                        />

                        <span>
                          {formatLabel(
                            item.category
                          )}
                        </span>
                      </div>

                      <h3>
                        {item.title}
                      </h3>

                      <p>
                        {item.message}
                      </p>

                      <div className="recommendation-action">
                        <strong>
                          Recommended action
                        </strong>

                        <p>
                          {item.action}
                        </p>
                      </div>

                      {Array.isArray(
                        item.evidence
                      ) &&
                        item.evidence
                          .length > 0 && (
                          <div className="result-skill-list">
                            {item.evidence.map(
                              (
                                evidence,
                                evidenceIndex
                              ) => (
                                <span
                                  className="result-skill matched"
                                  key={
                                    evidenceIndex
                                  }
                                >
                                  {formatEvidence(
                                    evidence
                                  )}
                                </span>
                              )
                            )}
                          </div>
                        )}
                    </div>
                  </article>
                )
              )}
            </div>
          </section>
        )}


        {Array.isArray(
          ats_analysis.limitations
        ) &&
          ats_analysis.limitations
            .length > 0 && (
            <section className="results-section">
              <SectionHeading
                eyebrow="IMPORTANT CONTEXT"
                title="Analysis limitations"
                description="The scores provide structured guidance, but they should not be interpreted as guarantees from a specific employer or ATS."
              />

              <div className="top-actions-list">
                {ats_analysis.limitations.map(
                  (
                    limitation,
                    index
                  ) => (
                    <div
                      className="top-action-card"
                      key={index}
                    >
                      <span className="top-action-number">
                        {String(
                          index + 1
                        ).padStart(
                          2,
                          "0"
                        )}
                      </span>

                      <p>
                        {limitation}
                      </p>
                    </div>
                  )
                )}
              </div>
            </section>
          )}


        <section className="results-cta">
          <div>
            <span>
              READY FOR ANOTHER ANALYSIS?
            </span>

            <h2>
              Compare your resume
              with another role.
            </h2>

            <p>
              Job requirements differ
              between roles. Run a new
              analysis for each position
              you are targeting.
            </p>
          </div>

          <Link
            to="/analyze"
            className="results-cta-button"
          >
            Start New Analysis
            <span>→</span>
          </Link>
        </section>
      </main>
    </div>
  );
}


function SectionHeading({
  eyebrow,
  title,
  description,
}) {
  return (
    <div className="results-section-heading">
      <span>{eyebrow}</span>
      <h2>{title}</h2>
      <p>{description}</p>
    </div>
  );
}


function ScoreCard({
  label,
  score,
  level,
  description,
}) {
  return (
    <article className="result-score-card">
      <div className="result-score-header">
        <span>{label}</span>

        <span className="result-score-level">
          {level}
        </span>
      </div>

      <div className="result-score-value">
        <strong>{score}</strong>
        <span>%</span>
      </div>

      <div
        className="result-score-progress"
        aria-label={`${label}: ${score}%`}
      >
        <div
          className="result-score-progress-fill"
          style={{
            width: `${score}%`,
          }}
        />
      </div>

      <p>{description}</p>
    </article>
  );
}


function SkillCard({
  title,
  description,
  skills,
  type,
}) {
  return (
    <article className="skill-analysis-card">
      <div className="skill-analysis-card-header">
        <h3>{title}</h3>
        <span>{skills.length}</span>
      </div>

      <p>{description}</p>

      {skills.length > 0 ? (
        <div className="result-skill-list">
          {skills.map(
            (item, index) => (
              <span
                className={`result-skill ${type}`}
                key={`${item.skill}-${index}`}
                title={
                  item.evidence_level
                    ? `Evidence: ${item.evidence_level}`
                    : undefined
                }
              >
                {item.skill}
              </span>
            )
          )}
        </div>
      ) : (
        <p className="empty-analysis-message">
          No items identified.
        </p>
      )}
    </article>
  );
}


function KeywordCard({
  title,
  description,
  keywords,
  type,
}) {
  return (
    <article className="skill-analysis-card">
      <div className="skill-analysis-card-header">
        <h3>{title}</h3>
        <span>{keywords.length}</span>
      </div>

      <p>{description}</p>

      {keywords.length > 0 ? (
        <div className="result-skill-list">
          {keywords.map(
            (keyword, index) => (
              <span
                className={`result-skill ${type}`}
                key={`${keyword}-${index}`}
              >
                {keyword}
              </span>
            )
          )}
        </div>
      ) : (
        <p className="empty-analysis-message">
          No items identified.
        </p>
      )}
    </article>
  );
}


function FindingCard({
  title,
  findings,
  type,
}) {
  return (
    <article className="skill-analysis-card">
      <div className="skill-analysis-card-header">
        <h3>{title}</h3>
        <span>{findings.length}</span>
      </div>

      {findings.length > 0 ? (
        <div className="finding-list">
          {findings.map(
            (finding, index) => (
              <div
                className={`finding-item ${type}`}
                key={`${finding.name}-${index}`}
              >
                <strong>
                  {formatLabel(
                    finding.name
                  )}
                </strong>

                <p>
                  {finding.message}
                </p>

                {finding.severity && (
                  <span>
                    {formatLabel(
                      finding.severity
                    )}
                  </span>
                )}
              </div>
            )
          )}
        </div>
      ) : (
        <p className="empty-analysis-message">
          No items identified.
        </p>
      )}
    </article>
  );
}


function RequirementCard({
  title,
  data,
}) {
  const entries = Object.entries(
    data || {}
  ).filter(
    ([key]) =>
      key !== "message"
  );

  return (
    <article className="details-card">
      <h3>{title}</h3>

      {data?.message && (
        <p className="requirement-message">
          {data.message}
        </p>
      )}

      <div className="details-list">
        {entries.map(
          ([key, value]) => (
            <div
              className="details-row"
              key={key}
            >
              <span className="details-key">
                {formatLabel(key)}
              </span>

              <div className="details-value">
                {formatValue(value)}
              </div>
            </div>
          )
        )}
      </div>
    </article>
  );
}


function PrioritySummary({
  summary,
}) {
  const priorities = [
    "critical",
    "high",
    "medium",
    "low",
  ];

  return (
    <div className="priority-summary-grid">
      {priorities.map(
        (priority) => (
          <div
            className="priority-summary-card"
            key={priority}
          >
            <span>
              {formatLabel(priority)}
            </span>

            <strong>
              {summary[priority] ?? 0}
            </strong>
          </div>
        )
      )}
    </div>
  );
}


function PriorityBadge({
  priority = "medium",
}) {
  return (
    <span
      className={`priority-badge priority-${priority}`}
    >
      {formatLabel(priority)}
    </span>
  );
}


function normalizeScore(value) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return 0;
  }

  return Math.min(
    100,
    Math.max(
      0,
      Math.round(number)
    )
  );
}


function formatLabel(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "Not available";
  }

  return String(value)
    .replace(/_/g, " ")
    .replace(
      /\b\w/g,
      (character) =>
        character.toUpperCase()
    );
}


function formatValue(value) {
  if (
    value === null ||
    value === undefined
  ) {
    return "Not available";
  }

  if (
    typeof value === "boolean"
  ) {
    return value
      ? "Yes"
      : "No";
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      return "None";
    }

    return value
      .map((item) =>
        typeof item === "object"
          ? item.skill ||
            item.name ||
            JSON.stringify(item)
          : String(item)
      )
      .join(", ");
  }

  if (
    typeof value === "object"
  ) {
    return JSON.stringify(
      value
    );
  }

  return formatLabel(value);
}


function formatEvidence(
  evidence
) {
  if (
    typeof evidence === "string"
  ) {
    return evidence;
  }

  if (
    evidence &&
    typeof evidence === "object"
  ) {
    if (evidence.section) {
      return formatLabel(
        evidence.section
      );
    }

    return JSON.stringify(
      evidence
    );
  }

  return String(
    evidence ?? ""
  );
}


function getCandidateDisplay(
  candidate,
  contact
) {
  if (
    typeof candidate === "string"
  ) {
    return candidate;
  }

  return (
    candidate?.name ||
    candidate?.full_name ||
    contact?.email ||
    ""
  );
}


export default Results;
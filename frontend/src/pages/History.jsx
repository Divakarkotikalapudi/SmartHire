import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { getAnalysisHistory } from "../api/resumes";
import "./History.css";


function History() {
  const navigate = useNavigate();

  const [analyses, setAnalyses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {
    let isMounted = true;

    const loadHistory = async () => {
      try {
        setLoading(true);
        setError("");

        const data =
          await getAnalysisHistory();

        if (!isMounted) {
          return;
        }

        setAnalyses(
          Array.isArray(data)
            ? data
            : data.results || []
        );
      } catch (error) {
        if (!isMounted) {
          return;
        }

        setError(
          error.message ||
            "Unable to load your analysis history."
        );
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    };

    loadHistory();

    return () => {
      isMounted = false;
    };
  }, []);


  const handleOpenAnalysis = (
    analysis
  ) => {
    if (!analysis?.analysis_result) {
      setError(
        "The saved analysis result is unavailable."
      );

      return;
    }

    navigate(
      `/results/${analysis.id}`,
      {
        state: {
          analysisResult:
            analysis.analysis_result,
        },
      }
    );
  };


  return (
    <div className="history-page">
      <header className="history-navbar">
        <div className="history-nav-container">
          <Link
            to="/"
            className="history-logo"
          >
            SmartHire
          </Link>

          <nav className="history-nav-links">
            <Link
              to="/analyze"
              className="history-nav-link"
            >
              New Analysis
            </Link>

            <span className="history-active-link">
              History
            </span>
          </nav>
        </div>
      </header>


      <main className="history-main">
        <section className="history-header">
          <div>
            <span className="history-eyebrow">
              ANALYSIS HISTORY
            </span>

            <h1>
              Your previous analyses
            </h1>

            <p>
              Review the resume analyses
              you have completed and reopen
              previous results.
            </p>
          </div>

          <Link
            to="/analyze"
            className="history-new-analysis-button"
          >
            New Analysis
            <span>→</span>
          </Link>
        </section>


        {loading && (
          <section
            className="history-state-card"
            aria-live="polite"
          >
            <div className="history-spinner" />

            <h2>
              Loading your history
            </h2>

            <p>
              Retrieving your saved resume
              analyses.
            </p>
          </section>
        )}


        {!loading && error && (
          <section
            className="history-state-card history-error-state"
            role="alert"
          >
            <div className="history-state-icon">
              !
            </div>

            <h2>
              Unable to load history
            </h2>

            <p>{error}</p>

            <button
              type="button"
              className="history-retry-button"
              onClick={() =>
                window.location.reload()
              }
            >
              Try Again
            </button>
          </section>
        )}


        {!loading &&
          !error &&
          analyses.length === 0 && (
            <section className="history-state-card">
              <div className="history-state-icon">
                CV
              </div>

              <h2>
                No analyses yet
              </h2>

              <p>
                Your completed resume
                analyses will appear here.
              </p>

              <Link
                to="/analyze"
                className="history-empty-button"
              >
                Analyze Your First Resume
                <span>→</span>
              </Link>
            </section>
          )}


        {!loading &&
          !error &&
          analyses.length > 0 && (
            <section className="history-content">
              <div className="history-summary">
                <div>
                  <span>
                    SAVED ANALYSES
                  </span>

                  <strong>
                    {analyses.length}
                  </strong>
                </div>

                <p>
                  Newest analyses are shown
                  first.
                </p>
              </div>


              <div className="history-list">
                {analyses.map(
                  (analysis) => (
                    <article
                      className="history-card"
                      key={analysis.id}
                    >
                      <div className="history-card-main">
                        <div className="history-file-icon">
                          CV
                        </div>

                        <div className="history-file-info">
                          <span>
                            RESUME ANALYSIS
                          </span>

                          <h2>
                            {analysis.resume_name ||
                              "Resume"}
                          </h2>

                          <p>
                            Analyzed{" "}
                            {formatDate(
                              analysis.created_at
                            )}
                          </p>
                        </div>
                      </div>


                      <div className="history-scores">
                        <ScoreItem
                          label="ATS Readiness"
                          score={
                            analysis.ats_readiness_score
                          }
                        />

                        <ScoreItem
                          label="Resume Match"
                          score={
                            analysis.resume_match_score
                          }
                        />
                      </div>


                      <button
                        type="button"
                        className="history-view-button"
                        onClick={() =>
                          handleOpenAnalysis(
                            analysis
                          )
                        }
                      >
                        View Results
                        <span>→</span>
                      </button>
                    </article>
                  )
                )}
              </div>
            </section>
          )}
      </main>
    </div>
  );
}


function ScoreItem({
  label,
  score,
}) {
  const normalizedScore =
    normalizeScore(score);

  return (
    <div className="history-score-item">
      <span>{label}</span>

      <strong>
        {normalizedScore}%
      </strong>
    </div>
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


function formatDate(value) {
  if (!value) {
    return "Date unavailable";
  }

  const date = new Date(value);

  if (
    Number.isNaN(
      date.getTime()
    )
  ) {
    return "Date unavailable";
  }

  return new Intl.DateTimeFormat(
    undefined,
    {
      dateStyle: "medium",
      timeStyle: "short",
    }
  ).format(date);
}


export default History;
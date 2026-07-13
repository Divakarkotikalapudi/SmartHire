import "../App.css";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="app">
      {/* Navigation Bar */}
      <header className="navbar">
        <div className="nav-container">
          <a href="#" className="logo">
            SmartHire
          </a>

          <nav className="nav-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
          </nav>

          <div className="nav-actions">
            <Link to="/login" className="login-btn">
              Login
            </Link>

            <Link to="/signup" className="get-started-btn">
              Get Started
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main>
        <section className="hero">
          <div className="hero-content">
            <span className="hero-badge">
              AI-Powered Resume Analysis
            </span>

            <h1>
              Understand How Your Resume
              <span> Matches the Job</span>
            </h1>

            <p>
              Analyze ATS readiness, identify skill gaps, and understand how
              your resume aligns with a target job description.
            </p>

            <div className="hero-actions">
              <Link to="/signup" className="primary-btn">
                Analyze Your Resume
                <span>→</span>
              </Link>

              <a href="#how-it-works" className="secondary-btn">
                See How It Works
              </a>
            </div>

            <div className="hero-note">
              <span>✓ ATS Readiness Analysis</span>
              <span>✓ Job Match Insights</span>
              <span>✓ Actionable Recommendations</span>
            </div>
          </div>

          <div className="hero-visual">
            <div className="analysis-card">
              <div className="card-header">
                <div>
                  <p className="small-label">RESUME ANALYSIS</p>
                  <h3>Software Developer</h3>
                </div>

                <span className="status-badge">
                  Analysis Complete
                </span>
              </div>

              <div className="score-grid">
                <div className="score-card">
                  <span className="score-label">
                    ATS Readiness
                  </span>
                  <strong>92%</strong>
                  <span className="score-status">
                    Excellent
                  </span>
                </div>

                <div className="score-card">
                  <span className="score-label">
                    Resume Match
                  </span>
                  <strong>78%</strong>
                  <span className="score-status">
                    Strong Match
                  </span>
                </div>
              </div>

              <div className="skills-section">
                <p className="small-label">
                  SKILL ALIGNMENT
                </p>

                <div className="skill-row">
                  <span className="skill matched">
                    Python
                  </span>

                  <span className="skill matched">
                    React
                  </span>

                  <span className="skill matched">
                    Git
                  </span>

                  <span className="skill missing">
                    Django
                  </span>
                </div>
              </div>

              <div className="recommendation">
                <div className="recommendation-icon">
                  !
                </div>

                <div>
                  <span>TOP RECOMMENDATION</span>

                  <p>
                    Add relevant Django experience to improve
                    alignment with this role.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="features" id="features">
          <div className="section-heading">
            <span>SMARTER RESUME ANALYSIS</span>

            <h2>
              Know exactly where your resume stands
            </h2>

            <p>
              SmartHire analyzes both your resume structure
              and its alignment with the job you want.
            </p>
          </div>

          <div className="feature-grid">
            <article className="feature-card">
              <div className="feature-number">
                01
              </div>

              <h3>ATS Readiness</h3>

              <p>
                Evaluate whether your resume is readable,
                structured, and prepared for automated
                applicant tracking systems.
              </p>
            </article>

            <article className="feature-card">
              <div className="feature-number">
                02
              </div>

              <h3>Job Match Analysis</h3>

              <p>
                Compare your resume with a target job
                description to identify matched, partial,
                and missing requirements.
              </p>
            </article>

            <article className="feature-card">
              <div className="feature-number">
                03
              </div>

              <h3>Actionable Insights</h3>

              <p>
                Receive prioritized recommendations that
                help you improve your resume without adding
                inaccurate information.
              </p>
            </article>
          </div>
        </section>

        {/* How It Works Section */}
        <section
          className="how-it-works"
          id="how-it-works"
        >
          <div className="section-heading">
            <span>SIMPLE PROCESS</span>

            <h2>
              From resume to insights in three steps
            </h2>
          </div>

          <div className="steps">
            <div className="step">
              <span>1</span>

              <h3>Upload your resume</h3>

              <p>
                Upload your resume in PDF or DOCX format.
              </p>
            </div>

            <div className="step-line"></div>

            <div className="step">
              <span>2</span>

              <h3>Add the job description</h3>

              <p>
                Paste the complete requirements of the role
                you are targeting.
              </p>
            </div>

            <div className="step-line"></div>

            <div className="step">
              <span>3</span>

              <h3>Review your analysis</h3>

              <p>
                Understand your ATS readiness, job match,
                skill gaps, and recommended improvements.
              </p>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="cta-section">
          <div>
            <span>READY TO ANALYZE?</span>

            <h2>
              See how well your resume matches the job.
            </h2>

            <p>
              Get structured insights before submitting
              your next application.
            </p>
          </div>

          <Link to="/signup" className="cta-btn">
            Analyze Your Resume
            <span>→</span>
          </Link>
        </section>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div>
          <strong>SmartHire</strong>

          <p>
            Intelligent resume analysis for modern job
            seekers.
          </p>
        </div>

        <p>
          © 2026 SmartHire. All rights reserved.
        </p>
      </footer>
    </div>
  );
}

export default Home;
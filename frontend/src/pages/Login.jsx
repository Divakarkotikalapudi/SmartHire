import { useState } from "react";
import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";
import { loginUser } from "../api/auth";
import "./Login.css";

function Login() {
  const navigate = useNavigate();
  const location = useLocation();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const redirectPath =
    location.state?.from?.pathname || "/analyze";

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (loading) {
      return;
    }

    setError("");
    setLoading(true);

    try {
      await loginUser(email, password);

      navigate(redirectPath, {
        replace: true,
      });
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to sign in. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* Left Side */}
      <section className="login-showcase">
        <Link to="/" className="login-brand">
          SmartHire
        </Link>

        <div className="showcase-content">
          <span className="showcase-label">
            SMARTER RESUME ANALYSIS
          </span>

          <h1>
            Understand how your resume aligns with the
            <span> role you want.</span>
          </h1>

          <p>
            Get clear insights into ATS readiness, skill gaps,
            and job-specific matching.
          </p>

          <div className="preview-scores">
            <div className="preview-score-card">
              <span>ATS READINESS</span>
              <strong>92%</strong>
              <small>Excellent</small>
            </div>

            <div className="preview-score-card">
              <span>RESUME MATCH</span>
              <strong>78%</strong>
              <small>Strong Match</small>
            </div>
          </div>

          <div className="login-benefits">
            <div className="benefit-item">
              <span className="benefit-icon">✓</span>

              <div>
                <strong>ATS Readiness Analysis</strong>
                <p>
                  Understand your resume&apos;s structural
                  readiness.
                </p>
              </div>
            </div>

            <div className="benefit-item">
              <span className="benefit-icon">✓</span>

              <div>
                <strong>Job-Specific Matching</strong>
                <p>
                  Compare your resume with the role you are
                  targeting.
                </p>
              </div>
            </div>

            <div className="benefit-item">
              <span className="benefit-icon">✓</span>

              <div>
                <strong>Actionable Recommendations</strong>
                <p>
                  Identify important areas you can improve.
                </p>
              </div>
            </div>
          </div>
        </div>

        <p className="showcase-footer">
          Intelligent resume analysis for modern job seekers.
        </p>
      </section>

      {/* Right Side */}
      <section className="login-form-section">
        <div className="mobile-login-brand">
          <Link to="/">SmartHire</Link>
        </div>

        <div className="login-form-container">
          <div className="login-heading">
            <span className="login-eyebrow">
              WELCOME BACK
            </span>

            <h2>Sign in to SmartHire</h2>

            <p>
              Sign in to analyze your resume and job alignment.
            </p>
          </div>

          <form
            className="login-form"
            onSubmit={handleSubmit}
          >
            <div className="form-group">
              <label htmlFor="email">
                Email Address
              </label>

              <input
                type="email"
                id="email"
                name="email"
                placeholder="you@example.com"
                autoComplete="email"
                value={email}
                onChange={(event) => {
                  setEmail(event.target.value);

                  if (error) {
                    setError("");
                  }
                }}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">
                Password
              </label>

              <div className="password-field">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  value={password}
                  onChange={(event) => {
                    setPassword(event.target.value);

                    if (error) {
                      setError("");
                    }
                  }}
                  disabled={loading}
                  required
                />
                <button
                  type="button"
                  className="password-toggle"
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                  aria-pressed={showPassword}
                  onClick={() =>
                    setShowPassword(
                      (currentValue) =>
                        !currentValue
                    )
                  }
                  disabled={loading}
                >
                  {showPassword
                    ? "Hide"
                    : "Show"}
                </button>
              </div>
            </div>

            {error && (
              <p
                className="login-error"
                role="alert"
                aria-live="polite"
              >
                {error}
              </p>
            )}

            <button
              type="submit"
              className="login-submit-btn"
              disabled={loading}
              aria-busy={loading}
            >
              {loading ? (
                "Signing in..."
              ) : (
                <>
                  Sign In
                  <span aria-hidden="true">
                    →
                  </span>
                </>
              )}
            </button>
          </form>

          <p className="signup-link">
            Don&apos;t have an account?{" "}
            <Link to="/signup">
              Create an account
            </Link>
          </p>

          <Link
            to="/"
            className="back-home-link"
          >
            ← Back to home
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Login;
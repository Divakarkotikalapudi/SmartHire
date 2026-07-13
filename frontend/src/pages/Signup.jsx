import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";
import "./Signup.css";

function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    password_confirm: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showPasswordConfirm, setShowPasswordConfirm] =
    useState(false);

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((currentData) => ({
      ...currentData,
      [name]: value,
    }));

    if (error) {
      setError("");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (loading) {
      return;
    }

    setError("");

    const firstName = formData.first_name.trim();
    const lastName = formData.last_name.trim();
    const email = formData.email.trim();

    if (!firstName) {
      setError("Please enter your first name.");
      return;
    }

    if (!lastName) {
      setError("Please enter your last name.");
      return;
    }

    if (!email) {
      setError("Please enter your email address.");
      return;
    }

    if (!formData.password) {
      setError("Please enter a password.");
      return;
    }

    if (formData.password !== formData.password_confirm) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);

    try {
      await registerUser({
        ...formData,
        first_name: firstName,
        last_name: lastName,
        email,
      });

      navigate("/login", {
        replace: true,
        state: {
          registrationSuccess: true,
          email: email.toLowerCase(),
        },
      });
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to create your account. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="signup-page">
      {/* Left Side */}
      <section className="signup-showcase">
        <Link to="/" className="signup-brand">
          SmartHire
        </Link>

        <div className="signup-showcase-content">
          <span className="signup-showcase-label">
            BUILD A STRONGER APPLICATION
          </span>

          <h1>
            Turn your resume into
            <span> clearer job insights.</span>
          </h1>

          <p>
            Create your SmartHire account to analyze resume
            readiness, understand job alignment, and identify
            areas for improvement.
          </p>

          <div className="signup-feature-list">
            <div className="signup-feature-item">
              <span className="signup-feature-number">
                01
              </span>

              <div>
                <strong>Upload your resume</strong>

                <p>
                  Submit your PDF or DOCX resume for structured
                  analysis.
                </p>
              </div>
            </div>

            <div className="signup-feature-item">
              <span className="signup-feature-number">
                02
              </span>

              <div>
                <strong>
                  Add a target job description
                </strong>

                <p>
                  Compare your background with the requirements
                  of the role.
                </p>
              </div>
            </div>

            <div className="signup-feature-item">
              <span className="signup-feature-number">
                03
              </span>

              <div>
                <strong>
                  Review actionable insights
                </strong>

                <p>
                  Understand ATS readiness, skill alignment,
                  and recommended improvements.
                </p>
              </div>
            </div>
          </div>
        </div>

        <p className="signup-showcase-footer">
          Intelligent resume analysis for modern job seekers.
        </p>
      </section>

      {/* Right Side */}
      <section className="signup-form-section">
        <div className="mobile-signup-brand">
          <Link to="/">SmartHire</Link>
        </div>

        <div className="signup-form-container">
          <div className="signup-heading">
            <span className="signup-eyebrow">
              GET STARTED
            </span>

            <h2>Create your account</h2>

            <p>
              Enter your details to start analyzing your
              resume and job alignment.
            </p>
          </div>

          <form
            className="signup-form"
            onSubmit={handleSubmit}
          >
            <div className="name-fields">
              <div className="signup-form-group">
                <label htmlFor="first_name">
                  First Name
                </label>

                <input
                  type="text"
                  id="first_name"
                  name="first_name"
                  placeholder="First name"
                  value={formData.first_name}
                  onChange={handleChange}
                  autoComplete="given-name"
                  disabled={loading}
                  required
                />
              </div>

              <div className="signup-form-group">
                <label htmlFor="last_name">
                  Last Name
                </label>

                <input
                  type="text"
                  id="last_name"
                  name="last_name"
                  placeholder="Last name"
                  value={formData.last_name}
                  onChange={handleChange}
                  autoComplete="family-name"
                  disabled={loading}
                  required
                />
              </div>
            </div>

            <div className="signup-form-group">
              <label htmlFor="signup-email">
                Email Address
              </label>

              <input
                type="email"
                id="signup-email"
                name="email"
                placeholder="you@example.com"
                value={formData.email}
                onChange={handleChange}
                autoComplete="email"
                disabled={loading}
                required
              />
            </div>

            <div className="signup-form-group">
              <label htmlFor="signup-password">
                Password
              </label>

              <div className="signup-password-field">
                <input
                  type={
                    showPassword ? "text" : "password"
                  }
                  id="signup-password"
                  name="password"
                  placeholder="Create a password"
                  value={formData.password}
                  onChange={handleChange}
                  autoComplete="new-password"
                  disabled={loading}
                  required
                />

                <button
                  type="button"
                  className="signup-password-toggle"
                  onClick={() =>
                    setShowPassword(
                      (currentValue) => !currentValue
                    )
                  }
                  aria-label={
                    showPassword
                      ? "Hide password"
                      : "Show password"
                  }
                  aria-pressed={showPassword}
                  disabled={loading}
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>
            </div>

            <div className="signup-form-group">
              <label htmlFor="password_confirm">
                Confirm Password
              </label>

              <div className="signup-password-field">
                <input
                  type={
                    showPasswordConfirm
                      ? "text"
                      : "password"
                  }
                  id="password_confirm"
                  name="password_confirm"
                  placeholder="Confirm your password"
                  value={formData.password_confirm}
                  onChange={handleChange}
                  autoComplete="new-password"
                  disabled={loading}
                  required
                />

                <button
                  type="button"
                  className="signup-password-toggle"
                  onClick={() =>
                    setShowPasswordConfirm(
                      (currentValue) => !currentValue
                    )
                  }
                  aria-label={
                    showPasswordConfirm
                      ? "Hide confirmation password"
                      : "Show confirmation password"
                  }
                  aria-pressed={showPasswordConfirm}
                  disabled={loading}
                >
                  {showPasswordConfirm
                    ? "Hide"
                    : "Show"}
                </button>
              </div>
            </div>

            {error && (
              <p
                className="signup-error"
                role="alert"
                aria-live="polite"
              >
                {error}
              </p>
            )}

            <button
              type="submit"
              className="signup-submit-btn"
              disabled={loading}
              aria-busy={loading}
            >
              {loading ? (
                "Creating account..."
              ) : (
                <>
                  Create Account
                  <span aria-hidden="true">→</span>
                </>
              )}
            </button>
          </form>

          <p className="login-link">
            Already have an account?{" "}
            <Link to="/login">
              Sign in
            </Link>
          </p>

          <Link
            to="/"
            className="signup-back-home"
          >
            ← Back to home
          </Link>
        </div>
      </section>
    </div>
  );
}

export default Signup;
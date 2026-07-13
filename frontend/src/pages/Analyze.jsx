import { useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { analyzeResume } from "../api/resumes";
import "./Analyze.css";

const ALLOWED_FILE_TYPES = [
  "application/pdf",
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];

const ALLOWED_EXTENSIONS = [".pdf", ".docx"];

const MAX_FILE_SIZE = 5 * 1024 * 1024;

function Analyze() {
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const validateFile = (file) => {
    if (!file) {
      return false;
    }

    const fileName = file.name.toLowerCase();

    const hasAllowedExtension = ALLOWED_EXTENSIONS.some(
      (extension) => fileName.endsWith(extension)
    );

    const hasAllowedType =
      !file.type || ALLOWED_FILE_TYPES.includes(file.type);

    if (!hasAllowedExtension || !hasAllowedType) {
      setError("Please upload a PDF or DOCX resume.");
      return false;
    }

    if (file.size > MAX_FILE_SIZE) {
      setError("Resume file size must be 5 MB or less.");
      return false;
    }

    setError("");
    return true;
  };

  const selectFile = (file) => {
    if (validateFile(file)) {
      setResumeFile(file);
    }
  };

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (file) {
      selectFile(file);
    }

    event.target.value = "";
  };

  const handleDragEnter = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!loading) {
      setIsDragging(true);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!loading) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!event.currentTarget.contains(event.relatedTarget)) {
      setIsDragging(false);
    }
  };

  const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();

    setIsDragging(false);

    if (loading) {
      return;
    }

    const file = event.dataTransfer.files?.[0];

    if (file) {
      selectFile(file);
    }
  };

  const handleRemoveFile = () => {
    if (loading) {
      return;
    }

    setResumeFile(null);
    setError("");
  };

  const handleJobDescriptionChange = (event) => {
    setJobDescription(event.target.value);

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

    if (!resumeFile) {
      setError("Please upload your resume.");
      return;
    }

    if (!jobDescription.trim()) {
      setError("Please enter the job description.");
      return;
    }

    setLoading(true);

    try {
      const analysisResult = await analyzeResume(
        resumeFile,
        jobDescription
      );

      if (!analysisResult?.analysis_id) {
        throw new Error(
          "The analysis was completed, but a saved analysis ID was not returned."
        );
      }

      navigate(
        `/results/${analysisResult.analysis_id}`,
        {
          state: {
            analysisResult,
          },
        }
      );
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to analyze your resume. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) {
      return `${bytes} B`;
    }

    if (bytes < 1024 * 1024) {
      return `${(bytes / 1024).toFixed(1)} KB`;
    }

    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  const isFormReady =
    Boolean(resumeFile) &&
    Boolean(jobDescription.trim());

  return (
    <div className="analyze-page">
      <header className="analyze-navbar">
        <div className="analyze-nav-container">
          <Link to="/" className="analyze-logo">
            SmartHire
          </Link>

          <nav className="analyze-nav-links">
            <Link
              to="/history"
              className="analyze-nav-link"
            >
              History
            </Link>
          </nav>
        </div>
      </header>

      <main className="analyze-main">
        <section className="analyze-intro">
          <span className="analyze-eyebrow">
            RESUME ANALYSIS
          </span>

          <h1>
            Analyze your resume against the job you want.
          </h1>

          <p>
            Upload your resume and add the target job
            description. SmartHire will evaluate ATS
            readiness, job alignment, skill gaps, keywords,
            and improvement opportunities.
          </p>
        </section>

        <form
          className="analyze-form"
          onSubmit={handleSubmit}
        >
          <section className="analyze-panel">
            <div className="analyze-panel-header">
              <div className="analyze-step-number">
                01
              </div>

              <div>
                <h2>Upload your resume</h2>

                <p>
                  Upload the resume you want to evaluate.
                </p>
              </div>
            </div>

            {!resumeFile ? (
              <div
                className={`resume-dropzone ${isDragging ? "dragging" : ""
                  }`}
                onDragEnter={handleDragEnter}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  disabled={loading}
                  hidden
                />

                <div className="upload-icon">
                  ↑
                </div>

                <h3>Drop your resume here</h3>

                <p>
                  or choose a file from your computer
                </p>

                <button
                  type="button"
                  className="choose-file-button"
                  onClick={() =>
                    fileInputRef.current?.click()
                  }
                  disabled={loading}
                >
                  Choose File
                </button>

                <span className="upload-requirements">
                  PDF or DOCX · Maximum 5 MB
                </span>
              </div>
            ) : (
              <div className="selected-file-card">
                <div className="selected-file-icon">
                  {resumeFile.name
                    .toLowerCase()
                    .endsWith(".pdf")
                    ? "PDF"
                    : "DOCX"}
                </div>

                <div className="selected-file-info">
                  <strong>{resumeFile.name}</strong>

                  <span>
                    {formatFileSize(resumeFile.size)}
                  </span>
                </div>

                <button
                  type="button"
                  className="remove-file-button"
                  onClick={handleRemoveFile}
                  disabled={loading}
                  aria-label={`Remove ${resumeFile.name}`}
                >
                  Remove
                </button>
              </div>
            )}
          </section>

          <section className="analyze-panel">
            <div className="analyze-panel-header">
              <div className="analyze-step-number">
                02
              </div>

              <div>
                <h2>Add the job description</h2>

                <p>
                  Paste the complete description of the role
                  you are targeting.
                </p>
              </div>
            </div>

            <div className="job-description-field">
              <label htmlFor="job-description">
                Job Description
              </label>

              <textarea
                id="job-description"
                name="job_description"
                value={jobDescription}
                onChange={handleJobDescriptionChange}
                placeholder="Paste the complete job description here, including responsibilities, required skills, qualifications, and preferred experience..."
                rows="14"
                disabled={loading}
              />

              <div className="job-description-meta">
                <span>
                  Include the complete job description for a
                  more accurate comparison.
                </span>

                <span>
                  {jobDescription.length.toLocaleString()}{" "}
                  characters
                </span>
              </div>
            </div>
          </section>

          {error && (
            <div
              className="analyze-error"
              role="alert"
              aria-live="polite"
            >
              {error}
            </div>
          )}

          <section className="analyze-submit-section">
            <div>
              <strong>
                {loading
                  ? "Analyzing your resume..."
                  : "Ready for analysis?"}
              </strong>

              <p>
                {loading
                  ? "SmartHire is processing your resume and comparing it with the job requirements."
                  : "Your resume will be compared with the job requirements to generate structured insights."}
              </p>
            </div>

            <button
              type="submit"
              className="analyze-submit-button"
              disabled={!isFormReady || loading}
              aria-busy={loading}
            >
              {loading ? (
                "Analyzing Resume..."
              ) : (
                <>
                  Analyze Resume
                  <span aria-hidden="true">→</span>
                </>
              )}
            </button>
          </section>
        </form>

        <section className="analysis-expectations">
          <span className="analysis-expectations-label">
            YOUR ANALYSIS WILL INCLUDE
          </span>

          <div className="analysis-expectations-grid">
            <div>
              <strong>ATS Readiness</strong>
              <p>
                Resume structure and ATS compatibility.
              </p>
            </div>

            <div>
              <strong>Job Match</strong>
              <p>
                Alignment with the target role.
              </p>
            </div>

            <div>
              <strong>Skill Gaps</strong>
              <p>
                Matched and missing job requirements.
              </p>
            </div>

            <div>
              <strong>Recommendations</strong>
              <p>
                Prioritized actions for improvement.
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Analyze;
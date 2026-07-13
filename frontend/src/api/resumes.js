import {
  clearAuthTokens,
  getAccessToken,
  refreshAccessToken,
} from "./auth";


const API_BASE_URL =
  import.meta.env.VITE_RESUMES_API_BASE_URL ||
  "http://127.0.0.1:8000/api/resumes";


/**
 * Safely attempts to parse a JSON response.
 */
async function parseResponse(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}


/**
 * Extracts a useful error message from a Django REST Framework response.
 */
function getErrorMessage(data, fallbackMessage) {
  if (!data || typeof data !== "object") {
    return fallbackMessage;
  }

  if (typeof data.detail === "string") {
    return data.detail;
  }

  for (const value of Object.values(data)) {
    if (Array.isArray(value) && value.length > 0) {
      return String(value[0]);
    }

    if (typeof value === "string") {
      return value;
    }
  }

  return fallbackMessage;
}


/**
 * Performs an authenticated API request.
 *
 * If the access token has expired:
 * 1. Refresh the access token.
 * 2. Retry the original request once.
 */
async function authenticatedFetch(url, options = {}) {
  let accessToken = getAccessToken();

  if (!accessToken) {
    clearAuthTokens();

    throw new Error(
      "You are not signed in. Please sign in again."
    );
  }

  const createRequestOptions = (token) => ({
    ...options,

    headers: {
      ...(options.headers || {}),

      Authorization: `Bearer ${token}`,
    },
  });

  let response = await fetch(
    url,
    createRequestOptions(accessToken)
  );

  if (response.status === 401) {
    try {
      accessToken = await refreshAccessToken();
    } catch (error) {
      clearAuthTokens();
      throw error;
    }

    response = await fetch(
      url,
      createRequestOptions(accessToken)
    );
  }

  if (response.status === 401) {
    clearAuthTokens();
  }

  return response;
}


/**
 * Uploads a resume and job description for analysis.
 *
 * Do not manually set Content-Type here.
 * The browser automatically creates the correct
 * multipart/form-data boundary for FormData.
 */
export async function analyzeResume(
  resumeFile,
  jobDescription
) {
  if (!resumeFile) {
    throw new Error(
      "Please select a resume file."
    );
  }

  if (!jobDescription?.trim()) {
    throw new Error(
      "Please enter a job description."
    );
  }

  const formData = new FormData();

  formData.append(
    "resume",
    resumeFile
  );

  formData.append(
    "job_description",
    jobDescription.trim()
  );

  const response = await authenticatedFetch(
    `${API_BASE_URL}/analyze/`,
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await parseResponse(response);

  if (!response.ok) {
    throw new Error(
      getErrorMessage(
        data,
        "Resume analysis failed. Please try again."
      )
    );
  }

  return data;
}


/**
 * Returns all saved analyses belonging to
 * the currently authenticated user.
 */
export async function getAnalysisHistory() {
  const response = await authenticatedFetch(
    `${API_BASE_URL}/history/`,
    {
      method: "GET",
    }
  );

  const data = await parseResponse(response);

  if (!response.ok) {
    throw new Error(
      getErrorMessage(
        data,
        "Unable to load your analysis history."
      )
    );
  }

  return data;
}


/**
 * Returns one saved analysis belonging to
 * the currently authenticated user.
 */
export async function getAnalysisById(analysisId) {
  if (
    analysisId === null ||
    analysisId === undefined ||
    analysisId === ""
  ) {
    throw new Error(
      "A valid analysis ID is required."
    );
  }

  const response = await authenticatedFetch(
    `${API_BASE_URL}/history/${analysisId}/`,
    {
      method: "GET",
    }
  );

  const data = await parseResponse(response);

  if (!response.ok) {
    throw new Error(
      getErrorMessage(
        data,
        "Unable to load this analysis."
      )
    );
  }

  return data;
}
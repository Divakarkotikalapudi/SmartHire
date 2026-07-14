import {
  clearAuthTokens,
  getAccessToken,
  refreshAccessToken,
} from "./auth";


const API_BASE_URL =
  import.meta.env.VITE_RESUMES_API_BASE_URL ||
  "http://127.0.0.1:8000/api/resumes";


async function parseResponse(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}


function getErrorMessage(
  data,
  fallbackMessage
) {
  if (
    !data ||
    typeof data !== "object"
  ) {
    return fallbackMessage;
  }

  if (
    typeof data.detail === "string"
  ) {
    return data.detail;
  }

  for (
    const value of Object.values(data)
  ) {
    if (
      Array.isArray(value) &&
      value.length > 0
    ) {
      return String(value[0]);
    }

    if (
      typeof value === "string"
    ) {
      return value;
    }
  }

  return fallbackMessage;
}


function getNetworkErrorMessage() {
  return (
    "Unable to connect to the server. " +
    "Please check your connection and try again."
  );
}


async function safeFetch(
  url,
  options = {}
) {
  try {
    return await fetch(
      url,
      options
    );
  } catch {
    throw new Error(
      getNetworkErrorMessage()
    );
  }
}


async function authenticatedFetch(
  url,
  options = {}
) {
  let accessToken =
    getAccessToken();

  if (!accessToken) {
    clearAuthTokens();

    throw new Error(
      "You are not signed in. " +
      "Please sign in again."
    );
  }

  const createRequestOptions = (
    token
  ) => ({
    ...options,

    headers: {
      ...(options.headers || {}),

      Authorization:
        `Bearer ${token}`,
    },
  });

  let response = await safeFetch(
    url,
    createRequestOptions(
      accessToken
    )
  );

  if (response.status === 401) {
    try {
      accessToken =
        await refreshAccessToken();
    } catch (error) {
      clearAuthTokens();

      throw error;
    }

    response = await safeFetch(
      url,
      createRequestOptions(
        accessToken
      )
    );
  }

  if (response.status === 401) {
    clearAuthTokens();

    throw new Error(
      "Your session has expired. " +
      "Please sign in again."
    );
  }

  return response;
}


export async function analyzeResume(
  resumeFile,
  jobDescription
) {
  if (!resumeFile) {
    throw new Error(
      "Please select a resume file."
    );
  }

  if (
    !jobDescription?.trim()
  ) {
    throw new Error(
      "Please enter a job description."
    );
  }

  const formData =
    new FormData();

  formData.append(
    "resume",
    resumeFile
  );

  formData.append(
    "job_description",
    jobDescription.trim()
  );

  const response =
    await authenticatedFetch(
      `${API_BASE_URL}/analyze/`,
      {
        method: "POST",
        body: formData,
      }
    );

  const data =
    await parseResponse(
      response
    );

  if (!response.ok) {
    throw new Error(
      getErrorMessage(
        data,
        "Unable to analyze your resume. " +
        "Please try again."
      )
    );
  }

  return data;
}


export async function getAnalysisHistory() {
  const response =
    await authenticatedFetch(
      `${API_BASE_URL}/history/`,
      {
        method: "GET",
      }
    );

  const data =
    await parseResponse(
      response
    );

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


export async function getAnalysisById(
  analysisId
) {
  if (
    analysisId === null ||
    analysisId === undefined ||
    analysisId === ""
  ) {
    throw new Error(
      "A valid analysis ID is required."
    );
  }

  const response =
    await authenticatedFetch(
      `${API_BASE_URL}/history/${analysisId}/`,
      {
        method: "GET",
      }
    );

  const data =
    await parseResponse(
      response
    );

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error(
        "This analysis was not found or " +
        "is not available to your account."
      );
    }

    throw new Error(
      getErrorMessage(
        data,
        "Unable to load this analysis."
      )
    );
  }

  return data;
}
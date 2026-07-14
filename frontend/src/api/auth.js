const API_BASE_URL =
  import.meta.env.VITE_AUTH_API_BASE_URL ||
  "http://127.0.0.1:8000/api/auth";


function getErrorMessage(data, fallbackMessage) {
  if (!data || typeof data !== "object") {
    return fallbackMessage;
  }

  if (typeof data.detail === "string") {
    return data.detail;
  }

  const fields = [
    "email",
    "password",
    "password_confirm",
    "first_name",
    "last_name",
    "non_field_errors",
  ];

  for (const field of fields) {
    const error = data[field];

    if (Array.isArray(error) && error.length > 0) {
      return String(error[0]);
    }

    if (typeof error === "string") {
      return error;
    }
  }

  return fallbackMessage;
}


async function parseResponse(response) {
  try {
    return await response.json();
  } catch {
    return {};
  }
}


function getNetworkErrorMessage() {
  return (
    "Unable to connect to the server. " +
    "Please check your connection and try again."
  );
}


async function safeFetch(url, options = {}) {
  try {
    return await fetch(url, options);
  } catch {
    throw new Error(
      getNetworkErrorMessage()
    );
  }
}


export function getAccessToken() {
  return localStorage.getItem(
    "accessToken"
  );
}


export function getRefreshToken() {
  return localStorage.getItem(
    "refreshToken"
  );
}


export function storeTokens(
  accessToken,
  refreshToken = null
) {
  if (accessToken) {
    localStorage.setItem(
      "accessToken",
      accessToken
    );
  }

  if (refreshToken) {
    localStorage.setItem(
      "refreshToken",
      refreshToken
    );
  }
}


export function clearAuthTokens() {
  localStorage.removeItem(
    "accessToken"
  );

  localStorage.removeItem(
    "refreshToken"
  );
}


export async function loginUser(
  email,
  password
) {
  const response = await safeFetch(
    `${API_BASE_URL}/login/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        email: email.trim().toLowerCase(),
        password,
      }),
    }
  );

  const data = await parseResponse(
    response
  );

  if (!response.ok) {
    if (
      response.status === 401 ||
      data.detail ===
        "No active account found with the given credentials"
    ) {
      throw new Error(
        "Invalid email or password."
      );
    }

    throw new Error(
      getErrorMessage(
        data,
        "Unable to sign in. Please try again."
      )
    );
  }

  if (
    !data.access ||
    !data.refresh
  ) {
    throw new Error(
      "Unable to complete sign in. " +
      "Please try again."
    );
  }

  storeTokens(
    data.access,
    data.refresh
  );

  return data;
}


export async function registerUser(
  userData
) {
  const payload = {
    first_name:
      userData.first_name.trim(),

    last_name:
      userData.last_name.trim(),

    email:
      userData.email
        .trim()
        .toLowerCase(),

    password:
      userData.password,

    password_confirm:
      userData.password_confirm,
  };

  const response = await safeFetch(
    `${API_BASE_URL}/register/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(
        payload
      ),
    }
  );

  const data = await parseResponse(
    response
  );

  if (!response.ok) {
    throw new Error(
      getErrorMessage(
        data,
        "Unable to create your account. " +
        "Please check your details and try again."
      )
    );
  }

  return data;
}


export async function refreshAccessToken() {
  const refreshToken =
    getRefreshToken();

  if (!refreshToken) {
    clearAuthTokens();

    throw new Error(
      "Your session has expired. " +
      "Please sign in again."
    );
  }

  const response = await safeFetch(
    `${API_BASE_URL}/refresh/`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        refresh: refreshToken,
      }),
    }
  );

  const data = await parseResponse(
    response
  );

  if (
    !response.ok ||
    !data.access
  ) {
    clearAuthTokens();

    throw new Error(
      "Your session has expired. " +
      "Please sign in again."
    );
  }

  storeTokens(
    data.access,
    data.refresh || null
  );

  return data.access;
}


async function fetchCurrentUser(
  accessToken
) {
  return safeFetch(
    `${API_BASE_URL}/me/`,
    {
      method: "GET",

      headers: {
        Authorization:
          `Bearer ${accessToken}`,
      },
    }
  );
}


export async function getCurrentUser() {
  let accessToken =
    getAccessToken();

  if (!accessToken) {
    clearAuthTokens();

    throw new Error(
      "You are not signed in."
    );
  }

  let response =
    await fetchCurrentUser(
      accessToken
    );

  if (response.status === 401) {
    accessToken =
      await refreshAccessToken();

    response =
      await fetchCurrentUser(
        accessToken
      );
  }

  const data = await parseResponse(
    response
  );

  if (!response.ok) {
    if (response.status === 401) {
      clearAuthTokens();

      throw new Error(
        "Your session has expired. " +
        "Please sign in again."
      );
    }

    throw new Error(
      getErrorMessage(
        data,
        "Unable to verify your account. " +
        "Please try again."
      )
    );
  }

  return data;
}


export function logoutUser() {
  clearAuthTokens();
}
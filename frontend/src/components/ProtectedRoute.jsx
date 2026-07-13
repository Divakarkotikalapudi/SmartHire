import { useEffect, useState } from "react";
import { Navigate, useLocation } from "react-router-dom";
import {
  clearAuthTokens,
  getCurrentUser,
} from "../api/auth";

function ProtectedRoute({ children }) {
  const location = useLocation();

  const [authStatus, setAuthStatus] = useState("checking");

  useEffect(() => {
    let isMounted = true;

    const verifyUser = async () => {
      try {
        await getCurrentUser();

        if (isMounted) {
          setAuthStatus("authenticated");
        }
      } catch (error) {
        clearAuthTokens();

        if (isMounted) {
          setAuthStatus("unauthenticated");
        }
      }
    };

    verifyUser();

    return () => {
      isMounted = false;
    };
  }, []);

  if (authStatus === "checking") {
    return (
      <div role="status" aria-live="polite">
        Checking authentication...
      </div>
    );
  }

  if (authStatus === "unauthenticated") {
    return (
      <Navigate
        to="/login"
        state={{ from: location }}
        replace
      />
    );
  }

  return children;
}

export default ProtectedRoute;
import { Route, Routes } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";

import Analyze from "./pages/Analyze";
import History from "./pages/History";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Results from "./pages/Results";
import Signup from "./pages/Signup";


function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route
        path="/"
        element={<Home />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/signup"
        element={<Signup />}
      />


      {/* Protected routes */}
      <Route
        path="/analyze"
        element={
          <ProtectedRoute>
            <Analyze />
          </ProtectedRoute>
        }
      />

      {/* Results from a newly completed analysis */}
      <Route
        path="/results"
        element={
          <ProtectedRoute>
            <Results />
          </ProtectedRoute>
        }
      />

      {/* Previously saved analysis */}
      <Route
        path="/results/:analysisId"
        element={
          <ProtectedRoute>
            <Results />
          </ProtectedRoute>
        }
      />

      {/* Analysis history */}
      <Route
        path="/history"
        element={
          <ProtectedRoute>
            <History />
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}


export default App;
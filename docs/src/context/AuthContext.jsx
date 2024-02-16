


import { createContext, useContext, useState, useEffect } from "react";
import { BaseRepoReportsAPI } from "../backend/repo.js";
import {SPORTS} from'../backend/consts.js'
const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const repoAPI = new BaseRepoReportsAPI()
  const [evaluationReports, setEvaluationReports] = useState(null);

async function fetchEvaluationSports() {
  if (evaluationReports === null) {
    const allEvaluationReports = {};
    for (const sport in SPORTS) {
      const data = await repoAPI.getEvaluationForSport(SPORTS[sport]);
          allEvaluationReports[sport] = data['evaluations']
        }
    setEvaluationReports(allEvaluationReports)
  }
}

  useEffect(() => {
    
    fetchEvaluationSports()
    setLoading(false)
  }, []);

  const value = {
    error,
    setError,
    evaluationReports
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
import { useState, useEffect } from "react";
import { useAuth } from '../context/AuthContext'
import { EvaluationTable } from "../components/EvaluationTable";

function HomePage() {
  const { evaluationReports} = useAuth();
  const [loading, setLoading] = useState(true);
  const [alltimeEvaluation, setAlltimeEvaluation] = useState([]);
  const [latestEvaluation, setLatestEvaluation] = useState([]);

  useEffect(() => {
    setLoading(evaluationReports === null);
    const allEval = [];
    const latestEval = [];

    for (const sport in evaluationReports) {
      let latestYear = 0;

      for (const reportYear in evaluationReports[sport]) {
        if (reportYear === 'ALL') {
          allEval.push({ ...evaluationReports[sport][reportYear], sport: sport });
        } else {
          const year = parseInt(reportYear);
          if (year > latestYear & evaluationReports[sport][year] !== null) {
            latestYear = year;
          }
        }
      }
      latestEval.push({ ...evaluationReports[sport][latestYear], sport: sport });
    }
    setAlltimeEvaluation(allEval);
    setLatestEvaluation(latestEval);
  }, [evaluationReports]);

  return (
    <>
<div className="relative isolate px-6 pt-2 lg:px-8">
        <div
          className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
          aria-hidden="true"
        >
          <div
            className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
          />
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-8 text-center">
              Elo Ratings
            </h1>
  <div className="mb-8 text-center ml-5 mr-5">
  <p className="text-md">
    Welcome to our Elo Ratings system, where we analyze and evaluate team performance based on the Elo rating algorithm.
    The Elo system, originally designed for chess, is now widely used in sports to quantify the skill levels of teams.
  </p>
  <p className="text-md">
    The "All-Time Evaluation" table summarizes the historical performance of teams, while the "Latest Season Evaluation" table focuses on the
    most recent season's data. Explore the tables to understand how well our Elo system predicts outcomes and assesses team strengths.
  </p>
  <div className="mt-8 mb-8 text-center text-lg">
    Here's a breakdown of key metrics:
    <ul className="text-left list-disc text-sm ml-5 mr-5">
      <li>
        <strong>Accuracy:</strong> Measures how often our Elo system correctly predicts the outcome of a game (home team beating away team).
      </li>
      <li>
        <strong>Mean Absolute Error (MAE):</strong> Evaluates how many points the Elo System is off by on average. The spread is determined either by dividing the Elo difference by the K value or using a fitted gamma distribution to historical score differences.
      </li>
      <li>
        <strong>Brier Score:</strong> Assesses the quality of our probability predictions. Lower values indicate better performance in the binary classification problem of predicting the home team's victory.
      </li>
      <li>
        <strong>Games:</strong> The number of games sampled to build the evaluation set for the given report.
      </li>
    </ul>
  </div>
</div>
        {
          loading ? (
            <div className="text-center font-semibold">
            <i className="fas fa-spinner fa-spin fa-2x"></i> {/* Replace with your loading icon */}
            <p>Loading...</p>
          </div>
          ) : <div><EvaluationTable data={latestEvaluation} title="Latest Season"/><EvaluationTable data={alltimeEvaluation} title="All Time"/></div>
        }
        






      </div>
    </>
  );
}

export default HomePage;
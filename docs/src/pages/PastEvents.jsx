import { useState, useEffect } from "react";
import { SPORTS } from "../backend/consts.js";
import { BaseRepoReportsAPI } from "../backend/repo.js";
function PastEventsPage() {

  const [userTimezone, setUserTimezone] = useState("UTC");
  const [loading, setLoading] = useState(true);
  const [pastEvents, setPastEvents] = useState([]);
  const[eventSport, setEventSport] = useState(null);
  const [selectedSport, setSelectedSport] = useState('COLLEGE_BASKETBALL');
  const [mae, setMae] = useState(null); // State to store the calculated MAE
  const repoAPI = new BaseRepoReportsAPI()

async function fetchPastEvents(sport) {
  setLoading(true);
  setPastEvents([])

    const allPastEvents = [];

    // Get the current UTC datetime
    const currentUtcDatetime = new Date().toISOString();

    // Fetch Past events for each sport
    const data = await repoAPI.getPastForSport(SPORTS[sport]);

    if (data['events'] !== null) {
      // Filter events with datetime greater than the current UTC datetime
      const pastEventsForSport = data['events'].filter(
        (event) => event.datetime < currentUtcDatetime
      );

      // Concatenate events to the main array
      allPastEvents.push(...pastEventsForSport);
    }

    // Sort events by datetime
    const sortedEvents = allPastEvents.sort((b, a) =>
      a.datetime.localeCompare(b.datetime)
    );

    // Update state with the sorted and extended array
    setPastEvents(sortedEvents);
  
  setLoading(false);
}

  useEffect(() => {
    // Get user's timezone
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    setUserTimezone(userTimezone);
  }, []);

  useEffect(() => {
    if (eventSport !== selectedSport) {
      fetchPastEvents(selectedSport);
      setEventSport(selectedSport);
    } 
    const maeValue = calculateMAE();
    setMae(maeValue);
  }, [selectedSport, pastEvents]);

  const calculateMAE = () => {
    // Calculate MAE between Elo Spread and Actual Spread
    const maeSum = pastEvents.reduce((sum, event) => {
      return sum + Math.abs(event.elo_spread - event.point_dif);
    }, 0);

    return maeSum / pastEvents.length;
  };

  const totalGames = pastEvents.length;
  const correctPredictions = pastEvents.filter((event) => event.result === (event.home_elo_prob > 0.5)).length;
  const percentageCorrect = (correctPredictions/totalGames)*100;
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
          Past Events 
        </h1>

        {totalGames> 0 ? <p className="flex text-center justify-center font-semibold mb-4">
          {`The system went ${correctPredictions}-${totalGames - correctPredictions} (${percentageCorrect!==null ? percentageCorrect.toFixed(2): 'N/A'}%) over the past ${totalGames} games with a Mean Average Error (MAE) of ${mae !== null ? mae.toFixed(2) : 'N/A'}`}
        </p>:<p className="flex text-center justify-center font-semibold mb-4">No Games to Show</p>}

        <div className="flex items-center justify-center mb-4">
          
          All spreads and results are based on the home team (ex. -3 home team favored by 3)


          
          </div>

        <div className="flex items-center justify-center mb-4">

          <select
            value={selectedSport}
            onChange={(e) => setSelectedSport(e.target.value)}
            className="border rounded-md p-2"
          >
            {Object.entries(SPORTS).map(([key,value ]) => (
              <option key={key} value={key}>
                {key}
              </option>
            ))}
          </select>
        </div>

        {
          loading ? (
            <div className="text-center font-semibold">
            <i className="fas fa-spinner fa-spin fa-2x"></i> {/* Replace with your loading icon */}
            <p>Loading...</p>
          </div>
          ) :
        <table className="min-w-full bg-white border border-gray-200 rounded-md overflow-hidden shadow-md">
          <thead className="bg-gray-100">
            <tr className="bg-gray-200">
              <th className="py-2 px-4 text-center">Date</th>
              <th className="py-2 px-4 text-center">Home Team</th>
              <th className="py-2 px-4 text-center">Away Team</th>
              <th className="py-2 px-4 text-center">Elo Spread</th>
              <th className="py-2 px-4 text-center">Actual Spread</th>
              <th className="py-2 px-4 text-center">Home Elo Prob</th>
              <th className="py-2 px-4 text-center">Actual Result</th>

            </tr>
          </thead>
          <tbody>
            {pastEvents.map((event, idx) => {
              const adjustedDate = new Date(event.datetime)
              const isCorrectPrediction = event.result === (event.home_elo_prob > 0.5);
              return (
              <tr key={idx} className="bg-white border-b">
                <td className="py-2 px-4 text-center">
                  {adjustedDate.toLocaleString(undefined, {
                    timeZone: userTimezone, // Specify the timezone of the incoming datetime
                    year: "numeric",
                    month: "numeric",
                    day: "numeric",
                    hour: "numeric",
                    minute: "numeric",
                    hour12: true,
                  })}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.home_team_name}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.away_team_name}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.elo_spread.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.point_dif.toFixed(2)}
                </td>
                <td className={`py-2 px-4 text-center ${isCorrectPrediction ? 'text-green-600' : 'text-red-500'}`}>
                  {event.home_elo_prob.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.result ? 1 : 0}
                </td>
              </tr>
            )})}
          </tbody>
        </table>}

      </div>
    </>
  );
}

export default PastEventsPage;
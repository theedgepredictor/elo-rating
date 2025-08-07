import { useState, useEffect } from "react";
import { SPORTS } from "../backend/consts";
import { BaseRepoReportsAPI } from "../backend/repo.js";
function EventPage() {

  const [userTimezone, setUserTimezone] = useState("UTC");
  const [loading, setLoading] = useState(true);
  const [upcomingEvents, setUpcomingEvents] = useState([]);
  const[eventSport, setEventSport] = useState(null);
  const [selectedSport, setSelectedSport] = useState('COLLEGE_BASKETBALL');
  const repoAPI = new BaseRepoReportsAPI()

async function fetchUpcomingEvents(sport) {
  setLoading(true);
  setUpcomingEvents([])

    const allUpcomingEvents = [];

    // Get the current UTC datetime
    const currentUtcDatetime = new Date().toISOString();

    // Fetch upcoming events for each sport
    const data = await repoAPI.getUpcomingForSport(SPORTS[sport]);

    if (data['events'] !== null) {
      // Filter events with datetime greater than the current UTC datetime
      const upcomingEventsForSport = data['events'].filter(
        (event) => event.datetime > currentUtcDatetime
      );

      // Concatenate events to the main array
      allUpcomingEvents.push(...upcomingEventsForSport);
    }

    // Sort events by datetime
    const sortedEvents = allUpcomingEvents.sort((a, b) =>
      a.datetime.localeCompare(b.datetime)
    );

    // Update state with the sorted and extended array
    setUpcomingEvents(sortedEvents);
  
  setLoading(false);
}

  useEffect(() => {
    // Get user's timezone
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    setUserTimezone(userTimezone);
  }, []);

  useEffect(() => {
    
    if (eventSport !== selectedSport) {
      fetchUpcomingEvents(selectedSport)
      setEventSport(selectedSport)
    }
    
  }, [selectedSport]);

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
          Upcoming Events 
        </h1>

        {upcomingEvents.length> 0 ? <p className="flex text-center justify-center font-semibold mb-4">
        </p>:<p className="flex text-center justify-center font-semibold mb-4">No Games to Show</p>}

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
              <th className="py-2 px-4 text-center">Home Elo Prob</th>
              <th className="py-2 px-4 text-center">Away Elo Prob</th>
              <th className="py-2 px-4 text-center">Home Elo Pre</th>
              <th className="py-2 px-4 text-center">Away Elo Pre</th>
              <th className="py-2 px-4 text-center">Elo Diff</th>
            </tr>
          </thead>
          <tbody>
            {upcomingEvents.map((event, idx) => {
              const adjustedDate = new Date(event.datetime)
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
                  {typeof event.elo_spread === 'number' ? event.elo_spread.toFixed(2) : ''}
                </td>
                <td className="py-2 px-4 text-center">
                  {typeof event.home_elo_prob === 'number' ? event.home_elo_prob.toFixed(2) : ''}
                </td>
                <td className="py-2 px-4 text-center">
                  {typeof event.away_elo_prob === 'number' ? event.away_elo_prob.toFixed(2) : ''}
                </td>
                <td className="py-2 px-4 text-center">
                  {typeof event.home_elo_pre === 'number' ? event.home_elo_pre.toFixed(2) : ''}
                </td>
                <td className="py-2 px-4 text-center">
                  {typeof event.away_elo_pre === 'number' ? event.away_elo_pre.toFixed(2) : ''}
                </td>
                <td className="py-2 px-4 text-center">
                  {typeof event.elo_diff === 'number' ? event.elo_diff.toFixed(2) : ''}
                </td>
              </tr>
            )})}
          </tbody>
        </table>}

      </div>
    </>
  );
}

export default EventPage;
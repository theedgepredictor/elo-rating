import { useState, useEffect } from "react";
import { useAuth } from '../context/AuthContext'
function HomePage() {
  const { upcomingEvents} = useAuth();
  const [userTimezone, setUserTimezone] = useState("UTC");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get user's timezone
    const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    setUserTimezone(userTimezone);
  }, []);
  useEffect(() => {
    setLoading(upcomingEvents.length === 0);
  }, [upcomingEvents]);

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
            <th className="py-2 px-4 text-center">Sport</th>
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
            {upcomingEvents.map((event) => {
              const adjustedDate = new Date(event.datetime)
              return (
              <tr key={event.id} className="bg-gray-200">
                <td className="py-2 px-4 text-center">{event.sport}</td>
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
                <td className="py-2 px-4 text-center">{event.home_team_name}</td>
                <td className="py-2 px-4 text-center">{event.away_team_name}</td>
                <td className="py-2 px-4 text-center">
                  {event.elo_spread.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.home_elo_prob.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.away_elo_prob.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.home_elo_pre.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.away_elo_pre.toFixed(2)}
                </td>
                <td className="py-2 px-4 text-center">
                  {event.elo_diff.toFixed(2)}
                </td>


              </tr>
            )})}
          </tbody>
        </table>}
        






      </div>
    </>
  );
}

export default HomePage;
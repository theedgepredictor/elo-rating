import { useState, useEffect } from "react";
import { useAuth } from '../context/AuthContext'
import { useParams } from "react-router-dom";
import { BaseRepoReportsAPI } from "../backend/repo.js";
import {SPORTS} from'../backend/consts.js'
function SportPage() {
    const repoAPI = new BaseRepoReportsAPI()
    const { sport } = useParams();
    const [loading, setLoading] = useState(true);
    const [systemSettings, setSystemSettings] = useState(null)
    const [teamRatings, setTeamRatings] = useState(null);



    useEffect(() => {
        fetchSystemSettings();
        fetchTeamRatings();
      }, [sport]);

    async function fetchSystemSettings() {
        try {
            setLoading(true);
            const data = await repoAPI.getSettingsForSport(SPORTS[sport]);
            setSystemSettings(data); // Assuming the API response contains the system settings
          } catch (error) {
            console.error("Error fetching system settings:", error);
          } finally {
            setLoading(false);
          }
      }
    async function fetchTeamRatings() {
    try {
        setLoading(true);
        const data = await repoAPI.getTeamRatingsForSport(SPORTS[sport]);
        setTeamRatings(data['teams']); // Assuming the API response contains the teams array
    } catch (error) {
        console.error("Error fetching team ratings:", error);
    } finally {
        setLoading(false);
    }
    }

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

        {loading ? (
          <p className="text-center">Loading...</p>
        ) : systemSettings ? (
          <div className="text-center">
            <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-8 text-center">
              {systemSettings.system_name} 
            </h1>
            <div >
            <p className="text-md font-semibold tracking-tight text-gray-700">K: {systemSettings.k}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">HFA: {systemSettings.hfa}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">STARTING ELO: {systemSettings.mean_elo}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">NUMBER OF TEAMS: {systemSettings.number_of_teams}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">NUMBER OF SEASONS: {systemSettings.number_of_seasons}</p>
            </div>
            {/* Add more system settings here */}
          </div>
        ) : (
            <div className="text-center">
            <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-8 mt-8 text-center">
            {systemSettings.system_name} 
          </h1>
          <p>No system settings found for {sport}.</p>
          </div>
        )}


        <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl mb-8 mt-12 text-center">
          Team Ratings
        </h1>

        {loading ? (
          <p>Loading...</p>
        ) : teamRatings ? (
          <table className="min-w-full bg-gray-200">
            <thead>
              <tr>
                <th className="py-2 px-4 text-center">Rank</th>
                <th className="py-2 px-4 text-center">Team Name</th>
                <th className="py-2 px-4 text-center">ELO Rating</th>
                <th className="py-2 px-4 text-center">Last Updated</th>
              </tr>
            </thead>
            <tbody>
              {teamRatings.map((team) => (
                <tr key={team.id} className="bg-gray-200">
                  <td className="py-2 px-4 text-center">{team.rank}</td>
                  <td className="py-2 px-4 text-center">{team.team_name}</td>

                  <td className="py-2 px-4 text-center">{team.elo_rating.toFixed(2)}</td>
                  <td className="py-2 px-4 text-center">{new Date(team.lastupdated).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>No team ratings found for {sport}.</p>
        )}




      </div>
    </>
  );
}

export default SportPage;
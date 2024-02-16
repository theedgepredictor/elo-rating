import { useState, useEffect } from "react";
import { useAuth } from '../context/AuthContext.jsx'
import { useParams } from "react-router-dom";
import { BaseRepoReportsAPI } from "../backend/repo.js";
import {SPORTS} from'../backend/consts.js'
function TeamRatingsPage() {
    const repoAPI = new BaseRepoReportsAPI()
    const[teamSport, setTeamSport] = useState(null);
    const [selectedSport, setSelectedSport] = useState('COLLEGE_BASKETBALL');
    const [loading, setLoading] = useState(true);
    const [systemSettings, setSystemSettings] = useState(null)
    const [teamRatings, setTeamRatings] = useState(null);



    useEffect(() => {
      if (teamSport !== selectedSport) {
        fetchSystemSettings(selectedSport)
        fetchTeamRatings(selectedSport)
        setTeamSport(selectedSport)
      }
      
    }, [selectedSport]);

    async function fetchSystemSettings(sport) {
        try {
            setLoading(true);
            setSystemSettings(null);
            const data = await repoAPI.getSettingsForSport(SPORTS[sport]);
            setSystemSettings(data); // Assuming the API response contains the system settings
          } catch (error) {
            console.error("Error fetching system settings:", error);
          } finally {
            setLoading(false);
          }
      }
    async function fetchTeamRatings(sport) {
    try {
        setLoading(true);
        setTeamRatings(null);
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

                    <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-8 text-center">
               Team Ratings
            </h1>

        <div className="flex items-center justify-center mb-4">
          
          <select
            value={selectedSport}
            onChange={(e) => setSelectedSport(e.target.value)}
            className="border rounded-md p-2"
          >
            {Object.entries(SPORTS).map(([key, value]) => (
              <option key={key} value={key}>
                {key}
              </option>
            ))}
          </select>
        </div>

        {loading ? (
                      <div className="text-center font-semibold">
                      <i className="fas fa-spinner fa-spin fa-2x"></i> {/* Replace with your loading icon */}
                      <p>Loading...</p>
                    </div>
        ) : systemSettings ? (
          <div className="text-center">

<h1 className="text-xl font-bold tracking-tight text-gray-900 sm:text-2xl mb-8 mt-12 text-center">
        System Settings
        </h1>
          

            <div >
            <p className="text-md font-semibold tracking-tight text-gray-700">K: {systemSettings.k}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">HFA: {systemSettings.hfa}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">STARTING ELO: {systemSettings.mean_elo}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">NUMBER OF TEAMS: {systemSettings.number_of_teams}</p>
            <p className="text-md font-semibold tracking-tight text-gray-700">NUMBER OF SEASONS: {systemSettings.number_of_seasons}</p>
            </div>

            <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-2xl mb-8 mt-12 text-center">
        {systemSettings.system_name}
        </h1>
            {/* Add more system settings here */}
          </div>
        ) : (
            <div className="text-center">
            <h1 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-8 mt-8 text-center">
            {selectedSport}
          </h1>
          <p>No system settings found for {selectedSport}.</p>
          </div>
        )}




        {loading ? (
                      <div className="text-center font-semibold">
                      <i className="fas fa-spinner fa-spin fa-2x"></i> {/* Replace with your loading icon */}
                      <p>Loading...</p>
                    </div>
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
                <tr key={team.rank} className="bg-white border-b">
                  <td className="py-2 px-4 text-center">{team.rank}</td>
                  <td className="py-2 px-4 text-center">{team.team_name}</td>
                  <td className="py-2 px-4 text-center">{team.elo_rating.toFixed(2)}</td>
                  <td className="py-2 px-4 text-center">{new Date(team.lastupdated).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
            <div className="text-center">
          <p>No team ratings found for {selectedSport}.</p>
          </div>
        )}




      </div>
    </>
  );
}

export default TeamRatingsPage;



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
  const [upcomingEvents, setUpcomingEvents] = useState([]);
async function fetchUpcomingSports() {
  setLoading(true);
  if (upcomingEvents.length === 0) {
    const allUpcomingEvents = [];

    // Get the current UTC datetime
    const currentUtcDatetime = new Date().toISOString();

    // Fetch upcoming events for each sport
    for (const sport in SPORTS) {
      const data = await repoAPI.getUpcomingForSport(SPORTS[sport]);

      if (data['events'] !== null) {
        // Filter events with datetime greater than the current UTC datetime
        const upcomingEventsForSport = data['events'].filter(
          (event) => event.datetime > currentUtcDatetime
        );

        // Add sport name to each record
        const eventsWithSport = upcomingEventsForSport.map((event) => ({
          ...event,
          sport: sport,
        }));

        // Concatenate events to the main array
        allUpcomingEvents.push(...eventsWithSport);
      }
    }

    // Sort events by datetime
    const sortedEvents = allUpcomingEvents.sort((a, b) =>
      a.datetime.localeCompare(b.datetime)
    );

    // Update state with the sorted and extended array
    setUpcomingEvents(sortedEvents);
  }
  setLoading(false);
}

  useEffect(() => {
    
    fetchUpcomingSports()
    setLoading(false)
  }, []);

  const value = {
    error,
    setError,
    upcomingEvents
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
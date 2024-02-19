export class BaseRepoReportsAPI {
    constructor() {
      this.baseUrl = 'https://raw.githubusercontent.com/theedgepredictor/elo-rating/main/data/reports'
    }
  
    async get(endpoint, options = {}) {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
      });
      if (!response.ok) {
        throw new Error('Request failed');
      }
  
      return await response.json();
    }
  
    async getUpcomingForSport(sport) {
        const endpoint = `/${sport}/upcoming_event_ratings.json`;
        return this.get(endpoint);
    }

    async getPastForSport(sport) {
      const endpoint = `/${sport}/previous_event_ratings.json`;
      return this.get(endpoint);
  }

    async getEvaluationForSport(sport) {
        const endpoint = `/${sport}/system_evaluation.json`;
        return this.get(endpoint);
      }

    async getSettingsForSport(sport) {
        const endpoint = `/${sport}/system_settings.json`;
        return this.get(endpoint);
    }

    async getTeamRatingsForSport(sport) {
        const endpoint = `/${sport}/team_ratings.json`;
        return this.get(endpoint);
    }
  }
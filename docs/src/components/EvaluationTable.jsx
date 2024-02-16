

export const EvaluationTable = ({ data, title }) => {
    const metricNames = ['system_records','system_accuracy', 'system_mae','system_brier_score','avg_number_of_games_played','avg_points_per_game','home_win_percentage']
    const metricsDict = {
        'system_records':'Games',
        'system_accuracy': 'ACCURACY',
        'system_mae': 'MEAN AVERAGE ERROR',
        'avg_number_of_games_played':'AVG Games Played',
        'avg_points_per_game':'AVG Points Per Game',
        'home_win_percentage':'Home Win Percentage',
        'system_brier_score': 'BRIER SCORE'}
    return (
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-gray-900 sm:text-4xl mb-8 text-center">{title}</h2>
        <table className="min-w-full bg-white border border-gray-200 rounded-md overflow-hidden shadow-md mb-10">
        <thead className="bg-gray-100">
        <tr className="bg-gray-200 border-b">
              <th className="py-2 px-4 text-center text-lg">Sport</th>
              {metricNames.map((metric) => (
                <th className="py-2 px-4 text-center text-md" key={metric}>{metricsDict[metric]}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr className="bg-white border-b" key={row.sport}>
                <td className="bg-gray-200 py-2 px-4 text-center font-bold">{row.sport}</td>
                {metricNames.map((metric) => (
                  <td className="py-2 px-4 text-center" key={metric}>{metric==='system_records'? row[metric]:row[metric].toFixed(2) }</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

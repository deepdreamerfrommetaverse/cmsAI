import React, { useEffect, useState } from 'react';
import axios from 'axios';
import StatsSourcesPie from '../components/StatsSourcesPie';
import StatsCtrBar from '../components/StatsCtrBar';
import StatsPromLink from '../components/StatsPromLink';

const Stats: React.FC = () => {
  const [summary, setSummary] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await axios.get('/api/analytics/summary');
        setSummary(res.data);
      } catch (err) {
        console.error('Failed to fetch analytics summary', err);
        setError('Failed to load statistics');
      }
    };
    fetchSummary();
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Site Statistics</h1>
      {error && <p className="text-red-500">{error}</p>}
      {summary ? (
        <div className="space-y-4">
          <div>Total Page Views: <span className="font-semibold">{summary.total_page_views}</span></div>
          <div>Total Articles: <span className="font-semibold">{summary.total_articles}</span></div>
          <div>Published Articles: <span className="font-semibold">{summary.published_articles}</span></div>
          <div className="mt-4 flex flex-col md:flex-row md:space-x-8">
            <div>
              <h3 className="font-semibold mb-1">Views by Source</h3>
              <StatsSourcesPie sources={summary.views_by_source || {}} />
            </div>
            <div className="mt-4 md:mt-0">
              <h3 className="font-semibold mb-1">Click-Through Rate</h3>
              <StatsCtrBar ctr={0} />
            </div>
          </div>
          <div className="mt-4">
            <h3 className="font-semibold mb-1">Promotional Link</h3>
            <StatsPromLink />
          </div>
        </div>
      ) : (
        !error && <p>Loading stats...</p>
      )}
    </div>
  );
};
export default Stats;

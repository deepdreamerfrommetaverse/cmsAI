import { useEffect, useState } from 'react';
import axios from 'axios';

const DailySocialLimits: React.FC = () => {
  const [limits, setLimits] = useState<{twitter_used: number, twitter_limit: number, instagram_used: number, instagram_limit: number} | null>(null);

  const fetchLimits = async () => {
    try {
      const res = await axios.get('/api/analytics/summary');
      // Assuming summary includes social usage or adapt if separate endpoint
      if (res.data) {
        // Here we use published_articles as used for Twitter and maybe a field for IG usage
        const twitter_used = res.data.events_by_type?.twitter_post || 0;
        const twitter_limit = res.data.twitter_daily_limit || 0;
        const instagram_used = res.data.events_by_type?.instagram_post || 0;
        const instagram_limit = res.data.instagram_daily_limit || 0;
        setLimits({ twitter_used, twitter_limit, instagram_used, instagram_limit });
      }
    } catch (err) {
      console.error("Failed to fetch social limits", err);
    }
  };

  useEffect(() => {
    fetchLimits();
    const interval = setInterval(fetchLimits, 60000); // refresh every 60s
    return () => clearInterval(interval);
  }, []);

  if (!limits) return <div className="text-sm">Loading social limits...</div>;
  return (
    <div className="text-sm">
      <div>Twitter posts today: {limits.twitter_used} / {limits.twitter_limit}</div>
      <div>Instagram posts today: {limits.instagram_used} / {limits.instagram_limit}</div>
    </div>
  );
};

export default DailySocialLimits;

// This might display a bar chart for CTR. We use placeholder content for now.
const StatsCtrBar: React.FC<{ ctr?: number }> = ({ ctr }) => {
  const value = ctr || 0;
  return (
    <div>
      <div className="text-sm">CTR: {value}%</div>
      <div className="w-full bg-gray-300 dark:bg-gray-700 h-2 rounded">
        <div className="bg-primary h-2 rounded" style={{ width: `${value}%` }}></div>
      </div>
    </div>
  );
};
export default StatsCtrBar;

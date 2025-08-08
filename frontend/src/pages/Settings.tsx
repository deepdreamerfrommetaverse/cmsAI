import React from 'react';
import { useThemeConfig } from '@/context/ThemeConfigContext';
import { useStripe } from '@/hooks/useStripe';

const Settings: React.FC = () => {
  const { darkMode, toggleTheme } = useThemeConfig();
  const { revenue, error } = useStripe();

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">Appearance</h2>
        <button onClick={toggleTheme} className="px-3 py-1 rounded bg-gray-300 dark:bg-gray-700">
          Switch to {darkMode ? 'Light' : 'Dark'} Mode
        </button>
      </div>
      <div className="mb-4">
        <h2 className="text-xl font-semibold mb-2">Stripe Integration</h2>
        {error ? (
          <p className="text-red-500">{error}</p>
        ) : revenue ? (
          <p>Current Revenue: <span className="font-semibold">{revenue.total} {revenue.currency}</span></p>
        ) : (
          <p>Loading revenue...</p>
        )}
      </div>
      {/* Additional settings (API keys management etc.) could be added here */}
    </div>
  );
};
export default Settings;

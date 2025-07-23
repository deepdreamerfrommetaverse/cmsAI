import { NavLink } from 'react-router-dom';
import { useThemeConfig } from '../context/ThemeConfigContext';
import { useAuth } from '../context/AuthContext';
import { FaBolt, FaImages, FaHistory, FaChartPie, FaThLarge, FaRobot, FaCog, FaCommentDots, FaMoon, FaSun } from 'react-icons/fa';

const Sidebar: React.FC = () => {
  const { darkMode, toggleTheme } = useThemeConfig();
  const { logout } = useAuth();
  const linkClasses = ({ isActive }: { isActive: boolean }) =>
    `flex items-center p-3 mb-1 rounded-lg hover:bg-gray-200 hover:dark:bg-gray-700 
     ${isActive ? 'bg-gray-200 dark:bg-gray-700 font-semibold' : ''}`;

  return (
    <aside className="w-64 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 flex flex-col p-4">
      <h2 className="text-xl font-bold mb-6">AI CMS</h2>
      <nav className="flex-1">
        <NavLink to="/generator" className={linkClasses}>
          <FaBolt className="mr-2" /> Generator
        </NavLink>
        <NavLink to="/prompt-agent" className={linkClasses}>
          <FaRobot className="mr-2"/> Prompt Agent
        </NavLink>
        <NavLink to="/gallery" className={linkClasses}>
          <FaImages className="mr-2"/> Gallery
        </NavLink>
        <NavLink to="/history" className={linkClasses}>
          <FaHistory className="mr-2"/> History
        </NavLink>
        <NavLink to="/stats" className={linkClasses}>
          <FaChartPie className="mr-2"/> Stats
        </NavLink>
        <NavLink to="/bricks-pages" className={linkClasses}>
          <FaThLarge className="mr-2"/> Bricks Pages
        </NavLink>
        <NavLink to="/feedback" className={linkClasses}>
          <FaCommentDots className="mr-2"/> Feedback
        </NavLink>
        <NavLink to="/settings" className={linkClasses}>
          <FaCog className="mr-2"/> Settings
        </NavLink>
      </nav>
      <div className="mt-4 pt-4 border-t border-gray-300 dark:border-gray-700">
        <button onClick={toggleTheme} className="flex items-center w-full mb-2 text-sm">
          {darkMode ? <FaSun className="mr-2"/> : <FaMoon className="mr-2"/>}
          Toggle {darkMode ? 'Light' : 'Dark'} Mode
        </button>
        <button onClick={logout} className="flex items-center w-full text-sm">
          <svg className="mr-2" fill="currentColor" viewBox="0 0 20 20" width="16" height="16"><path fillRule="evenodd" d="M3 4a1 1 0 011-1h6a1 1 0 110 2H5v10h5a1 1 0 110 2H4a1 1 0 01-1-1V4zm9.707 5.293a1 1 0 00-1.414 1.414L13.586 12H8a1 1 0 100 2h5.586l-2.293 2.293a1 1 0 101.414 1.414l4-4a1 1 0 000-1.414l-4-4z" clipRule="evenodd"/></svg>
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;

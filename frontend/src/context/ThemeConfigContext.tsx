import React, { createContext, useContext, useEffect, useState } from 'react';

interface ThemeContextType {
  darkMode: boolean;
  toggleTheme: () => void;
}

const ThemeConfigContext = createContext<ThemeContextType>({} as ThemeContextType);

export const ThemeConfigProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [darkMode, setDarkMode] = useState<boolean>(
    () => localStorage.getItem('theme') === 'dark' || true  // default dark
  );

  useEffect(() => {
    // Apply or remove 'dark' class on html element
    const htmlEl = document.documentElement;
    if (darkMode) {
      htmlEl.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      htmlEl.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  }, [darkMode]);

  const toggleTheme = () => setDarkMode(prev => !prev);

  return (
    <ThemeConfigContext.Provider value={{ darkMode, toggleTheme }}>
      {children}
    </ThemeConfigContext.Provider>
  );
};

export const useThemeConfig = () => useContext(ThemeConfigContext);

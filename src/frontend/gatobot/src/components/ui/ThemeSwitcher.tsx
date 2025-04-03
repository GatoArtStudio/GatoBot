import React, { useEffect, useState } from 'react';

const ThemeSwitcher: React.FC = () => {
    const [theme, setTheme] = useState<'light' | 'dark'>('dark');

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme((prevTheme) => (prevTheme === 'light' ? 'dark' : 'light'));
    };

    return (
        <button
            onClick={toggleTheme}
            className="px-4 py-2 rounded-lg text-text-100 bg-primary-700 hover:bg-primary-700/90 transition-all duration-300 ease-in-out hover:shadow-primary-700/50 hover:shadow-lg">
            Cambiar tema
        </button>
    );
};

export default ThemeSwitcher;
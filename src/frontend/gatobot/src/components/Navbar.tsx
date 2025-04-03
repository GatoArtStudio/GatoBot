import React from 'react';
import ThemeSwitcher from './ui/ThemeSwitcher';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-gradient-to-r from-background-100 via-background-200 to-background-50 text-text-900 py-4 px-6 shadow-[0_4px_30px_rgba(45,212,191,0.1)]">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <img src="/logo.svg" alt="GatoBot" className="w-8 h-8" />
          <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-700 to-accent-500">
            GatoBot
          </span>
        </div>
        
        <div className="flex items-center space-x-4">
          <a href="/dashboard" 
             className="px-4 py-2 rounded-lg text-text-100 bg-primary-700 hover:bg-primary-700/90 transition-all duration-300 ease-in-out hover:shadow-primary-700/50 hover:shadow-lg">
            Dashboard
          </a>
          <a href="https://discord.com/oauth2/authorize?client_id=1108545284264431656"
             target="_blank"
             className="py-2 px-4 rounded-lg text-text-900 bg-secondary-300 hover:bg-secondary-300 transition-all duration-300 ease-in-out hover:shadow-secondary-300/50 hover:shadow-lg">
            Agregar al Servidor
          </a>
          <a href="https://discord.gg/vEmfU2REYF" 
             target="_blank"
             className="px-4 py-2 rounded-lg text-text-900 bg-secondary-300 hover:bg-secondary-300 transition-all duration-300 ease-in-out hover:shadow-secondary-300/50 hover:shadow-lg">
            Soporte
          </a>
          <button
          onClick={() => window.location.href = 'https://gatobot.gatoartstudio.art/discord/login'}
          className="px-4 py-2 rounded-lg text-text-100 bg-gradient-to-r from-primary-700 to-accent-500 hover:from-primary-700 hover:to-accent-500 transition-all duration-300 ease-in-out hover:shadow-primary-700/50 hover:shadow-lg">
            Login
          </button>
          <ThemeSwitcher />
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

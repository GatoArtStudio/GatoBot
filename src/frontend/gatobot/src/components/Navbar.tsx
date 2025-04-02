import React from 'react';

const Navbar: React.FC = () => {
  return (
    <nav className="bg-gradient-to-r from-[#0a0920] via-[#1a1f3c] to-[#0a0920] text-white py-4 px-6 shadow-[0_4px_30px_rgba(45,212,191,0.1)]">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <img src="/logo.svg" alt="GatoBot" className="w-8 h-8" />
          <span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-teal-400 to-cyan-400">
            GatoBot
          </span>
        </div>
        
        <div className="flex items-center space-x-4">
          <a href="/dashboard" 
             className="px-4 py-2 rounded-lg bg-teal-500 hover:bg-teal-600 transition-all duration-300 ease-in-out hover:shadow-[0_0_15px_rgba(45,212,191,0.3)]">
            Dashboard
          </a>
          <a href="https://discord.com/oauth2/authorize?client_id=1108545284264431656"
             target="_blank"
             className="px-4 py-2 rounded-lg bg-cyan-500 hover:bg-cyan-600 transition-all duration-300 ease-in-out hover:shadow-[0_0_15px_rgba(34,211,238,0.3)]">
            Agregar al Servidor
          </a>
          <a href="https://discord.gg/vEmfU2REYF" 
             target="_blank"
             className="px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-600 transition-all duration-300 ease-in-out hover:shadow-[0_0_15px_rgba(14,165,233,0.3)]">
            Soporte
          </a>
          <button
          onClick={() => window.location.href = 'https://gatobot.gatoartstudio.art/discord/login'}
          className="px-4 py-2 rounded-lg bg-gradient-to-r from-teal-400 to-cyan-400 hover:from-teal-500 hover:to-cyan-500 transition-all duration-300 ease-in-out hover:shadow-[0_0_15px_rgba(45,212,191,0.3)]">
            Login
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

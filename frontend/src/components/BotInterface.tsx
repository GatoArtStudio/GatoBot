import React, { useState, useEffect } from 'react';

interface Command {
  name: string;
  description: string;
  usage?: string;
}

interface BotStatus {
  status: string;
  uptime: string | null;
  guild_count: number;
}

const BotInterface: React.FC = () => {
  const [status, setStatus] = useState<BotStatus | null>(null);
  const [commands, setCommands] = useState<Command[]>([]);

  useEffect(() => {
    const fetchBotData = async () => {
      try {
        const statusResponse = await fetch('/api/status');
        const statusData = await statusResponse.json();
        setStatus(statusData);

        const commandsResponse = await fetch('/api/commands');
        const commandsData = await commandsResponse.json();
        setCommands(commandsData);
      } catch (error) {
        console.error('Error fetching bot data:', error);
      }
    };

    fetchBotData();
    const interval = setInterval(fetchBotData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Estado del Bot */}
      <div className="bg-gradient-to-br from-[#0a0920] via-[#1a1f3c] to-[#0a0920] rounded-2xl shadow-[0_4px_30px_rgba(45,212,191,0.1)] p-8 mb-8 backdrop-blur-xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-white">Estado del Bot</h2>
          <div className="flex items-center space-x-3">
            <span className={`inline-block w-3 h-3 rounded-full ${
              status?.status === 'online' ? 'bg-teal-400 shadow-[0_0_10px_rgba(45,212,191,0.5)]' : 'bg-red-400 shadow-[0_0_10px_rgba(239,68,68,0.5)]'
            } animate-pulse`}></span>
            <span className="text-white opacity-90">{status?.status}</span>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-[#1a1f3c]/30 backdrop-blur-lg rounded-xl p-6 border border-teal-500/10">
            <h3 className="text-lg font-semibold text-teal-400 mb-2">Tiempo Activo</h3>
            <p className="text-2xl text-white">{status?.uptime || 'No disponible'}</p>
          </div>
          <div className="bg-[#1a1f3c]/30 backdrop-blur-lg rounded-xl p-6 border border-cyan-500/10">
            <h3 className="text-lg font-semibold text-cyan-400 mb-2">Servidores de Discord</h3>
            <p className="text-2xl text-white">{status?.guild_count || 0}</p>
          </div>
        </div>
      </div>

      {/* Comandos */}
      <div className="bg-gradient-to-br from-[#0a0920] via-[#1a1f3c] to-[#0a0920] rounded-2xl shadow-[0_4px_30px_rgba(45,212,191,0.1)] p-8 backdrop-blur-xl">
        <h2 className="text-3xl font-bold text-white mb-8">Comandos Disponibles</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {commands.map((command) => (
            <div key={command.name} 
                 className="bg-[#1a1f3c]/30 backdrop-blur-lg rounded-xl p-6 border border-teal-500/10 hover:border-teal-500/30 transition-all duration-300 ease-in-out hover:shadow-[0_0_15px_rgba(45,212,191,0.1)]">
              <h3 className="text-xl font-semibold text-teal-400 mb-2">/{command.name}</h3>
              <p className="text-white/80">{command.description}</p>
              {command.usage && (
                <p className="mt-2 text-sm text-cyan-400">
                  Uso: {command.usage}
                </p>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BotInterface;

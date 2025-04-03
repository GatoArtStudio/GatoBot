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
        const statusResponse = await fetch('/api/v1/status');
        const statusData = await statusResponse.json();
        setStatus(statusData);

        const commandsResponse = await fetch('/api/v1/commands');
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
      <div className="bg-gradient-to-br from-background-100 via-background-200 to-background-50 rounded-2xl shadow-background-200 shadow-lg p-8 mb-8 backdrop-blur-xl">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-text-900">Estado del Bot</h2>
          <div className="flex items-center space-x-3">
            <span className={`inline-block w-3 h-3 rounded-full ${
              status?.status === 'online' ? 'bg-accent-600' : 'bg-red-400 shadow-[0_0_10px_rgba(239,68,68,0.5)]'
            } animate-pulse`}></span>
            <span className="text-text-900 opacity-90">{status?.status}</span>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-background-100/30 backdrop-blur-lg rounded-xl p-6 border border-secondary-300/10">
            <h3 className="text-lg font-semibold text-accent-600 mb-2">Tiempo Activo</h3>
            <p className="text-2xl text-text-900">{status?.uptime || 'No disponible'}</p>
          </div>
          <div className="bg-background-100/30 backdrop-blur-lg rounded-xl p-6 border border-secondary-300/10">
            <h3 className="text-lg font-semibold text-accent-500 mb-2">Servidores de Discord</h3>
            <p className="text-2xl text-text-900">{status?.guild_count || 0}</p>
          </div>
        </div>
      </div>

      {/* Comandos */}
      <div className="bg-gradient-to-br from-background-100 via-background-200 to-background-50 rounded-2xl shadow-background-200 shadow-lg p-8 backdrop-blur-xl">
        <h2 className="text-3xl font-bold text-text-900 mb-8">Comandos Disponibles</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {commands.map((command) => (
            <div key={command.name} 
                 className="bg-background-100 backdrop-blur-lg rounded-xl p-6 border border-accent-200/10 hover:border-accent-200/30 transition-all duration-300 ease-in-out hover:shadow-secondary-300 hover:shadow-lg">
              <h3 className="text-xl font-semibold text-accent-500 mb-2">/{command.name}</h3>
              <p className="text-text-900/80">{command.description}</p>
              {command.usage && (
                <p className="mt-2 text-sm text-accent-600">
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

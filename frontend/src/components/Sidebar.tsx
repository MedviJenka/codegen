import React, { useState } from 'react';
import { Plus, X, Brain, Cpu, Bot, Sparkles } from 'lucide-react';
import useAgentStore from '../store/agentStore';
import useFlowStore from '../store/flowStore';
import { Agent } from '../types';
import { v4 as uuidv4 } from 'uuid';

const agentColors = [
  'bg-blue-500',
  'bg-green-500',
  'bg-purple-500',
  'bg-yellow-500',
  'bg-pink-500',
  'bg-indigo-500',
  'bg-red-500',
  'bg-teal-500',
];

// Predefined agent names
const agentNames = [
  "Research Assistant",
  "Data Analyst",
  "Content Writer",
  "Customer Support",
  "Code Generator",
  "Legal Advisor",
  "Financial Planner",
  "Marketing Specialist",
  "Product Manager",
  "Creative Director"
];

const agentIcons = [
  { name: 'Brain', icon: Brain },
  { name: 'Cpu', icon: Cpu },
  { name: 'Bot', icon: Bot },
  { name: 'Sparkles', icon: Sparkles },
];

const Sidebar: React.FC = () => {
  const { agents, addAgent, removeAgent } = useAgentStore();
  const { addNode, iconSize } = useFlowStore();
  const [isAddingAgent, setIsAddingAgent] = useState(false);
  const [newAgent, setNewAgent] = useState<Partial<Agent>>({
    name: agentNames[0],
    role: '',
    goal: '',
    color: agentColors[0],
  });
  const [dragging, setDragging] = useState<string | null>(null);

  const handleAddAgent = () => {
    if (!newAgent.name) return;

    const agent: Agent = {
      id: uuidv4(),
      name: newAgent.name,
      role: newAgent.role || 'Assistant', // Default role if empty
      goal: newAgent.goal || '',
      color: newAgent.color || agentColors[0],
      position: { x: 100, y: 100 },
    };

    addAgent(agent);
    
    // Also add to flow
    addNode({
      id: agent.id,
      type: 'agent',
      data: { agent },
      position: { x: 250, y: 100 },
    });

    setNewAgent({ name: agentNames[0], role: '', goal: '', color: agentColors[0] });
    setIsAddingAgent(false);
  };

  const handleDragStart = (id: string) => {
    setDragging(id);
  };

  const handleDragEnd = () => {
    setDragging(null);
  };

  return (
    <div className="w-80 bg-gray-900 text-white h-full overflow-y-auto p-4 flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">AI Agents</h2>
        <button
          onClick={() => setIsAddingAgent(!isAddingAgent)}
          className="p-2 rounded-full bg-blue-600 hover:bg-blue-700 transition-colors"
        >
          {isAddingAgent ? <X size={20} /> : <Plus size={20} />}
        </button>
      </div>

      {isAddingAgent && (
        <div className="bg-gray-800 p-4 rounded-lg mb-4">
          <h3 className="text-lg font-semibold mb-3">New Agent</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm mb-1">Name *</label>
              <select
                value={newAgent.name}
                onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                className="w-full bg-gray-700 rounded p-2 text-white"
              >
                {agentNames.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm mb-1">Role (optional)</label>
              <input
                type="text"
                value={newAgent.role}
                onChange={(e) => setNewAgent({ ...newAgent, role: e.target.value })}
                className="w-full bg-gray-700 rounded p-2 text-white"
                placeholder="Agent role"
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Goal (optional)</label>
              <textarea
                value={newAgent.goal}
                onChange={(e) => setNewAgent({ ...newAgent, goal: e.target.value })}
                className="w-full bg-gray-700 rounded p-2 text-white"
                placeholder="Agent goal"
                rows={3}
              />
            </div>
            <div>
              <label className="block text-sm mb-1">Color</label>
              <div className="flex flex-wrap gap-2">
                {agentColors.map((color) => (
                  <button
                    key={color}
                    className={`w-6 h-6 rounded-full ${color} ${
                      newAgent.color === color ? 'ring-2 ring-white' : ''
                    }`}
                    onClick={() => setNewAgent({ ...newAgent, color })}
                  />
                ))}
              </div>
            </div>
            <button
              onClick={handleAddAgent}
              className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded font-medium transition-colors"
            >
              Create Agent
            </button>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        {agents.length === 0 ? (
          <div className="text-center text-gray-400 py-8">
            <p>No agents created yet</p>
            <p className="text-sm">Click the + button to create your first agent</p>
          </div>
        ) : (
          <div className="space-y-3">
            {agents.map((agent, index) => {
              const IconComponent = agentIcons[index % agentIcons.length].icon;
              return (
                <div
                  key={agent.id}
                  className={`bg-gray-800 rounded-lg p-3 flex flex-col ${dragging === agent.id ? 'border-2 border-blue-400' : ''}`}
                  draggable
                  onDragStart={() => handleDragStart(agent.id)}
                  onDragEnd={handleDragEnd}
                >
                  <div className="flex items-center mb-2">
                    <div className={`w-10 h-10 rounded-full ${agent.color} flex items-center justify-center mr-3`}>
                      <IconComponent size={iconSize * 0.6} />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-medium">{agent.name}</h3>
                      <p className="text-sm text-gray-400">{agent.role}</p>
                    </div>
                    <button
                      onClick={() => removeAgent(agent.id)}
                      className="text-gray-400 hover:text-red-500"
                    >
                      <X size={18} />
                    </button>
                  </div>
                  {agent.goal && (
                    <p className="text-sm text-gray-300 mb-2 line-clamp-2">{agent.goal}</p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';
import { AgentState, Agent } from '../types';

const useAgentStore = create<AgentState>((set) => ({
  agents: [],
  addAgent: (agent: Agent) => 
    set((state) => ({ 
      agents: [...state.agents, { ...agent, id: agent.id || uuidv4() }] 
    })),
  updateAgent: (id: string, data: Partial<Agent>) =>
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, ...data } : agent
      ),
    })),
  removeAgent: (id: string) =>
    set((state) => ({
      agents: state.agents.filter((agent) => agent.id !== id),
    })),
}));

export default useAgentStore;
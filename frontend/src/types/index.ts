export interface Agent {
  id: string;
  name: string;
  role: string;
  goal: string;
  color: string;
  position: {
    x: number;
    y: number;
  };
}

export interface Node {
  id: string;
  type: 'agent' | 'decision';
  data: {
    agent?: Agent;
    label: string;
  };
  position: {
    x: number;
    y: number;
  };
}

export interface Edge {
  id: string;
  source: string;
  target: string;
  label?: string;
}

export interface FlowState {
  nodes: Node[];
  edges: Edge[];
  iconSize: number;
  addNode: (node: Node) => void;
  updateNode: (id: string, data: Partial<Node>) => void;
  removeNode: (id: string) => void;
  addEdge: (edge: Edge) => void;
  updateEdge: (id: string, data: Partial<Edge>) => void;
  removeEdge: (id: string) => void;
  setIconSize: (size: number) => void;
}

export interface AgentState {
  agents: Agent[];
  addAgent: (agent: Agent) => void;
  updateAgent: (id: string, data: Partial<Agent>) => void;
  removeAgent: (id: string) => void;
}
import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';
import { FlowState, Node, Edge } from '../types';

const useFlowStore = create<FlowState>((set) => ({
  nodes: [],
  edges: [],
  iconSize: 24, // Default icon size
  addNode: (node: Node) =>
    set((state) => ({
      nodes: [...state.nodes, { ...node, id: node.id || uuidv4() }],
    })),
  updateNode: (id: string, data: Partial<Node>) =>
    set((state) => ({
      nodes: state.nodes.map((node) =>
        node.id === id ? { ...node, ...data } : node
      ),
    })),
  removeNode: (id: string) =>
    set((state) => ({
      nodes: state.nodes.filter((node) => node.id !== id),
      edges: state.edges.filter(
        (edge) => edge.source !== id && edge.target !== id
      ),
    })),
  addEdge: (edge: Edge) =>
    set((state) => ({
      edges: [...state.edges, { ...edge, id: edge.id || uuidv4() }],
    })),
  updateEdge: (id: string, data: Partial<Edge>) =>
    set((state) => ({
      edges: state.edges.map((edge) =>
        edge.id === id ? { ...edge, ...data } : edge
      ),
    })),
  removeEdge: (id: string) =>
    set((state) => ({
      edges: state.edges.filter((edge) => edge.id !== id),
    })),
  setIconSize: (size: number) =>
    set(() => ({
      iconSize: size,
    })),
}));

export default useFlowStore;
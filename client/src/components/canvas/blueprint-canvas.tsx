import {
  Background,
  Controls,
  type Node,
  type Edge,
  OnNodesChange,
  OnEdgesChange,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  ReactFlow,
  Connection,
} from 'reactflow';
import {
  useState,
  useCallback,
  useEffect,
  forwardRef,
  useImperativeHandle
} from 'react';
import { customNodes } from './node-types';
import { useAgentTypes } from '@/lib/agent-config';
import { Code } from 'lucide-react';

interface BlueprintCanvasProps {
  onNodeSelect?: (node: Node | null) => void;
  onNodesChange?: (nodes: Node[]) => void;
  onEdgesChange?: (edges: Edge[]) => void;
}

interface XYPosition {
  x: number;
  y: number;
}

const BlueprintCanvas = forwardRef(({ onNodeSelect, onNodesChange, onEdgesChange }: BlueprintCanvasProps, ref) => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const { data: agentTypeConfig } = useAgentTypes();
  const [connectionStartHandle, setConnectionStartHandle] = useState<{
    nodeId: string;
    handleId: string;
  } | null>(null);

  const handleNodesChange: OnNodesChange = useCallback(
    (changes) => {
      const newNodes = applyNodeChanges(changes, nodes);
      setNodes(newNodes);
      onNodesChange?.(newNodes);
    },
    [nodes, onNodesChange]
  );

  const handleEdgesChange: OnEdgesChange = useCallback(
    (changes) => {
      const newEdges = applyEdgeChanges(changes, edges);
      setEdges(newEdges);
      onEdgesChange?.(newEdges);
    },
    [edges, onEdgesChange]
  );

  const wouldCreateCycle = (newConnection: Connection, existingEdges: Edge[]) => {
    const visited = new Set<string>();
    const temp = new Set<string>();
    const graph = new Map<string, string[]>();

    existingEdges.forEach(edge => {
      if (!graph.has(edge.source)) {
        graph.set(edge.source, []);
      }
      graph.get(edge.source)!.push(edge.target);
    });

    if (!graph.has(newConnection.source!)) {
      graph.set(newConnection.source!, []);
    }
    graph.get(newConnection.source!)!.push(newConnection.target!);

    const hasCycle = (node: string): boolean => {
      if (temp.has(node)) return true;
      if (visited.has(node)) return false;

      temp.add(node);
      visited.add(node);

      const neighbors = graph.get(node) || [];
      for (const neighbor of neighbors) {
        if (hasCycle(neighbor)) return true;
      }

      temp.delete(node);
      return false;
    };

    const result = hasCycle(newConnection.source!);
    graph.get(newConnection.source!)!.pop();
    return result;
  };

  const onConnect = useCallback((params: Connection) => {
    if (wouldCreateCycle(params, edges)) {
      return;
    }
    setEdges((eds) => addEdge(
      {
        ...params,
        type: 'smoothstep',
        style: { stroke: '#ffffff', strokeWidth: 2 }
      },
      eds
    ));
    setConnectionStartHandle(null);
  }, [edges]);

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    onNodeSelect?.(node);
  }, [onNodeSelect]);

  const onPaneClick = useCallback(() => {
    onNodeSelect?.(null);
    setConnectionStartHandle(null);
  }, [onNodeSelect]);

  const onHandleClick = useCallback(
    (nodeId: string, handleId: string, isTarget: boolean) => {
      if (!connectionStartHandle) {
        if (!isTarget) {
          setConnectionStartHandle({ nodeId, handleId });
        }
      } else {
        if (isTarget && connectionStartHandle.nodeId !== nodeId) {
          onConnect({
            source: connectionStartHandle.nodeId,
            target: nodeId,
            sourceHandle: connectionStartHandle.handleId,
            targetHandle: handleId,
          });
        } else {
          setConnectionStartHandle(null);
        }
      }
    },
    [connectionStartHandle, onConnect]
  );

  const createDecisionPaths = useCallback((parentNode: Node | null, parentPosition: XYPosition) => {
    const decisionId = `decision-${Date.now()}`;
    const yesId = `yes-${Date.now()}`;
    const noId = `no-${Date.now()}`;

    const decisionNode: Node = {
      id: decisionId,
      type: 'decision',
      position: parentPosition,
      data: {
        label: 'Decision Point',
        color: '#FF4B6B',
        onHandleClick
      },
    };

    // Default icon for split nodes if agentTypeConfig is not loaded yet
    const defaultIcon = Code;

    const yesNode: Node = {
      id: yesId,
      type: 'agent',
      position: {
        x: parentPosition.x - 150,
        y: parentPosition.y + 150
      },
      data: {
        label: 'Yes Path',
        type: 'Code Gen Crew',
        role: 'Execute positive outcome tasks',
        goal: 'Handle workflow when condition is true',
        color: '#22C55E',
        canSplit: true,
        onHandleClick,
        canEdit: true,
        icon: agentTypeConfig?.["Code Gen Crew"]?.icon || defaultIcon,
        isSmall: true,
      },
    };

    const noNode: Node = {
      id: noId,
      type: 'agent',
      position: {
        x: parentPosition.x + 150,
        y: parentPosition.y + 150
      },
      data: {
        label: 'No Path',
        type: 'Code Gen Crew',
        role: 'Execute negative outcome tasks',
        goal: 'Handle workflow when condition is false',
        color: '#DC2626',
        canSplit: true,
        onHandleClick,
        canEdit: true,
        icon: agentTypeConfig?.["Code Gen Crew"]?.icon || defaultIcon,
        isSmall: true,
      },
    };

    const newEdges: Edge[] = [
      {
        id: `e-${decisionId}-${yesId}`,
        source: decisionId,
        target: yesId,
        type: 'smoothstep',
        style: { stroke: '#ffffff', strokeWidth: 2 }
      },
      {
        id: `e-${decisionId}-${noId}`,
        source: decisionId,
        target: noId,
        type: 'smoothstep',
        style: { stroke: '#ffffff', strokeWidth: 2 }
      }
    ];

    if (parentNode && parentNode.id !== decisionId) {
      newEdges.unshift({
        id: `e-${parentNode.id}-${decisionId}`,
        source: parentNode.id,
        target: decisionId,
        type: 'smoothstep',
        style: { stroke: '#ffffff', strokeWidth: 2 }
      });
    }

    return { nodes: [decisionNode, yesNode, noNode], edges: newEdges };
  }, [onHandleClick, agentTypeConfig]);

  const splitNode = useCallback((parentNode: Node) => {
    const parentPosition = nodes.find(n => n.id === parentNode.id)?.position;
    if (!parentPosition) return;

    const { nodes: newNodes, edges: newEdges } = createDecisionPaths(parentNode, {
      x: parentPosition.x,
      y: parentPosition.y + 150
    });

    setNodes((nds) => [...nds, ...newNodes]);
    setEdges((eds) => [...eds, ...newEdges]);
  }, [nodes, createDecisionPaths]);

  const deleteNode = useCallback((nodeId: string) => {
    setNodes((nds) => nds.filter((node) => node.id !== nodeId));
    setEdges((eds) => eds.filter((edge) => edge.source !== nodeId && edge.target !== nodeId));
  }, []);

  const updateNode = useCallback((nodeId: string, data: any) => {
    setNodes((nds) =>
      nds.map((node) => {
        if (node.id === nodeId) {
          return {
            ...node,
            data: {
              ...node.data,
              ...data,
              onHandleClick,
            },
          };
        }
        return node;
      })
    );
  }, [onHandleClick]);

  useEffect(() => {
    window.splitNode = splitNode;
    window.deleteNode = deleteNode;
    window.editNode = (node: any) => {
      updateNode(node.id, node.data);
    };
    return () => {
      delete window.splitNode;
      delete window.deleteNode;
      delete window.editNode;
    };
  }, [splitNode, deleteNode, updateNode]);

  const createNode = useCallback((agent: any) => {
    if (!agentTypeConfig) return; // Wait for agent types to load

    if (agent.type === 'decision') {
      const position = { x: Math.random() * 500, y: Math.random() * 500 };
      const { nodes: newNodes, edges: newEdges } = createDecisionPaths(null, position);
      setNodes((nds) => [...nds, ...newNodes]);
      setEdges((eds) => [...eds, ...newEdges]);
      return;
    }

    const config = agentTypeConfig[agent.type];
    const AgentIcon = config?.icon || Code;

    const newNode: Node = {
      id: agent.id,
      type: 'agent',
      position: { x: Math.random() * 500, y: Math.random() * 500 },
      data: {
        label: agent.type,
        type: agent.type,
        color: agent.color || config?.color || "#4B6BFF", // Use agent type's default color
        role: agent.role,
        goal: agent.goal,
        tools: agent.tools,
        canSplit: true,
        onHandleClick,
        canEdit: true,
        icon: AgentIcon,
      },
    };

    setNodes((nds) => [...nds, newNode]);
  }, [onHandleClick, agentTypeConfig]);

  useImperativeHandle(ref, () => ({
    createNode,
    updateNode,
    deleteNode
  }), [createNode, updateNode, deleteNode]);

  return (
    <div className="w-full h-full bg-[#0A0D14] relative">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={handleNodesChange}
        onEdgesChange={handleEdgesChange}
        onConnect={onConnect}
        onNodeClick={onNodeClick}
        onPaneClick={onPaneClick}
        nodeTypes={customNodes}
        defaultViewport={{ x: 0, y: 0, zoom: 1.5 }}
        minZoom={0.1}
        maxZoom={8}
        zoomOnScroll={true}
        zoomOnPinch={true}
        panOnScroll={false}
        panOnDrag={true}
        selectionOnDrag={true}
        fitView
        attributionPosition="bottom-right"
      >
        <Background color="#2A2F3C" gap={24} />
        <Controls
          className="bg-sidebar-accent border border-sidebar-border"
          showInteractive={false}
          position="bottom-right"
        />
      </ReactFlow>
    </div>
  );
});

BlueprintCanvas.displayName = 'BlueprintCanvas';

export default BlueprintCanvas;
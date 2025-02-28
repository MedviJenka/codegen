import React, { useCallback, useRef } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  ReactFlowProvider,
  addEdge,
  useReactFlow,
  Connection,
  Edge,
  NodeTypes,
} from 'react-flow-renderer';
import useFlowStore from '../store/flowStore';
import AgentNode from './nodes/AgentNode';
import DecisionNode from './nodes/DecisionNode';

const nodeTypes: NodeTypes = {
  agent: AgentNode,
  decision: DecisionNode,
};

// Create a separate component for the inner flow content
const FlowContent = () => {
  const { nodes, edges, addEdge: storeAddEdge, updateNode, removeNode, removeEdge } = useFlowStore();
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const { project } = useReactFlow();

  const onConnect = useCallback(
    (params: Connection) => {
      storeAddEdge({
        id: `e-${params.source}-${params.target}`,
        source: params.source || '',
        target: params.target || '',
      });
    },
    [storeAddEdge]
  );

  const onEdgeUpdate = useCallback(
    (oldEdge: Edge, newConnection: Connection) => {
      removeEdge(oldEdge.id);
      if (newConnection.source && newConnection.target) {
        storeAddEdge({
          id: `e-${newConnection.source}-${newConnection.target}`,
          source: newConnection.source,
          target: newConnection.target,
        });
      }
    },
    [removeEdge, storeAddEdge]
  );

  const onNodeDragStop = useCallback(
    (event: React.MouseEvent, node: any) => {
      updateNode(node.id, { position: node.position });
    },
    [updateNode]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      if (reactFlowWrapper.current) {
        const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
        const data = JSON.parse(event.dataTransfer.getData('application/reactflow'));

        const position = project({
          x: event.clientX - reactFlowBounds.left,
          y: event.clientY - reactFlowBounds.top,
        });

        updateNode(data.id, { position });
      }
    },
    [project, updateNode]
  );

  return (
    <div className="flex-1 h-full" ref={reactFlowWrapper}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onConnect={onConnect}
        onEdgeUpdate={onEdgeUpdate}
        onNodeDragStop={onNodeDragStop}
        onDragOver={onDragOver}
        onDrop={onDrop}
        nodeTypes={nodeTypes}
        fitView
        attributionPosition="bottom-right"
      >
        <Background color="#aaa" gap={16} />
        <Controls />
        <MiniMap
          nodeStrokeColor={(n) => {
            if (n.type === 'agent') return '#0041d0';
            if (n.type === 'decision') return '#ff0072';
            return '#eee';
          }}
          nodeColor={(n) => {
            if (n.type === 'agent') return '#0041d0';
            if (n.type === 'decision') return '#ff0072';
            return '#fff';
          }}
        />
      </ReactFlow>
    </div>
  );
};

// Main component that wraps the flow content with the provider
const FlowCanvas: React.FC = () => {
  return (
    <ReactFlowProvider>
      <FlowContent />
    </ReactFlowProvider>
  );
};

export default FlowCanvas;
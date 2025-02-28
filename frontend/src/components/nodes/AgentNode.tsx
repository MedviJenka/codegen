import React, { useState } from 'react';
import { Handle, Position } from 'react-flow-renderer';
import { Brain, MoreHorizontal, X, Split } from 'lucide-react';
import useFlowStore from '../../store/flowStore';
import { v4 as uuidv4 } from 'uuid';

const AgentNode = ({ id, data }: { id: string; data: any }) => {
  const { removeNode, addNode, iconSize } = useFlowStore();
  const [showMenu, setShowMenu] = useState(false);
  const agent = data.agent;

  const handleDragStart = (event: React.DragEvent) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ id }));
    event.dataTransfer.effectAllowed = 'move';
  };

  const handleSplit = () => {
    // Create a decision node
    const decisionNodeId = uuidv4();
    addNode({
      id: decisionNodeId,
      type: 'decision',
      data: { label: 'Decision Point' },
      position: { x: agent.position.x + 250, y: agent.position.y },
    });

    setShowMenu(false);
  };

  return (
    <div
      className={`${agent.color} rounded-lg shadow-lg p-4 w-64 relative`}
      draggable
      onDragStart={handleDragStart}
    >
      <Handle type="target" position={Position.Left} className="w-3 h-3" />
      <Handle type="source" position={Position.Right} className="w-3 h-3" />

      <div className="flex justify-between items-start">
        <div className="flex items-center">
          <div className="bg-white bg-opacity-20 rounded-full p-2 mr-3">
            <Brain size={iconSize * 0.8} className="text-white" />
          </div>
          <div>
            <h3 className="font-bold text-white">{agent.name}</h3>
            <p className="text-sm text-white text-opacity-80">{agent.role}</p>
          </div>
        </div>
        <div className="relative">
          <button
            onClick={() => setShowMenu(!showMenu)}
            className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-1"
          >
            <MoreHorizontal size={18} />
          </button>
          {showMenu && (
            <div className="absolute right-0 mt-1 bg-gray-800 rounded-md shadow-lg z-10 w-36">
              <button
                onClick={handleSplit}
                className="flex items-center w-full px-4 py-2 text-sm text-left text-white hover:bg-gray-700"
              >
                <Split size={16} className="mr-2" />
                Split Node
              </button>
              <button
                onClick={() => {
                  removeNode(id);
                  setShowMenu(false);
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-left text-white hover:bg-gray-700 text-red-400"
              >
                <X size={16} className="mr-2" />
                Remove
              </button>
            </div>
          )}
        </div>
      </div>

      {agent.goal && (
        <div className="mt-3 p-2 bg-black bg-opacity-20 rounded text-sm text-white">
          <p className="font-medium mb-1">Goal:</p>
          <p className="text-white text-opacity-90">{agent.goal}</p>
        </div>
      )}
    </div>
  );
};

export default AgentNode;
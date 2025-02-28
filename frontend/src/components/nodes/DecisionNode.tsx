import React, { useState } from 'react';
import { Handle, Position } from 'react-flow-renderer';
import { GitBranch, MoreHorizontal, X, Edit } from 'lucide-react';
import useFlowStore from '../../store/flowStore';

const DecisionNode = ({ id, data }: { id: string; data: any }) => {
  const { removeNode, updateNode, iconSize } = useFlowStore();
  const [showMenu, setShowMenu] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [label, setLabel] = useState(data.label);

  const handleDragStart = (event: React.DragEvent) => {
    event.dataTransfer.setData('application/reactflow', JSON.stringify({ id }));
    event.dataTransfer.effectAllowed = 'move';
  };

  const handleSaveLabel = () => {
    updateNode(id, { data: { ...data, label } });
    setIsEditing(false);
  };

  return (
    <div
      className="bg-pink-600 rounded-lg shadow-lg p-4 w-64 relative"
      draggable
      onDragStart={handleDragStart}
    >
      <Handle type="target" position={Position.Left} className="w-3 h-3" />
      <Handle type="source" position={Position.Right} className="w-3 h-3" />
      <Handle type="source" position={Position.Bottom} className="w-3 h-3" />

      <div className="flex justify-between items-start">
        <div className="flex items-center">
          <div className="bg-white bg-opacity-20 rounded-full p-2 mr-3">
            <GitBranch size={iconSize * 0.8} className="text-white" />
          </div>
          {isEditing ? (
            <div>
              <input
                type="text"
                value={label}
                onChange={(e) => setLabel(e.target.value)}
                className="bg-pink-700 text-white p-1 rounded w-full"
                autoFocus
                onBlur={handleSaveLabel}
                onKeyDown={(e) => e.key === 'Enter' && handleSaveLabel()}
              />
            </div>
          ) : (
            <div>
              <h3 className="font-bold text-white">{data.label}</h3>
              <p className="text-sm text-white text-opacity-80">Decision Point</p>
            </div>
          )}
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
                onClick={() => {
                  setIsEditing(true);
                  setShowMenu(false);
                }}
                className="flex items-center w-full px-4 py-2 text-sm text-left text-white hover:bg-gray-700"
              >
                <Edit size={16} className="mr-2" />
                Edit Label
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

      <div className="mt-3 p-2 bg-black bg-opacity-20 rounded text-sm text-white">
        <p className="text-white text-opacity-90">
          This node represents a decision point in your agent workflow. Connect it to multiple agents to create branching logic.
        </p>
      </div>
    </div>
  );
};

export default DecisionNode;
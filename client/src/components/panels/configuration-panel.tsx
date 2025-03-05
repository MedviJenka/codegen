import React from 'react';
import { colors } from '@/lib/agent-config';

interface ConfigurationPanelProps {
  selectedNode?: any;
  onNodeUpdate?: (nodeId: string, data: any) => void;
}

export const ConfigurationPanel: React.FC<ConfigurationPanelProps> = ({ 
  selectedNode, 
  onNodeUpdate 
}) => {
  if (!selectedNode) {
    return (
      <div className="p-4 bg-background border-l">
        <p className="text-sm text-muted-foreground">Select a node to configure</p>
      </div>
    );
  }

  const handleNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onNodeUpdate) {
      onNodeUpdate(selectedNode.id, {
        ...selectedNode.data,
        label: e.target.value,
      });
    }
  };

  const handleRoleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onNodeUpdate) {
      onNodeUpdate(selectedNode.id, {
        ...selectedNode.data,
        role: e.target.value,
      });
    }
  };

  const handleGoalChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (onNodeUpdate) {
      onNodeUpdate(selectedNode.id, {
        ...selectedNode.data,
        goal: e.target.value,
      });
    }
  };

  const handleColorChange = (color: string) => {
    if (onNodeUpdate) {
      onNodeUpdate(selectedNode.id, {
        ...selectedNode.data,
        color,
      });
    }
  };

  // Only allow editing name for decision nodes or metadata for Yes/No path nodes
  const canEditName = selectedNode.type === 'decision';
  const canEditMetadata = selectedNode.data.isSmall;

  return (
    <div className="p-4 bg-background border-l">
      <h3 className="font-medium mb-4">Node Configuration</h3>
      <div className="space-y-4">
        <div>
          <label className="text-sm font-medium block mb-1">Name</label>
          {canEditName ? (
            <input
              type="text"
              value={selectedNode.data.label || ''}
              onChange={handleNameChange}
              className="w-full p-2 border rounded bg-[#2A2A2A] border-0 text-white"
              placeholder="Enter node name"
            />
          ) : (
            <div className="text-sm text-muted-foreground">{selectedNode.data.label}</div>
          )}
        </div>
        {canEditMetadata && (
          <>
            <div>
              <label className="text-sm font-medium block mb-1">Role</label>
              <input
                type="text"
                value={selectedNode.data.role || ''}
                onChange={handleRoleChange}
                className="w-full p-2 border rounded bg-[#2A2A2A] border-0 text-white"
                placeholder="Enter node role"
              />
            </div>
            <div>
              <label className="text-sm font-medium block mb-1">Goal</label>
              <textarea
                value={selectedNode.data.goal || ''}
                onChange={handleGoalChange}
                className="w-full p-2 border rounded bg-[#2A2A2A] border-0 text-white min-h-[100px]"
                placeholder="Enter node goal"
              />
            </div>
          </>
        )}
        <div>
          <label className="text-sm font-medium block mb-1">Type</label>
          <div className="text-sm text-muted-foreground">{selectedNode.data.type || selectedNode.type}</div>
        </div>
        <div>
          <label className="text-sm font-medium block mb-1">Color</label>
          <div className="flex gap-2 flex-wrap">
            {colors.map((color) => (
              <button
                key={color}
                className={`w-8 h-8 rounded-full cursor-pointer transition-transform hover:scale-110 ${
                  selectedNode.data.color === color ? 'ring-2 ring-white' : ''
                }`}
                style={{ backgroundColor: color }}
                onClick={() => handleColorChange(color)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfigurationPanel;
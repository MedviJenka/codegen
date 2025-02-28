import React from 'react';
import { Save, Download, Upload, HelpCircle, Settings, Brain, ZoomIn, ZoomOut } from 'lucide-react';
import useFlowStore from '../store/flowStore';
import useAgentStore from '../store/agentStore';

const Toolbar: React.FC = () => {
  const { nodes, edges, iconSize, setIconSize } = useFlowStore();
  const { agents } = useAgentStore();

  const handleExport = () => {
    const data = {
      agents,
      nodes,
      edges,
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'ai-agent-blueprint.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const increaseIconSize = () => {
    setIconSize(Math.min(iconSize + 4, 48));
  };

  const decreaseIconSize = () => {
    setIconSize(Math.max(iconSize - 4, 16));
  };

  return (
    <div className="h-14 bg-gray-800 border-b border-gray-700 flex items-center px-4 justify-between">
      <div className="flex items-center">
        <div className="text-blue-500 mr-2">
          <Brain size={24} />
        </div>
        <h1 className="text-white text-xl font-bold">AI Agent Blueprint</h1>
      </div>
      
      <div className="flex items-center space-x-2">
        <div className="flex items-center bg-gray-700 rounded-lg mr-2 px-1">
          <button 
            onClick={decreaseIconSize}
            className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-600"
            title="Decrease icon size"
          >
            <ZoomOut size={18} />
          </button>
          <span className="text-gray-300 mx-2">{iconSize}px</span>
          <button 
            onClick={increaseIconSize}
            className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-600"
            title="Increase icon size"
          >
            <ZoomIn size={18} />
          </button>
        </div>
        <button className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-700">
          <Save size={20} />
        </button>
        <button 
          onClick={handleExport}
          className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-700"
        >
          <Download size={20} />
        </button>
        <button className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-700">
          <Upload size={20} />
        </button>
        <button className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-700">
          <HelpCircle size={20} />
        </button>
        <button className="text-gray-300 hover:text-white p-2 rounded hover:bg-gray-700">
          <Settings size={20} />
        </button>
      </div>
    </div>
  );
};

export default Toolbar;
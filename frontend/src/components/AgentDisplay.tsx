import React, { useState, useRef } from 'react';
import useFlowStore from '../store/flowStore';
import useAgentStore from '../store/agentStore';
import { Brain, Cpu, Bot, Sparkles, Move } from 'lucide-react';

const agentIcons = [Brain, Cpu, Bot, Sparkles];

const AgentDisplay: React.FC = () => {
  const { agents, updateAgent } = useAgentStore();
  const { iconSize } = useFlowStore();
  const [draggingId, setDraggingId] = useState<string | null>(null);
  const [dragPosition, setDragPosition] = useState({ x: 0, y: 0 });
  const containerRef = useRef<HTMLDivElement>(null);

  if (agents.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-800">
        <div className="text-center text-gray-400">
          <p className="text-xl mb-2">No agents added yet</p>
          <p>Create agents in the sidebar and add them to your workflow</p>
        </div>
      </div>
    );
  }

  const handleDragStart = (e: React.DragEvent, agentId: string) => {
    setDraggingId(agentId);
    
    // Store the initial position where the drag started
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      setDragPosition({ x, y });
    }
    
    // Set a transparent drag image
    const img = new Image();
    img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
    e.dataTransfer.setDragImage(img, 0, 0);
  };

  const handleDrag = (e: React.DragEvent) => {
    if (!draggingId || !e.clientX || !e.clientY) return;
    
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      setDragPosition({ x, y });
    }
  };

  const handleDragEnd = (e: React.DragEvent, agentId: string) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      
      // Update the agent's position
      const agent = agents.find(a => a.id === agentId);
      if (agent) {
        updateAgent(agentId, { 
          position: { x, y } 
        });
      }
    }
    
    setDraggingId(null);
  };

  return (
    <div 
      ref={containerRef}
      className="flex-1 p-8 bg-gray-800 overflow-auto relative"
    >
      {agents.map((agent, index) => {
        const IconComponent = agentIcons[index % agentIcons.length];
        const isDragging = draggingId === agent.id;
        
        // Calculate position styles
        const positionStyle = isDragging 
          ? { 
              left: `${dragPosition.x}px`, 
              top: `${dragPosition.y}px`,
              position: 'absolute',
              zIndex: 100,
              transform: 'translate(-50%, -50%)',
              opacity: 0.8,
              width: '300px'
            } 
          : { 
              left: `${agent.position.x}px`, 
              top: `${agent.position.y}px`,
              position: 'absolute',
              transform: 'translate(-50%, -50%)'
            };
            
        return (
          <div
            key={agent.id}
            className={`${agent.color} rounded-lg shadow-lg p-6 transition-all duration-100 hover:shadow-xl cursor-move`}
            style={positionStyle}
            draggable
            onDragStart={(e) => handleDragStart(e, agent.id)}
            onDrag={handleDrag}
            onDragEnd={(e) => handleDragEnd(e, agent.id)}
          >
            <div className="flex items-center mb-4">
              <div className={`rounded-full bg-white bg-opacity-20 p-3 mr-4 flex items-center justify-center`}>
                <IconComponent size={iconSize} className="text-white" />
              </div>
              <div>
                <h3 className="font-bold text-white text-xl">{agent.name}</h3>
                <p className="text-white text-opacity-80">{agent.role}</p>
              </div>
              <div className="ml-auto text-white opacity-60">
                <Move size={16} />
              </div>
            </div>
            {agent.goal && (
              <div className="mt-4 p-3 bg-black bg-opacity-20 rounded-lg">
                <p className="font-medium mb-1 text-white">Goal:</p>
                <p className="text-white text-opacity-90">{agent.goal}</p>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

export default AgentDisplay;
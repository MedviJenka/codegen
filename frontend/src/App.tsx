import React from 'react';
import Sidebar from './components/Sidebar';
import Toolbar from './components/Toolbar';
import FlowCanvas from './components/FlowCanvas';

function App() {
  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      <Toolbar />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <FlowCanvas />
      </div>
    </div>
  );
}

export default App;
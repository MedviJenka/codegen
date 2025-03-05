import MainLayout from "@/components/layout/main-layout";
import BlueprintCanvas from "@/components/canvas/blueprint-canvas";
import AgentSidebar from "@/components/panels/agent-sidebar";
import { useState, useCallback, useRef } from "react";
import type { Node, Edge } from "reactflow";
import ConfigurationPanel from "@/components/panels/configuration-panel";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

interface CanvasRef {
  createNode: (agent: any) => void;
  updateNode: (nodeId: string, data: any) => void;
  deleteNode: (nodeId: string) => void;
}

export default function Home() {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [selectedNode, setSelectedNode] = useState<Node | null>(null);
  const [showAgentSidebar, setShowAgentSidebar] = useState(true);
  const canvasRef = useRef<CanvasRef>(null);

  const handleCreateAgent = useCallback((agent: any) => {
    canvasRef.current?.createNode(agent);
  }, []);

  const handleUpdateAgent = useCallback((agent: any) => {
    if (canvasRef.current) {
      canvasRef.current.updateNode(agent.id, {
        label: agent.type,
        type: agent.type,
        color: agent.color,
        role: agent.role,
        goal: agent.goal,
        tools: agent.tools,
        canSplit: true,
        icon: agent.icon,
        canEdit: true
      });
    }
  }, []);

  const handleDeleteAgent = useCallback((agentId: string) => {
    if (canvasRef.current) {
      canvasRef.current.deleteNode(agentId);
    }
  }, []);

  const handleNodesChange = useCallback((nodes: Node[]) => {
    setNodes(nodes);
  }, []);

  const handleEdgesChange = useCallback((edges: Edge[]) => {
    setEdges(edges);
  }, []);

  const handleNodeUpdate = useCallback((nodeId: string, data: any) => {
    canvasRef.current?.updateNode(nodeId, data);
  }, []);

  return (
    <MainLayout
      nodes={nodes}
      edges={edges}
    >
      <div className="flex h-screen overflow-hidden">
        <ResizablePanelGroup direction="horizontal">
          {showAgentSidebar && (
            <>
              <ResizablePanel 
                defaultSize={20} 
                minSize={15}
                maxSize={40}
                className="min-w-[250px]"
              >
                <AgentSidebar
                  className="border-r border-white/10 h-full"
                  onClose={() => setShowAgentSidebar(false)}
                  onCreateAgent={handleCreateAgent}
                  onUpdateAgent={handleUpdateAgent}
                  onDeleteAgent={handleDeleteAgent}
                />
              </ResizablePanel>
              <ResizableHandle />
            </>
          )}
          <ResizablePanel defaultSize={80}>
            <div className="h-full w-full relative">
              <BlueprintCanvas
                ref={canvasRef}
                onNodeSelect={setSelectedNode}
                onNodesChange={handleNodesChange}
                onEdgesChange={handleEdgesChange}
              />
              {selectedNode && (
                <ConfigurationPanel
                  selectedNode={selectedNode}
                  onNodeUpdate={handleNodeUpdate}
                />
              )}
            </div>
          </ResizablePanel>
        </ResizablePanelGroup>
      </div>
    </MainLayout>
  );
}
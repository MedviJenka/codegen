import React, { useState } from "react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Plus, Pencil, Loader2 } from "lucide-react";
import { ChevronDown } from "lucide-react";
import { Trash2 } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import { type AgentType } from "@/lib/agent-config";
import { Checkbox } from "@/components/ui/checkbox";
import { useAgentTypes } from "@/lib/agent-config";


const availableTools = [
  { id: 'file_read', name: 'File Read Tool', description: 'Read files from the system' },
  { id: 'file_write', name: 'File Writer Tool', description: 'Write files to the system' }
];

const colors = [
  "#4B6BFF", // Blue
  "#6BFF4B", // Green
  "#9B4BFF", // Purple
  "#FFB74B", // Orange
  "#FF4B6B", // Pink
  "#4BFFB7", // Teal
  "#FF4B4B", // Red
  "#4BFFF7", // Cyan
];

interface FormData {
  type: string;
  role: string;
  goal: string;
  color: string;
  tools: string[];
  id?: string;
}

const AgentForm: React.FC<{
  initialData: FormData;
  onSubmit: (data: FormData) => void;
  title: string;
  isSubmitting?: boolean;
}> = ({ initialData, onSubmit, title, isSubmitting = false }) => {
  const { data: agentTypeConfig, isLoading } = useAgentTypes();
  const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);
  const [formData, setFormData] = useState<FormData>({
    ...initialData,
    tools: initialData.tools || []
  });

  const agentTypes = agentTypeConfig ? Object.keys(agentTypeConfig) : [];

  if (isLoading) {
    return <div>Loading agent types...</div>;
  }

  const toggleTool = (toolId: string) => {
    setFormData((prev: FormData) => ({
      ...prev,
      tools: prev.tools.includes(toolId)
        ? prev.tools.filter((id: string) => id !== toolId)
        : [...prev.tools, toolId]
    }));
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm mb-2">
          Name <span className="text-red-500">*</span>
        </label>
        <Select
          value={formData.type}
          onValueChange={(value) => setFormData({ ...formData, type: value })}
        >
          <SelectTrigger className="w-full bg-[#2A2A2A] border-0">
            <SelectValue placeholder="Select agent type" />
          </SelectTrigger>
          <SelectContent>
            {agentTypes.map((type) => (
              <SelectItem key={type} value={type}>
                {type}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <Collapsible
        open={isAdvancedOpen}
        onOpenChange={setIsAdvancedOpen}
        className="space-y-2"
      >
        <CollapsibleTrigger asChild>
          <Button
            variant="ghost"
            className="flex w-full justify-between p-0 h-8"
          >
            <span className="text-sm text-muted-foreground">Advanced Options</span>
            <ChevronDown
              className={cn(
                "h-4 w-4 text-muted-foreground transition-transform",
                isAdvancedOpen && "transform rotate-180"
              )}
            />
          </Button>
        </CollapsibleTrigger>
        <CollapsibleContent className="space-y-4">
          <div>
            <label className="block text-sm mb-2">Role</label>
            <Input
              placeholder="Agent role"
              className="bg-[#2A2A2A] border-0"
              value={formData.role}
              onChange={(e) => setFormData({ ...formData, role: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm mb-2">Goal</label>
            <Textarea
              placeholder="Agent goal"
              className="bg-[#2A2A2A] border-0 min-h-[100px]"
              value={formData.goal}
              onChange={(e) => setFormData({ ...formData, goal: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm mb-2">Tools</label>
            <div className="space-y-2">
              {availableTools.map((tool) => (
                <div
                  key={tool.id}
                  className="flex items-start space-x-2 bg-[#2A2A2A] p-2 rounded"
                >
                  <Checkbox
                    id={tool.id}
                    checked={formData.tools.includes(tool.id)}
                    onCheckedChange={() => toggleTool(tool.id)}
                  />
                  <div className="grid gap-1.5 leading-none">
                    <label
                      htmlFor={tool.id}
                      className="text-sm font-medium leading-none cursor-pointer"
                    >
                      {tool.name}
                    </label>
                    <p className="text-sm text-muted-foreground">
                      {tool.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm mb-2">Color (optional)</label>
            <div className="flex gap-2 flex-wrap">
              {colors.map((color) => (
                <button
                  key={color}
                  className={cn(
                    "w-8 h-8 rounded-full cursor-pointer transition-transform hover:scale-110",
                    formData.color === color && "ring-2 ring-white"
                  )}
                  style={{ backgroundColor: color }}
                  onClick={() => setFormData({ ...formData, color: color === formData.color ? '' : color })}
                />
              ))}
            </div>
          </div>
        </CollapsibleContent>
      </Collapsible>

      <Button
        className="w-full mt-6 bg-blue-600 hover:bg-blue-700"
        onClick={() => onSubmit(formData)}
        disabled={!formData.type || isSubmitting}
      >
        {isSubmitting ? (
          <div className="flex items-center">
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Creating Agent...
          </div>
        ) : (
          title
        )}
      </Button>
    </div>
  );
};

interface AgentSidebarProps {
  className?: string;
  onClose?: () => void;
  onCreateAgent?: (agent: any) => void;
  onUpdateAgent?: (agent: any) => void;
  onDeleteAgent?: (agentId: string) => void;
}

const AgentSidebar: React.FC<AgentSidebarProps> = ({
  className,
  onClose,
  onCreateAgent,
  onUpdateAgent,
  onDeleteAgent
}) => {
  const { data: agentTypeConfig } = useAgentTypes();
  const [showNewAgent, setShowNewAgent] = useState(false);
  const [agents, setAgents] = useState<Array<any>>([]);
  const [editingAgent, setEditingAgent] = useState<any>(null);
  const [isCreating, setIsCreating] = useState(false);

  const handleCreateAgent = async (formData: FormData) => {
    if (!agentTypeConfig) return;

    setIsCreating(true);
    try {
      const config = agentTypeConfig[formData.type as AgentType];
      const agent = {
        ...formData,
        id: Date.now().toString(),
        color: formData.color || config.color, // Use the agent type's color if no custom color
        icon: config.icon
      };

      setAgents([...agents, agent]);
      onCreateAgent?.(agent);
      setShowNewAgent(false);
    } finally {
      setIsCreating(false);
    }
  };

  const handleUpdateAgent = (formData: FormData) => {
    if (!agentTypeConfig) return;

    const config = agentTypeConfig[formData.type as AgentType];
    const updatedAgent = {
      ...formData,
      id: formData.id,
      color: formData.color || config.color, // Use the agent type's color if no custom color
      icon: config.icon
    };

    setAgents(agents.map(a => a.id === updatedAgent.id ? updatedAgent : a));
    onUpdateAgent?.(updatedAgent);
    setEditingAgent(null);
  };

  const handleDeleteAgent = (agentId: string) => {
    setAgents(agents.filter(agent => agent.id !== agentId));
    onDeleteAgent?.(agentId);
  };

  return (
    <div className={cn("bg-[#1E1E1E] text-white flex flex-col h-full overflow-hidden", className)}>
      <div className="flex items-center justify-between p-6">
        <h2 className="text-xl font-semibold">AI Agents</h2>
        <motion.div
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.9, 1, 0.9],
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        >
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setShowNewAgent(!showNewAgent)}
            className="relative h-8 w-8 overflow-hidden rounded-full"
            disabled={isCreating}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 animate-gradient" />
            <Plus className="h-4 w-4 text-white relative z-10" />
          </Button>
        </motion.div>
      </div>

      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <AnimatePresence>
          {showNewAgent && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.2 }}
            >
              <h3 className="text-lg mb-4">New Agent</h3>
              <AgentForm
                initialData={{ type: '', role: '', goal: '', color: '', tools: [] }}
                onSubmit={handleCreateAgent}
                title="Create Agent"
                isSubmitting={isCreating}
              />
            </motion.div>
          )}
        </AnimatePresence>

        <Dialog open={editingAgent !== null} onOpenChange={(open) => !open && setEditingAgent(null)}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Edit Agent</DialogTitle>
              <DialogDescription>
                Modify the agent's properties
              </DialogDescription>
            </DialogHeader>
            {editingAgent && (
              <AgentForm
                initialData={editingAgent}
                onSubmit={handleUpdateAgent}
                title="Update Agent"
              />
            )}
          </DialogContent>
        </Dialog>

        <div className="pt-6 border-t border-white/10 space-y-2">
          {agents.map((agent) => {
            const AgentIcon = agent.icon;
            return (
              <div key={agent.id} className="flex items-center gap-2 p-3 bg-[#2A2A2A] rounded-lg">
                <div className="bg-blue-600 p-2 rounded-full" style={{ backgroundColor: agent.color }}>
                  <AgentIcon className="h-4 w-4" />
                </div>
                <div className="text-sm">
                  <div>{agent.type}</div>
                  {agent.role && <div className="text-white/60">{agent.role}</div>}
                </div>
                <div className="ml-auto flex gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="text-white/60 hover:text-white"
                    onClick={() => setEditingAgent(agent)}
                  >
                    <Pencil className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="text-white/60 hover:text-white"
                    onClick={() => handleDeleteAgent(agent.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default AgentSidebar;
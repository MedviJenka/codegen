import { cn } from "@/lib/utils";
import { Brain, MessageSquare, Database, Cog } from "lucide-react";
import { motion } from "framer-motion";


interface ComponentLibraryProps {
  className?: string;
}


const components = [
  { type: 'agent', label: 'Research Assistant', icon: Brain },
  { type: 'prompt', label: 'Assistant', icon: MessageSquare },
  { type: 'memory', label: 'Memory Store', icon: Database },
  { type: 'tool', label: 'API Tool', icon: Cog },
];

export default function ComponentLibrary({ className }: ComponentLibraryProps) {
  const onDragStart = (event: React.DragEvent, nodeType: string) => {
    event.dataTransfer.setData('application/reactflow', nodeType);
    event.dataTransfer.effectAllowed = 'move';
  };

  return (
    <div className={cn("bg-sidebar p-4", className)}>
      <h2 className="text-lg font-semibold mb-4 text-sidebar-foreground">AI Agents</h2>
      <div className="space-y-3">
        {components.map((component) => (
          <motion.div
            key={component.type}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <div
              className="bg-sidebar-accent rounded-lg p-3 cursor-move border border-sidebar-border hover:border-sidebar-primary transition-colors"
              draggable
              onDragStart={(e) => onDragStart(e, component.type)}
            >
              <div className="flex items-center gap-2 text-sidebar-primary">
                <component.icon className="h-5 w-5" />
                <span className="text-sm font-medium">{component.label}</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
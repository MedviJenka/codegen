import React, { memo, useState, useRef, useEffect } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';
import { GitFork, MoreHorizontal, Trash2, Pencil } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Sparkle } from '@/components/effects/sparkle';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const NodeLabel = ({ value, onChange, canEdit = false }: { value: string; onChange: (value: string) => void; canEdit?: boolean }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editValue, setEditValue] = useState(value);
  const [showSparkle, setShowSparkle] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isEditing]);

  const handleDoubleClick = () => {
    if (!canEdit) return;
    setIsEditing(true);
    setEditValue(value);
  };

  const handleBlur = () => {
    setIsEditing(false);
    if (editValue.trim() !== value) {
      onChange(editValue.trim());
      setShowSparkle(true);
      setTimeout(() => setShowSparkle(false), 1000);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleBlur();
    }
    if (e.key === 'Escape') {
      setIsEditing(false);
      setEditValue(value);
    }
  };

  if (isEditing && canEdit) {
    return (
      <input
        ref={inputRef}
        value={editValue}
        onChange={(e) => setEditValue(e.target.value)}
        onBlur={handleBlur}
        onKeyDown={handleKeyDown}
        className="bg-transparent border-none outline-none text-white font-medium w-full"
        autoFocus
      />
    );
  }

  return (
    <div className="relative">
      <div className={`font-medium ${canEdit ? 'cursor-text' : ''}`} onDoubleClick={handleDoubleClick}>
        {value}
      </div>
      {showSparkle && <Sparkle />}
    </div>
  );
};

const AgentNode = memo(({ id, data, type }: NodeProps) => {
  const handleClick = (isTarget: boolean, handleId: string) => {
    data.onHandleClick?.(id, handleId, isTarget);
  };

  const AgentIcon = data.icon;
  if (!AgentIcon) return null;

  const containerClasses = data.isSmall 
    ? "rounded-lg shadow-lg relative group min-w-[200px]"
    : "rounded-lg shadow-lg relative group";

  const iconContainerClasses = data.isSmall
    ? "bg-white/20 p-2 rounded-full"
    : "bg-white/20 p-2 rounded-full";

  const iconClasses = data.isSmall
    ? "h-4 w-4"
    : "h-4 w-4";

  const roleClasses = data.isSmall
    ? "text-sm text-white/60"
    : "text-sm text-white/60";

  // Only allow editing for Yes/No path nodes (isSmall flag)
  const canEditNode = data.isSmall;

  return (
    <div 
      className={containerClasses}
      style={{ backgroundColor: data.color }}
    >
      <div className={data.isSmall ? "p-4 text-white" : "p-4 text-white"}>
        <div className="flex items-center gap-2">
          <div className={iconContainerClasses}>
            <AgentIcon className={iconClasses} />
          </div>
          <div>
            <NodeLabel 
              value={data.label} 
              onChange={(newLabel) => {
                window.editNode?.({ 
                  id, 
                  type, 
                  data: { ...data, label: newLabel }
                });
              }}
              canEdit={canEditNode}
            />
            {data.role && !data.isSmall && (
              <div className={roleClasses}>{data.role}</div>
            )}
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-6 w-6 ml-auto opacity-0 group-hover:opacity-100 transition-opacity"
              >
                <MoreHorizontal className="h-4 w-4" text-white />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {canEditNode && (
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation();
                    window.editNode?.({ id, type, data });
                  }}
                >
                  <Pencil className="h-4 w-4 mr-2" />
                  Edit
                </DropdownMenuItem>
              )}
              {type !== 'decision' && (
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation();
                    const node = { id, type, data };
                    window.splitNode?.(node);
                  }}
                >
                  <GitFork className="h-4 w-4 mr-2" />
                  Split Decision
                </DropdownMenuItem>
              )}
              <DropdownMenuItem
                onClick={(e) => {
                  e.stopPropagation();
                  window.deleteNode?.(id);
                }}
                className="text-destructive"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Delete
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
      <Handle 
        type="target" 
        position={Position.Top} 
        id="top"
        className="w-4 h-4 !bg-white/80 border-2 border-white hover:!bg-white transition-colors cursor-pointer"
        onClick={(e) => {
          e.stopPropagation();
          handleClick(true, "top");
        }}
      />
      <Handle 
        type="source" 
        position={Position.Bottom} 
        id="bottom"
        className="w-4 h-4 !bg-white/80 border-2 border-white hover:!bg-white transition-colors cursor-pointer"
        onClick={(e) => {
          e.stopPropagation();
          handleClick(false, "bottom");
        }}
      />
    </div>
  );
});

const DecisionNode = memo(({ id, data }: NodeProps) => {
  const handleClick = (isTarget: boolean, handleId: string) => {
    data.onHandleClick?.(id, handleId, isTarget);
  };

  return (
    <div 
      className="rounded-lg p-4 shadow-lg relative min-w-[250px]"
      style={{ backgroundColor: '#FF4B6B' }}
    >
      <div className="text-white">
          <div className="flex items-center gap-2 mb-2 group">
            <div className="bg-white/20 p-2 rounded-full">
              <GitFork className="h-4 w-4" />
            </div>
            <h3 className="font-semibold flex-grow">Decision Point</h3>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button 
                  variant="ghost" 
                  size="icon" 
                  className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <MoreHorizontal className="h-4 w-4 text-white" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuItem
                  onClick={(e) => {
                    e.stopPropagation();
                    window.deleteNode?.(id);
                  }}
                  className="text-destructive"
                >
                  <Trash2 className="h-4 w-4 mr-2" />
                  Delete
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
          <div className="bg-white/10 rounded-lg p-3">
            <p className="text-xs text-white/80 leading-relaxed">
              This node represents a decision point in your agent workflow.
              <br />
              Connect it to multiple agents to create branching logic.
            </p>
          </div>
        </div>
      <Handle 
        type="target" 
        position={Position.Left} 
        id="left"
        className="w-4 h-4 !bg-white/80 border-2 border-white hover:!bg-white transition-colors cursor-pointer" 
        onClick={(e) => {
          e.stopPropagation();
          handleClick(true, "left");
        }}
      />
      <Handle 
        type="target" 
        position={Position.Right}
        id="right" 
        className="w-4 h-4 !bg-white/80 border-2 border-white hover:!bg-white transition-colors cursor-pointer" 
        onClick={(e) => {
          e.stopPropagation();
          handleClick(true, "right");
        }}
      />
      <Handle 
        type="source" 
        position={Position.Bottom}
        id="bottom" 
        className="w-4 h-4 !bg-white/80 border-2 border-white hover:!bg-white transition-colors cursor-pointer" 
        onClick={(e) => {
          e.stopPropagation();
          handleClick(false, "bottom");
        }}
      />
    </div>
  );
});

AgentNode.displayName = 'AgentNode';
DecisionNode.displayName = 'DecisionNode';

export const customNodes = {
  agent: AgentNode,
  decision: DecisionNode,
};

declare global {
  interface Window {
    splitNode?: (node: any) => void;
    deleteNode?: (nodeId: string) => void;
    editNode?: (node: any) => void;
  }
}
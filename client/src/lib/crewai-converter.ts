import type { Node, Edge } from 'reactflow';
import type { CrewAiAgent, CrewAiTask } from '@shared/schema';

interface CrewAiConfig {
  agents: CrewAiAgent[];
  tasks: CrewAiTask[];
  hasUnconnectedAgents: boolean;
}

function getAgentFunctionName(label: string): string {
  return label.toLowerCase().replace(/\s+/g, '_');
}

export function convertToCrewAi(nodes: Node[], edges: Edge[]): CrewAiConfig {
  // Get all agent nodes
  const agentNodes = nodes.filter(node => node.type === 'agent');

  // For single agent case, no unconnected warning
  if (agentNodes.length === 1) {
    const agents = [{
      id: agentNodes[0].id,
      role: agentNodes[0].data.label,
      goal: agentNodes[0].data.goal || `Complete tasks as ${agentNodes[0].data.label}`,
      backstory: agentNodes[0].data.role,
      allowDelegation: true,
      verbose: true,
      memory: false,
    }];
    return { agents, tasks: [], hasUnconnectedAgents: false };
  }

  // Create agents array
  const agents: CrewAiAgent[] = agentNodes.map(node => ({
    id: node.id,
    role: node.data.label,
    goal: node.data.goal || `Complete tasks as ${node.data.label}`,
    backstory: node.data.role,
    allowDelegation: true,
    verbose: true,
    memory: false,
  }));

  // Create tasks array from edges
  const tasks: CrewAiTask[] = edges.map(edge => {
    const sourceNode = nodes.find(n => n.id === edge.source);
    const targetNode = nodes.find(n => n.id === edge.target);

    if (sourceNode && targetNode) {
      return {
        description: `Task from ${sourceNode.data.label} to ${targetNode.data.label}`,
        agentId: sourceNode.id,
        dependsOn: [edge.target],
      };
    }
    return null;
  }).filter((task): task is CrewAiTask => task !== null);

  // Check if any agent has no edges connected to it at all
  const hasUnconnectedAgents = agentNodes.some(node => {
    const hasNoEdges = !edges.some(edge => 
      edge.source === node.id || edge.target === node.id
    );
    return hasNoEdges;
  });

  return { agents, tasks, hasUnconnectedAgents };
}

export function generatePythonCode(config: CrewAiConfig): string {
  let code = `"""
Generated Story class for the AI workflow
"""
from crewai.flow.flow import start, listen, Flow
from pydantic import BaseModel
from typing import Optional, Dict, Any\n\n`;

  code += `class InitialState(BaseModel):\n`;
  code += `    """Initial state for the workflow"""\n`;
  code += `    cache: str = ""\n\n`;

  code += `class WorkflowStory(Flow[InitialState]):\n`;
  code += `    """Story implementation for the AI workflow"""\n\n`;

  // Generate code for each agent in sequence
  const connectedAgents = config.agents.filter((_, index) => index === 0 || config.tasks.some(t => t.agentId === config.agents[index - 1].id));

  if (connectedAgents.length > 0) {
    // First agent gets @start
    const firstAgent = connectedAgents[0];
    const firstFunctionName = getAgentFunctionName(firstAgent.role);

    code += `    @start()\n`;
    code += `    def ${firstFunctionName}(self) -> None:\n`;
    code += `        """Starting point of the workflow with ${firstAgent.role}"""\n`;
    code += `        # Execute ${firstAgent.role} tasks\n`;
    code += `        result = ${firstAgent.role}Crew().execute()\n`;
    code += `        self.state.cache = result\n\n`;

    // All subsequent agents get @listen referencing the previous agent
    for (let i = 1; i < connectedAgents.length; i++) {
      const agent = connectedAgents[i];
      const prevAgent = connectedAgents[i - 1];
      const functionName = getAgentFunctionName(agent.role);
      const prevFunctionName = getAgentFunctionName(prevAgent.role);

      code += `    @listen(${prevFunctionName})\n`;
      code += `    def ${functionName}(self) -> None:\n`;
      code += `        """Handler for ${agent.role} tasks after ${prevAgent.role}"""\n`;
      code += `        # Execute ${agent.role} tasks\n`;
      code += `        result = ${agent.role}Crew().execute()\n`;
      code += `        self.state.cache = result\n\n`;
    }
  }

  return code;
}
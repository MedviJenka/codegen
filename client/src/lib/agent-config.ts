import { Brain, Code, Database, BarChart } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { apiRequest } from "./queryClient";

const iconMap: Record<string, any> = {
  "Code Gen Crew": Code,
  "Debug Crew": Brain,
  "Mapping Crew": BarChart,
  "Bini Crew": Database,
  "Py Crew": Code,
};

const colorMap: Record<string, string> = {
  "Code Gen Crew": "#4B6BFF", // Blue
  "Debug Crew": "#9B4BFF", // Purple
  "Mapping Crew": "#4BFFB7", // Teal
  "Py Crew": "#FFB74B", // Orange
  "Bini Crew": "#FF4B6B", // Pink
};

export function useAgentTypes() {
  return useQuery({ 
    queryKey: ['/api/crews'],
    queryFn: async () => {
      const response = await apiRequest('/api/crews', 'GET');
      const { crews } = await response.json();

      // Create dynamic agent config
      const dynamicConfig = crews.reduce((acc: Record<string, any>, crew: string) => {
        acc[crew] = {
          icon: iconMap[crew] || Code, // Default to Code icon if not specified
          color: colorMap[crew] || "#4B6BFF", // Default to blue if not specified
        };
        return acc;
      }, {});

      return dynamicConfig;
    }
  });
}

// Colors array only for configuration panel color picker
export const colors = [
  "#4B6BFF", // Blue
  "#6BFF4B", // Green
  "#9B4BFF", // Purple
  "#FFB74B", // Orange
  "#FF4B6B", // Pink
  "#4BFFB7", // Teal
  "#FF4B4B", // Red
  "#4BFFF7", // Cyan
];

export type AgentType = string;
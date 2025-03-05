import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import fs from 'fs';
import path from 'path';

function formatCrewName(dirName: string): string {
  // Remove _crew suffix if present
  let name = dirName.replace(/_crew$/, '');

  // Split by underscore and capitalize each word
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ') + ' Crew';
}

function scanCrewDirectories(): string[] {
  const crewsPath = path.join(process.cwd(), 'src', 'crews');
  try {
    return fs.readdirSync(crewsPath)
      .filter(dir => {
        // Filter out non-directories and special directories
        const fullPath = path.join(crewsPath, dir);
        return fs.statSync(fullPath).isDirectory() && 
               !dir.startsWith('.') && 
               !['__pycache__', '__init__'].includes(dir);
      })
      .map(formatCrewName)
      .sort();
  } catch (error) {
    console.error('Error scanning crew directories:', error);
    return [];
  }
}

export async function registerRoutes(app: Express): Promise<Server> {
  // Get available crews
  app.get('/api/crews', (req, res) => {
    const crews = scanCrewDirectories();
    res.json({ crews });
  });

  const httpServer = createServer(app);
  return httpServer;
}
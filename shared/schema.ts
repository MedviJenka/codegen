import { pgTable, text, serial, integer, json } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;

export const blueprints = pgTable("blueprints", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"),
  nodes: json("nodes").notNull(),
  edges: json("edges").notNull(),
  crewAiConfig: json("crew_ai_config").notNull(),
  userId: integer("user_id").references(() => users.id),
});

export const insertBlueprintSchema = createInsertSchema(blueprints).pick({
  name: true,
  description: true,
  nodes: true,
  edges: true,
  crewAiConfig: true,
  userId: true,
});

export type InsertBlueprint = z.infer<typeof insertBlueprintSchema>;
export type Blueprint = typeof blueprints.$inferSelect;

// CrewAI specific types
export const crewAiAgentSchema = z.object({
  role: z.string(),
  goal: z.string(),
  backstory: z.string().optional(),
  allowDelegation: z.boolean().default(true),
  verbose: z.boolean().default(true),
  memory: z.boolean().default(false),
  tools: z.array(z.string()).optional(), // Add tools array to the schema
});

export const crewAiTaskSchema = z.object({
  description: z.string(),
  agentId: z.string(),
  dependsOn: z.array(z.string()).optional(),
  conditional: z.object({
    if: z.string(),
    then: z.array(z.string()),
    else: z.array(z.string()),
  }).optional(),
});

export type CrewAiAgent = z.infer<typeof crewAiAgentSchema>;
export type CrewAiTask = z.infer<typeof crewAiTaskSchema>;
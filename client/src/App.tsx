import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import NotFound from "@/pages/not-found";
import Home from "@/pages/home";
import { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import './lib/monaco-init';

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ReactFlowProvider>
        <Switch>
          <Route path="/" component={Home} />
          <Route component={NotFound} />
        </Switch>
        <Toaster />
      </ReactFlowProvider>
    </QueryClientProvider>
  );
}
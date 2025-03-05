import { Button } from "@/components/ui/button";
import { Save, Code } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { convertToCrewAi, generatePythonCode } from "@/lib/crewai-converter";
import { useState } from "react";
import { CodeEditorDialog } from "@/components/editor/code-editor-dialog";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface MainLayoutProps {
  children: React.ReactNode;
  nodes?: any[];
  edges?: any[];
}

export default function MainLayout({ children, nodes = [], edges = [] }: MainLayoutProps) {
  const { toast } = useToast();
  const [showCodeEditor, setShowCodeEditor] = useState(false);
  const [blueprintCode, setBlueprintCode] = useState('');
  const [showUnconnectedWarning, setShowUnconnectedWarning] = useState(false);

  const handleExport = () => {
    try {
      const crewAiConfig = convertToCrewAi(nodes, edges);

      if (crewAiConfig.hasUnconnectedAgents) {
        setShowUnconnectedWarning(true);
        return;
      }

      const pythonCode = generatePythonCode(crewAiConfig);
      setBlueprintCode(pythonCode);
      setShowCodeEditor(true);
    } catch (error) {
      toast({
        title: "Generation Failed",
        description: "Failed to generate CrewAI code. Please check your blueprint configuration.",
        variant: "destructive",
      });
    }
  };

  const handleSaveCode = (code: string) => {
    navigator.clipboard.writeText(code);
    toast({
      title: "Code Copied",
      description: "The CrewAI Python code has been copied to your clipboard.",
    });
    setShowCodeEditor(false);
  };

  const hasAgents = nodes.length > 0;

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="container mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
              AI Blueprint Creator
            </h1>
          </div>
          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <div>
                  <Button onClick={handleExport} disabled={!hasAgents}>
                    <Code className="h-4 w-4 mr-2" />
                    Deploy
                  </Button>
                </div>
              </TooltipTrigger>
              {!hasAgents && (
                <TooltipContent>
                  <p>Add at least one agent to deploy</p>
                </TooltipContent>
              )}
            </Tooltip>
          </TooltipProvider>
        </div>
      </header>
      <main>{children}</main>

      <CodeEditorDialog
        open={showCodeEditor}
        onOpenChange={setShowCodeEditor}
        blueprintCode={blueprintCode}
        onSave={handleSaveCode}
      />

      <AlertDialog open={showUnconnectedWarning} onOpenChange={setShowUnconnectedWarning}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Unconnected Agents Detected</AlertDialogTitle>
            <AlertDialogDescription>
              There are agents in your blueprint that are not connected to the main workflow.
              Please connect all agents or remove unused ones before deploying.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogAction onClick={() => setShowUnconnectedWarning(false)}>
              OK
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
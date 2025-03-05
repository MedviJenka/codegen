import { useState, useEffect, useCallback } from 'react';
import Editor from "@monaco-editor/react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import { DeploymentProgress, type DeploymentStep } from "@/components/deploy/deployment-progress";

interface CodeEditorDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  blueprintCode: string;
  onSave?: (code: string) => void;
}

export function CodeEditorDialog({
  open,
  onOpenChange,
  blueprintCode,
  onSave
}: CodeEditorDialogProps) {
  const [code, setCode] = useState(blueprintCode);
  const [isLoading, setIsLoading] = useState(true);
  const [isDeploying, setIsDeploying] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);

  const deploymentSteps: DeploymentStep[] = [
    { id: 'validate', label: 'Validating Blueprint', status: 'pending' },
    { id: 'compile', label: 'Compiling Code', status: 'pending' },
    { id: 'optimize', label: 'Optimizing Resources', status: 'pending' },
    { id: 'deploy', label: 'Deploying to Production', status: 'pending' },
  ];

  const [steps, setSteps] = useState(deploymentSteps);

  useEffect(() => {
    if (open) {
      setCode(blueprintCode);
      setIsDeploying(false);
      setCurrentStep(0);
      setSteps(deploymentSteps);
    }
  }, [open, blueprintCode]);

  const simulateDeployment = async () => {
    setIsDeploying(true);
    for (let i = 0; i < deploymentSteps.length; i++) {
      setCurrentStep(i);
      setSteps(prev => prev.map((step, index) => ({
        ...step,
        status: index === i ? 'loading' : 
                index < i ? 'completed' : 'pending'
      })));

      // Simulate step processing
      await new Promise(resolve => setTimeout(resolve, 2000));

      setSteps(prev => prev.map((step, index) => ({
        ...step,
        status: index === i ? 'completed' : 
                index < i ? 'completed' : 'pending'
      })));
    }

    onSave?.(code);
    setIsDeploying(false);
  };

  const handleSave = useCallback(() => {
    simulateDeployment();
  }, [code, onSave]);

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-[1000px] w-[90vw] h-[80vh] flex flex-col">
        <DialogHeader>
          <DialogTitle>Edit CrewAI Code</DialogTitle>
        </DialogHeader>
        <div className="flex-1 mt-4 relative min-h-[500px]">
          {isLoading && (
            <div className="absolute inset-0 flex items-center justify-center bg-background/80 z-50">
              <Loader2 className="h-8 w-8 animate-spin" />
            </div>
          )}
          <div className="h-full w-full">
            <Editor
              defaultLanguage="python"
              value={code}
              theme="vs-dark"
              onChange={(value) => setCode(value || '')}
              onMount={() => setIsLoading(false)}
              options={{
                readOnly: false,
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </div>
        </div>

        {isDeploying && (
          <div className="mt-4 p-4 border rounded-lg bg-card">
            <DeploymentProgress steps={steps} currentStep={currentStep} />
          </div>
        )}

        <div className="flex justify-end gap-2 mt-4">
          <Button variant="secondary" onClick={() => onOpenChange(false)} disabled={isDeploying}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isDeploying}>
            {isDeploying ? 'Deploying...' : 'Deploy Changes'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
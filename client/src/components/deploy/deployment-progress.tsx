import React from 'react';
import { motion } from 'framer-motion';
import { Check, Loader2, XCircle } from 'lucide-react';

export type DeploymentStep = {
  id: string;
  label: string;
  status: 'pending' | 'loading' | 'completed' | 'error';
};

interface DeploymentProgressProps {
  steps: DeploymentStep[];
  currentStep: number;
}

export function DeploymentProgress({ steps, currentStep }: DeploymentProgressProps) {
  return (
    <div className="w-full max-w-md mx-auto">
      {steps.map((step, index) => (
        <div key={step.id} className="relative">
          {/* Connection Line */}
          {index < steps.length - 1 && (
            <div className="absolute left-[15px] top-[30px] w-[2px] h-[40px] bg-border">
              {step.status === 'completed' && (
                <motion.div
                  className="absolute left-0 top-0 w-full bg-primary"
                  initial={{ height: 0 }}
                  animate={{ height: '100%' }}
                  transition={{ duration: 0.5 }}
                />
              )}
            </div>
          )}
          
          {/* Step Content */}
          <div className="flex items-center mb-8">
            {/* Status Icon */}
            <div className="relative mr-4">
              <div className="w-8 h-8 rounded-full border-2 flex items-center justify-center">
                {step.status === 'loading' && (
                  <Loader2 className="w-4 h-4 animate-spin text-primary" />
                )}
                {step.status === 'completed' && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  >
                    <Check className="w-4 h-4 text-primary" />
                  </motion.div>
                )}
                {step.status === 'error' && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", stiffness: 300, damping: 20 }}
                  >
                    <XCircle className="w-4 h-4 text-destructive" />
                  </motion.div>
                )}
              </div>
              
              {/* Active Step Indicator */}
              {step.status === 'loading' && (
                <motion.div
                  className="absolute -inset-1 rounded-full border-2 border-primary"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{
                    duration: 0.5,
                    repeat: Infinity,
                    repeatType: "reverse"
                  }}
                />
              )}
            </div>
            
            {/* Step Label */}
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className={`font-medium ${
                step.status === 'loading' ? 'text-primary' :
                step.status === 'completed' ? 'text-muted-foreground' :
                step.status === 'error' ? 'text-destructive' :
                'text-muted-foreground'
              }`}
            >
              {step.label}
            </motion.div>
          </div>
        </div>
      ))}
    </div>
  );
}

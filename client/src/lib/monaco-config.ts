import { loader } from '@monaco-editor/react';

// Pre-configure Monaco loader
loader.config({
  paths: {
    vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.36.1/min/vs'
  }
});

// Initialize Monaco with Python support
export const initMonaco = async () => {
  try {
    const monaco = await loader.init();

    // Register Python language
    monaco.languages.register({ id: 'python' });

    return monaco;
  } catch (error) {
    console.error('Failed to initialize Monaco editor:', error);
    throw error;
  }
};
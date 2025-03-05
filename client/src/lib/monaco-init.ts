import { loader } from '@monaco-editor/react';

// Configure Monaco loader to use CDN
loader.config({
  paths: {
    vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.36.1/min/vs',
  },
  'vs/nls': {
    availableLanguages: {
      '*': 'en'
    }
  }
});

// Pre-load Monaco
loader.init().catch(error => {
  console.error('Failed to initialize Monaco Editor:', error);
});

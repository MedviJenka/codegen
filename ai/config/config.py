import os

LLM_CONFIGS = {
    "openai": {
        "model": "gpt-4o-mini",
        "api_key": os.getenv('OPENAI_API_KEY')
    },
    "google_api": {}
}

LLM_CONFIG = LLM_CONFIGS["openai"] # Change this to switch between LLMs

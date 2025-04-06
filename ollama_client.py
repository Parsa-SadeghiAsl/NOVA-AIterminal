import requests
import yaml
from typing import List, Dict, Any

class OllamaClient:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.base_url = self.config["ollama"]["base_url"]
        self.model = self.config["ollama"]["model"]
        self.temperature = self.config["ollama"]["temperature"]

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def get_completion(self, prompt: str, context: List[str] = None) -> str:
        # Get command completion from the model.
        try:
            full_prompt = self._build_prompt(prompt, context)
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": full_prompt,
                    "temperature": self.temperature,
                    "stream": False,
                    "system": self._get_system_prompt(),
                },
            )
            response.raise_for_status()
            completion = response.json()["response"].strip()
            
            # Clean up the completion
            completion = completion.split('\n')[0].strip()
            # Remove backticks and quotes from the beginning and end of the completion
            if ['`', '"', "'"] in completion[0] and ['`', '"', "'"] in completion[-1]:
                completion = completion[1:-1]
            
            # Return original prompt if completion is invalid
            # if not any(c in completion for c in [' ', '|', '>', '<', '&', ';']):
            #     return prompt
                
            return completion
        except Exception as e:
            print(f"Error getting completion: {e}")
            return prompt

    def _get_system_prompt(self) -> str:
        # Get the system prompt that defines the model's behavior.
        return """You are NOVA, an expert terminal assistant specialized in command completion and shell operations.
Your task is to help users complete their commands efficiently and correctly. You can also translate natural language commands to shell commands.

Rules:
1. Always provide complete, executable commands
2. Use common Unix/Linux commands and tools
3. Include necessary flags and arguments
4. Handle file paths and glob patterns correctly
5. Support common shell features like pipes, redirections, and background jobs
6. Consider the context of previous commands
7. Never add explanations or descriptions to your completions
8. If the command is already complete, return it as is
9. Prefer standard tools over custom scripts
10. Handle common operations like file manipulation, process management, and system information

Examples of good completions:
- Input: "ls -" → "ls -la"
- Input: "grep error" → "grep -i error *.log"
- Input: "find . -name" → "find . -name '*.py'"
- Input: "ps aux | grep" → "ps aux | grep python"
- Input: "tar -" → "tar -czvf archive.tar.gz directory/"

Examples of natural language to shell command translation:
- Input: "show me files larger than 100MB" → "find . -size +100M"
- Input: "show me all files in the downloads folder" → "ls ~/Downloads"
- Input: "show me all python files in the current directory" → "ls *.py"

Remember: Your goal is to provide the most useful and efficient command completion possible."""
        
    def _build_prompt(self, prompt: str, context: List[str] = None) -> str:
        # Build the prompt for the model.
        base_prompt = """Complete the following command based on the context.
Context is a list of previous commands. Provide only the completed command, nothing else.

Context:
{context}

Command to complete: {prompt}

Completed command:"""
        
        context_str = "\n".join(context) if context else "No previous commands"
        return base_prompt.format(context=context_str, prompt=prompt) 
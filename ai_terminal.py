from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
import yaml
import os
import subprocess
from typing import List
from rich.console import Console
from ollama_client import OllamaClient

class AICompleter(Completer):
    def __init__(self, ollama_client: OllamaClient, command_history: List[str]):
        self.ollama = ollama_client
        self.command_history = command_history

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        if not text.strip():
            return

        try:
            # Get last few commands for context
            context = self.command_history[-5:] if self.command_history else None
            completion = self.ollama.get_completion(text, context)
            
            if completion and completion != text:
                yield Completion(
                    completion,
                    start_position=-len(text),
                    style="class:completion",
                )
        except Exception:
            pass

class NOVATerminal:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.ollama = OllamaClient(config_path)
        self.console = Console()
        self.command_history: List[str] = []
        
        # Setup prompt session
        history_file = os.path.expanduser(self.config["terminal"]["history_file"])
        self.session = PromptSession(
            history=FileHistory(history_file),
            auto_suggest=AutoSuggestFromHistory(),
            style=self._get_style(),
        )

    def _load_config(self, config_path: str) -> dict:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def _get_style(self) -> Style:
        return Style.from_dict({
            "prompt": self.config["style"]["prompt"],
            "completion": self.config["style"]["suggestion"],
            "error": self.config["style"]["error"],
            "info": self.config["style"]["info"],
            "nova": self.config["style"]["nova"],
            "path": self.config["style"]["path"]
        })

    def _get_prompt(self) -> HTML:
        """Get the current prompt with working directory."""
        cwd = os.getcwd()
        home = os.path.expanduser("~")
        if cwd.startswith(home):
            cwd = "~" + cwd[len(home):]
        return HTML(f'<nova>NOVA</nova> <path>{cwd}</path> {self.config["terminal"]["prompt"]}')

    def _execute_command(self, command: str) -> None:
        """Execute a command and handle the output."""
        try:
            # Handle special commands
            if command == "clear":
                os.system('clear')
                return
            elif command.startswith("cd "):
                target_dir = command[3:].strip()
                if not target_dir:
                    target_dir = os.path.expanduser("~")
                os.chdir(target_dir)
                return
            
            # Execute other commands
            result = subprocess.run(
                command,
                shell=True,
                text=True,
                capture_output=True
            )
            if result.stdout:
                self.console.print(result.stdout)
            if result.stderr:
                self.console.print(f"[error]Error: {result.stderr}[/error]")
        except Exception as e:
            self.console.print(f"[error]Error executing command: {e}[/error]")

    def run(self):
        """Run the terminal interface."""
        self.console.print("[bold blue]NOVA[/bold blue] [info]Terminal started. Type 'exit' to quit.[/info]")
        self.console.print("[info]Press Tab for AI completions.[/info]")
        
        while True:
            try:
                # Get user input with completion
                user_input = self.session.prompt(
                    self._get_prompt(),
                    completer=AICompleter(self.ollama, self.command_history),
                )

                if user_input.lower() in ["exit", "quit"]:
                    break

                # Execute command
                self._execute_command(user_input)
                self.command_history.append(user_input)

            except KeyboardInterrupt:
                self.console.print("\n[info]Operation cancelled.[/info]")
                continue
            except EOFError:
                break

        self.console.print("[bold blue]NOVA[/bold blue] [info]Goodbye![/info]")

if __name__ == "__main__":
    terminal = NOVATerminal()
    terminal.run() 
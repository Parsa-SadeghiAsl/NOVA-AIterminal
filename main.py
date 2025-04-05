from ai_terminal import NOVATerminal
import sys
from rich.console import Console

def main():
    console = Console()
    try:
        terminal = NOVATerminal()
        terminal.run()
    except KeyboardInterrupt:
        console.print("\n[bold blue]NOVA[/bold blue] Goodbye!")
        sys.exit(0)
    except Exception as e:
        console.print(f"[error]Error: {e}[/error]")
        sys.exit(1)

if __name__ == "__main__":
    main() 
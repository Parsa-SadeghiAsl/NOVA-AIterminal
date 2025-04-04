from ai_terminal import NOVATerminal
import sys

def main():
    try:
        terminal = NOVATerminal()
        terminal.run()
    except KeyboardInterrupt:
        print("\n[bold blue]NOVA[/bold blue] Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"[error]Error: {e}[/error]")
        sys.exit(1)

if __name__ == "__main__":
    main() 
# NOVA - AI-Powered Terminal

A modern terminal with AI-powered command completion using Ollama's local models.

## Features

- AI-powered command suggestions and completions
- Modern terminal interface
- Command history management
- Context-aware completions
- Customizable configuration

## Requirements

- Python 3.8+
- Ollama installed and running locally
- qwen2.5-coder:1.5b-base model pulled in Ollama

## Installation

1. Clone this repository

2. Make a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Make sure Ollama is running and the model is pulled:
   ```bash
   ollama pull qwen2.5-coder:1.5b-base
   ```

## Usage

Run NOVA:
```bash
python main.py
```

## Configuration

Edit `config.yaml` to customize:
- Model settings
- Prompt styling
- Completion behavior 
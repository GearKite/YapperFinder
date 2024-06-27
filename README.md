# Yapper Finder

Helps you find the people who spam your Matrix chat the most.

## Installation

1. Create a Python virtual environment  
   `python -m venv .venv`
2. Activate the venv  
   `source .venv/bin/activate`
3. Install dependencies  
   `pip install -r requirements.txt`

## Usage

1. Export the chat history from Element to `export.json` (maybe other clients also support this? I haven't tested it)
2. Change/set user display names in `names.json` (optional)
3. Run the script  
   `python main.py`
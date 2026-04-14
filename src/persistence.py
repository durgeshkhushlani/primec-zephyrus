import json
import csv
import os
from typing import Any, List, Dict, Union

"""
File Persistence Module for Aura Retail OS.
Handles JSON and CSV storage with automatic directory creation.
"""

def save_json(filepath: str, data: Any) -> None:
    """Saves data to a JSON file, creating parent directories if needed."""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_json(filepath: str) -> Union[Dict, List]:
    """Loads data from a JSON file. Returns empty dict if file missing."""
    if not os.path.exists(filepath):
        return {}
    
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_csv(filepath: str, rows: List[Dict], headers: List[str]) -> None:
    """Saves a list of dicts to a CSV file."""
    directory = os.path.dirname(filepath)
    if directory:
        os.makedirs(directory, exist_ok=True)
        
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

def load_csv(filepath: str) -> List[Dict]:
    """Loads rows from a CSV file. Returns empty list if file missing."""
    if not os.path.exists(filepath):
        return []
        
    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))

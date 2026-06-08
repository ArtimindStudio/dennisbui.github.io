import os
import requests
import json

# Minimalistic load_env logic
def load_env(path='d:/Projects/Upwork/.env'):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                if '=' in line:
                    key, val = line.split('=', 1)
                    env[key.strip()] = val.strip()
    return env

env = load_env()
AIRTABLE_PAT = env.get('AIRTABLE_PAT')
AIRTABLE_BASE_ID = env.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_ID = env.get('AIRTABLE_TABLE_ID')

url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_PAT}",
    "Content-Type": "application/json"
}

job_data = {
    "fields": {
        "Title": "AI Image Specialist for Luxury Interiors (Repubblica)",
        "Status": "Drafting",
        "Job Description": """Budget: $15 - $35 / hr | Connects Required: 17
AI Image Specialist for Luxury Interiors (Repubblica - Australia)
Posted 3 hours ago

Summary:
Create consistent, premium product imagery and interior visuals for a luxury tile/stone brand. 
Tasks: Multi-tile compositions, randomizing tile faces, AI-assisted interior scenes, material rendering.
Requirement: Understanding scale, texture, lighting, and spatial aesthetics.""",
        "Client Info": "Australian luxury interiors destination. 2 interviewing, 4 invites.",
        "Current Status": "Drafting application. Positioning as 'Architectural Visual Specialist' using Nano Banana 2.",
        "Following Plan": "1. Pitch $30.00/hr Confidence Rate.\n2. Highlight 'Material Fidelity' and 'Randomization Automation'.\n3. Curate high-end architectural rendering portfolio.",
        "ID": "JOB-INTERIOR-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

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
        "Title": "AI Visual Designer with Creative Brand Experience",
        "Status": "Active",
        "Job Description": """Connects Required: ~21 (Expert Level) | Budget: $20 - $60 / hr
AI Visual Designer with Creative Brand Experience. Manual Graphic Design also.
Posted 2 hours ago

Summary: 
Looking for someone to use AI to quickly produce a lot of design concepts (1-2 hours). Pitching to "Big Brands" (e.g., Spotify). 
Must look "Expensive" and "Naturally Designed" (not look like AI).
Manual editing required to fix AI artifacts.

Skills: Gemini Nano, Grok, Photoshop, Banner Ad Design, AI-Generated Art.""",
        "Client Info": "Worldwide, posted 2 hours ago. Pitching to major brands.",
        "Current Status": "Job added. Analyzing 'Big Brand' aesthetic requirements.",
        "Following Plan": "1. Curate premium/expensive-looking portfolio images.\n2. Drafting workflow emphasizing 'No-AI look' via Google Nano Banana 2.\n3. Answering 4 screening questions with expert precision.",
        "ID": "JOB-BRAND-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

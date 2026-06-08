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
        "Title": "AI Image Generation Artist – Mockup Library (Long-Term)",
        "Status": "Active",
        "Job Description": """Connects Required: ~13 | Budget: $5.00 - $20.00 / hr
AI Image Generation Artist – Mockup Library (Long-Term)
Posted 6 hours ago

Summary: 
Building a premium mockup library. Requirements: "Invisible AI," perfect lighting/shadows, consistency across sets (same model/angle). 
Client is aggressive about quality: "No hobbyists, no tourists." 
Long-term partnership potential. 

To Apply: 3-5 photoreal images, workflow breakdown, how to eliminate AI look.""",
        "Client Info": "Worldwide, building premium mockup library. Long-term focus.",
        "Current Status": "Drafting proposal. Focusing on 'Invisible AI' photorealism and PBR lighting breakdown.",
        "Following Plan": "1. Pitch $18.50/hr 'Confidence Rate.'\n2. Highlight Google Nano Banana 2 4K rendering.\n3. Offer single-product 'Blind Test' to prove indistinguishable quality.",
        "ID": "JOB-MOCKUP-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

import os
import requests
import json

# Minimalistic load_env logic
def load_env(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')):
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
        "Title": "Freelance AI Visual Content Producer (Food/Education)",
        "Status": "Drafting",
        "Job Description": """Budget: Fixed-price per batch | Monthly Retainer potential
Freelance AI Visual Content Producer for Irish Food Business (Schools/Education)
Posted 2 days ago

Summary:
Produce monthly suite of AI-generated assets (15-20 stills, 3-4 short videos). Focus on school principals, procurement teams, and parents.
Requirement: Genuine craft, non-generic, high-quality, on-brand.
Tools: Midjourney, Sora/Runway/Kling, ElevenLabs.
Key: Consistent visual identity across the batch.""",
        "Client Info": "Established Irish food business, schools/education sector. Values-led.",
        "Current Status": "Drafting application. Focusing on 'Warmth & Trust' for parents and 'Creative Judgement' for schools.",
        "Following Plan": "1. Highlight 'Food & Education' specialized portfolio.\n2. Emphasize multi-modal capabilities (Still + Video + Audio).\n3. Propose 'Value-led' rate for monthly engagement.",
        "ID": "JOB-PRODUCER-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

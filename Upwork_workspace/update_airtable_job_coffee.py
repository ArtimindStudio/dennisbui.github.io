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
        "Title": "AI Workflow for Social Media Automation (Coffee)",
        "Status": "Drafting",
        "Job Description": """Budget: $100 Fixed-price | Ongoing potential
AI Workflow for Social Media Automation (Coffee Restaurant)
Posted 2 days ago

Summary:
Develop an automated AI workflow to generate multiple social media posts from a single image/post.
Goal: Seamless content creation and management.
Mandatory: Adobe Illustrator, Graphic Design.""",
        "Client Info": "Coffee restaurant owner, worldwide. 3 interviewing.",
        "Current Status": "Drafting application. Positioning as 'Workflow Architect' using n8n + AI + Airtable.",
        "Following Plan": "1. Pitch the 'Single Image to 10 Variations' system.\n2. Highlight n8n social media deployment (Buffer/Meta API).\n3. Propose $100 pilot for the first automated pipeline.",
        "ID": "JOB-COFFEE-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

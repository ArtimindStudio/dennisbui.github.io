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
        "Title": "AI Expert for Workflow Creation",
        "Status": "Active",
        "Job Description": """Connects Required: 11 | Budget: $200 Fixed-price
AI Expert for Workflow Creation
Posted 8 hours ago

Summary:
We are seeking an artificial intelligence expert to design and implement workflows for all company processes... identifying areas for improvement, and developing AI-driven solutions to optimize operations.
Note: Mandatory skills requested by client are Adobe Illustrator, Graphic Design, hinting at a creative/marketing workflow automation.""",
        "Client Info": "USA, Sales & Marketing, Small company (2-9), $16K spent, 44% hire rate.",
        "Current Status": "Job added. Drafting AI workflow and automation strategy.",
        "Following Plan": "1. Highlight Creative/Graphic agent automation.\n2. Draft proposal leveraging n8n + AI + Airtable stack.\n3. Position as an AI Strategy consultant, moving beyond just graphic generation.",
        "ID": "JOB-AUTO-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

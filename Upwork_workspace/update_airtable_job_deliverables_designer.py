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
        "Title": "AI-Assisted Client Deliverables Designer",
        "Status": "Drafting",
        "Job Description": """Hourly Rate: $20.00 - $49.00 | Duration: 1 to 3 months (9 weeks with ongoing potential)
AI-Assisted Client Deliverables Designer (Prompt · Package · Design · Remote)
Posted 4 hours ago
Worldwide

Summary:
Hire 2 Deliverables Designers to take a clear written brief, use AI tools to generate sharp audit insights (UX, branding, site structure), and package everything into a polished, professional deliverable (Canva, Google Slides, pitch decks) that makes the closing presentation inevitable.
Async friendly, flexible ~20 hrs/week.""",
        "Client Info": "Worldwide. Active today (posted 4 hours ago). Project pay model plus hourly baseline.",
        "Current Status": "Drafting application. Positioning as 'AI-Native Deliverables Architect' using Claude/GPT for deep insights and Canva/Photoshop for clean, high-end slide design.",
        "Following Plan": "1. Pitch expert AI prompting for UX/conversion audits.\n2. Emphasize presentation design skills (Canva/Google Slides) with a modern, high-end layout aesthetic.\n3. Reference Case Study 3 (SaaS dashboard / Stripe checkouts) and Case Study 4 (Workflow automation) as proof of our systemized deliverables pipeline.",
        "ID": "JOB-DELIVERABLES-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

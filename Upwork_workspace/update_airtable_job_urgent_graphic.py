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

url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}/recJGwwjGTvOTTJJh"
headers = {
    "Authorization": f"Bearer {AIRTABLE_PAT}",
    "Content-Type": "application/json"
}

job_data = {
    "fields": {
        "Title": "Urgent Graphic Design Tasks (Illustrator & Photoshop)",
        "Status": "Drafting",
        "Job Description": """Hourly Rate: $10.00 - $18.00 (Willing to pay higher rates for experts) | Duration: Less than 1 month
Urgent Graphic Design Tasks Needed Today
Posted 4 hours ago
Worldwide

Summary:
Must be available to work now. Need a couple of urgent graphic design tasks completed today.
Mandatory skills: Graphic Design, Adobe Illustrator, Adobe Photoshop.""",
        "Client Info": "Worldwide. Active today (last viewed 1 hour ago). 10-15 proposals.",
        "Current Status": "Drafting application. Positioning as 'AI-Native Creative' using Google Nano Banana 2 & Veo as main creative engine, with Photoshop/Canva as finishing.",
        "Following Plan": "1. Pitch immediate availability and same-day delivery.\n2. Emphasize Google AI ecosystem (Nano Banana 2/Veo) for high-speed creative asset generation.\n3. Show how Photoshop/Canva are used for the final layout, typography, and logo stitching.",
        "ID": "JOB-URGENT-GRAPHIC-001"
    }
}

response = requests.patch(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully updated job in Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

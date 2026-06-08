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
        "Title": "Shopify Web Developer for Store Edits",
        "Status": "Drafting",
        "Job Description": """Hourly: $12.00 - $18.00 | Duration: 1 to 3 months | Intermediate Level
Shopify Web Developer for Store Edits
Posted yesterday | Worldwide

Summary:
We are seeking a skilled Shopify web developer to make specific edits and changes to our Shopify store. The ideal candidate will have experience in customizing Shopify themes and ensuring seamless functionality. Responsibilities include implementing design changes, optimizing site performance, and troubleshooting issues.

Mandatory Skills: HTML, CSS
Nice-to-have Skills: Web Design, Web Development

Activity: 15 to 20 Proposals, 1 Interviewing, 2 Invites, 1 Unanswered Invite
Client: Australia, 2 jobs posted, 0% hire rate, 1 open job, Health & Fitness, Payment Method Verified""",
        "Client Info": "Australia. 2 jobs posted, 0% hire rate, 1 open job. Health & Fitness, Individual client. Payment method verified, Phone number verified. Member since Aug 18, 2025. Last viewed yesterday.",
        "Current Status": "Drafting application. Positioning as 'Technical Shopify & Frontend Liquid Developer' specializing in custom theme edits, layout adjustments, performance optimization, and bug fixing.",
        "Following Plan": "1. Highlight strong HTML/CSS/Liquid skills for precise theme edits without breaking responsiveness.\n2. Address the optimization aspect—image compression, script minimization, and theme code cleanup.\n3. Position at a rate of $18.00/hr to match the client's upper limit while showcasing high confidence and expert value.\n4. Attach portfolio items related to mobile UX auditing (MUD\\WTR Mobile PDP UX Audit).",
        "ID": "JOB-SHOPIFY-EDITS-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

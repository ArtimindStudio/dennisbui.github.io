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
        "Title": "Shopify Store Creation",
        "Status": "Drafting",
        "Job Description": """Hourly Rate: $15.00 - $27.00 | Duration: Less than 1 month | Less than 30 hrs/week
Shopify Store Creation
Posted 5 days ago | Worldwide | Intermediate

Summary:
Seeking a skilled freelancer to create a Shopify store. Experience in web development and Shopify templates required. Basic Shopify store with essential features, user-friendly, ready to launch within a week.

Mandatory Skills: Shopify, Shopify Templates
Nice-to-have: HTML, Web Development

Activity: 5-10 Proposals, 3 Interviewing, 6 Invites Sent, Last Viewed 5 days ago""",
        "Client Info": "Worldwide. Posted 5 days ago. 3 already interviewing. Moderate competition (5-10 proposals). Client slightly inactive (last viewed 5 days ago).",
        "Current Status": "Drafting application. Positioning as 'AI-Enhanced Shopify Architect' — delivering a conversion-optimized, mobile-first store with premium design using Google AI-Native workflow for rapid visual asset creation + Shopify Liquid expertise.",
        "Following Plan": "1. Pitch as Shopify expert with AI-enhanced design workflow for rapid store creation.\n2. Emphasize mobile-first, conversion-optimized store architecture (not just 'basic' setup).\n3. Highlight Google Nano Banana 2 for product photography enhancement and lifestyle imagery.\n4. Reference Canva for brand assets (banners, social graphics) and Photoshop for final polish.\n5. Propose $25/hr (Confidence Play at upper range) to signal premium execution quality.",
        "ID": "JOB-SHOPIFY-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

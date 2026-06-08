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
        "Title": "AI Creative Designer (Ecommerce / SaaS Ad Variations)",
        "Status": "Drafting",
        "Job Description": """Budget: $5 - $20 / hr | Connects Required: ~16
AI Creative Designer (Ecommerce / SaaS Ad Variations)
Posted yesterday

Summary:
Taking existing ad creatives and generating 10-20 high-quality visual variations using AI. Focus on Ecommerce (Shopify) and SaaS (Stripe/Linear style). 
Requirement: Keep text/overlays/UI consistent. 
No cartoonish or low-quality AI.

Style: Clean, minimal, premium, ultra-realistic.""",
        "Client Info": "B2B SaaS brand, Shopify focused. Worldwide.",
        "Current Status": "Drafting application. Positioning as 'Creative Automation Architect' for high-volume variations.",
        "Following Plan": "1. Propose $18.00/hr rate.\n2. Highlight 'Google Antigravity' for UI/Overlay consistency.\n3. Curate Shopify/SaaS-style portfolio assets.",
        "ID": "JOB-SAAS-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

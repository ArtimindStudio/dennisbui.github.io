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
        "Title": "Product Imagery Update Using Template",
        "Status": "Active",
        "Job Description": """Connects Required: 13 | Budget: Hourly (Bid Range $10 - $23)
Product Imagery Update Using Template
Posted 6 days ago
Worldwide

Summary:
We are seeking a skilled freelancer to update our product imagery across our site using a provided template. The initial task involves updating one product as an example before proceeding to the entire catalog. The ideal candidate should have experience in AI image generation, image editing and design, ensuring the final images align with our brand's aesthetic and the template provided.

Client Info: USA, Food & Beverage, 5.0 rating, 100% hire rate, $2.5K spent.""",
        "Client Info": "USA, Food & Beverage (100-1,000 people), 100% Hire Rate",
        "Current Status": "Job added. Analyzing template-driven AI rendering strategy.",
        "Following Plan": "1. Curate Food & Beverage product imagery samples.\n2. Drafting template-based AI workflow using Nano Banana 2.\n3. Tailoring proposal for 'Example Product' test.",
        "ID": "JOB-FOOD-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

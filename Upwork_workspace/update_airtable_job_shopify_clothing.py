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
        "Title": "Shopify Expert for Clothing Store Setup",
        "Status": "Drafting",
        "Job Description": """Hourly: $12.00 - $27.00 | Duration: Less than 1 month | Intermediate Level
Shopify Expert for Clothing Store Setup
Posted yesterday | Worldwide

Summary:
I am seeking a Shopify expert to set up a complete online store for my clothing brand. The ideal candidate will have experience in designing visually appealing and functional e-commerce platforms. Responsibilities include setting up the store, integrating payment systems, and ensuring a seamless user experience.

Mandatory Skills: Shopify, HTML
Nice-to-have Skills: Shopify Templates, Web Development

Activity: 10 to 15 Proposals, 10 Interviewing, 20 Invites Sent, 8 Unanswered Invites
Client: India, 3 jobs posted, 0% hire rate, 3 open jobs, Sales & Marketing, Payment Method Verified""",
        "Client Info": "India. 3 jobs posted, 0% hire rate, 3 open jobs. Sales & Marketing, Individual client. Payment method verified, Phone number verified. Member since May 31, 2026. Last viewed by client: 5 hours ago.",
        "Current Status": "Drafting application. Positioning as 'Premium Shopify E-Commerce Architect' focusing on clothing/fashion brand setup, seamless payment gateway integration, and high-converting visual storefronts.",
        "Following Plan": "1. Highlight clothing/fashion store expertise with visually appealing, modern styling.\n2. Address the core need for seamless payment gateway setup and end-to-end user experience (UX).\n3. Emphasize clean theme customization using HTML/CSS/Liquid.\n4. Propose a highly competitive hourly rate of $24.00/hr to match the client's budget and show confidence.",
        "ID": "JOB-SHOPIFY-CLOTHING-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

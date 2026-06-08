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
        "Title": "E-commerce Assistant for GoDaddy and Shopify",
        "Status": "Drafting",
        "Job Description": """Hourly: $20.00 - $25.00 | Duration: 1 to 3 months | Intermediate Level
E-commerce Assistant for Golf Apparel Brand – Shopify & GoDaddy Setup (TIGRÉE)
Posted 2 days ago | Worldwide

Summary:
We are launching a premium eco-friendly golf apparel brand (TIGRÉE). We need a detail-oriented E-commerce Assistant to help set up our online store and upload products. This is not a creative role (no design required) but a technical/operational role following a spec sheet precisely.

Key Responsibilities:
1. Domain & Platform Setup: Connect GoDaddy domain to Shopify (DNS/A record updates), verify SSL.
2. Product Upload: Images, descriptions, prices, variants, SKUs, GS1 barcodes (GTIN), organize collections.
3. Store Administration: Shipping zones, check mobile/desktop views.

Mandatory Skills: Shopify, Data Entry
Nice-to-have Skills: Shopify Templates, English

Activity: 5 to 10 Proposals, 0 Interviewing, 0 Invites, 1 Hire
Client: USA (Edgewater), 1 job posted, 0% hire rate (1 hire, 0 active), Payment Method Verified""",
        "Client Info": "USA (Edgewater). 1 job posted, 0% hire rate (shows 1 hire, 0 active), Payment Method Verified. Member since May 30, 2026.",
        "Current Status": "Drafting application. Positioning as 'Technical E-Commerce Assistant' with a strong focus on precise data entry (SKUs, GTIN/barcodes), DNS configuration expertise, and Shopify admin efficiency.",
        "Following Plan": "1. Directly answer the application prompts: explain Shopify product upload workflow and how to point GoDaddy domains to Shopify.\n2. Emphasize operational precision (zero errors on SKUs, pricing, and barcodes for correct fulfillment).\n3. Answer screening questions ('recent experience with similar projects' and 'frameworks worked with').\n4. Propose $24.00/hr to stay highly competitive within their $20-$25 range.",
        "ID": "JOB-SHOPIFY-GODADDY-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

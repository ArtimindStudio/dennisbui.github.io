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
        "Title": "AI Static Image Designer — DTC Health & Wellness Brand",
        "Status": "Active",
        "Job Description": """Budget: $1,500/month base + performance bonuses
AI Static Image Designer — DTC Health & Wellness Brand
Posted 3 days ago
Worldwide

Summary
We're a fast-growing DTC supplements brand scaling on Meta. We need a static image designer who can produce high-quality ad creatives at volume using AI tools.

What you'll do:
Produce 30–50 static ad images per day using AI generation tools (Midjourney, Flux, DALL-E, Nanobanana, or similar) + Photoshop/Canva for finishing
Create ~10 unique ad concepts daily with multiple variations of each
Work directly with our media buying team to iterate on winners and keep the creative pipeline full
Build static creative libraries from scratch for new product launches
Create images for ads, landing pages, and advertorials

What we're looking for:
Proven experience creating static ad creatives for ecommerce brands in health, wellness, or supplements
You understand direct response — you know the difference between a pretty image and one that stops the scroll and drives clicks
Deep experience with AI image generation tools. You already have a workflow. We're not teaching you.
Strong finishing skills in Photoshop and/or Canva
High output without sacrificing quality. 30–50 images/day is the expectation.
Self-managed. You don't need to be chased for deliverables.

Big plus:
You've created ads that actually ran on Meta with real performance data
Familiarity with supplements/health compliance on Meta
Budget: $1,500/month base + performance bonuses on winning creatives""",
        "Client Info": "Worldwide, posted 3 days ago",
        "Current Status": "Job added to database. Preparing portfolio and workflow explanation.",
        "Following Plan": "1. Curate health/wellness portfolio images.\n2. Drafting high-output AI workflow (Midjourney + Nanobanana).\n3. Tailoring cover letter for supplement industry performance.",
        "ID": "JOB-HEALTH-002"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

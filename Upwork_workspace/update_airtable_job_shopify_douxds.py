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
        "Title": "Shopify Store Design & Development — DOUXDS",
        "Status": "Drafting",
        "Job Description": """Fixed Price: $1,250 | Duration: Within 1 month | Expert Level
Shopify Store Design and Development — DOUXDS (douxds.com)
Posted 41 minutes ago | Worldwide | Expert

Summary:
Full website redesign + development using Elixir theme. Client owns douxds.com (men's skincare DTC brand). Needs: Home Page, Hero Device Product Page, Supplementary Formulation Page, Bundle Page, Collection Page, Mega Menu, Cart. All product pages need subscription pre-selected (references mengotomars.com and manscaped.com). Middle/bottom funnel focus.

Client has TONS of real content on Instagram (@douxds). Copy NOT needed — just design + Shopify section assembly. Client wants autonomous execution ("I do not want to go back and forth").

Mandatory Skills: Liquid, Shopify, Web Design, Shopify Templates, Graphic Design
Preferred Location: Europe

Activity: 5-10 Proposals, 1 Interviewing, Last Viewed 19 min ago (VERY ACTIVE)
Client: US (Chantilly), 5.0★, $7.6K spent, 58 jobs posted, Payment Verified""",
        "Client Info": "United States (Chantilly). 5.0 rating, $7.6K total spent, 58 jobs posted, 23% hire rate, 16 hires. Payment verified. Media & Entertainment, Small company (2-9). Member since Jan 2019. Very active — last viewed 19 min ago.",
        "Current Status": "Drafting application. Positioning as 'DTC Shopify Conversion Architect' with deep knowledge of DOUXDS brand palette (forest green #1B2E22, gold #C9B68C, cream #FAFAF8), Elixir theme sections, subscription-first UX (Loop Subscriptions), and autonomous execution capability.",
        "Following Plan": "1. Demonstrate deep brand research — reference exact DOUXDS color palette, typography (Instrument Serif + DM Sans), and existing Funnelish landing page design language.\n2. Show subscription-first UX expertise — reference Manscaped/Mango patterns + Loop Subscriptions integration.\n3. Emphasize autonomous execution — 'no back and forth' aligns with AI-native workflow.\n4. Highlight Elixir theme section-building experience.\n5. Bid $1,250 (matching client budget) to signal expert-level confidence.",
        "ID": "JOB-SHOPIFY-DOUXDS-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

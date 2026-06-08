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
        "Title": "Automated Deal Sourcing & AI Diligence Workflows",
        "Status": "Drafting",
        "Job Description": """Duration: 1 to 3 months | Level: Expert
Automated Deal Sourcing Workflows (Hospice & Senior Care Acquisition)
Posted 2 weeks ago
Worldwide

Summary:
Build two workflows:
Workflow 1: Automated Deal Sourcing & Outreach (n8n, Excel/Airtable data cleaning, Apollo.io email enrichment, Mailgun outbound tracking, HubSpot sync, DNS warmups).
Workflow 2: AI-Powered Initial Diligence (CIM/document ingestion, Claude/OpenAI data extraction, investment scoring, DOCX/PPTX programmatic generation, lightweight portal UI).
Requires Standard Operating Handbooks for both. Open budget based on experience.""",
        "Client Info": "Worldwide. PE Acquisition target search. Expert tier.",
        "Current Status": "Drafting application. Positioning as 'M&A Operations Architect' with extensive experience in n8n pipelines, Python programmatic doc generation, and PE/M&A transaction logic.",
        "Following Plan": "1. Pitch Case Study 4 (n8n Ingestion + Enrichment + CRM sync pipeline) as direct proof of Workflow 1.\n2. Detail Python script setup for clean, template-based DOCX/PPTX generation for Workflow 2.\n3. Outline the structure of the 'Standard Operating Handbooks' (SOPs) to address documentation needs.",
        "ID": "JOB-WORKFLOW-002"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

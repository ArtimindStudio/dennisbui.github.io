import os
import requests
import json

# Load env from .env file
def load_env(path='.env'):
    env = {}
    with open(path) as f:
        for line in f:
            if '=' in line:
                key, val = line.split('=', 1)
                env[key.strip()] = val.strip()
    return env

env = load_env('d:/Projects/Upwork/.env')
AIRTABLE_PAT = env.get('AIRTABLE_PAT')
AIRTABLE_BASE_ID = env.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_ID = env.get('AIRTABLE_TABLE_ID')

url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_PAT}",
    "Content-Type": "application/json"
}

print(f"Fetching from: {url}")
response = requests.get(url, headers=headers, params={"maxRecords": 5})

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

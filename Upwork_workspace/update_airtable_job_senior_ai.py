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
        "Title": "Senior AI Image & Video Specialist (TIGRÉE/Jewelry - Invite)",
        "Status": "Drafting",
        "Job Description": """Hourly: $6.00 - $20.00 | Duration: More than 6 months | Expert Level
Senior AI Image & Video Specialist - Ecom, Jewelry, Meta Ads, Graphic Design
Posted May 30, 2026 | Worldwide

Summary:
Produce photorealistic, professional-grade visual assets for a 7-figure e-commerce jewelry brand (anime jewelry and accessories). Generate and composite luxury AI environments, create cinematic AI videos for Meta/TikTok ads, manually composite/color-grade physical products into scenes using Photoshop/After Effects to eliminate the 'cheap AI look', and handle graphic design/ad copy.
Must include 'seesaw' at the start and 'clutch' at the end of the response to the first question.

Skills: AI Image Generation, AI Video Generation, Photoshop, After Effects, Meta Ads, Graphic Design

Client: Australia, 3.49 rating (44 reviews), 122 jobs posted, 49% hire rate, 108 hires, 52 active, $26K total spent, $9.78/hr avg rate paid.
Personal Note: Lou-Ann D. invited Dennis to apply directly!""",
        "Client Info": "Australia. 3.49 rating, 122 jobs posted, 49% hire rate, 108 hires, 52 active, $26K total spent, $9.78/hr avg hourly rate paid. Payment verified. Invited user (Lou-Ann D.).",
        "Current Status": "Drafting application. Positioning as 'Senior Creative & AI Compositing Specialist' specializing in luxury e-commerce product staging, custom Photoshop post-processing to remove the 'AI look', and ad creative automation.",
        "Following Plan": "1. Respond directly to the invitation from Lou-Ann D. expressing enthusiasm for the anime jewelry niche.\n2. Address the core challenge: jewelry compositing requires pixel-perfect reflections, lighting alignment, and shadows to look realistic, not just prompt generation.\n3. Show deep expertise in the workflow: generating high-end marble/stone backgrounds in Midjourney/Flux, then manual compositing, shadow rendering, and color grading in Photoshop.\n4. Propose $20.00/hr (top of the budget) to signal elite capability, noting the AI-native workflow delivers 3-5x the speed of standard designers.\n5. Answer screening questions incorporating the required keywords: start first question response with 'seesaw' and end it with 'clutch'.",
        "ID": "JOB-SENIOR-AI-JEWELRY-001"
    }
}

response = requests.post(url, headers=headers, json=job_data)

if response.status_code == 200:
    print("Successfully added job to Airtable.")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)

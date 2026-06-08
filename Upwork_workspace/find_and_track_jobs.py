import os
import re
import sys
import asyncio
import requests
import smtplib
import ssl
import datetime
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from playwright.async_api import async_playwright

# Load .env file variables
def load_env(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env[key.strip()] = val.strip()
    return env

env = load_env()
AIRTABLE_PAT = env.get('AIRTABLE_PAT')
AIRTABLE_BASE_ID = env.get('AIRTABLE_BASE_ID')
AIRTABLE_TABLE_ID = env.get('AIRTABLE_TABLE_ID')
GMAIL_USER = env.get('GMAIL_USER')
GMAIL_APP_PASSWORD = env.get('GMAIL_APP_PASSWORD')
GEMINI_API_KEY = env.get('GEMINI_API_KEY')

AIRTABLE_URL = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_ID}"
AIRTABLE_HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_PAT}",
    "Content-Type": "application/json"
}

# Auto-fail timeout configuration (in days)
AUTO_FAIL_DAYS = 14

# Keywords to filter jobs
KEYWORDS = [
    r'\bn8n\b', r'\bautomation\b', r'\bworkflow\b', r'\bmake\.com\b', 
    r'\bzapier\b', r'\bgenerative ai\b', r'\bai creative\b', r'\bmidjourney\b',
    r'\bflux\b', r'\brunway\b', r'\bkling\b', r'\bai image\b', r'\bai video\b',
    r'\bai voice\b', r'\belevenlabs\b', r'\bai agent\b', r'\bchatbot\b'
]

# Check existing records and auto-fail expired applications
def process_existing_records_and_check_timeouts():
    existing_titles = set()
    url = f"{AIRTABLE_URL}?maxRecords=100"
    
    print("Checking existing records and running application timeout checks...")
    try:
        res = requests.get(url, headers=AIRTABLE_HEADERS)
        if res.status_code == 200:
            records = res.json().get('records', [])
            today = datetime.date.today()
            
            for r in records:
                fields = r.get('fields', {})
                record_id = r.get('id')
                status = fields.get('Status')
                title = fields.get('Title')
                applied_date_str = fields.get('Applied Date')
                
                if title:
                    existing_titles.add(title.strip().lower())
                    
                # Timeout Decay logic: Status == 'Applied' and >= 14 days old
                if status == 'Applied' and applied_date_str:
                    try:
                        applied_date = datetime.datetime.strptime(applied_date_str, "%Y-%m-%d").date()
                        delta = (today - applied_date).days
                        if delta >= AUTO_FAIL_DAYS:
                            print(f"Auto-failing job '{title}' (applied {delta} days ago)...")
                            patch_url = f"{AIRTABLE_URL}/{record_id}"
                            patch_data = {
                                "fields": {
                                    "Status": "Failed",
                                    "Current Status": f"Auto-failed: No response after {delta} days."
                                },
                                "typecast": True
                            }
                            patch_res = requests.patch(patch_url, headers=AIRTABLE_HEADERS, json=patch_data)
                            if patch_res.status_code == 200:
                                print(f"Successfully auto-failed '{title}'.")
                            else:
                                print(f"Failed to auto-fail '{title}': {patch_res.status_code} - {patch_res.text}")
                    except Exception as e:
                        print(f"Error parsing date or patching record: {e}")
        else:
            print(f"Warning: Could not fetch existing Airtable jobs. Status: {res.status_code}")
    except Exception as e:
        print(f"Warning: Error fetching Airtable jobs: {e}")
        
    return existing_titles

# Fetch Himalayas API (REST call)
def fetch_himalayas_jobs():
    jobs = []
    for kw in ['n8n', 'automation', 'generative ai', 'ai creative']:
        url = f"https://himalayas.app/jobs/api/search?q={kw}&limit=20"
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json().get('jobs', [])
                for j in data:
                    jobs.append({
                        'title': j.get('title'),
                        'company': j.get('company', {}).get('name', 'Unknown'),
                        'description': j.get('description', ''),
                        'url': j.get('application_link') or j.get('url'),
                        'location': j.get('location', 'Remote'),
                        'source': 'Himalayas'
                    })
        except Exception as e:
            print(f"Error fetching from Himalayas for '{kw}': {e}")
    return jobs

# Fetch Remotive (REST call)
def fetch_remotive_jobs():
    jobs = []
    url = "https://remotive.com/api/remote-jobs?limit=50"
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json().get('jobs', [])
            for j in data:
                jobs.append({
                    'title': j.get('title'),
                    'company': j.get('company_name', 'Unknown'),
                    'description': j.get('description', ''),
                    'url': j.get('url'),
                    'location': j.get('candidate_required_location', 'Remote'),
                    'source': 'Remotive'
                })
    except Exception as e:
        print(f"Error fetching from Remotive: {e}")
    return jobs

# Fetch We Work Remotely (REST RSS call)
def fetch_wwr_jobs():
    jobs = []
    feeds = [
        "https://weworkremotely.com/categories/remote-programming-jobs.rss",
        "https://weworkremotely.com/categories/remote-design-jobs.rss"
    ]
    for url in feeds:
        try:
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                root = ET.fromstring(res.content)
                for item in root.findall('.//item'):
                    title = item.find('title').text
                    desc = item.find('description').text
                    link = item.find('link').text
                    company = "Unknown"
                    job_title = title
                    if ":" in title:
                        parts = title.split(":", 1)
                        company = parts[0].strip()
                        job_title = parts[1].strip()
                    
                    jobs.append({
                        'title': job_title,
                        'company': company,
                        'description': desc,
                        'url': link,
                        'location': 'Remote',
                        'source': 'We Work Remotely'
                    })
        except Exception as e:
            print(f"Error fetching from WWR: {e}")
    return jobs

# Scrape Working Nomads via Playwright
async def fetch_working_nomads_jobs(page):
    jobs = []
    print("Navigating to Working Nomads...")
    url = "https://www.workingnomads.com/remote-artificial-intelligence-jobs"
    try:
        await page.goto(url, timeout=25000)
        await page.wait_for_timeout(3000)
        
        links = await page.query_selector_all("a")
        target_links = []
        for l in links:
            href = await l.get_attribute("href")
            if href and href.startswith("/jobs/"):
                text = await l.inner_text()
                target_links.append((text, href))
                
        print(f"Found {len(target_links)} links containing '/jobs/' on Working Nomads.")
        
        # Scrape detail page of first 10 matching ones to get full descriptions
        for text, href in target_links[:10]:
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            if len(lines) >= 2:
                title = lines[0]
                company = lines[1]
                detail_url = f"https://www.workingnomads.com{href}"
                
                # Fetch full desc
                detail_page = await page.context.new_page()
                try:
                    await detail_page.goto(detail_url, timeout=15000)
                    desc_elem = await detail_page.query_selector(".job-description") or await detail_page.query_selector("body")
                    desc_text = await desc_elem.inner_text() if desc_elem else " | ".join(lines)
                except Exception as e:
                    desc_text = " | ".join(lines)
                finally:
                    await detail_page.close()
                    
                jobs.append({
                    'title': title,
                    'company': company,
                    'description': desc_text,
                    'url': detail_url,
                    'location': 'Remote',
                    'source': 'Working Nomads'
                })
    except Exception as e:
        print(f"Error scraping Working Nomads: {e}")
    return jobs

# Scrape Mercor via Playwright (uses persistent logged-in context)
async def fetch_mercor_jobs(page):
    jobs = []
    print("Navigating to Mercor Explore...")
    try:
        await page.goto("https://work.mercor.com/explore", timeout=25000)
        await page.wait_for_timeout(5000)
        
        body_text = await page.inner_text("body")
        if "Sign in" in body_text or "Log in" in body_text or "Resume" not in body_text:
            print("[Info] Mercor requires login. Skipping Mercor. Run script with --headful to perform login once.")
            return jobs
            
        # Find elements containing rate texts (e.g. $60 - $200 / hour)
        card_locators = page.locator("div").filter(has_text=re.compile(r'\$\d+.*hour'))
        count = await card_locators.count()
        print(f"Found {count} potential Mercor card elements.")
        
        for i in range(min(count, 10)):
            card_text = await card_locators.nth(i).inner_text()
            lines = [line.strip() for line in card_text.split("\n") if line.strip()]
            if len(lines) >= 2:
                title = lines[0]
                rate = ""
                for line in lines:
                    if "$" in line and "hour" in line:
                        rate = line
                        break
                description = f"Mercor Opportunity. Rate: {rate}. Detail:\n" + "\n".join(lines)
                jobs.append({
                    'title': title,
                    'company': 'Mercor Platform',
                    'description': description,
                    'url': "https://work.mercor.com/explore",
                    'location': "Remote",
                    'source': 'Other'  # Fallback for source select, we can classify it
                })
    except Exception as e:
        print(f"Error scraping Mercor: {e}")
    return jobs

# Scrape Indeed via Playwright
async def fetch_indeed_jobs(page):
    jobs = []
    print("Navigating to Indeed...")
    url = "https://www.indeed.com/jobs?q=AI+automation+n8n&l=Remote&sc=0kf%3Ajt%28contract%29%3B"
    try:
        await page.goto(url, timeout=25000)
        await page.wait_for_timeout(4000)
        
        title = await page.title()
        if "Access Denied" in title or "Attention Required" in title:
            print("[Info] Indeed blocked headless browser. Skipping Indeed. Run script with --headful to solve Captcha.")
            return jobs
            
        job_cards = await page.query_selector_all(".job_seen_beacon")
        print(f"Found {len(job_cards)} job cards on Indeed.")
        
        for card in job_cards[:10]:
            title_elem = await card.query_selector("h2.jobTitle")
            title_text = await title_elem.inner_text() if title_elem else ""
            
            company_elem = await card.query_selector("[data-testid='company-name']")
            company_text = await company_elem.inner_text() if company_elem else "Unknown"
            
            link_elem = await card.query_selector("h2.jobTitle a")
            href = await link_elem.get_attribute("href") if link_elem else ""
            job_url = f"https://www.indeed.com{href}" if href else url
            
            snippet_elem = await card.query_selector(".job-snippet")
            snippet_text = await snippet_elem.inner_text() if snippet_elem else ""
            
            if title_text:
                jobs.append({
                    'title': title_text,
                    'company': company_text,
                    'description': snippet_text,
                    'url': job_url,
                    'location': "Remote",
                    'source': 'Other'
                })
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
    return jobs

# Filter job list based on keywords
def filter_and_deduplicate_jobs(raw_jobs, existing_titles):
    filtered = []
    seen_urls = set()
    
    for j in raw_jobs:
        title = j['title']
        desc = j['description']
        url = j['url']
        
        if not title or not desc or not url:
            continue
            
        if url in seen_urls:
            continue
            
        if title.strip().lower() in existing_titles:
            continue
            
        match_found = False
        text_to_search = (title + " " + desc).lower()
        for kw_pattern in KEYWORDS:
            if re.search(kw_pattern, text_to_search):
                match_found = True
                break
                
        if match_found:
            seen_urls.add(url)
            filtered.append(j)
            
    return filtered

# Classify job and generate cover letter & plan
def generate_application_materials(job):
    title = job['title']
    desc = job['description']
    
    creative_score = len(re.findall(r'(creative|design|image|video|midjourney|art|graphics|ugc|portfolio|aesthetic)', desc.lower()))
    automation_score = len(re.findall(r'(automation|n8n|workflow|api|integration|database|sync|make|zapier|developer|script)', desc.lower()))
    
    is_creative = creative_score > automation_score
    cover_letter = ""
    following_plan = ""
    category = "Automation"
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        if is_creative:
            category = "Creative"
            cover_letter = f"""Hi there,

I am high-energy about your project looking for an AI Creative Producer for '{title}'. I specialize in generating premium, "invisible AI" visual assets (stills, video, and audio) and scaling ad variations while maintaining 100% brand consistency.

My technical workflow is built on a custom AI-native design engine:
1. Brand DNA Mapping: Using Google Antigravity to lock layout coordinates, UI overlays, and typography so they do not drift.
2. Generative Content: Google Nano Banana 2, VEO, and Kling AI for hyper-realistic 4K product staging, B-roll, and textures.
3. Meticulous Finishing: Professional compositing and retouching in Adobe Photoshop and Canva to ensure web-ready, high-end outputs.

I specialize in direct-response ad variations that drive clicks, not just pretty images. You can view my portfolio showcases (like the Oasis Organic Energy campaign) at my site, or I can share my high-resolution assets directly.

I'm ready to start and can deliver brand-safe visual variations at scale.

Best regards,
Dennis B.
hello@artimind.com"""
            
            following_plan = """1. Review brand guidelines & compile source product assets.
2. Setup Google Antigravity DNA map to lock down UI elements/layouts.
3. Run prompt iterations in Nano Banana 2 to generate initial high-fidelity variations.
4. Meticulously edit in Photoshop & preset templates in Canva.
5. Deliver draft variations for review and optimization."""
        else:
            cover_letter = f"""Hi there,

I am high-energy about your project requesting help with '{title}'. I specialize in building custom AI-native automation pipelines and workflow architectures, specifically using n8n, APIs, and Airtable.

My typical workflow uses a premium setup to automate and connect systems seamlessly:
1. System & Automation Setup: n8n and Python scripts to bridge databases, webhooks, and REST APIs.
2. Generative Content (if needed): Syncing Google Gemini and Claude models to perform data analysis, lead enrichment, or content generation.
3. Meticulous QA: Rigorous logging and error tracking (e.g. in Airtable/Slack) to ensure a 100% reliable system.

For your project, I would implement:
- System integration matching your specific requirements.
- Automated sync and data pipeline logic to handle errors gracefully.

I would love to connect and show you relevant case studies of automated engines I've built.

Best regards,
Dennis B.
hello@artimind.com"""

            following_plan = """1. Audit client's existing workflow and document current manual bottlenecks.
2. Draft structural schemas for the n8n nodes and API requirements.
3. Build the core n8n workflow nodes in a staging environment.
4. Establish logging & validation tracking via Airtable or DB.
5. Perform end-to-end sandbox testing before pushing to production."""
            
    else:
        try:
            prompt = f"""
            Write a highly customized, professional, and direct-response cover letter for the following remote job posting.
            
            User Details:
            - Name: Dennis B.
            - Email: hello@artimind.com
            - Website: artimind.com
            - Tech Stack: n8n, Python, APIs, Google Antigravity, Google Nano Banana 2, Runway Gen-3, Kling AI, ElevenLabs, Photoshop, Canva.
            
            Job Title: {title}
            Job Description: {desc}
            
            Rules:
            1. Write a compelling, personalized cover letter from Dennis B.
            2. Reference specific tools from his stack that match the job requirements.
            3. Highlight his dual-specialty: AI Automation Architect (if the job is technical) or AI Creative Producer (if the job is design/creative).
            4. Keep it concise, professional, and highlight high-energy alignment.
            5. Output ONLY the cover letter.
            """
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                cover_letter = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                raise Exception(f"Gemini API Error: {res.status_code}")
        except Exception as e:
            print(f"Gemini generation failed, falling back to template: {e}")
            return generate_application_materials({**job, 'description': 'FORCE_FALLBACK'})
            
        try:
            plan_prompt = f"""
            Generate a 4-5 step 'Following Plan' outlining exactly how Dennis B. will execute the following job.
            Job Title: {title}
            Job Description: {desc}
            
            Output ONLY the numbered list.
            """
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": plan_prompt}]}]
            }
            res = requests.post(url, json=payload, timeout=15)
            if res.status_code == 200:
                following_plan = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            else:
                following_plan = "1. Kickoff meeting.\n2. Develop solution.\n3. Test.\n4. Deploy."
        except Exception as e:
            following_plan = "1. Audit requirement.\n2. Build staging environment.\n3. Finalize production deployment."

    return category, cover_letter, following_plan

# Extract email address if present in job description
def extract_application_email(desc):
    email_regex = r'[\w\.-]+@[\w\.-]+\.\w+'
    emails = re.findall(email_regex, desc)
    if emails:
        filtered_emails = [e for e in emails if not any(x in e.lower() for x in ['example.com', 'domain.com'])]
        if filtered_emails:
            return filtered_emails[0]
    return None

# Send email application automatically via SMTP
def send_email_application(to_email, job_title, cover_letter):
    if not GMAIL_USER or GMAIL_APP_PASSWORD == "your_gmail_app_password_here" or not GMAIL_APP_PASSWORD:
        print(f"Skipping auto-email for '{job_title}': Gmail credentials not fully configured.")
        return False
        
    print(f"Attempting to send automated email to: {to_email}...")
    
    message = MIMEMultipart()
    message["From"] = GMAIL_USER
    message["To"] = to_email
    message["Subject"] = f"Application for {job_title} — Dennis B."
    message.attach(MIMEText(cover_letter, "plain"))
    
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, message.as_string())
        print(f"Successfully sent application email to {to_email}!")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

# Main Execution Loop
async def run_pipeline(headless):
    print("Starting Freelance/Remote Job Finder Pipeline...")
    
    # 1. Fetch Airtable existing entries & check timeouts
    existing_titles = process_existing_records_and_check_timeouts()
    print(f"Retrieved {len(existing_titles)} existing job titles from Airtable.")
    
    # 2. Scrape jobs from platforms
    raw_jobs = []
    
    print("Fetching from Himalayas API...")
    raw_jobs.extend(fetch_himalayas_jobs())
    
    print("Fetching from Remotive API...")
    raw_jobs.extend(fetch_remotive_jobs())
    
    print("Fetching from We Work Remotely RSS Feeds...")
    raw_jobs.extend(fetch_wwr_jobs())
    
    # Run Playwright scrapers
    async with async_playwright() as p:
        # Launch persistent context
        profile_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".chrome_profile")
        print(f"Launching Playwright (headless={headless}, profile={profile_path})...")
        context = await p.chromium.launch_persistent_context(
            profile_path,
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = await context.new_page()
        
        # Scrape Working Nomads
        wn_jobs = await fetch_working_nomads_jobs(page)
        raw_jobs.extend(wn_jobs)
        
        # Scrape Mercor (authenticated)
        mercor_jobs = await fetch_mercor_jobs(page)
        raw_jobs.extend(mercor_jobs)
        
        # Scrape Indeed
        indeed_jobs = await fetch_indeed_jobs(page)
        raw_jobs.extend(indeed_jobs)
        
        await context.close()
        
    print(f"\nFetched {len(raw_jobs)} total raw jobs.")
    
    # 3. Filter & Deduplicate
    matching_jobs = filter_and_deduplicate_jobs(raw_jobs, existing_titles)
    print(f"Found {len(matching_jobs)} new jobs matching target keywords.")
    
    # 4. Process each matching job
    for job in matching_jobs:
        title = job['title']
        company = job['company']
        source = job['source']
        url = job['url']
        desc = job['description']
        
        print(f"\nProcessing Job: '{title}' at {company} ({source})")
        
        # Classify and draft
        category, cover_letter, following_plan = generate_application_materials(job)
        
        # Check for email application method
        email_to_apply = extract_application_email(desc)
        
        status = "Discovery"
        current_status = "Discovered. Apply via job URL."
        applied_date = None
        
        if email_to_apply:
            email_sent = send_email_application(email_to_apply, title, cover_letter)
            if email_sent:
                status = "Applied"
                current_status = f"Applied automatically via email outreach to {email_to_apply}."
                applied_date = datetime.date.today().strftime("%Y-%m-%d")
            else:
                status = "Drafting"
                current_status = f"Discovered. Requires email application to {email_to_apply}."
                
        # Prep Airtable payload
        clean_desc = re.sub('<[^<]+?>', '', desc)
        if len(clean_desc) > 5000:
            clean_desc = clean_desc[:5000] + "\n...[truncated]..."
            
        job_id = f"JOB-EXT-{source[:3].upper()}-{hash(title) % 1000:03d}"
        
        # Validate Source dropdown configuration option
        # Airtable dropdown choices: 'Upwork', 'Himalayas', 'Remotive', 'We Work Remotely', 'Other'
        source_val = source
        if source_val not in ['Upwork', 'Himalayas', 'Remotive', 'We Work Remotely']:
            source_val = 'Other'
            
        job_fields = {
            "Title": title,
            "Status": status,
            "Job Description": f"Source: {source}\nURL: {url}\nCompany: {company}\nLocation: {job['location']}\n\n{clean_desc}",
            "Client Info": f"{company} ({source}), Location: {job['location']}",
            "Current Status": current_status,
            "Following Plan": following_plan,
            "Cover Letter": cover_letter,
            "ID": job_id,
            "Source": source_val
        }
        
        if applied_date:
            job_fields["Applied Date"] = applied_date
            
        job_data = {
            "fields": job_fields,
            "typecast": True
        }
        
        # Push to Airtable
        print(f"Logging job '{title}' to Airtable...")
        response = requests.post(AIRTABLE_URL, headers=AIRTABLE_HEADERS, json=job_data)
        if response.status_code == 200:
            print("Successfully logged to Airtable.")
        else:
            print(f"Error logging to Airtable: {response.status_code}")
            print(response.text)
            
    print("\nPipeline complete.")

if __name__ == "__main__":
    # Check if --headful flag is passed
    headless_mode = True
    if "--headful" in sys.argv:
        headless_mode = False
    
    asyncio.run(run_pipeline(headless_mode))

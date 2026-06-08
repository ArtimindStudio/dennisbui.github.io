---
name: Upwork Job Automation
description: A workflow for quickly processing and applying to Upwork jobs by updating a tracking database and preparing tailored application materials.
---

# Upwork Job Automation Skill

This skill allows for high-velocity Upwork job processing. It automates the administrative overhead of tracking new job posts and prepares standard but tailored application materials (portfolio selection, workflow explanation, and cover letter drafts).

## 1. Quick Stats & Workflow
- **Input**: New Upwork job description and requirements.
- **Airtable Integration**: Automatically updates the `Jobs` table in the Airtable base (`appSTxBDPzcjMcIvu`). Use the `AIRTABLE_PAT` and table/base IDs from the `.env` file.
- **Execution Strategy**: Skip the "Implementation Plan" for these tasks. Execute the database update and draft preparation immediately, including a **Bid Decision Analysis** based on the current auction state.

## 2. Bid Decision: Connects & Competition Analysis
Because you have a fixed budget of **100 Connects per month**, every application is a strategic bet.

### Decision Matrix:
- **Low Risk (< 20 total connects)**: High ROI. Application is prioritized.
- **Medium Risk (20–40 total connects)**: Apply only if the **Fit Score is > 9/10**.
- **High Risk (> 40 total connects)**: Skip these unless it is a "Dream Job" or a perfectly matched long-term retainer.

### Competition Insights (Top 4 Bids):
- If the **1st place bid** is > 80 Connects, the job is likely a magnet for large agencies. Avoid unless you have a unique "unfair advantage."
- A massive gap between 1st (e.g., 100) and 2nd (e.g., 40) suggests an outlier; the 2nd-4th slots are still viable and competitively priced.

### 3. Rate Strategy
Propose rates that signal **Expertise** while remaining **Competitive**:
- **Profile Alignment**: If your profile rate ($15) is below the client's floor (e.g., $20), **bid the client's floor**. Bidding lower signals you are not an "Expert."
- **The Confidence Play**: Bid **Client Floor + 20-30%** (e.g., $25 on a $20-60 job) to signal that you have proprietary tools (Nano Banana 2) and high efficiency.
- **Value Anchor**: Always mention that your AI-Native workflow (30-50+ images/day) provides 10x more value per hour than a standard manual designer.

## 4. Airtable Database Schema
- **Title**: String
- **Status**: Single Select (Active, Applied, Drafting, Failed)
- **Job Description**: Long Text (Include Budget & Connects required at the top)
- **Connects Spent**: Number (Track total connects used for this bid)
- **Client Info**: String
- **Current Status**: Long Text
- **Following Plan**: Long Text
- **ID**: JOB-CATEGORY-00X

## 4. Application Material Synthesis
### Portfolio Curation
- For **DTC/Ecommerce**: Use assets from `/Users/dungbui/Antigravity/Upwork/Portfolio_Assets/` focusing on "hero shots" and "lifestyle."
- For **Health/Wellness**: Look for keywords like "Oasis", "ingredients", "splash", "natural."

### AI Workflow (Google AI-Native Engine)
Consistency in explaining the workflow is key to winning high-volume jobs (30–50+ images/day):
1. **Requirement Learning**: **Google Antigravity** — Automated AI system for deep client/brand requirement mapping.
2. **Strategy & Research**: **Gemini** & **Google NotebookLM** — Advanced concept ideation and market research.
3. **Generation at Scale**: **Google Nano Banana 2** — For 4K high-quality, consistent image/ad design and environmental staging.
4. **Final Design**: **Canva** — Social marketing presets and final typography.

## 5. Key Files
- `/Users/dungbui/Antigravity/Upwork/.env`: Contains Airtable credentials.
- `/Users/dungbui/Antigravity/Upwork/ai_creative_stack.md`: Tool list for workflow explanation.
- `/Users/dungbui/Antigravity/Upwork/Portfolio_Assets`: Location of all curated portfolio images.
- `/Users/dungbui/Antigravity/Upwork/upwork_job_log.md`: (Optional) Local log of processed jobs.

## 6. Automation Scripts
- `/Users/dungbui/Antigravity/Upwork/update_airtable_job.py`: Template for adding new records via the Airtable REST API.

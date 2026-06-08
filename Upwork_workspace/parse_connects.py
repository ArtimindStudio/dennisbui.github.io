import os
import re

from collections import defaultdict

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "connects_raw.txt"), "r", encoding="utf-8") as f:
    lines = f.readlines()

jobs = defaultdict(int)
total_spent = 0
total_refunded = 0

ignore_phrases = [
    "Monthly Connects renewal",
    "Membership upgraded to Plus",
    "Earned Connects by completing task",
    "Rising Talent Achievement"
]

for i in range(0, len(lines), 3):
    if i + 2 >= len(lines):
        break
    
    date_line = lines[i].strip()
    desc_line = lines[i+1].strip()
    amount_line = lines[i+2].strip()
    
    # Check if we should ignore this block based on description
    skip = False
    for phrase in ignore_phrases:
        if phrase in desc_line:
            skip = True
            break
            
    if skip:
        continue
        
    # Extract Amount
    match = re.search(r'([+-]\d+)', amount_line)
    if not match:
        continue
        
    amount = int(match.group(1))
    
    # Try to extract Job Name. The description line often has: Action, then Job Name.
    # We can split by known actions
    action_prefixes = [
        "You've been outbid to boost your proposal",
        "Connects bid for boosted proposal.",
        "Applied to job",
        "Refunded Connects for Connects Award",
        "We accepted your bid to boost a proposal. This is the final bid charge.",
        "We accepted your bid to boost a proposal. This is a refund for your total bid.",
        "Job cancelled"
    ]
    
    job_name = desc_line
    for prefix in action_prefixes:
        if desc_line.startswith(prefix):
            job_name = desc_line[len(prefix):].strip()
            break
            
    jobs[job_name] += amount
    
    if amount < 0:
        total_spent += abs(amount)
    else:
        total_refunded += amount


print(f"Total connects spent: {total_spent}")
print(f"Total connects refunded: {total_refunded}")
net_spent = total_spent - total_refunded
print(f"Net Connects Spent on Jobs: {net_spent}")
print(f"\nNet Connects Cost ($0.15 each): ${net_spent * 0.15:.2f}\n")

print("Connects per Job (Net):")
for job, amt in sorted(jobs.items(), key=lambda x: x[1]):
    print(f"- {job}: {amt}")

@echo off
echo Starting Job Finder in HEADFUL mode for one-time logins...
echo -----------------------------------------------------------
echo Please log in to Mercor (https://work.mercor.com/explore) 
echo and Indeed (https://www.indeed.com) in the browser window.
echo 
echo This will save your cookies and sessions into your persistent profile 
echo (d:\Projects\Upwork\.chrome_profile) for future background runs.
echo -----------------------------------------------------------
python "%~dp0find_and_track_jobs.py" --headful
pause

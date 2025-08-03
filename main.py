import subprocess
import os
from datetime import datetime

# Get token from Railway environment
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not set. Add it to Railway project variables.")

# Step 1: Run the tagging script
subprocess.run(["python3", "review-binary-tagger.py"], check=True)

# Step 2: Rename the output with date & time
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
new_filename = f"reviews_tagged_{timestamp}.csv"
if os.path.exists("reviews_tagged.csv"):
    os.rename("reviews_tagged.csv", new_filename)

# Step 3: Commit & push to GitHub
os.system("git config --global user.email 'railway-bot@example.com'")
os.system("git config --global user.name 'Railway Bot'")
os.system(f"git remote set-url origin https://{GITHUB_TOKEN}@github.com/unknown1system32/taphereAI.git")
os.system("git add *.csv")
os.system(f"git commit -m 'Add processed reviews file: {new_filename}' || echo 'No changes to commit'")
os.system("git push origin main")

# --------------------------
# 1. Generate SSH Key for GitHub Authentication
# --------------------------
ssh-keygen -t rsa -b 4096 -C "maiyaadhikari2017@gmail.com"
# (Press Enter to accept default file location and optionally add a passphrase)
# Your public key is saved at ~/.ssh/id_rsa.pub

# Display the public key to add to GitHub
cat ~/.ssh/id_rsa.pub
# Copy this entire output to GitHub Settings > SSH and GPG Keys > New SSH Key

# --------------------------
# 2. Configure Git to Use SSH for Your Repo
# --------------------------
# Change the remote URL to use SSH instead of HTTPS
git remote set-url origin git@github.com:RohanAdhikari/Product-Purchase.git

# --------------------------
# 3. Stage and Commit Your Changes
# --------------------------
git add .
git commit -m "Your commit message here"

# --------------------------
# 4. Push Your Changes to GitHub using SSH
# --------------------------
git push -u origin main

# If remote repo has new commits, you might need to pull first:
git pull origin main --rebase
git push origin main

# --------------------------
# 5. Set up GitHub Actions Workflow File
# --------------------------
# Place your workflow YAML file (e.g. ci-basic.yaml) under:
# /PythonProject/.github/workflows/ci-basic.yaml

# Example: Stage and commit the workflow file
git add .github/workflows/ci-basic.yaml
git commit -m "Add GitHub Actions workflow for Streamlit CI"
git push origin main

# --------------------------
# 6. Trigger GitHub Actions CI Pipeline
# --------------------------
# The CI workflow triggers automatically on:
# - git push to 'main'
# - Pull requests to 'main'

# You can also manually trigger workflow runs on GitHub UI (Actions tab)

# --------------------------
# 7. Check CI Pipeline Status on GitHub
# --------------------------
# Go to your GitHub repo > Actions tab
# Select the latest workflow run to view logs and results

# --------------------------
# 8. (Optional) Troubleshooting
# --------------------------
# To debug SSH connection issues:
ssh -T git@github.com
# Should respond with a success message for GitHub

# To check current remote URLs:
git remote -v

# To view commit history:
git log --oneline --graph --decorate

________________________________________________________________________________________________________________

#To save the applied changes in files , we can directly save in github by running:
# Stage the changed file
git add PRODUCT_APP/main.py

# Commit with a message
git commit -m "Update main.py logic or fix bug"

# Push to GitHub (this triggers CI pipeline if configured)
git push origin main

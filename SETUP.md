# 🚀 Setup Guide: Automated Data Collection

This guide provides step-by-step instructions for completing the automated collection of all 325+ CSV files containing company-tagged LeetCode interview questions.

## 📋 Prerequisites

- **LeetCode Premium Account**: Required to access company-tagged questions
- **GitHub Account**: You already have this!
- **Web Browser**: Chrome, Firefox, Safari, or Edge

## 🔑 Step 1: Extract LeetCode Credentials

### Method 1: Using Browser Developer Tools (Recommended)

1. **Open LeetCode in your browser** and make sure you're logged in
   - Go to https://leetcode.com

2. **Open Developer Tools**:
   - **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac)
   - **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac)
   - **Safari**: Press `Cmd+Option+I`

3. **Navigate to the Application/Storage tab**:
   - Chrome/Edge: Click "Application" tab → "Cookies" → "https://leetcode.com"
   - Firefox: Click "Storage" tab → "Cookies" → "https://leetcode.com"
   - Safari: Click "Storage" tab → "Cookies" → "leetcode.com"

4. **Find and copy two cookies**:
   - **LEETCODE_SESSION**: Look for a cookie named `LEETCODE_SESSION` or `leetcode_session`
     - Copy the entire **Value** field (should be a long alphanumeric string)
   - **csrftoken**: Look for a cookie named `csrftoken`
     - Copy the entire **Value** field

5. **Save these values** somewhere safe (you'll need them in the next step)

### Method 2: Using Browser Console

1. Open LeetCode.com (make sure you're logged in)
2. Open Developer Console:
   - Press `F12` or `Ctrl+Shift+J` (Windows/Linux)
   - Press `Cmd+Option+J` (Mac)
3. Type the following and press Enter:
   ```javascript
   document.cookie.split('; ').find(row => row.startsWith('LEETCODE_SESSION')).split('=')[1]
   ```
4. Copy the output (your session cookie)
5. Repeat for CSRF token:
   ```javascript
   document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1]
   ```

## 🔐 Step 2: Add Credentials to GitHub Secrets

1. **Navigate to this repository's Settings**:
   - Go to: https://github.com/abhinavrajgupta/leetcode-company-interview-archive/settings/secrets/actions

2. **Add LEETCODE_SESSION secret**:
   - Click "New repository secret"
   - Name: `LEETCODE_SESSION`
   - Secret: Paste the `LEETCODE_SESSION` cookie value you copied
   - Click "Add secret"

3. **Add LEETCODE_CSRF secret**:
   - Click "New repository secret"
   - Name: `LEETCODE_CSRF`
   - Secret: Paste the `csrftoken` value you copied
   - Click "Add secret"

## ▶️ Step 3: Run the Automated Data Collection

1. **Navigate to GitHub Actions**:
   - Go to: https://github.com/abhinavrajgupta/leetcode-company-interview-archive/actions/workflows/collect_data.yml

2. **Trigger the workflow**:
   - Click the "Run workflow" button (on the right side)
   - Select branch: `main`
   - Click "Run workflow" (green button)

3. **Monitor progress**:
   - The workflow will appear in the list below
   - Click on it to view real-time logs
   - Expected duration: 10-15 minutes
   - The workflow will:
     - Fetch data for all 65+ companies
     - Create 325+ CSV files organized by company/timeframe
     - Commit them to the repository

4. **Verify completion**:
   - Once complete, you'll see a green checkmark ✅
   - Browse the repository to see all company folders with CSV files

## 📂 Expected Output Structure

After successful completion, your repository will contain:

```
/
├── Amazon/
│   ├── 30_days.csv
│   ├── 3_months.csv
│   ├── 6_months.csv
│   ├── 1_year.csv
│   └── all_time.csv
├── Google/
│   ├── 30_days.csv
│   ├── 3_months.csv
│   ├── 6_months.csv
│   ├── 1_year.csv
│   └── all_time.csv
├── Meta/
│   ├── ...
... (65+ companies)
```

## 🔄 Alternative: Manual Local Collection

If you prefer to run the script locally:

```bash
# Clone the repository
git clone https://github.com/abhinavrajgupta/leetcode-company-interview-archive.git
cd leetcode-company-interview-archive

# Install dependencies
pip install requests

# Set environment variables (replace with your actual values)
export LEETCODE_SESSION="your_leetcode_session_value"
export LEETCODE_CSRF="your_csrf_token_value"

# Run the collector
python scripts/collect.py

# The script will create all company folders and CSV files
# Review the output, then commit and push to GitHub
git add .
git commit -m "Add collected company interview data"
git push origin main
```

## ⚠️ Troubleshooting

### "LEETCODE_SESSION env var not set" Error
- Make sure you've added the secrets correctly in GitHub Settings
- Secret names must match exactly: `LEETCODE_SESSION` and `LEETCODE_CSRF`
- Re-trigger the workflow after adding secrets

### "Unauthorized" or "Access Denied" Errors
- Your LeetCode session may have expired
- Log out and log back into LeetCode, then extract fresh cookies
- Update the GitHub secrets with the new values

### Empty or Missing CSVs
- Ensure you have an active LeetCode Premium subscription
- Some companies may have no questions for certain timeframes (this is expected)

### Workflow Times Out
- The workflow has a 15-minute timeout
- If collecting all data takes longer, you can:
  1. Modify the workflow to collect in batches
  2. Run the Python script locally instead

## 🎉 Next Steps

Once data collection is complete:

1. Browse the CSVs to find questions for your target companies
2. Filter by timeframe (e.g., focus on last 30 days for current trends)
3. Sort by frequency to prioritize high-priority questions
4. Use the links in CSVs to practice on LeetCode

## 📊 Data Statistics

After collection completes, you'll have:
- **65+ companies**
- **5 timeframes per company**
- **325+ total CSV files**
- **Thousands of unique LeetCode problems**

## 🔒 Security Notes

- **Never commit secrets to the repository**
- GitHub Secrets are encrypted and only accessible to workflows
- Your credentials are never exposed in logs or outputs
- Rotate your LeetCode session periodically for security

## 📞 Need Help?

If you encounter issues:
1. Check the workflow logs for specific error messages
2. Verify your LeetCode Premium status
3. Ensure cookies were copied correctly (including full values)
4. Try re-running the workflow after fixing issues

---

**Ready to start?** Begin with Step 1: Extract your LeetCode credentials!

# 📊 LeetCode Company Interview Questions Archive

A comprehensive archive of LeetCode Premium company-tagged interview questions organized by company and timeframe.

## 🎯 Purpose

This repository permanently archives company-specific LeetCode interview questions to help job seekers prepare for technical interviews at top tech companies. Questions are organized by:
- **Company**: 65+ top tech companies hiring new graduates and experienced engineers
- **Timeframe**: 5 time-based snapshots (30 days, 3 months, 6 months, 1 year, all time)

## 📁 Repository Structure

```
/
├── Company_Name/
│   ├── 30_days.csv
│   ├── 3_months.csv
│   ├── 6_months.csv
│   ├── 1_year.csv
│   └── all_time.csv
├── scripts/
│   └── collect.py          # Data collection automation
├── .github/workflows/
│   └── collect_data.yml    # GitHub Actions workflow
└── README.md
```

## 🏢 Companies Included

### FAANG & Big Tech
Amazon, Google (Alphabet), Meta (Facebook), Apple, Microsoft, Netflix

### Top Tech Companies
NVIDIA, AMD, Intel, Oracle, Salesforce, Adobe, Cisco, Qualcomm, IBM, Samsung, Yahoo

### Unicorns & High-Growth Startups
Uber, Airbnb, Stripe, DoorDash, Coinbase, Databricks, Snowflake, Palantir, OpenAI, Anthropic

### E-Commerce & Marketplaces
eBay, PayPal, Walmart Global Tech, Shopify, Instacart

### Enterprise Software
ServiceNow, MongoDB, Atlassian, Twilio, Zoom, Dropbox, Box, Slack, SAP

### Social & Content
LinkedIn, Pinterest, Snap, Twitter, TikTok, ByteDance, Spotify, Roblox

### Fintech & Trading
Goldman Sachs, JP Morgan, Citadel, Two Sigma, Jane Street, DE Shaw, Visa, Capital One, Robinhood

### EdTech & Gaming
Duolingo, Riot Games, Electronic Arts

### Others
Tesla, Bloomberg, Expedia, Yelp, Red Hat, Square, Lyft, DraftKings, Wayfair, Coupang

## 📊 CSV Format

Each CSV file contains the following columns:
- **Problem Number**: LeetCode problem ID
- **Problem Title**: Full problem name
- **Difficulty**: Easy, Medium, or Hard
- **Frequency**: Company-specific frequency score
- **Link**: Direct URL to the LeetCode problem
- **Company**: Company name
- **Timeframe**: Time period (30_days, 3_months, 6_months, 1_year, all_time)

All CSVs are sorted by **Frequency (descending)** to highlight the most commonly asked questions.

## 🔄 Data Collection

### Automated Collection

To collect data for all companies:

1. **Set up LeetCode credentials**:
   ```bash
   # Login to LeetCode Premium in your browser
   # Extract cookies: LEETCODE_SESSION and csrftoken
   ```

2. **Add GitHub Secrets**:
   - Go to Repository Settings → Secrets and variables → Actions
   - Add `LEETCODE_SESSION`: Your LeetCode session cookie value
   - Add `LEETCODE_CSRF`: Your LeetCode CSRF token value

3. **Run the GitHub Actions workflow**:
   - Navigate to Actions → Collect LeetCode Company Interview Questions
   - Click "Run workflow"
   - Wait for completion (~10-15 minutes)

### Manual Collection

```bash
# Clone the repository
git clone https://github.com/abhinavrajgupta/leetcode-company-interview-archive.git
cd leetcode-company-interview-archive

# Install dependencies
pip install requests

# Export credentials
export LEETCODE_SESSION="your_session_cookie"
export LEETCODE_CSRF="your_csrf_token"

# Run collector
python scripts/collect.py
```

## 📈 Data Statistics

- **Total Companies**: 65+
- **Timeframes per Company**: 5
- **Total CSV Files**: 325+
- **Data Collection**: Automated via GraphQL API
- **Update Frequency**: On-demand (run workflow manually)

## ⚠️ Important Notes

- **LeetCode Premium Required**: This data is sourced from LeetCode Premium's company tags feature
- **Personal Use Only**: Data is archived for educational and interview preparation purposes
- **No Redistribution**: Please do not redistribute or commercialize this data
- **Accuracy**: Questions and frequencies reflect LeetCode's data at the time of collection
- **Links**: All problem links are verified and point to leetcode.com

## 🔗 Related Resources

- [LeetCode](https://leetcode.com/)
- [LeetCode Discuss](https://leetcode.com/discuss/)
- [Blind](https://www.teamblind.com/) - Tech interview discussions
- [Levels.fyi](https://www.levels.fyi/) - Compensation data

## 📝 License

This repository is for personal educational use. All LeetCode problems and data remain property of LeetCode LLC.

## 🙏 Acknowledgments

- **LeetCode** for providing comprehensive problem sets and company tags
- **Contributors** who help maintain and update this archive

---

**Last Updated**: 2025-01-23  
**Repository Maintainer**: [@abhinavrajgupta](https://github.com/abhinavrajgupta)

#!/usr/bin/env python3
"""
LeetCode Company Interview Questions Collector
Fetches company-tagged questions from LeetCode Premium GraphQL API
and saves them as CSVs organized by company and timeframe.
"""

import os
import csv
import json
import time
import requests
from pathlib import Path
from collections import defaultdict
from datetime import date

# ── Configuration ────────────────────────────────────────────────────────────

COMPANIES = {
    "Amazon":           "amazon",
    "Google":           "google",
    "Meta":             "facebook",
    "Apple":            "apple",
    "Microsoft":        "microsoft",
    "Netflix":          "netflix",
    "NVIDIA":           "nvidia",
    "AMD":              "amd",
    "Intel":            "intel",
    "Oracle":           "oracle",
    "Salesforce":       "salesforce",
    "Uber":             "uber",
    "Airbnb":           "airbnb",
    "Stripe":           "stripe",
    "Databricks":       "databricks",
    "Snowflake":        "snowflake",
    "Palantir":         "palantir-technologies",
    "OpenAI":           "openai",
    "Anthropic":        "anthropic",
    "Tesla":            "tesla",
    "DoorDash":         "doordash",
    "Pinterest":        "pinterest",
    "Robinhood":        "robinhood",
    "LinkedIn":         "linkedin",
    "Cisco":            "cisco",
    "Qualcomm":         "qualcomm",
    "Adobe":            "adobe",
    "Expedia":          "expedia",
    "Atlassian":        "atlassian",
    "MongoDB":          "mongodb",
    "Dropbox":          "dropbox",
    "Bloomberg":        "bloomberg",
    "Twilio":           "twilio",
    "Yelp":             "yelp",
    "Coinbase":         "coinbase",
    "Visa":             "visa",
    "Capital One":      "capital-one",
    "Walmart Global Tech": "walmart-labs",
    "PayPal":           "paypal",
    "eBay":             "ebay",
    "ServiceNow":       "servicenow",
    "SAP":              "sap",
    "Red Hat":          "red-hat",
    "IBM":              "ibm",
    "Samsung":          "samsung",
    "TikTok":           "tiktok",
    "ByteDance":        "bytedance",
    "Yahoo":            "yahoo",
    "Zoom":             "zoom",
    "Lyft":             "lyft",
    "Box":              "box",
    "Slack":            "slack",
    "Duolingo":         "duolingo",
    # Bonus new-grad focused
    "Two Sigma":        "two-sigma",
    "Jane Street":      "jane-street",
    "Goldman Sachs":    "goldman-sachs",
    "JP Morgan":        "jpmorgan",
    "Citadel":          "citadel",
    "DE Shaw":          "de-shaw",
    "Roblox":           "roblox",
    "Snap":             "snapchat",
    "Twitter":          "twitter",
    "Spotify":          "spotify",
    "Square":           "square",
    "Coupang":          "coupang",
    "DraftKings":       "draftkings",
    "Wayfair":          "wayfair",
    "Instacart":        "instacart",
    "Riot Games":       "riot-games",
    "Electronic Arts":  "electronic-arts",
    "Nvidia (again)":   "nvidia",
}

TIMEFRAMES = {
    "30_days":    "thirty-days",
    "3_months":   "three-months",
    "6_months":   "six-months",
    "1_year":     "more-than-six-months",
    "all_time":   "all",
}

GRAPHQL_URL = "https://leetcode.com/graphql"
QUERY = """
query favoriteQuestionList($favoriteSlug: String!) {
  favoriteQuestionList(favoriteSlug: $favoriteSlug) {
    questions {
      questionFrontendId
      title
      titleSlug
      difficulty
      frequency
    }
    totalLength
  }
}
"""

# ── Session Setup ─────────────────────────────────────────────────────────────

def get_session():
    session = requests.Session()
    lc_session = os.environ.get("LEETCODE_SESSION", "")
    csrf_token  = os.environ.get("LEETCODE_CSRF", "")

    if not lc_session:
        raise ValueError("LEETCODE_SESSION env var not set. "
                         "Copy it from your browser cookies after logging in.")

    session.cookies.set("LEETCODE_SESSION", lc_session, domain="leetcode.com")
    session.cookies.set("csrftoken", csrf_token, domain="leetcode.com")
    session.headers.update({
        "Content-Type":   "application/json",
        "Referer":        "https://leetcode.com/",
        "x-csrftoken":    csrf_token,
        "User-Agent":     "Mozilla/5.0",
    })
    return session


# ── Data Fetching ─────────────────────────────────────────────────────────────

def fetch_questions(session, slug: str) -> list[dict]:
    payload = {
        "query":     QUERY,
        "variables": {"favoriteSlug": slug},
    }
    try:
        resp = session.post(GRAPHQL_URL, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["data"]["favoriteQuestionList"]["questions"]
    except Exception as exc:
        print(f"  ERROR fetching {slug}: {exc}")
        return []


# ── CSV Writing ───────────────────────────────────────────────────────────────

CSV_HEADERS = ["Problem Number", "Title", "Difficulty", "Frequency", "Link", "Company", "Timeframe"]

def questions_to_csv(questions, company_name, timeframe_label) -> str:
    rows = []
    for q in questions:
        num   = q.get("questionFrontendId", "")
        title = q.get("title", "")
        diff  = q.get("difficulty", "").capitalize()
        freq  = round(q.get("frequency") or 0, 2)
        slug  = q.get("titleSlug", "")
        link  = f"https://leetcode.com/problems/{slug}/"
        rows.append([num, title, diff, freq, link, company_name, timeframe_label])

    rows.sort(key=lambda r: float(r[3]), reverse=True)

    lines = [",".join(map(str, CSV_HEADERS))]
    for r in rows:
        # Wrap fields that may contain commas
        safe = []
        for v in r:
            v = str(v)
            if "," in v or '"' in v:
                v = '"' + v.replace('"', '""') + '"'
            safe.append(v)
        lines.append(",".join(safe))
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    session = get_session()
    base    = Path(".")
    all_data = defaultdict(list)   # slug -> list of (company, timeframe, questions)

    # Track per-company data for bonus files
    company_data = {}

    total_files = 0

    for company_name, company_slug in COMPANIES.items():
        print(f"\n{'='*60}")
        print(f"Company: {company_name}  (slug: {company_slug})")
        folder = base / company_name.replace(" ", "_")
        folder.mkdir(parents=True, exist_ok=True)

        company_questions = {}

        for timeframe_key, timeframe_suffix in TIMEFRAMES.items():
            favorite_slug = f"{company_slug}-{timeframe_suffix}"
            print(f"  Fetching {timeframe_key} ({favorite_slug}) ... ", end="", flush=True)

            questions = fetch_questions(session, favorite_slug)
            print(f"{len(questions)} problems")

            if not questions:
                # Write empty file with header only
                content = ",".join(CSV_HEADERS)
            else:
                content = questions_to_csv(questions, company_name, timeframe_key)
                # Store for bonus generation
                for q in questions:
                    key = q.get("questionFrontendId", "")
                    if key not in all_data:
                        all_data[key] = {
                            "num":   key,
                            "title": q.get("title", ""),
                            "diff":  q.get("difficulty", "").capitalize(),
                            "slug":  q.get("titleSlug", ""),
                        }
                    all_data[key].setdefault("companies", set()).add(company_name)
                    all_data[key].setdefault("max_freq", 0)
                    freq = q.get("frequency") or 0
                    if freq > all_data[key]["max_freq"]:
                        all_data[key]["max_freq"] = freq

            out_file = folder / f"{timeframe_key}.csv"
            out_file.write_text(content, encoding="utf-8")
            total_files += 1

            company_questions[timeframe_key] = questions
            time.sleep(0.4)   # polite rate-limiting

        company_data[company_name] = company_questions

    # ── Bonus: Top100_Global.csv ──────────────────────────────────────────────
    print("\n[Bonus] Generating Top100_Global.csv ...")
    top100 = sorted(all_data.values(), key=lambda x: x["max_freq"], reverse=True)[:100]
    write_bonus_csv(top100, base / "Top100_Global.csv")
    total_files += 1

    # ── Bonus: Most_Common_FAANG.csv ──────────────────────────────────────────
    faang = {"Amazon", "Google", "Meta", "Apple", "Microsoft"}
    write_filtered_bonus(all_data, faang, base / "Most_Common_FAANG.csv", min_companies=2)
    total_files += 1

    # ── Bonus: Most_Common_Unicorns.csv ───────────────────────────────────────
    unicorns = {"Stripe", "Databricks", "Snowflake", "Airbnb", "Uber", "DoorDash", "Palantir", "Duolingo"}
    write_filtered_bonus(all_data, unicorns, base / "Most_Common_Unicorns.csv", min_companies=2)
    total_files += 1

    # ── Bonus: Most_Common_AI.csv ─────────────────────────────────────────────
    ai_cos = {"OpenAI", "Anthropic", "NVIDIA", "AMD", "Google", "Meta"}
    write_filtered_bonus(all_data, ai_cos, base / "Most_Common_AI.csv", min_companies=2)
    total_files += 1

    # ── Bonus: Most_Common_NewGrad.csv ────────────────────────────────────────
    newgrad_cos = {"Amazon", "Google", "Meta", "Microsoft", "Apple", "Uber", "Airbnb",
                   "LinkedIn", "Salesforce", "Adobe", "Oracle", "Atlassian",
                   "DoorDash", "Lyft", "Snap", "Roblox", "Spotify"}
    write_filtered_bonus(all_data, newgrad_cos, base / "Most_Common_NewGrad.csv", min_companies=2)
    total_files += 1

    print(f"\n✅ Done! {total_files} files created across {len(COMPANIES)} companies.")
    print(f"   Total unique problems tracked: {len(all_data)}")


def write_bonus_csv(problems: list, path: Path):
    headers = ["Problem Number", "Title", "Difficulty", "Frequency", "Link", "Appears In (companies)"]
    lines = [",".join(headers)]
    for p in problems:
        link = f"https://leetcode.com/problems/{p['slug']}/"
        companies_str = "|".join(sorted(p.get("companies", set())))
        row = [p["num"], p["title"], p["diff"], round(p["max_freq"], 2), link, companies_str]
        safe = []
        for v in row:
            v = str(v)
            if "," in v or '"' in v:
                v = '"' + v.replace('"', '""') + '"'
            safe.append(v)
        lines.append(",".join(safe))
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote {path.name} ({len(problems)} problems)")


def write_filtered_bonus(all_data: dict, target_companies: set, path: Path, min_companies: int = 2):
    filtered = []
    for p in all_data.values():
        overlap = p.get("companies", set()) & target_companies
        if len(overlap) >= min_companies:
            entry = dict(p)
            entry["companies"] = overlap
            filtered.append(entry)
    filtered.sort(key=lambda x: x["max_freq"], reverse=True)
    write_bonus_csv(filtered, path)


if __name__ == "__main__":
    main()

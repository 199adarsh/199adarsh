#!/usr/bin/env python3
"""
Scrape real daily contribution counts from GitHub's public contributions endpoint
and write data/contributions.json with raw days plus stats.
"""
import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_PROFILE_USER", "199adarsh")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")


def fetch_days():
    resp = requests.get(URL, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        print("no calendar cells found -- github markup may have changed", file=sys.stderr)
        sys.exit(1)

    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        td_id = td.get("id")
        tooltip_el = soup.find("tool-tip", attrs={"for": td_id}) if td_id else None
        text = tooltip_el.get_text(strip=True) if tooltip_el else ""
        if re.search(r"no contributions", text, re.I):
            count = 0
        else:
            m = re.match(r"(\d+)", text)
            count = int(m.group(1)) if m else 0
        days.append({"date": date, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def compute_current_streak(days):
    idx = len(days) - 1
    if days[idx]["count"] == 0:
        idx -= 1
    streak = 0
    end_idx = idx
    while idx >= 0 and days[idx]["count"] > 0:
        streak += 1
        idx -= 1
    start_idx = idx + 1
    if streak == 0:
        return 0, None, None
    return streak, days[start_idx]["date"], days[end_idx]["date"]


def compute_longest_streak(days):
    longest = run = 0
    longest_start = longest_end = None
    run_start_idx = None
    for i, d in enumerate(days):
        if d["count"] > 0:
            if run == 0:
                run_start_idx = i
            run += 1
            if run > longest:
                longest = run
                longest_start = days[run_start_idx]["date"]
                longest_end = days[i]["date"]
        else:
            run = 0
    return longest, longest_start, longest_end


def build_data(days):
    total = sum(d["count"] for d in days)
    active_days = sum(1 for d in days if d["count"] > 0)
    best = max(days, key=lambda d: d["count"])
    cur_len, cur_start, cur_end = compute_current_streak(days)
    long_len, long_start, long_end = compute_longest_streak(days)

    monthly = {}
    for d in days:
        key = d["date"][:7]
        monthly[key] = monthly.get(key, 0) + d["count"]
    monthly_list = [{"month": k, "total": v} for k, v in sorted(monthly.items())]

    return {
        "username": USERNAME,
        "fetched_at": datetime.datetime.utcnow().isoformat() + "Z",
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "total_contributions": total,
        "active_days": active_days,
        "best_day": best,
        "current_streak": {"length": cur_len, "start": cur_start, "end": cur_end},
        "longest_streak": {"length": long_len, "start": long_start, "end": long_end},
        "monthly": monthly_list,
        "days": days,
    }


def main():
    days = fetch_days()
    data = build_data(days)

    if os.path.exists(OUT_PATH):
        try:
            with open(OUT_PATH, "r", encoding="utf-8") as f:
                old_data = json.load(f)

            last_fetched = old_data.get("fetched_at", "")
            if not last_fetched:
                last_fetched = (datetime.datetime.utcnow() - datetime.timedelta(days=2)).isoformat() + "Z"

            url = f"https://api.github.com/repos/{USERNAME}/{USERNAME}/commits?since={last_fetched}"
            try:
                resp = requests.get(url, headers={"User-Agent": "profile-readme-bot/1.0"}, timeout=30)
                profile_counts = {}
                if resp.status_code == 200:
                    for c in resp.json():
                        date_str = c["commit"]["author"]["date"][:10]
                        profile_counts[date_str] = profile_counts.get(date_str, 0) + 1
            except Exception as e:
                print(f"Failed to fetch profile commits: {e}", file=sys.stderr)
                profile_counts = {}

            old_days = {d["date"]: d.get("count", 0) for d in old_data.get("days", [])}
            new_days = {d["date"]: d.get("count", 0) for d in data.get("days", [])}

            has_real_changes = False
            for date_str, new_count in new_days.items():
                old_count = old_days.get(date_str, 0)
                if new_count - old_count > profile_counts.get(date_str, 0):
                    has_real_changes = True
                    break

            if not has_real_changes:
                for date_str, old_count in old_days.items():
                    if old_count > new_days.get(date_str, 0):
                        has_real_changes = True
                        break

            if not has_real_changes:
                print("No contribution changes from other repos detected. Skipping update.")
                if os.environ.get("GITHUB_ENV"):
                    with open(os.environ["GITHUB_ENV"], "a") as env_file:
                        env_file.write("SKIP_UPDATE=true\n")
                sys.exit(0)
        except Exception as e:
            print(f"Could not check non-profile changes: {e}", file=sys.stderr)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"wrote {OUT_PATH} with {len(days)} days, {data['total_contributions']} total contributions")


if __name__ == "__main__":
    main()

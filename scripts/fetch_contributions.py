import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

USERNAME = "199adarsh"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_contributions():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    days = []
    for td in soup.find_all("td", class_="ContributionCalendar-day"):
        date = td.get("data-date")
        count = td.get("data-level") or "0"
        if date:
            days.append({"date": date, "count": int(count)})
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump({"username": USERNAME, "updated": datetime.utcnow().isoformat(), "days": days}, f, indent=2)

if __name__ == "__main__":
    fetch_contributions()

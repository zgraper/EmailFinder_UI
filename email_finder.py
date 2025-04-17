# email_finder.py

import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def find_emails(domain):
    """
    Attempts to find emails by visiting the homepage and common subpages
    like /about, /contact, /team, etc.
    """
    base_url = f"https://{domain}"
    candidate_paths = ["", "about", "contact", "team", "staff", "leadership", "info"]
    visited_pages = set()
    found_emails = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; EmailFinderBot/1.0; +https://example.com/bot)"
    }

    for path in candidate_paths:
        url = urljoin(base_url, path)
        if url in visited_pages:
            continue
        visited_pages.add(url)
        try:
            response = requests.get(url, timeout=10, headers=headers)
            if response.status_code != 200:
                continue
            content = response.text

            # Extract emails from page
            emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", content))
            found_emails.update(emails)

            # Also check for additional links in case there are nested team/contact/about pages
            soup = BeautifulSoup(content, "html.parser")
            links = soup.find_all("a", href=True)
            for link in links:
                href = link["href"]
                if any(word in href.lower() for word in ["about", "contact", "team", "staff", "leadership"]):
                    sub_url = urljoin(base_url, href)
                    if sub_url not in visited_pages:
                        visited_pages.add(sub_url)
                        try:
                            sub_resp = requests.get(sub_url, timeout=10, headers=headers)
                            sub_emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", sub_resp.text))
                            found_emails.update(sub_emails)
                        except Exception:
                            continue

        except Exception:
            continue

    return list(found_emails) if found_emails else ["No emails found."]
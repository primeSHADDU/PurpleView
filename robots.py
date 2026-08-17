import urllib.request
import urllib.error
from urllib.parse import urljoin

def get_robots_txt(domain):
    """Fetch and parse robots.txt from a given domain."""
    if not domain.startswith(('http://', 'https://')):
        domain = 'https://' + domain

    robots_url = urljoin(domain, '/robots.txt')

    try:
        req = urllib.request.Request(robots_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: robots.txt not found or inaccessible at {robots_url}")
        return
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
        return

    print(f"--- Raw robots.txt from {robots_url} ---\n")
    print(content)
    print("\n--- Parsed Summary ---\n")

    parse_robots(content)
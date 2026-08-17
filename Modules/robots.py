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

def parse_robots(content):
    current_agent = None
    rules = {}
    sitemaps = []

    for line in content.splitlines():
        line = line.split('#', 1)[0].strip()  # strip comments
        if not line:
            continue

        if ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip().lower()
        value = value.strip()

        if key == 'user-agent':
            current_agent = value
            rules.setdefault(current_agent, {'disallow': [], 'allow': []})
        elif key == 'disallow' and current_agent:
            rules[current_agent]['disallow'].append(value)
        elif key == 'allow' and current_agent:
            rules[current_agent]['allow'].append(value)
        elif key == 'sitemap':
            sitemaps.append(value)
        elif key == 'crawl-delay' and current_agent:
            rules[current_agent]['crawl-delay'] = value

    for agent, r in rules.items():
        print(f"User-agent: {agent}")
        if r['disallow']:
            print(f"  Disallow: {r['disallow']}")
        if r['allow']:
            print(f"  Allow: {r['allow']}")
        if 'crawl-delay' in r:
            print(f"  Crawl-delay: {r['crawl-delay']}")
        print()

    if sitemaps:
        print(f"Sitemaps: {sitemaps}")


if __name__ == '_main_':
    domain = input("Enter domain (e.g. example.com): ").strip()
    get_robots_txt(domain)

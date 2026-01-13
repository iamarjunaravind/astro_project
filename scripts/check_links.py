import os
import sys
import django
from collections import deque
from urllib.parse import urlparse, urljoin
import re

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astro_project.settings')
django.setup()

from django.test import Client

def check_links():
    client = Client()
    start_url = '/'
    visited = set()
    queue = deque([start_url])
    broken_links = []
    
    # Regex to find hrefs
    href_pattern = re.compile(r'href=["\'](.*?)["\']')

    print(f"Starting crawl at {start_url}...")

    while queue:
        current_url = queue.popleft()
        
        if current_url in visited:
            continue
        
        visited.add(current_url)
        
        # Skip static/media/external/anchor/javascript links
        if any(x in current_url for x in ['static/', 'media/', 'http:', 'https:', 'mailto:', 'tel:', '#', 'javascript:', 'None']):
            continue

        try:
            response = client.get(current_url, follow=True)
            status = response.status_code
            
            print(f"[{status}] {current_url}")

            if status != 200:
                broken_links.append((current_url, status))
                continue
            
            # Content type check
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
                
            # Parse links
            content = response.content.decode('utf-8', errors='ignore')
            links = href_pattern.findall(content)
            
            for link in links:
                # Normalize URL
                full_url = urljoin(current_url, link)
                parsed = urlparse(full_url)
                
                # Internal links only
                if not parsed.netloc and parsed.path not in visited:
                    # Clean path
                    path = parsed.path
                    if not path.startswith('/'):
                        path = '/' + path
                    
                    if path not in visited and path not in queue:
                        queue.append(path)

        except Exception as e:
            print(f"[ERROR] {current_url}: {e}")
            broken_links.append((current_url, str(e)))

    print("\n--- Crawl Complete ---")
    if broken_links:
        print(f"Found {len(broken_links)} broken links:")
        for url, reason in broken_links:
            print(f" - {url} : {reason}")
    else:
        print("No broken links found!")

if __name__ == '__main__':
    check_links()

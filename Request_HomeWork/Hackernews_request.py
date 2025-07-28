import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/" 

try:
    # Fetching the HTML content of the web page
    response = requests.get(url)
    response.raise_for_status() # Raises an exception for HTTP errors (e.g., 404, 500)

    # Creating a BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    print(f"Successfully created BeautifulSoup object for: {url}")

    all_links = soup.find_all('a')

    news_items_count = 0
    print("\nFirst 30 News Titles and Links:")

    for link in all_links:
        if news_items_count >= 30:
            break 

        link_text = link.get_text(strip=True) 
        link_url = link.get('href')

        # This logic is based on the original script's structure for finding links
        if link_url and link_text and link_url.startswith('item?id='):
            # Convert relative URLs to absolute URLs
            full_url = requests.compat.urljoin(url, link_url)

            print(f"  {news_items_count + 1}. Title: '{link_text}'")
            print(f"     Link: {full_url}\n")
            news_items_count += 1
        elif link_url and link_text and link_url.startswith('http') and len(link_text) > 10:
            print(f"  {news_items_count + 1}. Title: '{link_text}'")
            print(f"     Link: {link_url}\n")
            news_items_count += 1

    if news_items_count == 0:
        print("No news titles and links matching the specified criteria were found.")
        print("Please consider inspecting the site's HTML structure to make the 'find_all' method more specific.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the web page: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"HTTP Response Code: {e.response.status_code}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

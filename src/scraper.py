import requests
from bs4 import BeautifulSoup
import csv
import re

def parse_traffic(traffic_str):
    """Convert traffic string (e.g. '200+', '10000+') to number for sorting"""
    if not traffic_str or traffic_str == 'N/A':
        return 0
    number = int(re.sub(r'[^0-9]', '', traffic_str))
    return number

def is_english(text):
    """Check if the text is mostly English by ensuring it contains only ASCII characters"""
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    return True

def fetch_trends(geo="IN"):
    url = f"https://trends.google.com/trending/rss?geo={geo}&hours=24&status=active&hl=en-US"
    
    try:
        # Fetch the RSS feed
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse XML with BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')
        
        # Find all items
        items = soup.find_all('item')
        
        trends = []
        for item in items:
            title = item.find('title').text
            if not is_english(title):
                continue  # Skip non-English items
            
            traffic = item.find('ht:approx_traffic').text if item.find('ht:approx_traffic') else 'N/A'
            picture = item.find('ht:picture').text if item.find('ht:picture') else None
            
            # Get news items
            news_items = []
            for news in item.find_all('ht:news_item'):
                news_items.append({
                    'title': news.find('ht:news_item_title').text,
                    'source': news.find('ht:news_item_source').text,
                    'url': news.find('ht:news_item_url').text,
                    'news_item_picture': news.find('ht:news_item_picture').text if news.find('ht:news_item_picture') else None
                })
            
            trends.append({
                'topic': title,
                'traffic': traffic,
                'picture': picture,
                'news_items': news_items
            })
        
        # Sort trends by traffic (highest to lowest)
        trends.sort(key=lambda x: parse_traffic(x['traffic']), reverse=True)
        
        # Filter out trends with traffic <= 1000
        trends = [trend for trend in trends if parse_traffic(trend['traffic']) > 200]
        
        return trends
            
    except requests.RequestException as e:
        print(f"Error fetching trends: {e}")
        return []

def print_trends(trends):
    print("\nCurrent Google Trends (Sorted by Traffic):")
    print("=" * 80)
    
    for trend in trends:
        print(f"\n{trend['topic']} ({trend['traffic']})")
        print("-" * 40)
        
        print("Related News:")
        for idx, news in enumerate(trend['news_items'], 1):
            print(f"  {idx}. {news['title']}")
            print(f"     Source: {news['source']}")
            print(f"     URL: {news['url']}\n")
    
    print("=" * 80)

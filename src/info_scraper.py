import os
import requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
import time  # Import time for adding delays

def validate_image_relevance(img_url, img_alt, topic_keywords):
    """Helper function to validate image relevance based on URL and alt text."""
    # Convert everything to lowercase for comparison
    img_url = img_url.lower()
    img_alt = (img_alt or '').lower()
    
    # Skip common UI elements and icons
    if any(term in img_url for term in ['logo', 'icon', 'avatar', 'button', 'ui', '/static/']):
        print("Skipping UI element/icon")
        return False
        
    # Skip small image formats and data URLs
    if img_url.endswith(('.gif', '.svg')) or 'data:image' in img_url:
        print("Skipping invalid image format")
        return False
        
    # Check if any keyword appears in either URL or alt text
    for keyword in topic_keywords:
        if keyword in img_url or keyword in img_alt:
            print(f"Found matching keyword '{keyword}' in {'URL' if keyword in img_url else 'alt text'}")
            return True
            
    print("No keyword match found in URL or alt text")
    return False

def collect_image_urls(news_item_url, trend_topic):
    """Collect image URLs from the news item page that contain the trend topic."""
    print(f"\nAttempting to collect images for topic '{trend_topic}' from URL: {news_item_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        print("Making HTTP request...")
        response = requests.get(news_item_url, headers=headers, timeout=10)
        response.raise_for_status()
        print("Response received successfully")

        print("Parsing HTML content...")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content section (adjust the selector as needed)
        print("Looking for main content section...")
        main_content = soup.find('div', class_='main-content')  # Example class name
        if not main_content:
            print("Main content section not found, using whole page")
            main_content = soup  # Fallback to the whole page if not found
        else:
            print("Main content section found")

        # Find all image tags within the main content
        print("Searching for image tags...")
        images = main_content.find_all('img')
        print(f"Found {len(images)} total images")

        # Filter images based on certain criteria
        filtered_images = []
        trend_topic_lower = trend_topic.lower()
        trend_keywords = trend_topic_lower.split()
        print(f"Looking for images matching keywords: {trend_keywords}")

        # Only process first 20 images to avoid getting stuck
        print("Processing first 20 images...")
        for i, img in enumerate(images[:20]):
            print(f"\nProcessing image {i+1}/20")
            
            # Skip small images (likely icons)
            if 'width' in img.attrs and 'height' in img.attrs:
                try:
                    width = int(img['width'])
                    height = int(img['height'])
                    if width < 100 or height < 100:
                        print(f"Skipping small image ({width}x{height})")
                        continue
                except (ValueError, TypeError):
                    print("Could not determine image dimensions")

            if 'src' in img.attrs:
                img_src = img['src']
                img_alt = img.get('alt', '')
                print(f"Checking image URL: {img_src}")
                print(f"Image alt text: {img_alt}")
                
                if validate_image_relevance(img_src, img_alt, trend_keywords):
                    print("Found matching image!")
                    filtered_images.append(img_src)
                    # Return immediately after finding first suitable image
                    if len(filtered_images) == 1:
                        print("Returning first matching image")
                        return filtered_images

        print(f"No suitable images found on page. Trying Google Images...")
        google_image = fetch_google_image(trend_topic)
        return [google_image]  # Will always return at least the default image

    except requests.exceptions.Timeout:
        print(f"Request timed out after 10 seconds for URL: {news_item_url}")
        print("Trying Google Images instead...")
        google_image = fetch_google_image(trend_topic)
        return [google_image]
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request error for {news_item_url}: {e}")
        print("Trying Google Images instead...")
        google_image = fetch_google_image(trend_topic)
        return [google_image]
    except Exception as e:
        print(f"Error in collect_image_urls: {e}")
        print("Trying Google Images instead...")
        google_image = fetch_google_image(trend_topic)
        return [google_image]

def fetch_google_image(search_term):
    """Fetch image URL using DuckDuckGo image search."""
    print(f"Searching DuckDuckGo Images for: {search_term}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Create keywords from search term
    search_keywords = search_term.lower().split()
    
    # Create variations of the search term
    variations = [
        search_term,
        f"{search_term} image",
        f"{search_term} photo"
    ]

    for variation in variations:
        try:
            # Use DuckDuckGo image search
            search_url = f"https://duckduckgo.com/?q={variation}&iax=images&ia=images"
            print(f"Trying URL: {search_url}")
            
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # First try to find image tiles
            print("Looking for image tiles...")
            images = soup.find_all('img', {'class': 'tile--img__img'})
            
            if not images:
                # Fallback: look for any image with http/https source
                print("Trying fallback method...")
                images = soup.find_all('img', src=lambda x: x and ('http://' in x or 'https://' in x))
            
            for img in images:
                img_url = img.get('src', '')
                img_alt = img.get('alt', '')
                
                if img_url and img_url.startswith('http'):
                    if validate_image_relevance(img_url, img_alt, search_keywords):
                        print(f"Found relevant image URL: {img_url[:100]}...")
                        return img_url
            
            time.sleep(2)  # Delay between attempts
            
        except Exception as e:
            print(f"Error fetching image for '{variation}': {e}")
            continue

    # If all attempts fail, try Bing as last resort
    try:
        print("Trying Bing Images as last resort...")
        bing_url = f"https://www.bing.com/images/search?q={search_term}&form=HDRSC2"
        response = requests.get(bing_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        images = soup.find_all('img', src=lambda x: x and x.startswith('http'))
        for img in images[1:]:  # Skip first image as it might be a logo
            img_url = img.get('src', '')
            img_alt = img.get('alt', '')
            
            if validate_image_relevance(img_url, img_alt, search_keywords):
                print(f"Found relevant Bing image URL: {img_url[:100]}...")
                return img_url
                    
    except Exception as e:
        print(f"Bing Images attempt failed: {e}")

    # If everything fails, return default image
    default_image = "https://placehold.co/600x400/png?text=No+Image+Available"
    print(f"All image search attempts failed. Using default fallback image: {default_image}")
    return default_image

def create_story_files(trends):
    """Create separate HTML files for each trend containing all its news items."""
    if not os.path.exists('hosted_files/stories'):
        os.makedirs('hosted_files/stories')  # Create a directory for story files

    for trend in trends:
        if 'topic' not in trend:
            print(f"Warning: 'topic' key not found in trend: {trend}")
            continue

        trend_name = trend['topic'].replace(" ", "_").replace("/", "_").lower()
        file_name = f"{trend_name}.html"
        story_file_path = os.path.join('hosted_files/stories', file_name)

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{trend['topic']} - Hot Topic Insights</title>
            <meta name="description" content="Read the latest news about {trend['topic']} and stay updated.">
            <meta name="keywords" content="{trend['topic']}, trending news, hot topics">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4; }}
                h1 {{ color: #333; text-align: center; margin-top: 20px; }}
                h2 {{ color: #555; margin: 10px 0; }}
                .container {{ max-width: 800px; margin: auto; padding: 20px; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); }}
                .cover-image {{ width: 100%; height: 400px; object-fit: cover; border-radius: 8px; margin-bottom: 20px; }}
                .news-item {{ border-bottom: 1px solid #ccc; padding: 20px 0; display: flex; gap: 20px; }}
                .news-item:last-child {{ border-bottom: none; }}
                .news-image {{ width: 200px; height: 150px; object-fit: cover; border-radius: 5px; }}
                .news-content {{ flex: 1; }}
                .news-source {{ color: #666; font-size: 0.9em; margin: 5px 0; }}
                .read-more {{ color: #e74c3c; text-decoration: none; display: inline-flex; align-items: center; gap: 5px; }}
                .read-more:hover {{ text-decoration: underline; }}
                .footer {{ text-align: center; margin-top: 20px; font-size: 0.9em; color: #777; }}
                .brand {{ font-weight: bold; color: #e74c3c; }}
                .traffic {{ text-align: center; color: #666; margin: 10px 0; }}
                @media (max-width: 600px) {{
                    .news-item {{ flex-direction: column; }}
                    .news-image {{ width: 100%; height: 200px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hot Topic Insights: {trend['topic']}</h1>
                <div class="traffic">Trending with {trend.get('traffic', 'N/A')} searches</div>
        """

        # Add the trend's main image if available
        if 'picture' in trend:
            html_content += f'<img class="cover-image" src="{trend["picture"]}" alt="Cover image for {trend["topic"]}">'

        # Add each news item with its image
        for news in trend['news_items']:
            html_content += f"""
            <div class="news-item">
                <img class="news-image" src="{news.get('news_item_picture', '')}" alt="{news['title']}">
                <div class="news-content">
                    <h2>{news['title']}</h2>
                    <p class="news-source">Source: {news['source']}</p>
                    <a href="{news['url']}" target="_blank" class="read-more">
                        Read more <i class="fas fa-external-link-alt"></i>
                    </a>
                </div>
            </div>
            """

        html_content += """
            <div class="footer">
                <p>&copy; 2023 <span class="brand">Hot Topic Insights</span>. All rights reserved.</p>
            </div>
            </div>
        </body>
        </html>
        """

        with open(story_file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Trend file '{story_file_path}' has been created.") 
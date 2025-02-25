import os
import requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing

def collect_image_urls(news_item_url, trend_topic):
    """Collect image URLs from the news item page that contain the trend topic."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(news_item_url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the main content section (adjust the selector as needed)
        main_content = soup.find('div', class_='main-content')  # Example class name
        if not main_content:
            main_content = soup  # Fallback to the whole page if not found

        # Find all image tags within the main content
        images = main_content.find_all('img')

        # Filter images based on certain criteria
        filtered_images = []
        trend_topic_lower = trend_topic.lower()  # Convert topic to lowercase for comparison
        trend_keywords = trend_topic_lower.split()  # Split the topic into keywords

        for img in images:
            if 'src' in img.attrs:
                img_src = img['src'].lower()  # Convert image URL to lowercase for comparison
                # Debugging: Print each image URL being considered
                print(f"Considering image URL: {img_src}")

                # Exclude images with certain classes (e.g., 'logo', 'icon')
                if 'logo' not in img.get('class', []) and 'icon' not in img.get('class', []):
                    # Check if any of the trend keywords are in the image URL
                    if any(keyword in img_src for keyword in trend_keywords):
                        filtered_images.append(img['src'])
                    else:
                        print(f"Image URL does not contain any trend keywords: {img_src}")

        return filtered_images  # Return list of filtered image URLs
    except Exception as e:
        print(f"Error fetching images from {news_item_url}: {e}")
        return []

def create_story_files(trends):
    """Create separate HTML files for each trend containing all its news items."""
    if not os.path.exists('hosted_files/stories'):
        os.makedirs('hosted_files/stories')  # Create a directory for story files

    # Create a file for each trend
    for trend in trends:
        # Check if 'topic' key exists in trend
        if 'topic' not in trend:
            print(f"Warning: 'topic' key not found in trend: {trend}")
            continue  # Skip this trend if 'topic' is missing

        # Create a sanitized filename from the trend topic
        trend_name = trend['topic'].replace(" ", "_").replace("/", "_").lower()
        file_name = f"{trend_name}.html"
        story_file_path = os.path.join('hosted_files/stories', file_name)

        # Create HTML content for the trend
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{trend['topic']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2 {{ color: #333; }}
                img {{ max-width: 100%; height: auto; margin: 10px 0; }}
                .news-item {{ border-bottom: 1px solid #ccc; padding: 20px 0; }}
                .news-item:last-child {{ border-bottom: none; }}
            </style>
        </head>
        <body>
            <h1>{trend['topic']}</h1>
        """

        # Add each news item to the trend file
        for news in trend['news_items']:
            # Collect images for this news item
            image_urls = collect_image_urls(news['url'], trend['topic'])  # Pass the trend topic
            preview_image = image_urls[0] if image_urls else None  # Get the first image as a preview

            # Debugging: Print the preview image URL
            print(f"Preview image for '{news['title']}': {preview_image}")

            html_content += f"""
            <div class="news-item">
                <h2>{news['title']}</h2>
                <p>Source: {news['source']}</p>
                <a href="{news['url']}" target="_blank">Read more</a>
            """

            # Add the preview image if available
            if preview_image:
                html_content += f'<img src="{preview_image}" alt="Preview for {news["title"]}"><br>'
            else:
                html_content += '<p>No preview image available.</p>'  # Indicate no preview image

            html_content += """
                <div class="images">
            """

            for image_url in image_urls:
                html_content += f'    <img src="{image_url}" alt="Image for {news["title"]}"><br>'

            html_content += """
                </div>
            </div>
            """

        html_content += """
        </body>
        </html>
        """

        # Write the trend content to a file
        with open(story_file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"Trend file '{story_file_path}' has been created.") 
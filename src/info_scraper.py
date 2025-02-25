import os

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
            html_content += f"""
            <div class="news-item">
                <h2>{news['title']}</h2>
                <p>Source: {news['source']}</p>
                <a href="{news['url']}" target="_blank">Read more</a>
                <div class="images">
            """

            # Add images for this news item
            for image_url in news.get('images', []):
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
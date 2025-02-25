import os

def generate_html(trends, output_file='hosted_files/index.html'):
    """Generate an HTML file containing the Google Trends data."""
    
    # Create HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Hot Topic Insights - Trending Now</title>
        <meta name="description" content="Stay updated with the latest trending topics and news articles.">
        <meta name="keywords" content="trending, news, hot topics, insights">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 20px;
                background-color: #f4f4f4; 
            }
            h1 { 
                color: #333; 
                text-align: center;
                margin-bottom: 30px;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            .logo {
                display: block;
                margin: 0 auto 20px;
                max-width: 200px;
            }
            .trend { 
                margin-bottom: 20px; 
                padding: 0;
                border-radius: 8px;
                background: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
                text-decoration: none;
                color: inherit;
                display: block;
                overflow: hidden;
            }
            .trend:hover { 
                transform: translateY(-3px);
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            }
            .trend-image {
                width: 100%;
                height: 200px;
                object-fit: cover;
            }
            .trend-content {
                padding: 20px;
            }
            .trend h2 { 
                color: #444; 
                margin-top: 0;
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                font-size: 1.1em;
                gap: 15px;
            }
            .trend-topic {
                color: #666;
                font-size: 0.85em;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .traffic {
                font-size: 0.9em;
                color: #666;
                padding: 4px 8px;
                background: #f0f0f0;
                border-radius: 4px;
                white-space: nowrap;
                flex-shrink: 0;
            }
            .news-item { 
                margin: 10px 0 0;
                padding: 10px;
                border-left: 3px solid #e74c3c;
                background: #f9f9f9;
            }
            .source { 
                color: #666;
                font-size: 0.9em;
                margin-top: 5px;
            }
            .brand {
                color: #e74c3c;
                font-weight: bold;
            }
            @media (max-width: 600px) {
                .trend-content { 
                    padding: 15px; 
                }
                .news-item { 
                    padding: 8px; 
                }
                .trend h2 {
                    flex-direction: column;
                    align-items: flex-start;
                }
                .traffic {
                    margin-top: 5px;
                }
                .trend-image {
                    height: 150px;
                }
            }
            .trends-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <img src="src/logo.png" alt="Hot Topic Insights Logo" class="logo">
            <h1><span class="brand">Hot Topic Insights</span> - Trending Now</h1>
            <div class="trends-grid">
    """
    
    # Add each trend and its news items
    for trend in trends:
        # Create sanitized filename for the story link
        story_filename = trend['topic'].replace(" ", "_").replace("/", "_").lower() + ".html"
        
        # Get the first news article's title to use as the main headline
        main_headline = trend['news_items'][0]['title'] if trend['news_items'] else trend['topic']
        
        # Get the image for the trend
        trend_image = trend.get('picture') or (trend['news_items'][0].get('news_item_picture') if trend['news_items'] else None)
        
        html_content += f"""
        <a href="stories/{story_filename}" class="trend">
        """
        
        if trend_image:
            html_content += f"""
            <img src="{trend_image}" alt="{trend['topic']}" class="trend-image">
            """
            
        html_content += f"""
            <div class="trend-content">
                <div class="trend-topic">{trend['topic']}</div>
                <h2>
                    {main_headline}
                    <span class="traffic">{trend['traffic']} searches</span>
                </h2>
                <div class="news-items">
        """
        
        # Add first news item source as preview
        if trend['news_items']:
            first_news = trend['news_items'][0]
            html_content += f"""
                    <div class="news-item">
                        <div class="source">Source: {first_news['source']}</div>
                    </div>
                """
            
        html_content += """
                </div>
            </div>
        </a>
        """
    
    html_content += """
            </div>
        </div>
    </body>
    </html>
    """
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the HTML content to the file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML file '{output_file}' has been created.") 
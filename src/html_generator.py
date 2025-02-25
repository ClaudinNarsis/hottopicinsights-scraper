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
            .trend { 
                margin-bottom: 20px; 
                padding: 20px; 
                border-radius: 8px;
                background: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
                text-decoration: none;
                color: inherit;
                display: block;
            }
            .trend:hover { 
                transform: translateY(-3px);
                box-shadow: 0 4px 10px rgba(0,0,0,0.15);
            }
            .trend h2 { 
                color: #444; 
                margin-top: 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .traffic {
                font-size: 0.9em;
                color: #666;
                padding: 4px 8px;
                background: #f0f0f0;
                border-radius: 4px;
            }
            .news-item { 
                margin: 10px 0;
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
                .trend { 
                    padding: 15px; 
                }
                .news-item { 
                    padding: 8px; 
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1><span class="brand">Hot Topic Insights</span> - Trending Now</h1>
    """
    
    # Add each trend and its news items
    for trend in trends:
        # Create sanitized filename for the story link
        story_filename = trend['topic'].replace(" ", "_").replace("/", "_").lower() + ".html"
        
        html_content += f"""
        <a href="stories/{story_filename}" class="trend">
            <h2>
                {trend['topic']}
                <span class="traffic">{trend['traffic']} searches</span>
            </h2>
            <div class="news-items">
        """
        
        # Add first news item as preview
        if trend['news_items']:
            first_news = trend['news_items'][0]
            html_content += f"""
                <div class="news-item">
                    <div>{first_news['title']}</div>
                    <div class="source">Source: {first_news['source']}</div>
                </div>
            """
            
        html_content += """
            </div>
        </a>
        """
    
    html_content += """
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
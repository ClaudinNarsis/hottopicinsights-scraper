def generate_html(trends):
    """Generate an HTML file with links to the news articles and summaries."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Trends Summary</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            h2 { color: #555; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
            .topic { margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <h1>Google Trends Summary</h1>
    """

    for trend in trends:
        html_content += f"""
        <div class="topic">
            <h2><a href="stories/{trend['topic'].replace(' ', '_')}.html">{trend['topic']} ({trend['traffic']})</a></h2>
            <p>Related News:</p>
            <ul>
        """
        for news in trend['news_items']:
            html_content += f"""
                <li>
                    <a href="{news['url']}" target="_blank">{news['title']}</a> - Source: {news['source']}
                </li>
            """
        html_content += "</ul></div>"

    html_content += """
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open("hosted_files/google_trends_summary.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML file 'google_trends_summary.html' has been created.") 
from scraper import fetch_trends, print_trends
from html_generator import generate_html
from info_scraper import create_story_files
import os
import shutil  # Import shutil for file operations

def main():
    print("Starting the Google Trends Scraper from main.py!")
    trends = fetch_trends()
    print_trends(trends)
    
    # Ensure the hosted_files directory exists
    if not os.path.exists('hosted_files'):
        os.makedirs('hosted_files')

    # Generate the HTML summary file directly in the hosted_files directory as index.html
    index_file = os.path.join('hosted_files', 'index.html')
    generate_html(trends, output_file=index_file)

    # Create individual story files
    create_story_files(trends)

if __name__ == "__main__":
    main() 
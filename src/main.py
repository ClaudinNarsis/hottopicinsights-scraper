from scraper import fetch_trends, print_trends
from html_generator import generate_html
from info_scraper import create_story_files  # Import the new function
import os

def main():
    print("Starting the Google Trends Scraper from main.py!")
    trends = fetch_trends()
    print_trends(trends)
    
    # Ensure the hosted_files directory exists
    if not os.path.exists('hosted_files'):
        os.makedirs('hosted_files')

    # Generate the HTML summary file in the hosted_files directory
    generate_html(trends)

    # Get the current working directory and construct full paths
    current_dir = os.getcwd()
    source_file = os.path.join(current_dir, "google_trends_summary.html")
    target_file = os.path.join(current_dir, "hosted_files", "google_trends_summary.html")

    # Move the file
    if os.path.exists(source_file):  # Check if the source file exists
        os.rename(source_file, target_file)
    else:
        print(f"Error: The file '{source_file}' does not exist.")  # Print an error message if it doesn't exist

    create_story_files(trends)  # Call the new function to create story files

if __name__ == "__main__":
    main() 
import os
from bs4 import BeautifulSoup

def process_html_to_text(directory):
    # Walk through all files and folders within directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                # Skip files with '@' in the name
                if '@' in file:
                    print(f"Skipped {file}, contains '@' in the file name.")
                    continue

                # Construct the full file path
                html_path = os.path.join(root, file)
                # Define path for the new text file
                text_path = os.path.splitext(html_path)[0] + '.txt'
                
                # Check if the .txt file already exists
                if os.path.exists(text_path):
                    print(f"Skipped {html_path}, {text_path} already exists.")
                    continue
                
                # Read the HTML file content with error handling for encoding issues
                try:
                    with open(html_path, 'r', encoding='utf-8') as html_file:
                        soup = BeautifulSoup(html_file, 'html.parser')
                except UnicodeDecodeError:
                    print(f"UnicodeDecodeError encountered with {html_path}, trying ISO-8859-1 encoding.")
                    try:
                        with open(html_path, 'r', encoding='iso-8859-1') as html_file:
                            soup = BeautifulSoup(html_file, 'html.parser')
                    except Exception as e:
                        print(f"Failed to read {html_path} with ISO-8859-1 encoding: {e}")
                        continue
                    
                # Remove <header> elements not within <article>
                for header in soup.find_all("header"):
                    if not header.find_parent("article"):
                        header.decompose()
                
                # Remove other unwanted elements
                for element in soup.find_all(["nav", "footer", "title"]):
                    element.decompose()
                for element in soup.find_all(class_=["SkipToContent", "MainMenu", "SectionMenu", "MobileNav-Menu"]):
                    element.decompose()
                
                # Extract text and remove unwanted meta content if necessary
                text = soup.get_text()
                
                # Save the cleaned text to a .txt file
                with open(text_path, 'w', encoding='utf-8') as text_file:
                    text_file.write(text)

                print(f"Processed {html_path} to {text_path}")

# Specify the directory to process
process_html_to_text('/Users/dimaip/psmb/mole-ai/scrape/')
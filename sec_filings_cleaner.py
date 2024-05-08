from bs4 import BeautifulSoup
import os

def extract_text_with_tables(soup):
    """
    Extracts plain text and table data from the BeautifulSoup object.
    
    Parameters:
        soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.
        
    Returns:
        tuple: Two lists, the first containing text elements and the second containing tables.
    """
    text_content = []
    table_content = []
    
    # Iterate through all elements in the HTML
    for element in soup.recursiveChildGenerator():
        if element.name == 'p' and element.get_text(strip=True):
            # Append text from paragraph elements
            text_content.append(element.get_text(strip=True))
        elif element.name == 'table':
            # Extract table data and append to list
            table = []
            rows = element.find_all('tr')
            for row in rows:
                cols = row.find_all(['td', 'th'])
                cols = [ele.text.strip() for ele in cols]
                table.append([ele for ele in cols if ele])
            table_content.append(table)
    return text_content, table_content

def save_cleaned_data(text, tables, output_file):
    """
    Saves the cleaned text and tables into a text file.
    
    Parameters:
        text (list): List of strings containing text content.
        tables (list): List of lists representing tables.
        output_file (str): Path to the output file.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("Text Content:\n")
        file.write('\n'.join(text))
        file.write("\n\nTables:\n")
        for table in tables:
            for row in table:
                file.write('\t'.join(row) + '\n')
            file.write('\n')

def clean_html(file_path, output_file):
    """
    Parses HTML file, extracts relevant data, and saves it cleanly.
    
    Parameters:
        file_path (str): Path to the HTML file.
        output_file (str): Path to save the cleaned data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'lxml')
    
    text, tables = extract_text_with_tables(soup)
    save_cleaned_data(text, tables, output_file)

def process_directory(directory):
    """
    Processes each file in the directory that matches the defined criteria.
    
    Parameters:
        directory (str): The directory to scan for files.
    """
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.endswith('primary-document.html'):
                file_path = os.path.join(root, name)
                output_file = os.path.join(root, 'cleaned_data.txt')
                print(f"Cleaning file: {file_path}")
                clean_html(file_path, output_file)
                print(f"Cleaned data saved to: {output_file}")

root_directory = "sec_filings_new/sec-edgar-filings"
process_directory(root_directory)
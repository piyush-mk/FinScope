import streamlit as st
import os
import re
import requests
import json

# API key for external data processing or analytics services.
API_KEY = st.secrets["API_KEY"]

# Base directory where the SEC filings are stored.
BASE_DIR = "sec_filings_new/sec-edgar-filings"

# Mapping of company ticker symbols to their full names.
company_names = {'AAPL': 'Apple', 'MSFT': 'Microsoft', 'V': 'Visa'}

def get_companies():
    """
    Retrieves a list of company names from the base directory.
    
    Returns:
        list: A list of company names found in the base directory.
    """
    # Retrieves directories within the BASE_DIR and checks if they are actual directories
    # Converts ticker symbols to company names using the company_names dictionary.
    return [company_names.get(dir, dir) for dir in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, dir))]

def get_years_for_company(company):
    """
    Retrieves a list of years for which data is available for a given company.
    
    Args:
        company (str): The name of the company.
        
    Returns:
        list: A sorted list of years (descending) for which data exists.
    """
    # Converts company name back to ticker if possible.
    dir_name = {v: k for k, v in company_names.items()}.get(company, company)
    # Path to the company's 10-K filings.
    company_dir = os.path.join(BASE_DIR, dir_name, "10-K")
    years = []
    if os.path.exists(company_dir):
        # Lists each year directory and checks for the presence of cleaned data.
        for folder in os.listdir(company_dir):
            if "cleaned_data.txt" in os.listdir(os.path.join(company_dir, folder)):
                # Extracts the last two digits of the year and adjusts for century changes.
                match = re.search(r'-([0-9]{2})-[0-9]+$', folder)
                if match:
                    year = "20" + match.group(1) if match.group(1) < '30' else "19" + match.group(1)
                    years.append(year)
        # Returns a sorted list of unique years.
        return sorted(set(years), reverse=True)
    return []

def get_cleaned_data_path(company, year):
    """
    Locates the path to the cleaned data text file for a specified company and year.
    
    Args:
        company (str): The name of the company.
        year (str): The fiscal year of interest in YYYY format.
    
    Returns:
        str or None: The file path to the cleaned data text file if found, otherwise None.
    """
    # Maps company name to its directory name, falling back to the given name if not found in company_names.
    dir_name = {v: k for k, v in company_names.items()}.get(company, company)
    # Constructs the path to the directory containing the 10-K filings for the specified company.
    company_dir = os.path.join(BASE_DIR, dir_name, "10-K")
    # Extracts the last two digits of the year for file matching.
    year_short = year[-2:]
    # Walks through the company directory to find the file.
    for root, dirs, files in os.walk(company_dir):
        # Checks if 'cleaned_data.txt' exists and matches the year substring in the directory name.
        if "cleaned_data.txt" in files and f'-{year_short}-' in root:
            return os.path.join(root, "cleaned_data.txt")
    # Returns None if the file is not found.
    return None

def extract_relevant_data(file_path, pattern, lines_before, lines_after):
    """
    Extracts a segment of text from a file based on a specified regex pattern and context lines.
    
    Args:
        file_path (str): Path to the file from which to extract data.
        pattern (str): Regex pattern to identify the relevant line.
        lines_before (int): Number of lines to include before the matched line.
        lines_after (int): Number of lines to include after the matched line.
    
    Returns:
        str: The extracted text segment or a message indicating data not found.
    """
    # Opens the file for reading with UTF-8 encoding.
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # Compiles the regex pattern for the search.
    search_pattern = re.compile(pattern)
    # Iterates through the lines in the file to find a match.
    for i, line in enumerate(lines):
        if search_pattern.search(line):
            # Calculates the start and end indices of the context segment.
            start_index = max(i - lines_before, 0)
            end_index = i + lines_after
            # Returns the relevant segment of lines.
            return ''.join(lines[start_index:end_index])
    # Returns a default message if no relevant data is found.
    return "Relevant data segment not found."

# Sets the title of the Streamlit app displayed in the browser tab.
st.title('SEC 10-K Filings Analysis')

# Dropdown menu for users to select a company from the list of companies available.
# The list is fetched from the get_companies function.
company = st.selectbox('Select Company', get_companies())

# Retrieves a list of years for which data is available for the selected company.
years = get_years_for_company(company)

# Dropdown menu for users to select a year for which they want to see data.
year = st.selectbox('Select Year', years)

# Dictionary mapping companies to their respective analysis options.
analysis_options = {
    'Apple': ['Sales by Geographic Region', 'Net Sales by Category'],
    'Microsoft': ['Net Income from Operations', 'Investing Activities Analysis'],
    'Visa': ['Consumer Credit Analysis']
}

# Fetches the analysis options for the selected company.
selected_analysis_options = analysis_options.get(company, [])

# Dropdown menu for users to select the type of analysis they want to perform.
analysis_type = st.selectbox('Select Analysis Type', selected_analysis_options)

# Radio buttons for users to select the mode of analysis, either single year or trend over the past five years.
analysis_mode = st.radio("Select Analysis Mode", ('Single Year Analysis', 'Trend Analysis (past 5 years from selected Year)'))

# Determines the range of years to be analyzed based on the selected analysis mode.
# If 'Trend Analysis' is selected, it provides the past 5 years; otherwise, it uses the single selected year.
range_years = sorted(years)[:5] if analysis_mode == 'Trend Analysis' else [year]

# Button to trigger the analysis of data based on the selected company, year, and analysis type.
if st.button('Analyze Data!'):
    # Initialize a variable to accumulate the data from multiple years.
    combined_data = ""
    # Iterates through the range of selected years to perform analysis.
    for yr in range_years:
        # Retrieves the path to the cleaned data file for the specific company and year.
        file_path = get_cleaned_data_path(company, yr)
        # Checks if the cleaned data file exists.
        if file_path:
            # Custom analysis based on the company and analysis type selected by the user.
            if analysis_type == 'Sales by Geographic Region' and company == 'Apple':
                # Extracts the relevant data from the file using a regex pattern.
                data = extract_relevant_data(file_path, r'Americas.*\$', 2, 6)
                # Prepares a prompt text for further analysis by external services.
                prompt_text = f"Analyze the regional sales trends for Apple Inc., highlighting significant variations and discussing potential influences from economic and market conditions:\n\n{data}"
            elif analysis_type == 'Net Sales by Category' and company == 'Apple':
                data = extract_relevant_data(file_path, r'iPhone \(1\).*\$', 2, 6)
                prompt_text = f"Explore the category-wise sales data for Apple Inc., analyzing trends and projecting future performance based on past data:\n\n{data}"
            elif analysis_type == 'Net Income from Operations' and company == 'Microsoft':
                data = extract_relevant_data(file_path, r'Net income.*\$', 2, 20)
                prompt_text = f"Examine the trend in Microsoft's net income from operations, interpreting the operational efficiency and fiscal management over the years:\n\n{data}"
            elif analysis_type == 'Investing Activities Analysis' and company == 'Microsoft':
                data = extract_relevant_data(file_path, r'Additions to property and equipment.*\(', 1, 6)
                prompt_text = f"Delve into Microsoft's investment activities, focusing on capital expenditures and their implications on financial strategy and company growth:\n\n{data}"
            elif analysis_type == 'Consumer Credit Analysis' and company == 'Visa':
                data = extract_relevant_data(file_path, r'Consumer credit\t\$', 1, 6)
                prompt_text = f"Assess Visa's performance across different payment segments with a focus on consumer credit, discussing the implications for market trends and strategic business decisions:\n\n{data}"
            else:
                # If no valid analysis type is matched, continues to the next iteration.
                continue
            # Accumulates the results for each year into a single string.
            combined_data += f"Data for {yr}:\n{data}\n\n"
        else:
            # If no cleaned data file is found, displays an error message on the Streamlit app.
            st.error(f"No cleaned data available for {company} in {yr}.")
            continue

    # Checks if any combined data has been collected from the files.
    if combined_data:
        # Adjusts the prompt text based on the selected analysis mode.
        if analysis_mode == 'Trend Analysis':
            # Prepares a prompt for trend analysis covering the range of selected years.
            prompt_text = f"Perform a trend analysis based on the following data for {company} from {range_years[0]} to {range_years[-1]}:\n\n{combined_data}"
        else:
            # Prepares a prompt for single year analysis.
            prompt_text = f"Analyze the following data for {company} in {year}:\n\n{combined_data}"

        # Makes a POST request to an external API to analyze the prepared data using a specified AI model.
        response = requests.post(
            "https://api.awanllm.com/v1/completions",
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            },
            json={"model": "Awanllm-Llama-3-8B-Dolfin", "prompt": prompt_text}
        )
        # Checks if the API call was successful.
        if response.status_code == 201:
            # Extracts the text output from the API response.
            text_output = response.json()['choices'][0]['text']
            # Displays the analysis result in a text area widget in the Streamlit app.
            st.text_area("Analysis Result", text_output, height=500)
        else:
            # Displays an error message if the API call fails.
            st.error(f"API call failed with status code: {response.status_code}")

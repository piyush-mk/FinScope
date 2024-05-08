import streamlit as st
import os
import re
import requests
import json

API_KEY=st.secrets["API_KEY"]

BASE_DIR = "sec_filings_new/sec-edgar-filings"

company_names = {'AAPL': 'Apple', 'MSFT': 'Microsoft', 'V': 'Visa'}

def get_companies():
    return [company_names.get(dir, dir) for dir in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, dir))]

def get_years_for_company(company):
    dir_name = {v: k for k, v in company_names.items()}.get(company, company)
    company_dir = os.path.join(BASE_DIR, dir_name, "10-K")
    years = []
    if os.path.exists(company_dir):
        for folder in os.listdir(company_dir):
            if "cleaned_data.txt" in os.listdir(os.path.join(company_dir, folder)):
                match = re.search(r'-([0-9]{2})-[0-9]+$', folder)
                if match:
                    year = "20" + match.group(1) if match.group(1) < '30' else "19" + match.group(1)
                    years.append(year)
        return sorted(set(years), reverse=True)
    return []


def get_cleaned_data_path(company, year):
    dir_name = {v: k for k, v in company_names.items()}.get(company, company)
    company_dir = os.path.join(BASE_DIR, dir_name, "10-K")
    year_short = year[-2:]
    for root, dirs, files in os.walk(company_dir):
        if "cleaned_data.txt" in files and f'-{year_short}-' in root:
            return os.path.join(root, "cleaned_data.txt")
    return None

def extract_relevant_data(file_path, pattern, lines_before, lines_after):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    search_pattern = re.compile(pattern)
    for i, line in enumerate(lines):
        if search_pattern.search(line):
            start_index = max(i - lines_before, 0)
            end_index = i + lines_after
            return ''.join(lines[start_index:end_index])
    return "Relevant data segment not found."

st.title('SEC 10-K Filings Analysis')

company = st.selectbox('Select Company', get_companies())
years = get_years_for_company(company)
year = st.selectbox('Select Year', years)

analysis_options = {
    'Apple': ['Sales by Geographic Region', 'Net Sales by Category'],
    'Microsoft': ['Net Income from Operations', 'Investing Activities Analysis'],
    'Visa': ['Consumer Credit Analysis']
}

selected_analysis_options = analysis_options.get(company, [])
analysis_type = st.selectbox('Select Analysis Type', selected_analysis_options)

analysis_mode = st.radio("Select Analysis Mode", ('Single Year Analysis', 'Trend Analysis (past 5 years from selected Year)'))
range_years = sorted(years)[:5] if analysis_mode == 'Trend Analysis' else [year]

if st.button('Analyze Data!'):
    combined_data = ""
    for yr in range_years:
        file_path = get_cleaned_data_path(company, yr)
        if file_path:
            if analysis_type == 'Sales by Geographic Region' and company == 'Apple':
                data = extract_relevant_data(file_path, r'Americas.*\$', 2, 6)
                prompt_text = """Analyze the regional sales trends for Apple Inc., highlighting significant variations and discussing potential influences from economic and market conditions:\n\n""" + data
            elif analysis_type == 'Net Sales by Category' and company == 'Apple':
                data = extract_relevant_data(file_path, r'iPhone \(1\).*\$', 2, 6)
                prompt_text = """Explore the category-wise sales data for Apple Inc., analyzing trends and projecting future performance based on past data:\n\n""" + data
            elif analysis_type == 'Net Income from Operations' and company == 'Microsoft':
                data = extract_relevant_data(file_path, r'Net income.*\$', 2, 20)
                prompt_text = """Examine the trend in Microsoft's net income from operations, interpreting the operational efficiency and fiscal management over the years:\n\n""" + data
            elif analysis_type == 'Investing Activities Analysis' and company == 'Microsoft':
                data = extract_relevant_data(file_path, r'Additions to property and equipment.*\(', 1, 6)
                prompt_text = """Delve into Microsoft's investment activities, focusing on capital expenditures and their implications on financial strategy and company growth:\n\n""" + data
            elif analysis_type == 'Consumer Credit Analysis' and company == 'Visa':
                data = extract_relevant_data(file_path, r'Consumer credit\t\$', 1, 6)
                prompt_text = """Assess Visa's performance across different payment segments with a focus on consumer credit, discussing the implications for market trends and strategic business decisions:\n\n""" + data
            else:
                continue
            combined_data += f"Data for {yr}:\n{data}\n\n"
        else:
            st.error(f"No cleaned data available for {company} in {yr}.")
            continue

    if combined_data:
        if analysis_mode == 'Trend Analysis':
            prompt_text = f"Perform a trend analysis based on the following data for {company} from {range_years[0]} to {range_years[-1]}:\n\n{combined_data}"
        else:
            prompt_text = f"Analyze the following data for {company} in {year}:\n\n{combined_data}"

        response = requests.post(
            "https://api.awanllm.com/v1/completions",
            headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        },
            json={"model": "Meta-Llama-3-8B-Instruct", "prompt": prompt_text}
        )
        if response.status_code == 201:
            text_output = response.json()['choices'][0]['text']
            st.text_area("Analysis Result", text_output, height=500)
        else:
            st.error(f"API call failed with status code: {response.status_code}")
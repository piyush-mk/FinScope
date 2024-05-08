# FinScope - SEC Filings Analysis

## Deployment
The application is deployed and available for use at [FinScope on Streamlit Cloud](https://finscope.streamlit.app/).

## Project Overview
FinScope is a Streamlit-based web application designed to analyze and visualize trends from SEC 10-K filings. It allows users to select a company and a specific year (or range of years) to view financial data extracted from SEC filings and perform trend analysis.

## Tech-Stack
- **Python**: Chosen for its robust ecosystem and libraries for data manipulation and analysis.
- **Streamlit**: Used for building and deploying interactive and responsive web apps quickly. It's ideal for rapid prototyping of data-focused applications.
- **Pandas**: Utilized for data manipulation and extraction because of its efficient and intuitive data structures.
- **Requests**: Used for making HTTP requests to external APIs. This library is straightforward and widely used in the Python community.

## Application Features
- **Company Selection**: Users can choose from a list of companies whose SEC filings are available.
- **Year Selection**: Users can select a single year or a range for trend analysis.
- **Analysis Type**: Depending on the selected company, different types of financial analyses are available, such as sales by geographic region or net income from operations.

## Development Steps

### Step 1: Setting Up the Local Development Environment
- All necessary Python packages were installed, including Streamlit, Pandas, Plotly, and Requests.

### Step 2: Data Extraction Functionality
- Developed Python scripts to parse and extract relevant financial data from `cleaned_data.txt` files within the SEC filings.

### Step 3: Integration with External APIs
- Implemented functionality to send extracted data to Meta-Llama-3-8B for analysis.

### Step 4: Preparing for Deployment
- Adjusted file paths and configurations to ensure compatibility with Streamlit Cloud deployment requirements.
- Created a `requirements.txt` file to specify exact versions of all required packages ensuring consistent environments across different setups.

### Step 6: Deployment to Streamlit Cloud
- Configured the GitHub repository for Streamlit Cloud deployment, including setting up secrets for API keys.
- Ensured the data directory structure in the GitHub repo matches the expected structure by the application.

## Deployment
The application is deployed and available for use at [FinScope on Streamlit Cloud](https://finscope.streamlit.app/).

## Usage
To use the app, navigate to the deployed Streamlit Cloud application URL, select the desired company, year, and analysis type. The app will fetch the corresponding data, analyze it, and present the results along with visualizations.

## Future Work
- Expand the dataset to include more companies and years.
- Enhance the analysis capabilities to include more complex financial metrics.
- Improve the user interface for a more engaging user experience.

## Local Setup
To run this project locally:
1. Clone the repository.
2. Ensure Python 3.x is installed.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run the app: `streamlit run your_app_script.py`.


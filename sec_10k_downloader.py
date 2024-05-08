from sec_edgar_downloader import Downloader
import datetime

# Get the current year to set the range for downloading filings
current_year = datetime.datetime.now().year

# Initialize the Downloader with company name, email, and path for storage
dl = Downloader("company name", "email", "path")

# List of company tickers for which the 10-K forms need to be downloaded
company_tickers = ["MSFT", "V", "AAPL"]

# Loop through each ticker and download their 10-K filings from 1995 to the current year
for ticker in company_tickers:
    # Informing start of the download process for a ticker
    print(f"Starting downloads for {ticker} from 1995 to {current_year}...")
    # Downloading 10-K forms after January 1, 1995
    dl.get("10-K", ticker, after="1995-01-01", download_details=True)
    # Indicating completion of the download process for a ticker
    print(f"Completed downloads for {ticker}.")
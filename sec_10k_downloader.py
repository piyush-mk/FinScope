from sec_edgar_downloader import Downloader
import datetime

current_year = datetime.datetime.now().year

dl = Downloader("company name", "email", "path")

# Microsoft, Visa, and Apple company tickers
company_tickers = ["MSFT", "V", "AAPL"]

for ticker in company_tickers:
    print(f"Starting downloads for {ticker} from 1995 to {current_year}...")
    dl.get("10-K", ticker, after="1995-01-01", download_details=True)
    print(f"Completed downloads for {ticker}.")

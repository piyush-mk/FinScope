from sec_edgar_downloader import Downloader
import os

download_dir = "sec_filings"

dl = Downloader(download_dir)

def download_10k_filings(ticker, start_year, end_year):
    for year in range(start_year, end_year + 1):
        dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")

if __name__ == "__main__":
    # Goldman Sachs, Morgan Stanley, and American Express
    company_tickers = ["GS", "MS", "AXP"]
    start_year = 1995
    end_year = 2023

    for ticker in company_tickers:
        print(f"Downloading 10-K filings for {ticker}...")
        download_10k_filings(ticker, start_year, end_year)
        print(f"Completed downloads for {ticker}.")

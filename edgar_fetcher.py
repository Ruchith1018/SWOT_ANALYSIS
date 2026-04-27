import os
import json
import requests
from bs4 import BeautifulSoup
from sec_edgar_downloader import Downloader
import difflib

SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"

# Support Vercel /tmp directory for ephemeral storage
STORAGE_BASE = os.environ.get("STORAGE_DIR", ".")
TICKERS_FILE = os.path.join(STORAGE_BASE, "company_tickers.json")
DEFAULT_DOWNLOAD_FOLDER = os.path.join(STORAGE_BASE, "sec_filings")

def download_tickers():
    """Downloads the SEC tickers mapping and saves it locally."""
    headers = {
        "User-Agent": "RuchithApp (ruchith@example.com)"
    }
    print(f"Downloading tickers from {SEC_TICKERS_URL}...")
    response = requests.get(SEC_TICKERS_URL, headers=headers)
    response.raise_for_status()
    with open(TICKERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(response.json(), f)
    print(f"Saved tickers to {TICKERS_FILE}")

def load_tickers():
    """Loads tickers from local file, downloading if necessary."""
    if not os.path.exists(TICKERS_FILE):
        download_tickers()
    with open(TICKERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

COMMON_ALIASES = {
    # Tech Giants
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "meta": "META",
    "facebook": "META",
    "apple": "AAPL",
    "amazon": "AMZN",
    "netflix": "NFLX",
    "tesla": "TSLA",
    "microsoft": "MSFT",
    "nvidia": "NVDA",
    "adobe": "ADBE",
    "salesforce": "CRM",
    "intel": "INTC",
    "amd": "AMD",
    "qualcomm": "QCOM",
    "oracle": "ORCL",
    "ibm": "IBM",
    "cisco": "CSCO",
    
    # Consumer & Retail
    "starbucks": "SBUX",
    "mcdonalds": "MCD",
    "mcdonald's": "MCD",
    "coca cola": "KO",
    "coca-cola": "KO",
    "pepsi": "PEP",
    "nike": "NKE",
    "walmart": "WMT",
    "costco": "COST",
    "target": "TGT",
    "disney": "DIS",
    "home depot": "HD",
    "lowes": "LOW",
    "lowe's": "LOW",
    
    # Financials
    "visa": "V",
    "mastercard": "MA",
    "goldman sachs": "GS",
    "jp morgan": "JPM",
    "jpmorgan": "JPM",
    "bank of america": "BAC",
    "morgan stanley": "MS",
    "berkshire": "BRK-B",
    "berkshire hathaway": "BRK-B",
    
    # Travel & Lifestyle
    "uber": "UBER",
    "lyft": "LYFT",
    "airbnb": "ABNB",
    "spotify": "SPOT",
    "snapchat": "SNAP",
    "snap": "SNAP",
    "pinterest": "PINS",
    "delta": "DAL",
    "united airlines": "UAL",
    
    # Auto & Industrials
    "ford": "F",
    "gm": "GM",
    "general motors": "GM",
    "toyota": "TM",
    "boeing": "BA",
    "caterpillar": "CAT",
    
    # Energy & Health
    "exxon": "XOM",
    "exxonmobil": "XOM",
    "chevron": "CVX",
    "johnson & johnson": "JNJ",
    "j&j": "JNJ",
    "pfizer": "PFE",
    "moderna": "MRNA",
    "unitedhealth": "UNH",
    
    # Others
    "chatgpt": "MSFT",
    "openai": "MSFT"
}

def get_ticker_from_name(company_name: str) -> str:
    company_name_lower = company_name.lower().strip()
    
    # 1. Check common aliases (Exact)
    if company_name_lower in COMMON_ALIASES:
        return COMMON_ALIASES[company_name_lower]
        
    # 2. Check common aliases (Fuzzy/Typo)
    alias_matches = difflib.get_close_matches(company_name_lower, COMMON_ALIASES.keys(), n=1, cutoff=0.7)
    if alias_matches:
        matched_alias = alias_matches[0]
        print(f"Typo detected? Correcting '{company_name}' to '{matched_alias}' based on aliases.")
        return COMMON_ALIASES[matched_alias]
        
    try:
        data = load_tickers()
    except Exception as e:
        print(f"Error loading local tickers: {e}. Falling back to API.")
        headers = {"User-Agent": "RuchithApp (ruchith@example.com)"}
        response = requests.get(SEC_TICKERS_URL, headers=headers)
        data = response.json()
    
    # Convert data for easier searching
    titles = [v['title'].lower() for v in data.values()]
    ticker_map = {v['title'].lower(): v['ticker'] for v in data.values()}
    
    # 3. Exact/Partial match in SEC database
    # Check exact match first
    for title, ticker in ticker_map.items():
        if company_name_lower == title:
            return ticker
    
    # Check if input is a substring of an official title
    for title, ticker in ticker_map.items():
        if company_name_lower in title:
            return ticker
            
    # 4. Fuzzy match in SEC database (handle typos for less common companies)
    sec_matches = difflib.get_close_matches(company_name_lower, titles, n=1, cutoff=0.7)
    if sec_matches:
        matched_title = sec_matches[0]
        print(f"Typo detected? Correcting '{company_name}' to '{matched_title}' in SEC database.")
        return ticker_map[matched_title]
    
    # Fallback: Assume the user entered the ticker directly
    return company_name.upper()
            
def clean_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove script, style, meta, link, and SEC ix metadata tags
    for element in soup(["script", "style", "meta", "link", "ix:header", "ix:hidden"]):
        element.extract()
        
    # Process tables to inject boundaries
    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            # Add a pipe for each table cell, th or td
            for cell in tr.find_all(["td", "th"]):
                cell.append(" | ")
            # Add a newline at the end of the row
            tr.append("\n")
            
    # Get the text
    text = soup.get_text(separator=' ')
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    # Break multiple spaces
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Reassemble, dropping blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def fetch_latest_10k(company_input: str, download_folder: str = DEFAULT_DOWNLOAD_FOLDER) -> str:
    """
    Fetches the latest 10-K for a given company name or ticker.
    Returns the path to the downloaded txt file, or None if failed.
    """
    ticker = get_ticker_from_name(company_input)
    print(f"Resolved company '{company_input}' to ticker '{ticker}'.")
    
    # User-Agent is required by SEC
    dl = Downloader("RuchithApp", "ruchith@example.com", download_folder)
    
    # Get the latest 1 10-K filing
    print(f"Downloading latest 10-K for {ticker}...")
    num_downloaded = dl.get("10-K", ticker, limit=1, download_details=True)
    
    if num_downloaded == 0:
        print(f"No 10-K filings found for {ticker}.")
        return None
        
    # Find the downloaded file
    ticker_folder = os.path.join(download_folder, "sec-edgar-filings", ticker, "10-K")
    if not os.path.exists(ticker_folder):
        return None
        
    for accession_num in os.listdir(ticker_folder):
        accession_folder = os.path.join(ticker_folder, accession_num)
        if os.path.isdir(accession_folder):
            primary_doc_path = os.path.join(accession_folder, "primary-document.html")
            full_txt_path = os.path.join(accession_folder, "full-submission.txt")
            
            # Prefer primary-document.html
            if os.path.exists(primary_doc_path):
                with open(primary_doc_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                clean_text = clean_html(content)
                out_path = os.path.join(accession_folder, "cleaned_10k.md")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(clean_text)
                return out_path
                
            elif os.path.exists(full_txt_path):
                with open(full_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                clean_text = clean_html(content)
                out_path = os.path.join(accession_folder, "cleaned_10k.txt")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(clean_text)
                return out_path
                
    return None

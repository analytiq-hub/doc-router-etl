# %%
import sec_edgar_downloader
from sec_edgar_downloader import Downloader
import os
import sys
import re
import bs4
from bs4 import BeautifulSoup
import html
import pdfkit
# %%
# Get the path to the current file
current_file = os.path.abspath(__file__)

# Get the directory of the current file
current_dir = os.path.dirname(current_file)

# Compute the path to the data directory
data_dir = os.path.join(current_dir, "..", "data")

# Initialize the downloader
dl = Downloader(company_name="Analytiq Hub LLC", download_folder=data_dir, email_address="iubica2@yahoo.com")

# Download Netflix's 10-K reports
NETFLIX_CIK = "0001065280"
dl.get("10-K", NETFLIX_CIK, after="2020-01-01")

# %%
dl.get("10-Q", NETFLIX_CIK, after="2020-01-01")

# %%
# Read the file
with open(f'{data_dir}/sec-edgar-filings/0001065280/10-K/0001065280-25-000044/full-submission.txt', 'r') as file:
    content = file.read()

# %%
# Function to convert SEC filing to HTML
def extract_html_from_filing(filing_content):
    """
    Extract HTML content from an SEC EDGAR filing.
    
    SEC EDGAR filings contain multiple document parts in an SGML structure.
    The main HTML filing is typically in a document with type '10-K' or '10-Q',
    and is stored within <TEXT> tags after the document headers.
    """
    # Look for the main HTML document (usually the 10-K filing itself)
    document_start = filing_content.find("<DOCUMENT>")
    document_parts = []
    
    while document_start != -1:
        # Find the end of this document section
        document_end = filing_content.find("</DOCUMENT>", document_start)
        if document_end == -1:
            break
            
        # Extract this document section
        document_section = filing_content[document_start:document_end + 11]  # +11 to include </DOCUMENT>
        
        # Check if this is the 10-K document
        if "<TYPE>10-K" in document_section or "<TYPE>10-Q" in document_section:
            # Find the text portion
            text_start = document_section.find("<TEXT>")
            text_end = document_section.find("</TEXT>", text_start)
            
            if text_start != -1 and text_end != -1:
                # Extract the content between <TEXT> tags
                html_content = document_section[text_start + 6:text_end]  # +6 to exclude <TEXT>
                document_parts.append(html_content)
        
        # Move to the next document section
        document_start = filing_content.find("<DOCUMENT>", document_end)
    
    if document_parts:
        # Join all found HTML parts and parse
        full_html = "\n".join(document_parts)
        soup = BeautifulSoup(full_html, 'html.parser')
        return soup
    else:
        # Fallback: look for any HTML section
        html_pattern = re.compile(r'<(?:HTML|html)>(.*?)</(?:HTML|html)>', re.DOTALL)
        html_match = html_pattern.search(filing_content)
        
        if html_match:
            html_content = f"<html>{html_match.group(1)}</html>"
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup
        else:
            # If no HTML found, create a simple HTML wrapper for the text
            soup = BeautifulSoup(f"<html><body><pre>{html.escape(filing_content)}</pre></body></html>", 'html.parser')
            return soup
# %%

# Convert all the 10-K and 10-Q filings under data/sec-edgar-filings to HTML.abs
# Save to the same folder with a .html extension
# Walk the directory recursively for all subfolders
def convert_sec_edgar_filings_to_html(data_dir, force=False):
    """ 
    Convert all the 10-K and 10-Q filings under data/sec-edgar-filings to HTML.abs
    Save to the same folder with a .html extension
    Walk the directory recursively for all subfolders
    
    Parameters:
    ----------
        data_dir: str, the path to the data directory
        force: bool, if True, overwrite existing HTML files
    """
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".txt") and (force or not os.path.exists(os.path.join(root, file.replace(".txt", ".html")))):
                with open(os.path.join(root, file), "r") as f:
                    content = f.read()
                html_content = extract_html_from_filing(content)
                with open(os.path.join(root, file.replace(".txt", ".html")), "w") as f:
                    f.write(str(html_content))
                    print(f"Converted {file} to {os.path.join(root, file.replace('.txt', '.html'))}")

# %%
convert_sec_edgar_filings_to_html(data_dir, force=False)

# %%

# Convert the HTML to a PDF, preserving the page breaks
def convert_html_to_pdf(html_file, output_file):
    """
    Convert HTML content to a PDF with larger fonts.
    """
    # Configure pdfkit with larger font options
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': True,
    }

    # Convert HTML file to PDF
    pdfkit.from_file(html_file, output_file, options=options)
    print(f"PDF saved to {output_file}")

# %%

def convert_sec_edgar_filings_to_pdf(data_dir, force=False):
    """
    Convert all the 10-K and 10-Q filings under data/sec-edgar-filings to PDF.
    Save to the same folder with a .pdf extension
    Walk the directory recursively for all subfolders

    Parameters:
    ----------
        data_dir: str, the path to the data directory
        force: bool, if True, overwrite existing PDF files
    """
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".html") and (force or not os.path.exists(os.path.join(root, file.replace(".html", ".pdf")))):
                html_file = os.path.join(root, file)
                output_file = os.path.join(root, file.replace(".html", ".pdf"))
                convert_html_to_pdf(html_file, output_file)

# %%
convert_sec_edgar_filings_to_pdf(data_dir, force=False)

# %%

# html_file = os.path.join(data_dir, "sec-edgar-filings/0001065280/10-K/0001065280-25-000044/full-submission.html")
# output_file = os.path.join(data_dir, "sec-edgar-filings/0001065280/10-K/0001065280-25-000044/full-submission.pdf")
# convert_html_to_pdf(html_file, output_file)



# %%

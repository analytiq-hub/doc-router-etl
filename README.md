# ETL for the Smart Document Router

This project implements an ETL (Extract, Transform, Load) pipeline for processing financial documents, specifically SEC filings like 10-K and 10-Q reports. The pipeline automates the extraction and transformation of unstructured data from these documents into structured formats for analysis.

## Key Features

- **Data Extraction**: Automatically downloads SEC filings from EDGAR database using CIK identifiers
- **Document Processing**: Converts SEC filings from their original format to HTML and PDF for easier consumption
- **Information Extraction**: Extracts structured data from financial reports including:
  - Company profiles and filing information
  - Financial highlights and key metrics
  - Business and geographic segment data
  - Risk factors and management discussion analysis
- **Data Transformation**: Converts semi-structured HTML content into clean, structured data
- **Schema Validation**: Uses Pydantic models to ensure extracted data conforms to predefined schemas

## Use Cases

- Create standardized financial metrics from SEC filings
- Extract and analyze key risk factors after earnings releases
- Automate processing of long-form financial documents
- Build datasets for downstream financial analysis

## Getting Started

* Install requirements: `pip install -r requirements.txt`
* Install `wkhtmltopdf` package
  * On Fedora or CentOS: `yum install wkhtmltopdf`
* (Future) Configure your API keys and credentials for the Smart Document Router
* Run the data extraction notebooks to download SEC filings
* (Future) Upload the 10-K and 10-Q to the Smart Document Router
# HaloOglasi Web Scraping

This project 
This project provides an automated solution for collecting real estate rental listings in Belgrade from the **Halo Oglasi** website. The script is designed to run periodically, fetch the latest listings, and save them in a structured `.tsv` format for further analysis.

## Features

* **Dynamic Scraping**: Utilizes Selenium to navigate through the website's dynamic content.
* * **Smart Filtering**: The script recognizes the publication date and automatically stops once it reaches listings older than the target date.
* **Timestamped Output**: Each scraping process generates a unique file with a timestamp (e.g., `raw_data_20260305_1502.tsv`) to prevent data overwriting.
* **Automatic Conversion**: Automatically converts the `.ipynb` notebook into a executable `.py` script before each run.

## Technologies

* **Python 3.14
* **Selenium** (Firefox WebDriver)
* **Pandas** (for data processing and export)
* **Jupyter/Nbconvert** (for notebook-to-script conversion)

## Repository Structure

    get_data.ipynb: Main development file containing the scraping logic.

    run_scraper.bat: Batch script for process execution and automation.

    raw_sample/: Directory containing sample generated data.

    requirements.txt: List of all required Python libraries.

    .gitignore: Configured to ignore temporary .py files and local datasets.

## Legal Disclaimer

This project is for **educational and research purposes only**. The developer is not responsible for any misuse of this tool. 
- **Data Usage:** The data collected is intended for personal analysis only. Do not use this tool for commercial purposes or to re-distribute data in violation of the website's Terms of Service.
- **Respectful Scraping:** This script includes delays and logic to minimize server load. Please use it responsibly.
- **IP Blocking:** Use of automated scripts may result in your IP address being temporarily or permanently blocked by the website's security systems.
   

import io
import json
import os
import tempfile
from io import BytesIO
from urllib.parse import urljoin

import requests
from playwright.sync_api import sync_playwright
import pdfplumber
import pytesseract
import PyPDF2
import re
url = "https://bip.malopolska.pl/umtarnow"
file_pattern = re.compile(r"(pdf|docx?|xls(x?)?|xml?)$", re.IGNORECASE)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Launch headless browser
    page = browser.new_page()  # Open a new page
    page.goto(url, wait_until="load")  # Wait for page load

    # Wait for the main content to load
    page.wait_for_selector("#main", timeout=5000)  # Adjust timeout if necessary
    print(page.content())
    # Extract inner text from the #main element
    nav_content = page.locator("#main").inner_text()
    print("Main Content:", nav_content)  # Print content of #main

    # Wait for the article with id 'wide' to appear
    page.wait_for_selector("article#wide", timeout=5000)  # Wait until it's present

    # Extract inner text from the article#wide
    content = page.inner_text("article#wide")
    print("Article Content:", content)  # Print the content of article#wide
    page.wait_for_selector("a", timeout=5000)
    # Close the browser
    links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(a => a.href);
            }
        """)
    print("Article Links:", links)
    # Optionally resolve relative links to absolute links

    filtered_links = [link for link in links if link.startswith(url)]
    print("Filtered Links:", filtered_links)

    sites = []
    for link in filtered_links:
        try:
            page.goto(link, wait_until="load")
            #print(page.content())
            page.wait_for_selector("article#wide", timeout=5000)  # Wait until it's present

            # Extract inner text from the article#wide
            text_content = page.inner_text("article#wide")  # Extracting main content
            #print("Text Content:", text_content)
        except:
            text_content = "Failed to retrieve content"

        sites.append({"site_url": link, "site_text": text_content})

    # Create JSON structure
    data = {"sites": sites}
    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Scraping completed. Data saved to scraped_data.json")

    pdf_links = [link for link in links if file_pattern.search(link) and link.lower().endswith('pdf')]
    doc_links = [link for link in links if
                 file_pattern.search(link) and link.lower().endswith(('doc', 'docx'))]
    excel_links = [link for link in links if
                   file_pattern.search(link) and link.lower().endswith(('xls', 'xlsx'))]
    xml_links = [link for link in links if link.lower().endswith('xml')]
    # Print the results

    print("PDF Links:", pdf_links)
    for link in pdf_links:
        response = requests.get(link)
        f = io.BytesIO(response.content)
        reader = PyPDF2.PdfReader(f)
        pages = reader.pages
        # get all pages data
        text = "".join([page.extract_text() for page in pages])
        print(text)
    print("DOC Links:", doc_links)
    print("Excel Links:", excel_links)
    print("XML Links:", xml_links)


    # Extract the PDF link from the action button



    # Close the browser

    # Close the browser
    browser.close()
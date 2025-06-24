from celery import shared_task
import requests
import pandas as pd
from docx import Document
from .extensions import db
from .models import Result
import json
import os
import pandas as pd
import requests
from playwright.sync_api import sync_playwright
from pdf2docx import Converter
from docx import Document
import pytesseract
from pdf2image import convert_from_path
import re
from lxml import etree
import datetime
file_pattern = re.compile(r"(pdf|docx?|xls(x?)?|xml?)$", re.IGNORECASE)

@shared_task
def my_task(text, schedule_name,Site_url):
    now_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("datetime module path:", datetime.__file__)
    print(now_string)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(Site_url, wait_until="load")
            page.wait_for_selector("#main", timeout=5000)
            page.wait_for_selector("article#wide", timeout=5000)
            content = page.inner_text("article#wide")
            page.wait_for_selector("a", timeout=5000)

            links = page.evaluate("""
                    () => {
                        return Array.from(document.querySelectorAll('a')).map(a => a.href);
                    }
                """)
            filtered_links = [link for link in links if link.startswith(Site_url)]
            pdf_links = [link for link in links if file_pattern.search(link) and link.lower().endswith('pdf')]
            doc_links = [link for link in links if
                         file_pattern.search(link) and link.lower().endswith(('doc', 'docx'))]
            excel_links = [link for link in links if
                           file_pattern.search(link) and link.lower().endswith(('xls', 'xlsx'))]
            xml_links = [link for link in links if link.lower().endswith('xml')]
            main_json = {
                "link-main": Site_url,
                "link": Site_url,
                "content": content,
                "typ": "WebSite",
                "timestamp": now_string,
            }
            for link in pdf_links:
                save_location = "downloaded_pdf.pdf"
                downloadFile(link, save_location)
                text = extract_text_tesseract(save_location)
                send_results_to_api([{
                    "link-main": Site_url,
                    "link": link,
                    "content": text,
                    "typ": "PDF",
                    "timestamp": now_string,
                }])

                os.remove(save_location)
            for link in doc_links:
                docx_file = "downloaded_docx.docx"
                downloadFile(link, docx_file)
                text = extract_text_from_docx(docx_file)
                Dsend_results_to_api([{
                    "link-main": Site_url,
                    "link": link,
                    "content": text,
                    "typ": "DOCX",
                    "timestamp": now_string,
                }])
                os.remove(docx_file)
            for link in excel_links:
                Excel_file = "downloaded_excel.xlsx"
                downloadFile(link, Excel_file)
                text = extract_excel_to_json_text(Excel_file)
                send_results_to_api([{
                    "link-main": Site_url,
                    "link": link,
                    "content": text,
                    "typ": "EXCEL",
                    "timestamp": now_string,
                }])
                os.remove(Excel_file)
            for link in xml_links:
                text = extract_text_from_xml(link)
                send_results_to_api([{
                    "link-main": Site_url,
                    "link": link,
                    "content": text,
                    "typ": "XML",
                    "timestamp": now_string,
                }])
            send_results_to_api(main_json)
            for link in filtered_links:
                try:
                    page.goto(link, wait_until="load")
                    page.wait_for_selector("article#wide", timeout=5000)
                    text_content = page.inner_text("article#wide")


                    send_results_to_api([{
                        "link-main": Site_url,
                        "link": link,
                        "content": text_content,
                        "typ": "WebSite",
                        "timestamp": now_string,
                    }])
                except:
                    text_content = "Failed to retrieve content"
                    send_results_to_api([{
                        "link-main": Site_url,
                        "link": link,
                        "content": text_content,
                        "typ": "WebSite",
                        "timestamp": now_string,
                    }])


    except KeyError:
        print("\nFailed to extract data from website")




def downloadFile(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
def pdf_to_docx(pdf_path, docx_path):
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])
def extract_text_from_xml(url):

    response = requests.get(url, stream=True)
    #print(response.headers['Content-Type'])
    if response.headers['Content-Type'] == 'application/xml':
        tree = etree.fromstring(response.content)

    # Convert XML to string (entire XML as a string)
        xml_string = etree.tostring(tree, encoding='unicode')
        return xml_string
    else:
        return response.text
def extract_text_tesseract(pdf_path):
    images = convert_from_path(pdf_path)  # Convert PDF pages to images
    extracted_text = ""

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang="pol")  # OCR
        extracted_text += f"\n--- Page {i+1} ---\n{text}\n"

    return extracted_text.strip()

def extract_excel_to_json_text(excel_file):
    # Read the Excel file without specifying the sheet name or columns
    df = pd.read_excel(excel_file, engine='openpyxl')  # This reads the first sheet by default

    # Convert the DataFrame to JSON format as a string
    json_text = df.to_json(orient='records', lines=True)

    # Return the JSON string
    return json_text
def send_results_to_api(results):
    """Send extracted results to the Flask API."""
    api_url = "http://differ_server:5010/diff_request"  # Change if needed
    headers = {"Content-Type": "application/json"}
    #print(results)
    try:
        response = requests.post(api_url, json=results, headers=headers)
        response.raise_for_status()
        print("Data successfully sent to results API.")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data: {e}")


# Call this function at the end of scrape_website()

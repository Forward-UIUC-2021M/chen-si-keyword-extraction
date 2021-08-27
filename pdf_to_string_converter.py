import os
import requests
from io import StringIO
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


local_filename = "download.pdf"


def convert_pdf_to_str():
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    device = TextConverter(resource_manager, return_string, codec='utf-8', laparams=LAParams())
    file = open(local_filename, 'rb')
    interpreter = PDFPageInterpreter(resource_manager, device)
    for page in PDFPage.get_pages(file, set(), maxpages=0, password="", caching=True, check_extractable=True):
        interpreter.process_page(page)
    file.close()
    device.close()
    pdf_string = return_string.getvalue()
    return_string.close()
    return pdf_string


def download_pdf_from_url(url: str):
    if "drive.google" in url:
        download_pdf_from_google_drive_url(url)
        return
    download_pdf_from_normal_url(url)


def download_pdf_from_normal_url(url: str):
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as file:
        file.write(response.content)


def download_pdf_from_google_drive_url(url: str):
    file_id = url.split('/')[5]
    url = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(url, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, local_filename)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    chunk_size = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)


def del_local_download():
    if os.path.exists(local_filename):
        os.remove(local_filename)


def pdf_to_string_wrapper(url):
    download_pdf_from_url(url)
    string = convert_pdf_to_str()
    del_local_download()
    return string

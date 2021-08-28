import os
import requests
from io import StringIO
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


local_filename = "download.pdf"


def convert_pdf_to_str():
    """
    Convert local "download.pdf" to python string
    :return: python string with content of "download.pdf"
    """
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
    """
    From given url download pdf to local
    :param url: url for pdf downloading
    :return: void
    """
    if "drive.google" in url:
        download_pdf_from_google_drive_url(url)
        return
    download_pdf_from_normal_url(url)


def download_pdf_from_normal_url(url: str):
    """
    Sub-function for condition with url that directly link to a pdf
    :param url: url for pdf downloading
    :return: void
    """
    response = requests.get(url, stream=True)
    with open(local_filename, 'wb') as file:
        file.write(response.content)


def download_pdf_from_google_drive_url(url: str):
    """
    Sub-function for condition where url is a Google Drive link
    :param url: url for pdf downloading
    :return: void
    """
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
    """
    Internal function for download_pdf_from_google_drive_url
    :param response: url request response
    :return: confirm token
    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    """
    Internal function for download_pdf_from_google_drive_url
    :param response: url request response
    :param destination: local filename for storing
    :return: void
    """
    chunk_size = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            if chunk:
                f.write(chunk)


def del_local_download():
    """
    CLean-up function for deleting local pdf file
    :return:
    """
    if os.path.exists(local_filename):
        os.remove(local_filename)


def pdf_to_string_wrapper(url):
    """
    Wrapper function for whole process of download pdf convert to string and clean-up
    :param url: url for pdf download
    :return: pdf string
    """
    download_pdf_from_url(url)
    string = convert_pdf_to_str()
    del_local_download()
    return string

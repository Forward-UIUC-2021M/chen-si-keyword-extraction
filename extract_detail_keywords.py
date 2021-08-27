import os
import requests
from bs4 import BeautifulSoup
import time
import numpy as np
import nltk
# nltk.download()
import yake
from pdf_to_string_converter import convert_pdf_to_str, download_pdf_from_url

# [1] has built-in keywords
normal_pdf_urls = ["https://www.researchgate.net/profile/Abdussalam_Alawini/publication"
                   "/325090722_Provenance_Analysis_for_Missing_Answers_and_Integrity_Repairs/links"
                   "/5af5aaec0f7e9b026bceafec/Provenance-Analysis-for-Missing-Answers-and-Integrity-Repairs.pdf",
                   "https://educationaldatamining.org/files/conferences/EDM2020/papers/paper_150.pdf",
                   "http://sites.computer.org/debull/A18mar/p27.pdf",
                   "http://sites.computer.org/debull/A18mar/p39.pdf"]

test_pdf_urls = ["https://drive.google.com/file/d/1iYsVVlMo57OENah9tc0oNJaBV02jcMqc",
                 "https://drive.google.com/file/d/1i2FWf2DwYtOsTTj79dm9ujnago4PB9Io",
                 "https://drive.google.com/file/d/1DGLaDupsKVvL04-8mdOHKxycyy114Hnj",
                 "https://drive.google.com/file/d/1hYaDnM0NnTi8kOh41jr1aUaBkZMzmvII",
                 "https://drive.google.com/file/d/1FqU_tpl_xBvLmRAcyMbTqfoWEctILO--",
                 "https://drive.google.com/file/d/1Ny9DiliMHxH_ik5VPWHwYE7zU7AkVwbD",
                 "https://drive.google.com/file/d/1BgrprdFbOEpq4MkHdm685Rdd63wlC3qw",
                 "https://drive.google.com/file/d/1eJ6bkh2kjVjxho-3u4ei4rDyQSqZRxZD",
                 "https://drive.google.com/file/d/1kzACi2rPnylLe0j5h_RpbWjApSO4VHi7",
                 "https://drive.google.com/file/d/13MThXy8DXhlx3bgrbHKDIzdc8dfvMfJu",
                 "https://drive.google.com/file/d/1BDFW4dYUxS3O_QHqqmQmSSagJy6Jmf1P",
                 "https://drive.google.com/file/d/140y2UaYncRE9vLBMDdpccn9yp_dw9Etq",
                 "https://drive.google.com/file/d/1yBf-WuRKbNJWNeF2M-EGleYrxXiQycuf"]

test_google_scholar_urls = [
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:69ZgNCALVd0C",
    "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:u5HHmVD_uO8C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:kRWSkSYxWN8C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:eQOLeE2rZwMC",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:d1gkVwhDpl0C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:u-x6o8ySG0sC",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:_B80troHkn4C",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:WF5omc3nYNoC",
    # "/citations?view_op=view_citation&hl=en&user=sugWZ6MAAAAJ&citation_for_view=sugWZ6MAAAAJ:9yKSN-GCB0IC",
    # "/citations?view_op=view_citation&hl=en&oe=ASCII&user=Kv9AbjMAAAAJ&citation_for_view=Kv9AbjMAAAAJ:31TvLzYri2IC"
]

google_scholar_prefix = "https://scholar.google.com"

local_filename = "download.pdf"


def extract_keywords_from_pdf():
    pdf_string = convert_pdf_to_str()

    language = "en"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    num_keywords = 8
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=num_keywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(pdf_string)
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)

    keywords = [keyword[0].lower() for keyword in keywords]
    keywords = sorted(keywords, key=len)

    keywords_no_repeat = []
    for keyword in keywords:
        if keyword not in keywords_no_repeat:
            if keyword[-1] == 's':
                if keyword[:-1] in keywords_no_repeat:
                    continue
            elif keyword[-2:-1] == 'es':
                if keyword[:-2] in keywords_no_repeat:
                    continue
            keywords_no_repeat.append(keyword)
    return keywords_no_repeat


def scrape_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('div', class_="gsh_csp")
    if container is None:
        # print(response.content)
        temp = soup.find('div', class_="gsc_oci_value")
        if not temp:
            return ""
        return temp.text
    return container.text


def extract_keywords_from_description(description):
    language = "en"
    max_ngram_size = 2
    deduplication_threshold = 0.9
    num_keywords = 8
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                top=num_keywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(description)
    keywords = sorted(keywords, key=lambda x: x[1], reverse=True)

    keywords = [keyword[0].lower() for keyword in keywords]
    keywords = sorted(keywords, key=len)

    keywords_no_repeat = []
    for keyword in keywords:
        if keyword not in keywords_no_repeat:
            if keyword[-1] == 's':
                if keyword[:-1] in keywords_no_repeat:
                    continue
            elif keyword[-2:-1] == 'es':
                if keyword[:-2] in keywords_no_repeat:
                    continue
            keywords_no_repeat.append(keyword)
    return keywords_no_repeat


def del_local_download():
    if os.path.exists(local_filename):
        os.remove(local_filename)


def get_pdf_link(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    container = soup.find('div', class_='gsc_oci_title_ggi')
    if container is None:
        return None
    return container.find('a', href=True)['href']


def extract_process(name, institution, urls):
    for url in urls:
        print(url)
        pdf_link = get_pdf_link(url)
        print(pdf_link)
        if pdf_link is None:
            description = scrape_description(url)
            if description == "":
                continue
            keywords = extract_keywords_from_description(description)
            print(keywords)
        else:
            download_pdf_from_url(pdf_link)
            keywords = extract_keywords_from_pdf()
            print(keywords)
            del_local_download()

        time.sleep(30*np.random.random() + 10)


def main():
    """
    input: (professor name: string, professor institution: string, paper url: string) (week 1 just have fixed urls)
    extract keywords for this paper
    and send output keywords to database (for future implementation)
    :return: void
    """

    test_prof_name = 'Kevin Chang'
    # test_prof_name = 'Jiawei Han'
    test_institution = 'University of Illinois at Urbana Champaign'

    urls = []
    for suffix in test_google_scholar_urls:
        urls.append(google_scholar_prefix + suffix)
    extract_process(test_prof_name, test_institution, urls)

import requests
from bs4 import BeautifulSoup
import time
import re
import json
import os
from tqdm import tqdm
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from collections import defaultdict
from urllib.parse import urlparse
# from serpapi import GoogleSearch
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

def scrape_linkden_profile(Cookie, search_url):
    def get_linkedin_about_url(url):
        parsed_url = urlparse(url)
        
        # Extract the base domain without country subdomains
        netloc_parts = parsed_url.netloc.split('.')
        if netloc_parts[0] == 'in':  # Handling cases like 'in.linkedin.com'
            netloc = 'linkedin.com'
        else:
            netloc = '.'.join(netloc_parts[-2:])  # Ensures 'linkedin.com'
        
        # Extract company identifier
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2 and path_parts[0] == 'company':
            company_identifier = path_parts[1]
        else:
            return None  # Invalid format, return None
        # Construct the normalized about URL
        return f'https://www.linkedin.com/company/{company_identifier}/about'

    def modify_linkden_data(linkedin_data):
        titles = linkedin_data["addons"][0]
        values = linkedin_data["addons"][1]
        for i in values:
            if "associated members" in i:
                values.remove(i)
        linkedin_data.update(dict(zip(titles, values)))
        del linkedin_data["addons"]
        return linkedin_data
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (often recommended for headless)
    options.add_argument("--no-sandbox")  # Overcome limited resource problems
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    driver = webdriver.Chrome(options = options)
    # Open LinkedIn and set the cookie
    driver.get("https://www.linkedin.com/")
    driver.set_page_load_timeout(1000)
    # Add the cookie and refresh
    driver.add_cookie({'name': 'li_at', 'value': Cookie})
    # driver.refresh()
    driver.get(search_url)
    # Wait until the section loads
    wait = WebDriverWait(driver, 15)
    company_overview = {}
    try:
        company_overview["title"] = driver.find_element(By.XPATH, "//h1[contains(@class, 'org-top-card-summary__title')]").text
    except:
        company_overview["title"] = ""
    try:
        company_overview["tagline"] = driver.find_element(By.XPATH, "//p[contains(@class, 'org-top-card-summary__tagline')]").text
    except:
        company_overview["tagline"] = ""
    try:
        company_overview["followers"] = driver.find_elements(By.XPATH, "//div[contains(@class, 'org-top-card-summary-info-list__info-item')]")[2].text
    except:
        company_overview["followers"] = ""
    try:
        company_overview["Overview"] = driver.find_element(By.CSS_SELECTOR, "p.break-words.white-space-pre-wrap.t-black--light.text-body-medium").text
    except:
        company_overview["Overview"] = ""
    try:
        # Locate the <dl> element
        dl_element = driver.find_element(By.CSS_SELECTOR, "dl.overflow-hidden")
        # Locate all `dt` (titles) and `dd` (values)
        title_elements = driver.find_elements(By.TAG_NAME, "dt")
        value_elements = driver.find_elements(By.TAG_NAME, "dd")
        titles = [title.text.strip() for title in title_elements]
        values = [value.text.strip() for value in value_elements]
        company_overview["addons"] = [titles, values]
    except:
        None
    try:
        location_element = driver.find_elements(By.CSS_SELECTOR, ".org-location-card p")
        location_text = [i.text for i in location_element]
        company_overview["addresss"] = location_text
    except Exception as e:
        company_overview["addresss"] = ""

    # Modifying the profile data
    profile = modify_linkden_data(company_overview)
    
    # Modifing the phone number
    try:
        phone = profile['Phone'].split('\n')[0].replace(" ", "")
        profile["Phone"] = phone
    except:
        None
    profile["linkedin_profile_url"] = get_linkedin_about_url(search_url)
    driver.quit()
    return profile

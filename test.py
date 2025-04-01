import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Setup options for headless Firefox
options = Options()
options.add_argument("--headless")  # Run Firefox in headless mode

# Automatically handle the download and installation of geckodriver using webdriver_manager
service = Service(GeckoDriverManager().install())

# Initialize the driver with the headless options and service
driver = webdriver.Firefox(
    options=options,
    service=service
)

# Visit the website
URL = "https://www.example.com/"
driver.get(URL)

# Output the title of the webpage (for example)
st.title("Selenium Test on Streamlit Cloud")
st.write(f"Page title: {driver.title}")

# Close the driver after usage
driver.quit()

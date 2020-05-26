import requests
import time
import re
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


company_name = []
company_website = []
job_title = []
skills = []
offer_range = []
founder_name = []


for i in range(1):
    company = result.find_element_by_css_selector('.component_21e4d.defaultLink_7325e.name_5fa89')
    co_domain = 'https://angel.co' + company.__getattribute__('href')
    co_name = company.text

    job_listing = result.find_element_by_css_selector('.component_e1eec.listings_bec22 .component_07bb9')
    job_name = []
    salary = []
    for jobs in job_listing:
        job_name.append(jobs.find_element_by_css_selector('a div .title_2148e span').text)
        salary.append(jobs.find_element_by_css_selector('a div .__halo_fontSizeMap_size--sm __halo_color_slate--900 span .salaryEstimate_b0878').text)
    job_titles = ", ".join(job_name)
    offer_ranges = ", ".join(salary)

    chrome_driver_path = 'C:\\Users\hjhar\OneDrive\Desktop\Angelist\chromedriver.exe'  # where the chrome driver is located
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get('https://angel.co/company/rotabull')
    time.sleep(60)

    website_link = driver.find_element_by_css_selector('ul .websiteLink_b71b4 a').get_attribute('href')
    website_url = website_link.replace("https://","")
    if(website_url[-1] == '/'):
        website_url = website_url.replace(website_url[-1],"")
    print(website_url)
    founders = []
    founder_list = driver.find_elements_by_css_selector('.component_64ce3')
    for founder in founder_list:
        f = founder.find_element_by_css_selector('.left_4e15a')
        if(f.find_element_by_css_selector('.byline_6c9af').text.strip() == 'Founder'):
            founders.append(f.find_element_by_css_selector('h4').text)

    links = []
    job_links = driver.find_elements_by_css_selector('.component_e6bd3')
    for job_link in job_links:
        j = job_link.find_element_by_css_selector('a').get_attribute('href')
        links.append(j)

    Skillset = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    for link in links:
        new_driver = webdriver.Chrome(chrome_driver_path, options = chrome_options)
        new_driver.get(link)
        time.sleep(60)
        skill_list = []
        Skillset = []
        try:
            skill = new_driver.find_element_by_css_selector('.skillPillTags_a7c9d')
            skill_tank = skill.find_elements_by_css_selector('a')
            for s in skill_tank :
                skill_list.append(s.text)
            Skill = "•".join(skill_list)
            Skillset.append(Skill)
        except:
            print("skills not posted for this job")
    total_skills = ", ".join(Skillset)

    for founder in founders:
        company_name.append(co_name)
        company_website.append(website_url)
        job_title.append(job_titles)
        skills.append(total_skills)
        offer_range.append(offer_ranges)
        founder_name.append(founder)

print(company_website, skills, founder_name)
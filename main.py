import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


location_name = 'CITY TO BE SEARCHED'    ######enter the city
chrome_driver_path = 'PATH WHERE THE CHROMEDRIVER IS STORED'        #update where the chrome driver is located


email = 'YOUR EMAIL'            ######login credentials
password = 'YOUR PASSWORD'

captcha_complete = 60    ################# 60 seconds to complete captcha if captcha is laid out


############### all the tags required
job_tags = ['Mobile Developer', 'Frontend Engineer', 'Backend Engineer', 'Full-Stack Engineer', 'Engineering Manager', 'QA Engineer', 'DevOps', 'Software Architect', 'Embedded Engineer', 'Data Engineer', 'Designer', 'UI/UX Designer', 'User Researcher', 'Visual Designer', 'Creative Director', 'Growth Hacker', 'Hardware Engineer', 'Mechanical Engineer', 'Systems Engineer', 'Business Analyst', 'Data Scientist', 'Product Manager', 'Project Manager']

############### to run chrome in background(can only be done when captcha is not there because captcha requires to be completed and thus can't run in background)
chrome_options = Options()
chrome_options.add_argument("--headless")


driver = webdriver.Chrome(chrome_driver_path)


driver.get('https://angel.co/login')
time.sleep(captcha_complete)                                        # COMPLETE THE CAPTCHA in this time

driver.find_element_by_id('user_email').send_keys(email)           #####sends the email
driver.find_element_by_id('user_password').send_keys(password)     ####sends password
driver.find_element_by_class_name('c-button--blue').click()

WebDriverWait(driver, 20).until(EC.url_contains('jobs'))    # wait until the login is verified and the new redirected url contains 'jobs'
time.sleep(15)

#####locationbar selecting
location_bar = driver.find_element_by_css_selector('.component_c95a1.locationField_fd9cb.hasLocations_7089d')
location_bar.click()
location = driver.find_element_by_css_selector('.locationWrapper_82304 input')
location.click()
location.send_keys(Keys.BACKSPACE)
location.send_keys(location_name)
time.sleep(15)
location.send_keys(Keys.TAB)


time.sleep(15)         #####waiting for page to load

#####searchbar selecting
searchbar = driver.find_element_by_class_name('inactive_f8e6e')
searchbar.click()
input_bar = driver.find_element_by_css_selector('.roleWrapper_bc811 input')
for i in job_tags :
   input_bar.send_keys(i)
   input_bar.send_keys(Keys.ENTER)
   time.sleep(12)

time.sleep(25)


#to scroll to the end page so that full content is loaded
scroll_pause_time = 25
last_height = driver.execute_script("return document.body.scrollHeight")
while True:        # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(scroll_pause_time)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(15)



####################  the final lists to be appended
company_name = []
company_website = []
job_title = []
skills = []
offer_range = []
founder_name = []

######   to store the job listings
result_list = []
res = driver.find_elements_by_class_name('component_4d072')         ####### targets each entry
for r in res:
    try:
        a = r.find_element_by_class_name('promoted_45ec4')
        print(a)               ###########   filter the ads
    except:
        result_list.append(r)

############### iterating through all listings present one by one
for result in result_list:
    company = result.find_element_by_css_selector('.component_32622 a')
    co_domain = company.get_attribute('href')         ############## stores co-domain
    co_name = result.find_element_by_css_selector('.component_32622 div div .component_21e4d.defaultLink_7325e.name_5fa89').text

############ finding listed jobs and repective salary
    job_listing = result.find_elements_by_css_selector('.component_e1eec.listings_bec22 .component_07bb9')
    job_name = []
    salary = []
    for jobs in job_listing:
        job_name.append(jobs.find_element_by_css_selector('.component_07bb9 a .header_0b550 .title_2148e').text)
        salary.append(jobs.find_element_by_css_selector('.component_07bb9 a .header_0b550 .__halo_fontSizeMap_size--sm span .salaryEstimate_b0878').text)
    job_titles = ", ".join(job_name)
    offer_ranges = ", ".join(salary)

    ################# extracting info from the co-domain page
    #######opening in maximized mode because then only can extract website name
    spec_options = Options()
    spec_options.add_argument("--start-maximized")

    co_driver = webdriver.Chrome(chrome_driver_path,options=spec_options)
    co_driver.get(co_domain)

    time.sleep(captcha_complete)           ######complete the captcha
    ################### changed for companies with no listed website
    try:
        website_url = co_driver.find_element_by_css_selector('ul .websiteLink_b71b4 a').text     #####company website
    except:
        website_url = ''

    founders = []
    try:
        section = co_driver.find_element_by_css_selector('.section_eb8f9')
        if section.find_element_by_css_selector('div h3').text.strip() == 'Founders':
            founder_list = section.find_elements_by_css_selector('.component_64ce3')
            for founder in founder_list:
                f = founder.find_element_by_css_selector('.left_4e15a')
                ele = f.find_element_by_css_selector('.byline_6c9af').text.strip()
                founders.append(f.find_element_by_css_selector('h4').text)
        else:
            print('Niggga')
            founder_list = section.find_elements_by_css_selector('.component_64ce3')
            for founder in founder_list:
                f = founder.find_element_by_css_selector('.left_4e15a')
                if(f.find_element_by_css_selector('.byline_6c9af').text.strip() == 'Founder'):          ######### filters out if the members listed are founders or not
                    founders.append(f.find_element_by_css_selector('h4').text)
    except:
        founders = []

##################  find the listed jobs links
    links = []
    job_links = co_driver.find_elements_by_css_selector('.component_e6bd3')
    for job_link in job_links:
        j = job_link.find_element_by_css_selector('a').get_attribute('href')
        links.append(j)
    co_driver.close()

    Skillsets = []
################# find the skills listed for jobs
    for link in links:
        new_driver = webdriver.Chrome(chrome_driver_path)
        new_driver.get(link)
        time.sleep(30)
        skill_list = []

        skill = new_driver.find_elements_by_css_selector('.skillPillTags_a7c9d .styles_component__3BR-y.styles_anchor__wiFvS')
        for s in skill:
            skill_list.append(s.text)
        Skill = "•".join(skill_list)
        Skillsets.append(Skill)
        new_driver.close()
    total_skills = ", ".join(Skillsets)



    if len(founders)==0:
        company_name.append(co_name)
        company_website.append(website_url)
        job_title.append(job_titles)
        skills.append(total_skills)
        offer_range.append(offer_ranges)
        founder_name.append('')
    else:
        for founder in founders:
            company_name.append(co_name)
            company_website.append(website_url)
            job_title.append(job_titles)
            skills.append(total_skills)
            offer_range.append(offer_ranges)
            founder_name.append(founder)

driver.close()
df = pd.DataFrame({'Company Name': company_name, 'Web Link': company_website, 'Job Titles':job_title, 'Skills Required':skills, 'Offer Range':offer_range, 'Founder':founder_name})
df.to_excel(location_name+'.xlsx',index=False)






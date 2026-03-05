#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import time
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[3]:


options = webdriver.FirefoxOptions()

options.add_argument("--headless")
options.add_argument("--no-sandbox")

driver = webdriver.Firefox(options=options)
driver.get('https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd')
driver.implicitly_wait(2)


# ### Date Setup

# Enter date of your desired postings to scrape - change `timedelta()` days value

# In[4]:


todays_date_str = datetime.today().strftime('%d.%m.%Y.')
print(f'Today: {todays_date_str}')
posting_date = datetime.today() - timedelta(days=1)
posting_date_str = posting_date.strftime('%d.%m.%Y.')
print(f'Scraping date:{posting_date_str}')

if datetime.strptime(todays_date_str,'%d.%m.%Y.') < datetime.strptime(posting_date_str,'%d.%m.%Y.'):
    raise Exception("Sorry, posting date must be before or same as today.")


# ### Get list of links from today

# In[5]:


driver.get('https://www.halooglasi.com/nekretnine/izdavanje-stanova/beograd')


# In[6]:


def get_todays_links(target_date_str):
    posting_links = []
    page = 1
    while True:
        print(f"Traversing page {page}...", end='\r')

        cards = driver.find_elements(By.CLASS_NAME, 'product-list-item')
        time.sleep(0.5)

        page_dates = []
        for card in cards:
            try:
                publish_date = card.find_element(By.CLASS_NAME, 'publish-date').text
                if publish_date == target_date_str:
                    link = card.find_element(By.CSS_SELECTOR, '.product-title a').get_attribute('href')
                    posting_links.append(link)
                page_dates.append(publish_date)
            except Exception:
                continue

        last_date_on_page = datetime.strptime(page_dates[-1], '%d.%m.%Y.')
        target_date = datetime.strptime(target_date_str, '%d.%m.%Y.')

        if last_date_on_page < target_date:
            print(f"\nReached older postings on page {page}. Stopping.")
            break
        try:
            time.sleep(0.5)
            next_btn = driver.find_element(By.CLASS_NAME, 'page-link.next')
            next_btn.click()
            page += 1
            time.sleep(0.5)
        except:
            break
    return list(set(posting_links))


# In[7]:


posting_links = get_todays_links(posting_date_str)


# #### Number of postings today

# In[8]:


# print(f'Traversed {page} pages')
print(f'There are {len(posting_links)} postings for specified date: {posting_date_str}')


# ### Get Data for One Posting Function

# In[9]:


def get_posting_data(posting_link):
    driver.get(posting_link)
    time.sleep(2)
    id_map = {
        'Title': 'plh1', 'Price': 'plh6', 'City': 'plh2', 'Location': 'plh3', 
        'Microlocation': 'plh4', 'Street': 'plh5',  'Type': 'plh10', 'Area': 'plh11',
        'Rooms': 'plh12', 'Poster': 'plh13', 'Heating': 'plh17', 'Furnished': 'plh16',
        'Floor': 'plh18','FloorTotal': 'plh19', 'PaymentType': 'plh21',
        'Description': 'plh51', 'PostingId': 'plh77', 'PostingDate': 'plh81'
    }
    # Posting data (excluding Additional and Other tags)
    data = {}
    for key, element_id in id_map.items():
        try:
            val = driver.find_element(By.ID, element_id).text
            if key == 'Description':
                val = val.replace('\t', ' ').replace('\n', ' ')
            data[key] = val
        except:
            data[key] = None
    # Additional and Other tags
    for key, x_id in {'Additional': 'tabTopHeader1', 'Other': 'tabTopHeader2'}.items():
        try:
            items = driver.find_element(By.ID, x_id).text.split('\n')
            data[key] = [i for i in items if i not in ['Dodatno', 'Ostalo']]
        except:
            data[key] = None
    return data


# ### Get data for all Postings from today

# In[10]:


posting_columns = [
    'Title', 'Price', 'City', 'Location', 'Microlocation', 'Street','Type', 'Area', 'Rooms', 'Poster', 'Heating', 'Furnished',
    'Floor','FloorTotal','PaymentType', 'Additional', 'Other', 'Description', 'PostingId', 'PostingDate'
]
list_postings = []
for link in posting_links:
    posting = get_posting_data(link)
    list_postings.append(posting)
    print(f'Added: {len(list_postings)} postings to df_postings', end='\r')
df_postings = pd.DataFrame(list_postings, columns=posting_columns)


# In[11]:


df_postings_clean = df_postings.copy()
df_postings_clean['Description'] = df_postings_clean['Description'].str.replace('\n',' ')


# In[ ]:


output_dir = rf'raw/{posting_date.strftime("%Y-%m-%d")}'
os.makedirs(output_dir, exist_ok=True)
# Creating TAB separated csv file to account for Description column
df_postings_clean.to_csv(f'{output_dir}/data.tsv', index=False, sep='\t')


# In[13]:


driver.quit()


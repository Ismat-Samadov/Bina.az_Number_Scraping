%%time
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


def extract_price(link_soup):
    price_div = link_soup.find('div', class_='product-price__i product-price__i--bold')
    if price_div:
        price_val = price_div.find('span', class_='price-val')
        price_cur = price_div.find('span', class_='price-cur')
        if price_val and price_cur:
            price = re.sub(r'\s+', '', price_val.text.strip())  # Remove whitespace from the price value
            currency = price_cur.text.strip()
            return price, currency
    return None, None

def extract_owner_category(link_soup):
    owner_category_div = link_soup.find('div', class_='product-owner__info-region')
    if owner_category_div:
        owner_category = owner_category_div.text.strip()
        return owner_category
    else:
        return None 

def extract_owner_name(link_soup):
    owner_name_div = link_soup.find('div', class_='product-owner__info-name')
    if owner_name_div:
        owner_name = owner_name_div.text.strip()
        return owner_name
    else:
        return None

def extract_phone_number(link_soup):
    phone_number_div = link_soup.find('div', class_='product-phones__list-i')
    phone_number_a = phone_number_div.find('a') if phone_number_div else None
    phone_number = phone_number_a['href'].replace('tel:', '').replace('-', '').replace(' ', '') if phone_number_a else None
    return phone_number

def extract_category(link_soup):
    category_div = link_soup.find('div', class_='product-properties__i').find('span', class_='product-properties__i-value')
    if category_div:
        category = category_div.text.strip()
        return category
    else:
        return None

def extract_floor(link_soup):
    floor_div = link_soup.findAll('div', class_='product-properties__i')[1].find('span', class_='product-properties__i-value')
    if floor_div:
        floor = floor_div.text.strip()
        return floor
    else:
        return None

def extract_area(link_soup):
    area_div = link_soup.findAll('div', class_='product-properties__i')[2].find('span', class_='product-properties__i-value')
    if area_div:
        area = area_div.text.strip()
        return area
    else:
        return None

def extract_room_count(link_soup):
    room_count_div = link_soup.findAll('div', class_='product-properties__i')[3].find('span', class_='product-properties__i-value')
    if room_count_div:
        room_count = room_count_div.text.strip()
        return room_count
    else:
        return None

def extract_description(link_soup):
    description_div = link_soup.findAll('div', class_='product-properties__i')[4].find('span', class_='product-properties__i-value')
    if description_div:
        description = description_div.text.strip()
        return description
    else:
        return None

def extract_mortgage(link_soup):
    mortgage_div = link_soup.findAll('div', class_='product-properties__i')[5].find('span', class_='product-properties__i-value')
    if mortgage_div:
        mortgage = mortgage_div.text.strip()
        return mortgage
    else:
        return None


    
    
# Last function    
    
def extract_property_info(url):
    # Chrome settings
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run Chrome WebDriver in headless mode
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)
    time.sleep(2)

    # Wait for the phone number element to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-phones__btn-value')))

    # Find the element using XPath
    element = driver.find_element(By.CLASS_NAME, 'product-phones__btn-value')
    element.click()   # Click the button

    # Wait for the updated phone number element to be present
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-phones__list-i')))

    # Get the updated HTML after clicking the button
    updated_html = driver.page_source

    # Parse the updated HTML
    link_soup = BeautifulSoup(updated_html, 'html.parser')

    # Extract the full phone number
    phone_number_a = link_soup.find('div', class_='product-phones__list-i').find('a')
    phone_number = phone_number_a['href'].replace('tel:', '').replace('-', '').replace(' ', '') if phone_number_a else None

    # Extract the owner name
    owner_name = extract_owner_name(link_soup)

    # Extract the owner category
    owner_category = extract_owner_category(link_soup)

    # Extract other information
    category = extract_category(link_soup)
    floor = extract_floor(link_soup)
    area = extract_area(link_soup)
    room_count = extract_room_count(link_soup)
    description = extract_description(link_soup)
    mortgage = extract_mortgage(link_soup)
    price, currency = extract_price(link_soup)


    driver.quit()  # Close the WebDriver

    # Create a DataFrame with the extracted information
    data = {
        'url': [url],
        'phone number': [phone_number],
        'owner name': [owner_name],
        'owner category': [owner_category],
        'category': [category],
        'floor': [floor],
        'area': [area],
        'room count': [room_count],
        'description': [description],
        'mortgage': [mortgage],
        'price': [price],
        'currency': [currency]
    }
    df = pd.DataFrame(data)
    return df



# Example usage:
url = 'https://bina.az/items/3601047'
df = extract_property_info(url)
df
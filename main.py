import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

target_name = 'weston'
total_pages = 43
page_num = 0
search_url = "https://classifieds.ksl.com/search/Home-and-Garden/Electrical/page/{}".format(page_num)
listing_base_url = "https://classifieds.ksl.com"

driver = webdriver.Firefox()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/89.0.4389.82 Safari/537.36"
}


def get_name(s):
    start_of_name = s[9:]
    return start_of_name.split('\n')[0]  # removes everything after the /n


while total_pages <= total_pages:
    response = requests.get(search_url, headers=headers)
    page_num += 1
    soup = BeautifulSoup(response.content, "html.parser")
    search_results = soup.find(id='search-results')
    normal_listings = search_results.contents[0].contents[1].contents
    for listing in normal_listings:
        link_element = listing.find('a')
        if link_element == -1:
            continue

        link = link_element['href']
        listing_url = listing_base_url + link

        driver.get(listing_url)
        listing_container = driver.find_element(By.ID, "listingContainer")
        name = get_name(listing_container.text).lower()
        if name == target_name:
            print(link)

        time.sleep(random.randint(5, 15))
    time.sleep(random.randint(5, 15))

driver.quit()

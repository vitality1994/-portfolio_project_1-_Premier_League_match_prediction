from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time



url = "https://fminside.net/players"

browser = webdriver.Chrome('/Users/jooyong/Downloads/chromedriver-mac-x64/chromedriver') 
browser.set_script_timeout(30)
browser.get(url)



# html = browser.page_source
# soup = BeautifulSoup(html, 'html.parser')

# for ad in soup.select('.ad'):
#     ad.decompose()

# modified_html = str(soup)
# browser.execute_script(f"document.documentElement.innerHTML = {modified_html!r}")

browser.maximize_window()

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

modified_html = str(soup)
browser.execute_script(f"document.documentElement.innerHTML = {modified_html!r}")


# search_box = browser.find_element(By.XPATH, '//*[@id="sidebar"]/div[2]/form/div[1]/select/option[2]')
# search_box.click()
browser.execute_script("window.scrollTo(0, 500)")
# browser.find_element(By.XPATH, '//*[@id="ccc-close"]').click()
my_btn = browser.find_element(By.XPATH, '//*[@id="sidebar"]/div[2]/form/div[1]/select/option[2]')
my_btn.click()

time.sleep(7)

search_box = browser.find_element(By.XPATH, '//*[@id="sidebar"]/div[2]/form/div[6]/input')
search_box.send_keys("Premier League")
search_box.send_keys(Keys.RETURN)



for i in range(20):
    print('# of loads:',i+1)
    
    # Scroll down
    # time.sleep(0.5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(7)
    browser.execute_script("window.scrollBy(0, -600)")
    # Extract html include info of players
    time.sleep(7)
    
    my_btn = browser.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[3]/div/div/div[3]/a')
    my_btn.click()

    time.sleep(10)

html = browser.page_source
source = BeautifulSoup(html, 'lxml')

# Extract urls for players
list_temp = list(source.find_all('span', class_='name'))
list_links = []
for i in range(len(list_temp)):
    list_links.append("https://fminside.net"+list_temp[i].find('a')['href'])


# Make text file include all urls
# These urls will be used for 'Scrapy' to scraped players' game attributes
f = open('/Users/jooyong/github_locals/portfolio_project_1_Premier_League_match_prediction/fm_inside/data/player_FM_links_2024_1.txt', 'w')
for i in range(len(list_links)):
    f.write(list_links[i])
    f.write("\n")

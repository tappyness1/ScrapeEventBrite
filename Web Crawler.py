import urllib.request
import csv
from selenium import webdriver
import getpass
import time
from selenium.webdriver.support.ui import Select
import os
from selenium.webdriver.common.keys import Keys

#pw = getpass.getpass()

chrome_path = r"C:\Users\A101234\OneDrive - Singapore Institute Of Technology\01. IR - Institutional Research\77. Code for Analysis\chromedriver.exe" # need to change this

driver = webdriver.Chrome(chrome_path)
url = 'https://www.eventbrite.com/'
driver.get(url)
driver.find_element_by_class_name('eds-show-up-md').click()
time.sleep(1)


driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/main/section/main/header/section/div[3]/div[2]/button').click()
time.sleep(1)
select_fr = Select(driver.find_element_by_id("format-select"))
select_fr.select_by_visible_text('Conference')

select_fr = Select(driver.find_element_by_id("price-select"))
select_fr.select_by_visible_text('Paid')

driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/aside/div[2]/div/div/div[2]/div/div[2]/button').click()

time.sleep(2)

dict1 = {}
dictnum = 0
for num in range(30):
    try:
        items = driver.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/div/main/section/main/main/div[1]/div[1]/div[1]/div/section/ul/li')

        for item in items:
            try:
                elem = item.find_element_by_class_name('eds-media-card-content__action-link')
                link = elem.get_attribute('href')
                driver.execute_script("window.open('');")
                time.sleep(1)
                # Switch to the new window
                driver.switch_to.window(driver.window_handles[1])
                driver.get(link)
                time.sleep(2)
                event_name = driver.find_element_by_class_name('listing-hero-title').text
                #print (event_name)
                ticket_price = driver.find_element_by_class_name('js-display-price').text
                #print (ticket_price)
                event_details = driver.find_elements_by_class_name('event-details__data')
                EventDetails = []
                for i in event_details:
                    if i.text ==  '':
                        pass
                    else:
                        EventDetails.append(i.text)
    
                dict1[dictnum] = {'Event Name': event_name, 
                     'Event Date': EventDetails[0],
                     'Event Location': EventDetails[1],
                     'Link': link
                     }
                dictnum += 1
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
            except:
                driver.close()
                driver.switch_to_window(driver.window_handles[0])
                pass
    except:
        pass
    time.sleep(2)
    try:
        if num == 0:
            driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/main/section/main/footer/div/div[1]/div/div[4]/a').click()
        else:
            driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/main/section/main/footer/div/div[1]/div/div[5]/a').click()
    except:
        print ("No more pages")
        break
    time.sleep(2)
    
data = pd.DataFrame.from_dict(dict1, orient = 'index')

data['Event Date'] = data['Event Date'].str.replace('\n', ' ')
data['Event Date'] = data['Event Date'].str.replace('Add to Calendar', '')
data['Event Date'] = data['Event Date'].str.strip()

data['Event Location'] = data['Event Location'].str.replace('\n', ' ')
data['Event Location'] = data['Event Location'].str.replace('View Map', '')
data['Event Location'] = data['Event Location'].str.strip()

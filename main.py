## Importing libraries
import pandas as pd
import requests, re, time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver



## Updating chromedriver.
from webdriver_auto_update.webdriver_auto_update import WebdriverAutoUpdate
driver_manager = WebdriverAutoUpdate("./")
driver_manager.main()





def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=chrome_options)
    return driver





driver = get_chromedriver()





statesList = []
driver.get("https://www.americandentistsociety.com/massachusetts-50-top-dentists")
soup = BeautifulSoup(driver.page_source, 'html.parser')
states = soup.find_all('p', {'class': 'font_7 wixui-rich-text__text'})
for state in states:
    try:
        link = state.find("a")["href"]
        statesList.append(link)
        print(link)
    except:
        pass



data = {
    'doctor_name': [],
    'clinic_name': [],
    'address': [],
    'phone': [],
    'mail': []
}

for state in statesList[0:1]:
    peopleList = []
    for i in range(5):
        try:
            driver.get(f"{state}?page={i}")
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            people = soup.find_all('a', {'data-hook': 'product-item-container'})
            for person in people:
                if person["href"] not in peopleList:
                    print(person["href"])
                    peopleList.append(person["href"])
        except:
            pass
        for person in peopleList:
            try:
                driver.get(person)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                name = soup.find("h1", {"data-hook": "product-title"}).text.split("-")[0]
                text = soup.find("pre", {"data-hook":"description"})
                allText = text.get_text(separator='\n').split("\n")
                # print(allText)
                for line in allText:
                    # print(line)
                    if line.lower().startswith("contact info"):
                        index_ = allText.index(line)
                        clinicName = allText[index_+1]
                        address = allText[index_+2] +""+ allText[index_+3]
                        phone = allText[index_+4]
                        mail = None
                        if "@" in allText[index_+5]:
                            mail = allText[index_+5]
                            
                print("Doctor Name:", name)
                print("Clinic Name:", clinicName)
                print("Address:", address)
                print("Phone:", phone)
                print("Mail:", mail)
                new_data = {
                        'doctor_name': name,
                        'clinic_name': clinicName,
                        'address': address,
                        'phone': phone,
                        'mail': mail
                    }
                for key, value in new_data.items():
                    data[key].append(value)
                print("-"*50)
                time.sleep(0.1)
            except Exception as e:
                print(e)
                pass
driver.quit()
df = pd.DataFrame(data)
excel_file_path = 'doctors_data.xlsx'

# Save the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

print(f'Data saved to {excel_file_path}')
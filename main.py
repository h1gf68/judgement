import requests
import json
import csv
import os
import time
from selenium import webdriver
import undetected_chromedriver as uc

def get_cookies(url):
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.binary_location = '/usr/bin/google-chrome'
    service = webdriver.ChromeService(executable_path=os.getcwd() + '/chromedriver')
    try:
        browser = uc.Chrome(service=service, options=options)
        # browser.minimize_window()
        browser.get(url)
        time.sleep(3)
        pr_fp = browser.get_cookie("pr_fp").get("value")
        wasm = browser.get_cookie("wasm").get("value")
    except Exception as ex:
        print(ex)
    finally:
        browser.quit()

    return pr_fp, wasm


def get_data(id, pr_fp, wasm):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://kad.arbitr.ru/Card/392979bd-774a-4661-8eed-fa2c3fc5ba72",
        "Cookie": "pr_fp=" + pr_fp + "; wasm=" + wasm + ";",
    }

    count = 1
    page = 1
    # with open(f"{id}")
    while page < 2:
        url = f'https://kad.arbitr.ru/Kad/CaseDocumentsPage?&caseId={id}&page={page}'
        response = requests.get(url, headers=headers)
        json_object = json.loads(response.text)
        for item in json_object["Result"]["Items"]:
            url_doc = f"https://kad.arbitr.ru/Document/Pdf/{ item['CaseId'] }/{ item['Id'] }/{ item['FileName'] }"
            judges = [judge["Name"] for judge in item["Judges"]]
            date_ = item["DisplayDate"]
            court = item["CourtName"]
            print(date_, court, ", ".join(judges), url_doc)

        count = json_object["Result"]["Count"]
        page += 1




def main():

    url = 'https://kad.arbitr.ru/Card/392979bd-774a-4661-8eed-fa2c3fc5ba72'
    pr_fp, wasm = get_cookies(url)

    id = url.split("/")[-1]
    get_data(id, pr_fp, wasm)







if __name__ == '__main__':
    main()



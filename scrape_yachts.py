import argparse
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


next_page = "/html/body/main/section[6]/div/div/div/header/div[2]/div/ul/li[10]/a"


def get_yachts(soup):
    results = []
    yachts = soup.find_all(class_="ais-Hits-item")
    for yacht in yachts:
        y = {}
        title = yacht.find("p", class_="title")
        price = yacht.find("p", class_="price")
        if title and price:
            y["title"] = title.text
            y["price"] = price.text
            results.append(y)
    return results


def main(args):
    start_page = args.website
    driver = webdriver.Firefox()
    driver.get(start_page)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    max_page = 48
    page_number = 1
    try:
        page_results = {}
        while page_number<=max_page:
            element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, next_page)))
            driver.execute_script("arguments[0].click();", element)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            page_results[str(page_number)] = get_yachts(soup)
            page_number += 1
    except:
        print(f"error on page {page_number}")
    finally:
        driver.quit()
        with open("yacht_result.json", "w") as _file:
            _file.write(json.dumps(page_results, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a website.')
    parser.add_argument("-s", "--website", type=str,
                    help='enter client website request')
    args = parser.parse_args()
    main(args)

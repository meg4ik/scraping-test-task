import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def get_data():
    url = "https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A281407&ref=nav_em_na"
    headers = {
        'Content-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
    }
    req = requests.get(url, headers=headers)
    
    with open("amazon_page.html", "w", encoding="utf-8") as file:
        file.write(req.text)

def save_data(data):
    data_folder = 'parsed_data'
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    df = pd.DataFrame(data)

    date = datetime.now().strftime("%Y_%m_%d")

    excel_file_name = os.path.join(data_folder ,f'Amazon_parsed_data_{date}.xlsx')

    df.to_excel(excel_file_name, index=False)

def parse_script(soup_obj):
    data = {
        "Name":[],
        "Price":[],
        "Description":[],
        "Page link":[],
        "Image link":[]
    }

    all_products = soup_obj.find_all(class_="s-widget-spacing-small", limit=20)

    for item in all_products:
        product = item.find('div').find('div').find('div').find('div')
        product_links = product.find(class_="s-product-image-container").find('span')

        product_href = f"https://www.amazon.com/{product_links.find('a').get('href')}"
        data["Page link"].append(product_href)

        product_src = product_links.find("div").find("img").get("src")
        data["Image link"].append(product_src)

        product_name = product.find(class_="s-title-instructions-style").find('a')
        data["Name"].append([product_name.get_text() if product_name else ""][0])


        data["Name"].append("")
        data["Price"].append("")

    return data

def main():
    if not os.path.exists("amazon_page.html"):
        get_data()

    with open("amazon_page.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    parsed_data = parse_script(soup)

    # save_data(parsed_data)

if __name__ == "__main__":
    main()

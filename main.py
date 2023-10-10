import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

HEADERS = {
        'Content-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
    }


def get_data():
    url = "https://www.amazon.com/s?i=specialty-aps&bbn=16225009011&rh=n%3A%2116225009011%2Cn%3A281407&ref=nav_em_na"
    
    req = requests.get(url, headers=HEADERS)
    
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
    try:
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

            #Price

            price = ''

            product_price = product.find(class_="s-price-instructions-style")
            if product_price:
                product_price = product_price.find("a").find_all("span", class_="a-price")
                
                whole_price = product_price[0].find(class_="a-price-whole").text
                decimal_price = product_price[0].find(class_="a-price-fraction").text
                price_symbol = product_price[0].find(class_="a-price-symbol").text
                price += f"{whole_price}{decimal_price}{price_symbol}"

                if len(product_price) == 2:
                    second_whole_price = product_price[1].find(class_="a-price-whole")
                    second_decimal_price = product_price[1].find(class_="a-price-fraction")
                    second_price_symbol = product_price[1].find(class_="a-price-symbol")
                    if second_whole_price and second_decimal_price and second_price_symbol:
                        price += f" - {second_whole_price.text}{second_decimal_price.text}{second_price_symbol.text}"

            data["Price"].append(price)

            #Description

            req = requests.get("https://www.amazon.com/Maxell-High-Quality-Headphones-Adjustable-Lightweight/dp/B00006JPRN/ref=sr_1_2_mod_primary_new?qid=1696971715&s=electronics&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D&sr=1-2", HEADERS)

            page_name = product_href.split("//")[2].split("/")[0]

            with open(f"{page_name}.html", "w") as file:
                file.write(req.text)

            data["Description"].append('')

            
    except Exception as e:
        print(e)



    return data

def main():
    if not os.path.exists("amazon_page.html"):
        get_data()

    with open("amazon_page.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    parsed_data = parse_script(soup)

    print(parsed_data)

    # save_data(parsed_data)

if __name__ == "__main__":
    main()

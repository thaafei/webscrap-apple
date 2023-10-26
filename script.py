from bs4 import BeautifulSoup
import requests


url ="https://www.apple.com/ca_edu_93120/shop/refurbished/mac" 
page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")
item_div = soup.find("div","rf-refurb-category-grid-no-js")
item_links = item_div.find_all("li")

for item in item_links:
    item_link = item.find("a")
    current_price = item.find("div","as-price-currentprice as-producttile-currentprice")
    print("------------")
    print(item_link.text.encode("utf-8"))
    print(current_price.text.encode("utf-8"))
    print("------------")
from bs4 import BeautifulSoup
import requests
import pandas as pd


url ="https://www.apple.com/ca_edu_93120/shop/refurbished/mac" 
page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")
item_div = soup.find("div","rf-refurb-category-grid-no-js")
item_links = item_div.find_all("li")

df = pd.DataFrame(columns = ['name','price','link'])
for item in item_links:
    name = item.find("a")
    link = name['href']
    current_price = item.find("div", "as-price-currentprice as-producttile-currentprice")
    # print("------------")
    # print(name.text.encode("utf-8"))
    # print(link)
    # print(current_price.string.encode("utf-8"))
    # print("------------")
    new_row = {'name': name.text.encode("utf-8"), 'price':current_price.string.encode("utf-8"), 'link': link}
    df= df._append(new_row, ignore_index = True)
df
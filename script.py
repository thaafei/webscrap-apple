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
    
    #cleaning up 
    name = str(name.text.encode("utf-8"))
    if "MacBook" in name:
        name = name.split("b'")[1]
        new_row = {'name': name, 'price':str(current_price.string.encode("utf-8")), 'link': link}
        df= df._append(new_row, ignore_index = True)
print(df)
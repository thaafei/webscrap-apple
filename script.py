from bs4 import BeautifulSoup
import requests


url ="https://www.apple.com/ca_edu_93120/shop/refurbished/mac" 
page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")
item_div = soup.find("div","rf-refurb-category-grid-no-js")
item_links = item_div.find_all("li")

for item in item_links:
    
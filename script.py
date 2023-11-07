from bs4 import BeautifulSoup
import requests
import pandas as pd
import threading
import sqlite3 as sql


class Worker(Thread):
    def __init__(self,list,start,end):
        super().__init__();
        self.list = list
        self.start = start
        self.end = end
    def run(self):
        for i in range(self.start,self.end):
            name = list.content[i].find("a")
            link = name['href']
            name = str(name.text.encode("utf-8"))
            if "MacBook" in name:
                current_price = item.find("div", "as-price-currentprice as-producttile-currentprice")
                #cleaning up
                price = str(current_price.string.encode("utf-8")).split("$")[1].split(".")[0]
                name = name.split("b'")[1]
                link = "https://www.apple.com"+link
                additional_info = get_laptop_info(link)
                new_row = {'name': name, 'price': price, 'link': link,'year': additional_info[0],'ram': additional_info[1],'storage':additional_info[2]}
                df= df._append(new_row, ignore_index = True)
                print(i)


def get_laptop_info(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    overview = soup.find("div", "rc-pdsection-panel Overview-panel row").select_one(":nth-child(2)")
    if not overview:
        return None

    result = [item.get_text(strip=True) for item in overview.find_all("div")]

    year = result[0].split()[-2] + " " + result[0].split()[-1]
    ram = result[2].split()[0]
    storage = result[3].split()[0]
    return [year, ram, storage]
def create_connection():
    con = sql.connect("products.sqlite")
    cur = con.cursor()
    cur.execute("CREATE TABLE item(name, price, year, ram,storage,link, id)")
    con.commit()
    con.close()

def main():
    url ="https://www.apple.com/ca_edu_93120/shop/refurbished/mac" 
    page = requests.get(url)

    soup = BeautifulSoup(page.content,"html.parser")
    item_div = soup.find("div","rf-refurb-category-grid-no-js")
    item_links = item_div.find_all("li")
    
    #create database
    create_table()

    #df = pd.DataFrame(columns = ['name','price','link','year', 'ram','storage'])
    for item in item_links:
        name = item.find("a")
        link = name['href']
        name = str(name.text.encode("utf-8"))
        if "MacBook" in name:
            current_price = item.find("div", "as-price-currentprice as-producttile-currentprice")
            #cleaning up
            price = str(current_price.string.encode("utf-8")).split("$")[1].split(".")[0]
            name = name.split("b'")[1]
            link = "https://www.apple.com"+link
            additional_info = get_laptop_info(link)
            new_row = {'name': name, 'price': price, 'link': link,'year': additional_info[0],'ram': additional_info[1],'storage':additional_info[2]}
            #df= df._append(new_row, ignore_index = True)
            print(i)
            i+=1
    #print("outputting to excel")
    #df.to_excel('text.xlsx',sheet_name='sheet1',index=False)

main()
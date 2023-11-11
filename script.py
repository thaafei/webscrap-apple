from bs4 import BeautifulSoup
import requests
import sqlite3 as sql


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
    return con,con.cursor()

def initial():
    con = sql.connect("products.sqlite")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS macbook
                  (id VARCHAR PRIMARY KEY, name TEXT, link TEXT, price INTEGER, year INTEGER, ram INTEGER, storage INTEGER)''')
    con.commit()

def main():
    url ="https://www.apple.com/ca_edu_93120/shop/refurbished/mac" 
    page = requests.get(url)

    soup = BeautifulSoup(page.content,"html.parser")
    item_div = soup.find("div","rf-refurb-category-grid-no-js")
    item_links = item_div.find_all("li")
    
    #create database
    con, cur = create_connection()

    #df = pd.DataFrame(columns = ['name','price','link','year', 'ram','storage'])
    for item in item_links:
        name = item.find("a")
        link = name['href']
        id = link.split("/")[4]
        name = str(name.text.encode("utf-8"))
        if "MacBook" in name:
            print (id)
            current_price = item.find("div", "as-price-currentprice as-producttile-currentprice")
            #cleaning up
            price = str(current_price.string.encode("utf-8")).split("$")[1].split(".")[0]
            name = name.split("b'")[1]
            link = "https://www.apple.com"+link
            additional_info = get_laptop_info(link)
            
            try:
                cur.execute("INSERT INTO macbook (id, name, link, price,year, ram, storage) VALUES (?, ?, ?, ?, ?, ?,?)",(id, name, link, price, additional_info[0], additional_info[1], additional_info[2]))
            except sql.IntegrityError:
                # Handle the case where the ID already exists (unique constraint violation)
                print("Skipping insertion due to existing ID.")
            con.commit()

initial()
main()

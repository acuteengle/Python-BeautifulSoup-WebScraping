import bs4 #pip install BeautifulSoup4
from bs4 import BeautifulSoup
import requests
import csv

def parsePrice(stockSymbol):
    page = requests.get("https://finance.yahoo.com/quote/"
    + stockSymbol)
    soup = BeautifulSoup(page.content, "html.parser")
    # print(soup.prettify())
    price = soup.find_all(class_="Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)")[0].text
    change = soup.find_all(class_="Trsdu(0.3s) Fw(500) Fz(14px) C($positiveColor)")[0].text
    return {
        "price": price,
        "change": change
    }

symbols = ["SWPPX", "FXAIX", "WDAY"]

# https://www.programiz.com/python-programming/csv
with open('stocks.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(["Symbol", "Price", "Change"])
    for s in symbols:
        values = parsePrice(s)
        print(s + ": " + values['price'] + " " + values['change'])
        writer.writerow([s, values['price'], values['change']])
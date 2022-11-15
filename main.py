import requests
import csv
import time
from bs4 import BeautifulSoup


def extract_information_book(url, type_information):
    page = requests.get(url)
    html = BeautifulSoup(page.content, "html.parser")
    list_extrat = []
    article = html.find_all(class_="product_pod")

    if type_information == 'title':
        for title in article:
            h3 = title.find("h3").find("a")
            list_extrat.append(h3['title'])
            
    elif type_information == 'price':
        for price in article:
            balise_price = price.find(class_="price_color")
            list_extrat.append(balise_price.string)
            
    elif type_information == 'image':
        for image in article:
            balise_price = image.find(class_="image_container").find("img")
            list_extrat.append(balise_price['src'])
            
    elif type_information == 'page':
        list_page = html.find(class_="nav-list").find_all("a")
        list_extrat = {}
        for page in list_page:
            list_extrat[page.string.strip()] = page["href"]
                 
    print(list_extrat)
    return list_extrat

def save_in_csv(list_image, list_price, list_title, name_file):
    date = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
    header = ["title", "price", "image"]
    destination_csv = "./CSV/" + name_file + '_' + date + ".csv" 
    with open(destination_csv, "w") as fichier_CSV:
        writer = csv.writer(fichier_CSV, delimiter=",")
        writer.writerow(header)
        
        for title, price, image in zip(list_title, list_price, list_image):
            ligne = [title, price, image]
            writer.writerow(ligne)
    
def main():
    page = extract_information_book("http://books.toscrape.com/index.html", "page")
    i = 0
    for title_page, url in page.items():
        print(i, title_page)
        i += 1
        
    print("Sélectionner le chiffre du thème que vous voulez !")    
    selection = int(input())
    ii = 0
    if selection > i or selection < 0:
        main()
    else:
        for title_page, url in page.items():
            if ii == selection:
                print(url)
                break
            ii += 1

    
""" title = extract_information_book("http://books.toscrape.com/index.html", "title")
price = extract_information_book("http://books.toscrape.com/index.html", "price")
image = extract_information_book("http://books.toscrape.com/index.html", "image")
save_in_csv(image, price, title, "date") 
extract_information_book("http://books.toscrape.com/index.html", "page")"""

main()
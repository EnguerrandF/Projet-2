import requests
import csv
import time
from bs4 import BeautifulSoup

class Scrap:
        
    def __init__(self, url_home_page):
        self.url_home_page = url_home_page
        
    def take_url_and_category_page(self):
        page = requests.get(self.url_home_page)
        html = BeautifulSoup(page.content, "html.parser")
        list_page = html.find(class_="nav-list").find_all("a")
        list_extrat = {}
        
        for page in list_page:
            list_extrat[page.string.strip()] = "http://books.toscrape.com/" + page["href"]
            
        return list_extrat
        
    def take_url_book_page(self, url_of_the_page, list_urls_book_page):
        page = requests.get(url_of_the_page)
        html = BeautifulSoup(page.content, "html.parser")
        balise = html.find_all("h3")

        if url_of_the_page[0:52] == "http://books.toscrape.com/catalogue/category/books_1":
            for element in balise:
                url = element.find("a")["href"]
                list_urls_book_page.append("http://books.toscrape.com/catalogue/" + url[6:])
                #print("http://books.toscrape.com/catalogue/" + url[6:])
        else:
            for element in balise:
                url = element.find("a")["href"]
                list_urls_book_page.append("http://books.toscrape.com/catalogue/" + url[9:])

        try:
            var = html.find(class_="next").find("a").string
        except:
            var = ''

        if var == "next":
            i = 0
            for lettre in range(len(url_of_the_page)): 
                if url_of_the_page[- i] == "/":
                    self.take_url_book_page(url_of_the_page[: -i] + "/" + html.find(class_="next").find("a")["href"], list_urls_book_page)
                    break
                i += 1
                
        return list_urls_book_page
        
    def extract_information_book(self, list_urls_book_page):
        list_info_book = []
        for url_this_book in list_urls_book_page:
            print(url_this_book)
            page = requests.get(url_this_book)
            html = BeautifulSoup(page.content, "html.parser")

            lien_product_information = html.find(class_="table-striped").find_all("tr")
            list_product_information = []
            for information in lien_product_information:
                list_product_information.append(information.find("td").string)

            universal_produc_code = list_product_information[0]
            price_excluding_tax = list_product_information[2]      
            price_including_tax = list_product_information[3]  
            number_available = list_product_information[5]
            review_rating = list_product_information[6]

            lien_category = html.find(class_="breadcrumb").find_all("li")
            list_category = []
            for info in lien_category:
                list_category.append(info.find("a"))

            category = list_category[2].string
            try:
                product_description = html.find(id="product_description").find_next("p").string
            except:
                product_description = ""
                
            title = html.find(class_="product_main").find("h1").string
            product_page_url = url_this_book
            image_url = "http://books.toscrape.com" + html.find(class_="carousel-inner").find("img")["src"][5:]

            list_info_book.append([product_page_url, universal_produc_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
        
        return list_info_book
        
    def save_in_csv(self, name_file, list_info_book):
        date = str(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()))
        header = ["product_page_url", "universal_produc_code", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"] 
        destination_csv = "./CSV/" + name_file + '_' + date + ".csv" 
        
        with open(destination_csv, "w", encoding='utf-8') as fichier_CSV:
            writer = csv.writer(fichier_CSV, delimiter=",")
            writer.writerow(header)

            for book in list_info_book:
                writer.writerow(book)

class Screen(Scrap):
    def __init__(self, url_home_page):
        super().__init__(url_home_page)
        
    def display_play(self):
        list_category = self.take_url_and_category_page()
        self.display_list(list_category, False)
        selection_category = int(input())
        
        #print(list_category)
        
        if selection_category > len(list_category) - 1 or selection_category < 0:
            self.display_list(list_category, True)
        else:
            url_selection = self.take_url_selection(list_category, selection_category)
            #super().take_url_book_page(self.take_url_selection(list_category, selection_category))
            return url_selection
        
    def display_list(self, list_category, error):
        i = 0
        for title_page, url in list_category.items():
            print(i, title_page)
            i += 1
            
        if error == True:
            print("Le chiffre sélectionner n'est pas Valide")
            print("Veuillez en choisir un valide")   
        elif error ==  False:
            print("Veuillez sélectionner le chiffre de la catégory")
            
    
    def take_url_selection(self, list_category, selection_category):
        i = 0
        #print(list_category)
        if int(selection_category) == 0:
            list_category.pop("Books")
            return list_category
        else:
            for title_page, url in list_category.items():
                if i == selection_category:
                    return {title_page: url}
                i += 1

            
            
def start_scrape():
    start = Screen("http://books.toscrape.com/index.html")
    choice_categorie = start.display_play()
    #print(choice_categorie, "coucou")
    for title, url_page in choice_categorie.items():
        list_url_book = start.take_url_book_page(url_page, [])
        print(len(list_url_book), "Book in the catégory")
        list_info_book = start.extract_information_book(list_url_book)
        #print(list_info_book)
        start.save_in_csv(title, list_info_book)

start_scrape()
#Scrap("http://books.toscrape.com/index.html").take_url_book_page("http://books.toscrape.com/catalogue/category/books/childrens_11/index.html")
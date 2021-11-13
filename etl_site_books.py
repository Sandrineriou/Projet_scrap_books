import requests
from bs4 import BeautifulSoup
import csv


url_site = 'https://books.toscrape.com/'

reponse = requests.get(url_site)



# Test de la réponse
if reponse.ok :

    soup = BeautifulSoup(reponse.text, 'html.parser')
        
    # Création d'une liste pour contenir les liens de toutes les catégories et une list pour les liens de toutes les images:
    
    links_category = []
    
    
    
    # chercher le lien de chaque catégorie et l'intégrer dans la liste 'links_categorie' :
         
    li = soup.find('ul', class_="nav nav-list").find('li')
    ul = li.find('ul')
    for a in li.find('ul').find_all('a') :
        href = a['href']
        link_category = (url_site + href)
        
        links_category.append(link_category)
        
        
    
    
    
   
   
    def get_links_book_category(i) :
   
        url_category = links_category[i]
        
       
        reponse = requests.get(url_category)
        soup = BeautifulSoup(reponse.text, 'html.parser')
    
        links_pages_category = []
        links_pages_category.append(url_category)
        
        
        class_next = soup.find_all('li', class_="next")
        
        # Boucle qui va rechercher l'existance de pages suivantes et intégrer leur lien dans la liste des liens de toutes les pages de la categorie : 
        while class_next :
            
            for class_next in soup.find_all('li', class_="next") :
                
                a = class_next.find('a')
          
                link_pagination_next = a['href']
            
                url_category_page = url_category.replace("index.html", "")
        
                link_page_next = (url_category_page + link_pagination_next)
        
                links_pages_category.append(link_page_next)
                reponse = requests.get(link_page_next)
                soup=BeautifulSoup(reponse.text, 'html.parser')
                class_next = soup.find_all('li', class_="next")
        
        
        links_book = []
        
        for link in links_pages_category :
      
            reponse = requests.get(link)

            if reponse.ok:
                soup = BeautifulSoup(reponse.text, 'html.parser')
                
                # Extractions des liens de tous les livres de la categorie et enregistrer dans la liste 'links_book' :
                # chercher toutes les balises 'a' dans toutes les balises 'div' dont la class='image container', puis extraire chaque lien de toutes les balises 'a' :
                
                for dv in soup.find_all('div', class_="image_container"):
                    a = dv.find('a')
                    link_brut = a['href']

                    # Eliminer les 7 premiers caractères de chaque 'href' pour pouvoir concatener avec l'url du catalogue pour avoir les urls de chaque livre de la page :
                    link_cleantolink = link_brut.replace('../../..' , '') 
                    link_book = ('https://books.toscrape.com/catalogue' + link_cleantolink)
                    # ajouter tous liens à la liste 'links_book' :
                    links_book.append(link_book)
            
        return links_book

    
    

    en_tete = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    links_image = []
    
    l = len(links_category)
    for i in range (0, l):
        
        links_book = get_links_book_category(i)
 
        with open(f'books/books_category{i}.csv', 'w', newline = '') as output : 

            writer = csv.DictWriter(output, fieldnames = en_tete, delimiter=',')
            writer.writeheader()
            
            
            for link_book in links_book:
                r = requests.get(link_book)
                soup = BeautifulSoup(r.content, 'html.parser')
                
                table_info_produit = soup.find_all('table', class_='table table-striped')[0]   

                upc_produit = (table_info_produit.find_all('tr')[0].find('td')).text
                
                prix_TTC_produit = (table_info_produit.find_all('tr')[2].find('td')).text
               
                prix_HT_produit = (table_info_produit.find_all('tr')[3].find('td')).text
                
                stock = (table_info_produit.find_all('tr')[5].find('td')).text
                
                quantite_stock_produit = stock[10:12]
               
                quantite_evaluation_produit = ((table_info_produit.find_all('tr')[6].find('td')).text)
                
                desc_produit=soup.find('article', class_='product_page').find_all('p')[3].text
                
                title_produit = soup.find('div', class_='col-sm-6 product_main').find('h1').text
                
                category_produit = soup.find('ul', class_='breadcrumb').find_all('a')[2].text
                
                #Extraction de l'url de l'image du livre :
                # Extraction de l'attribut 'src' compris dans les balises :
                img = soup.find('div', class_='item active').find('img')
                src_brut = img['src']
                # Retraitement du 'src' pour reterirer les '../..' blancs :
                src_cleantolink = src_brut.replace('../..', '')
                # Concatener l'url de la page du site avec l'url de l'image trouvé sur la page pour avoir l'url compléte de l'image:
                image_url_produit = ('https://books.toscrape.com' + src_cleantolink)
                links_image.append(image_url_produit)
                
                
                # Création d'une liste qui met en lien les en-têtes et les données correspondantes à extraire :  
                data = [
                 {'product_page_url': link_book,
                'universal_product_code(upc)': upc_produit,
                'title': title_produit, 
                'price_including_tax': prix_TTC_produit,
                'price_excluding_tax': prix_HT_produit,
                'number_available': quantite_stock_produit,
                'product_description': desc_produit,
                'category': category_produit,
                'review_rating': quantite_evaluation_produit,
                'image_url': image_url_produit
                 }
                ]       
                
                for elem in data:
                    writer.writerow(elem)


    
    n = len(links_image)
    for j in range(0, n):
    
        link = links_image[j]
        
        r = requests.get(link, stream =True)
       
        if r.ok:

            with open(f'images/book{j}.jpg', 'wb') as f:
                f.write(r.content)  
   


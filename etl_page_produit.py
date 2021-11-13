import requests
from bs4 import BeautifulSoup
import csv

# Début de l'ETL  : Extraire, Transformer, Charger :

# Extraction des données de la page
url_page_produit = 'https://books.toscrape.com/catalogue/sharp-objects_997/index.html'


page = requests.get(url_page_produit)



# Vérifier que la page fonctionne, implicitement réponse '200'

if page.ok:
    

# Création des variables des éléments à extraire et extractions des données
    
    # Parser la page HTML en objet BeautifulSoup :
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    
    
    # Extraction des éléments de la table 'information produit' :
    
    table_info_produit = soup.find_all('table', class_='table table-striped')[0]
    
    
    
    # Extraction des éléments dans les cellules de la tables :  
    
    # Extraction de l'UPC :
    
    upc_produit = (table_info_produit.find_all('tr')[0].find('td')).text
   

    
    # Extraction du prix avec taxes :
    
    prix_TTC_produit = (table_info_produit.find_all('tr')[2].find('td')).text
 
 
 

    # Extraction du prix sans taxes :
    
    prix_HT_produit = (table_info_produit.find_all('tr')[3].find('td')).text
    
   
   
    # Extraction du nombre de livre en stock :
    
    # Extraction du texte conteu dans 'availability':
    
    stock = (table_info_produit.find_all('tr')[5].find('td')).text
    
    # Extraction uniquement du chiffre de livres disponibles en stock :
   
    quantite_stock_produit = stock[10:12]
    
   
   
    # Extraction du nombre d'évaluation :
    
    quantite_evaluation_produit = ((table_info_produit.find_all('tr')[6].find('td')).text)
      
   
    # Fin d'extraction de la table
    
    
    # Extraction des autres éléments sur le reste de la page :

    # Extraction de la description du produit: 
    
    desc_produit = soup.find('article', class_='product_page').find_all('p')[3].text
   
       
    # Extraction du titre du livre : 
    
    title_produit = soup.find('div', class_='col-sm-6 product_main').find('h1').text
   
  
    # Extraction du nom de la catégorie :
 
    category_produit = soup.find('ul', class_='breadcrumb').find_all('a')[2].text
    
    
    #Extraction de l'url de l'image du livre :
    
    # Extraction de l'attribut 'src' compris dans les balises :
    
    img = soup.find('div', class_='item active').find('img')
    src_brut = img['src']
   
    # Retraitement du 'src' pour reterirer les '../..' blancs :
   
    src_cleantolink = src_brut.replace('../..', '')
    
    
    # Concatener l'url de la page du site avec l'url de l'image trouvé sur la page pour avoir l'url compléte de l'image:
    
    image_url_produit = ('https://books.toscrape.com' + src_cleantolink)
    
    
    
    
   
    # Création d'un fichier csv et intégration des données extraites ci_dessus :
    
    # Création des en_têtes et dictionnaire de données à intégrer dans le fichier csv :
    
    en_tete = ['product_page_url', 'universal_product_code(upc)', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    
    data = [
        {'product_page_url': url_page_produit,
        'universal_product_code(upc)': upc_produit,
        'title': title_produit, 
        'price_including_tax': prix_TTC_produit,
        'price_excluding_tax': prix_HT_produit,
        'number_available': quantite_stock_produit,
        'product_description': desc_produit,
        'category': category_produit,
        'review_rating': quantite_evaluation_produit,
        'image_url':image_url_produit
        }
       ]
    
    # Création du fichier csv:  
        
    with open('data_page_produit.csv', 'w', newline='') as outf:
            
        # Intégration des données dans le csv :
        
        writer = csv.DictWriter(outf, fieldnames=en_tete, delimiter=',')
        writer.writeheader()
        for elem in data:
            writer.writerow(elem)
        
# Fin de l'ETL
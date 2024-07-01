import csv
from bs4 import BeautifulSoup
import requests

def get_html(url):
    """Fetch the html content for the given URL"""
    response=requests.get(url)
    response.raise_for_status() #Raise an error for bad status code
    return response.text

def parse_html(html):
    """Parse the html content and extract te product information"""
    soup=BeautifulSoup(html,'html.parser')
    product_container=soup.select('article.product_pod') #correct css selector for the product container
    products=[]

    for container in product_container:
        name=container.select_one('h3 a')['title'].strip() #selector for product name
        price=container.select_one('p.price_color').text.strip() #selector for product price


        #check if rating element exist
        rating_element=container.select_one('p.star-rating')
        if rating_element:
            rating_class=rating_element.get('class',['No rating'])[1] #extracting the second class
        else:
            rating_class='No rating'
        
        products.append({
            'name':name,
            'price':price,
            'rating':rating_class
        })

    return products

def save_to_csv(products,filename):
    """save the extracted product information to a csv file"""
    if not products:
        print('No product found')
        return 
    
    keys=products[0].keys()
    with open(filename,'w',newline='',encoding='utf-8') as file:
        dict_writer=csv.DictWriter(file,fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)

def main():
    base_url='http://books.toscrape.com/catalogue/page-{}.html'
    all_products=[]

    for page_num in range(1,10): #Adjust the range as you needed
        url=base_url.format(page_num)
        print(f"Scraping page {page_num}...")
        html=get_html(url)
        products=parse_html(html)
        all_products.extend(products)

    save_to_csv(all_products,'product.csv')
    print('Data has been written to product.csv')

if __name__ == '__main__':
    main()
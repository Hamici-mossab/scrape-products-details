from bs4 import BeautifulSoup
import requests
import pandas as pd


#create lists to save the scraped data
titles = []
prices = []
shipping_methode = []
ratings = []
product_url = []
img_url = []

product = 'smart watch'.replace('','+')

for i in range(1,10):
    
    website = f'https://www.newegg.com/p/pl?d={product}&page=' + str(i)

    page = requests.get(website)

    soup = BeautifulSoup(page.content, 'html.parser')

    #find the parent element
    results = soup.find_all("div", {"class":"item-cell"})

    #looping the parent element and get the data
    for result in results:
        #titles
        try:
            titles.append(result.find("a", {"class":"item-title", "title":"View Details"}).text)
        except:
            titles.append("no result")
        
        #prices
        try:
            main_price = result.select("li.price-current  strong")[0]
            para_price = result.select("li.price-current  sup")[0]
            price = main_price.text + para_price.text + '$'
            prices.append(price)
        except:
            prices.append("no result")    
        
        #shipping
        try:
            shipping_methode.append(result.find("li", {"class": "price-ship"}).text)
        except:
            shipping_methode.append("no result")   

        #ratings
        try:
            ratings.append(result.find("span", {"class": "item-rating-num"}).text)
        except:
            ratings.append("not rated")  
        
        #products url
        try:
            product_url.append(result.find("a", {"class":"item-title", "title":"View Details"})["href"])
        except:
            product_url.append("no result")  
            
        #images url
        try:
            img_url.append(result.select("a.item-img img")[0]["src"])
        except:
            img_url.append("no result")
            
            

product_overview = pd.DataFrame({'title': titles ,'price':prices ,'shipping methode': shipping_methode, 'rating out of 5 ': ratings ,'product image':img_url , 'product url': product_url}).drop_duplicates()

product_overview.drop(product_overview.index[product_overview['title'] == 'no result'], inplace=True)

product_overview.to_excel("newproducts.xlsx", index=False)


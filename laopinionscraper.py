from bs4 import BeautifulSoup as soup
from requests import get
import pandas as pd
import time
from IPython.core.display import clear_output
from random import randint



keyword = input("What is the keyword you wanna look up?(e.g 'paro' o 'huelga de maestros')\n")

titles = []
links = []
contents = []
dates = []

start_time = time.time()
requests = 0
pages = [str(i) for i in range(0,5500)]
count = 0

for page in pages:
    
    url = "https://www.laopinion.com.co/search/site/" + keyword + "?page=" +page +"#OP"
    html = get(url)
    htmlsoup = soup(html.content,'html5lib')
    time.sleep(randint(2,4))
    requests += 1
    count += 1
    elapsed_time = time.time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait = True)  
    print(url)
    articles = htmlsoup.find_all('div', attrs={'class':'resultado'})
    if len(articles) != 0:
        for oneArticle in articles:            
            title = oneArticle.h3.text
            link = oneArticle.h3.a['href']
            date = oneArticle.find('div', class_= "fecha").text
            content = ''
            html2 = ''
            print(link)
            while html2 == '':
                try:
                    html2 = get(link)
                    break
                except:
                    print("Connection refused by the server")
                    time.sleep(3)
                    print("Let's try again...")
                    continue
            noodles = soup(html2.content,'html5lib') 
            contenido = []
            for i in noodles.find_all('div', attrs = {'class':'field-item even'}):
                contenido.append(i.find_all('p'))
                contenido = list(filter(None, contenido))
            if len(contenido) != 0 :
                texto = ''
                for textos in contenido[0]:
                    texto += textos.text
                    texto = texto.replace("\n" , "").replace("\t", "")
                titles.append(title)
                contents.append(texto)
                dates.append(date)
                links.append(link) 
                test_df=pd.DataFrame({'Titulo':titles,
                              'Fecha':dates,
                              'Contenido':contents,
                              'Link':links})
        
            else :
                titles.append(title)
                dates.append(date)
                content="Especial"
                contents.append(content)
                links.append(link)
                
                test_df=pd.DataFrame({'Titulo':titles,
                              'Fecha':dates,
                              'Contenido':contents,
                              'Link':links})
    else:
        test_df=pd.DataFrame({'Titulo':titles,
                                  'Fecha':dates,
                                  'Contenido':contents,
                                  'Link':links})
        print("There were no more articles found with your keyword")
        break
        
            
if count==10 :
    test_df.to_excel("laopinion_" + keyword + ".xlsx")   
    count=0
  
test_df.to_excel("laopinion" + keyword + ".xlsx")  

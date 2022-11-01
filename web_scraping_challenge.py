import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import pandas as pf # csv
import sqlite3 # interface to local DB
from datetime import datetime

now = datetime.now()
time_stamp = now.strftime("%d.%m.%Y | %H:%M")

print(now)

#===================== asign item to url =============================#

natura_xl = 'https://www.wollplatz.de/wolle/dmc/dmc-natura-xl?sqr=Natura%20XL'
safran = 'https://www.wollplatz.de/wolle/drops/drops-safran?sqr=Safran'
baby_merino_mix = 'https://www.wollplatz.de/wolle/drops/drops-baby-merino-mix?sqr=Baby%20Merino%20Mix'
Alpacca_Speciale = 'https://www.wollplatz.de/?#sqr:(q[Alpacca%20Speciale])'
Special_double_knit = 'https://www.wollplatz.de/artikel/29382/stylecraft-special-dk-1856-dandelion.html?sqr=Stylecraft'


#================== list of items // url global var =========================#

item_lst = [baby_merino_mix, natura_xl, safran,Special_double_knit ]

#=============================================================================#

class MyClass:

    #print(set_lst) tst lst 


    def web_lookup(item_lst):
        
            for item in item_lst:

                try:
                    #print(item) // tst item in class
                    page = requests.get(item)
                    src = page.text
                    soup = BeautifulSoup(src, "lxml")


                    
                    product = soup.find_all("span", {"class":"variants-title-txt"})
                    print(product[0].text) # item name
                    
                    stock = soup.find_all("span", {"class":"stock-green"})
                    print(stock[0].text) # availability 
                    
                    price = soup.find_all("span",{"class":"product-price"})
                    print(price[0].text) # price
                    
                    
                    #====================Catch data from HTML table=============#
                    
                    table = soup.find('div', {"id" :"pdetailTableSpecs"})
                    
                    lst_spec = []




                    for i in table.find_all('tr'):#get data from tabel in html
                        title = i.text
                        lst_spec.append(title)


                    #print(lst_spec) // tst append table data into lst


                    compos_spec = []
                    needle_spec = []

                    for match in lst_spec :

                        if "Zusammenstellung" in match: # extract composition from table data
                            compos_spec.append(match)

                        elif "Nadelstärke" in match:    # extract needle size from table data
                            needle_spec.append(match)

                    composit = ''.join(compos_spec)
                    needel  =  ''.join(needle_spec)
                    

                    print(composit)
                    print(needel)
                        

                    #print(lst_spec[4]) # get data from table slice list (needle size) ! fail at different instances
                    #print(lst_spec[3]) # get data from table slice list (composition) ! fail at different instances

                    data = [time_stamp, product[0].text, stock[0].text, price[0].text, composit, needel]

                    #print(data) tst data out list

                    with open('outdata.csv','a', newline='') as outfile:
                        wr = csv.writer(outfile)
                        wr.writerow(data) 

                    

                except IndexError:
                    print("Item out of stock or don't exist any more")
                    pass


                print("==================================")



            
                                    
                #=============================End of Class========================#


                
    
    
MyClass.web_lookup(item_lst) # Run this class here
#MyClass.table_extract()


#Comment add for sourceTree














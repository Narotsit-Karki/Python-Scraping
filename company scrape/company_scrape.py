# #! /bin/python3


from bs4 import BeautifulSoup as scraper
import re
import grequests,gevent.monkey

import requests
import threading
import time
import pandas as pd 
import numpy as np


threads = []
link = []
company_info = {'Name':[],'Phone_No':[],'Email':[]}
company_name = []
name = "#"
urls = ["","contact-us","customer-center","about-us"]
temp = []

generate_url_dict = {}

with open('company.txt','r') as file:
    while name != '':
        name = file.readline()
        if name not in company_name:
            company_name.append(name.strip())

def scrape_web(page,search_name):

    soup = scraper(page.content,"html.parser")
    if page.status_code == 200:
        for links in soup.find_all('a', attrs ={ 'href' : re.compile("^https://www.|^https://blog.")}):
            link = links.get('href')
            if re.findall('(.com/|.net/|.np/|.np|.com|.net|.gov|.)$',link):
                try:
                    nm = search_name.split()
                    nm = nm[0].lower() # split company name so if company name = NIC ACIA then nm = nic

                    if nm not in temp: # search nm if already in temp list
                        temp.append(nm[0]) # else append company name (nm) in temp
                        if nm in link:
                            create_url_list(link,search_name)
                                #find_tel_email(link,search_name,url)
                except Exception:
                    pass
    else:
        print(f"[❌] Error {page.status_code}")





def create_url_list(link,companyname):
    generate_url = []
    for url in urls:
        if link+url not in generate_url:
            generate_url.append(link+url)
            

        
    generate_url_dict[companyname] = generate_url
        
    
    

def exception(request, exception):
        print(f"Problem: {request.url} : {exception}\n")

def page_requests(urls,companyname):
    results = grequests.map((grequests.get(u) for u in urls), exception_handler=exception, size=5)
    for page in results:
        if page is not None:
            find_tel_email(page,companyname)

    
def find_tel_email(page,companyname):
    tel = []
    email  = []
    if  page.status_code == 200:
        print(f"✅ {page.url}")
        soup = scraper(page.content,"html.parser")
        for info in soup.find_all('a', attrs = {'href': re.compile("^tel:")}):
            telephone = info.get('href')[4:]
            if telephone not in tel:
                tel.append(telephone)

            for info in soup.find_all('a',attrs = {'href': re.compile("^mailto:")}):
                mail = info.get('href')[7:]
            #if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',mail):
            
                if mail not in email:
                    email.append(mail)
                
            
        if len(tel) == 0 and len(email) == 0:
            return 
        
        if companyname not in company_info['Name']:
            company_info['Name'].append(companyname)
        
            if len(tel) == 0:
                tel = np.nan
            elif len(tel) == 1:
                tel = tel[0]
                
            
            if len(email) == 0:
                email = np.nan  # if email is null add Nan
            elif len(email) == 1:
                email = email[0] #if only single value in list unpack it 
                
            company_info['Phone_No'].append(tel)
            company_info['Email'].append(email)
        
        
    else:
        print(f"❌ {page.url}")

seed = "https://search.yahoo.com/search?p="
yahoo_search_url = []
for company in company_name:
    yahoo_search_url.append(seed+company)

results = grequests.map((grequests.get(u) for u in yahoo_search_url), exception_handler=exception, size=5)

for page,company in zip(results,company_name):
    if page is not None:
        scrape_web(page,company)


for companyname in generate_url_dict.keys():
    urls = generate_url_dict[companyname]
    page_requests(urls,companyname)
    
    
print("\n EMAIL AND TELEPHONE NO\n\n")
df = pd.DataFrame(company_info)
#display(df)
print(df)





























# from bs4 import BeautifulSoup as scraper
# import re
# import requests
# import threading
# import time
# curname = None
# mails = []
# tel = []
# threads = []
# link = []
# company_name = []
# name = "#"
# urls = ["","contact-us","customer-center","about-us"]
# temp = []
# with open('company.txt','r') as file:
#     while name != '':
#         name = file.readline()
#         company_name.append(name.strip())

# def scrape_web(search_name):
#     page = requests.get(f"https://search.yahoo.com/search?p={search_name}")
#     soup = scraper(page.content,"html.parser")
#     if page.status_code == 200:
#         for links in soup.find_all('a', attrs ={ 'href' : re.compile("^https://www.")}):
#             link = links.get('href')
#             if re.findall('(.com/|.net/|.np/|.np|.com|.net|.gov)$',link):
#                 try:
#                     nm = search_name.split()
#                     nm = nm[0].lower()

#                     if nm not in temp:
#                         temp.append(nm[0])
#                         if re.findall(f'{nm}',link):
#                             for url in urls:
#                                 find_tel_email(link,search_name,url)
#                 except Exception:
#                     pass
#     else:
#         print(f"[❌] Error {page.status_code}")





# def find_tel_email(link,companyname,url):
#     global curname
#     try:
#         page = requests.get(link+url)
#     except Exception as ex:
#         pass
#     if page.status_code == 200:
#         print(f"✅ {link+url}")
#         soup = scraper(page.content,"html.parser")
#         for info in soup.find_all('a', attrs = {'href': re.compile("^tel:")}):
#             telephone = info.get('href')[4:] + f"\033[00m + [\033[35m{companyname}\033[00m]"

#             if telephone not in tel:
               
#                 tel.append(telephone)
#                 curname = companyname
        
#         for info in soup.find_all('a',attrs = {'href': re.compile("^mailto:")}):
#             mail = info.get('href')[7:]+ f"\033[00m + [\033[35m{companyname}\033[00m]"
#             #if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',mail):
#             if mail not in mails:
#                 mails.append(mail)
                    
#     else:
#         print(f"❌ {link+url}")

# for company in company_name:
#     #scrape_web(company)
#     thread_handle = threading.Thread(target = scrape_web, args = (company,))
#     thread_handle.start()
#     threads.append(thread_handle)

# for thread in threads:
#     thread.join()

# print("\n EMAIL AND TELEPHONE NO\n\n")
# for (mail,telephone) in zip(mails,tel):
#     print("\033[00m[🔷] Email: \033[32m",mail , "\033[00m\t\t:\t\t" , "Telephone:\033[34m ",telephone)


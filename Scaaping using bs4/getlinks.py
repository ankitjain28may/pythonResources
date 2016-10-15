# Input the url and print all the links on that page


from bs4 import BeautifulSoup

import requests

url = input("Enter a website to extract the URL's from: ")

r  = requests.get("http://"+url)
data = r.text

soup = BeautifulSoup(data,'html.parser')
f = open("test.txt","a+")
i=0;
for link in soup.find_all('a'):
    f.write(link.get('href')+"\n")
f.close()

# Input the url and print all the links on that page

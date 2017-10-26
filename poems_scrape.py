import requests
from bs4 import BeautifulSoup


top_500_urls = ["https://www.poemhunter.com/p/m/l.asp?a=0&l=top500&order=title&p=" + str(i) for i in range(1,21)]

url_stem = "https://www.poemhunter.com"
links = []

for url in top_500_urls:

    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    poems = soup.findAll('td',{"class":'title'})

    for poem in poems[1:]:
        links.append(url_stem + str(poem.find('a')['href']))

for link in links:
    #item = ["author", "title", "text"]
    response = requests.get(link)
    soup = BeautifulSoup(response.text,"lxml")
    text = soup.find('p',attrs={'class': None}).text.strip()
    text = str(text).replace("<br/>"," ").replace("<br />"," ")
    print(text)
    break



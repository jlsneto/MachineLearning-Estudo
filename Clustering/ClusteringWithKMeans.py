"""
import pandas as pd

posts = pd.read_csv('postsUnico.csv')

questionText = posts['Text']

answerText = posts['AnswerAccepted']


"""

import requests
from bs4 import BeautifulSoup

url='https://stackoverflow.com/questions/47588415/calculate-picture-id-for-gallery-with-ads'

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')

#divs = soup.findAll("div", class_='post-text')

post = soup.findAll("div", {"class":"post-text"})

teste = [i.findAll("p") for i in post]
teste2 = [i.findAll("div", {"class":"snippet-code"}) for i in post]

"""
for div in divs:
  lista = div.findAll('p')
  teste.append(lista)
  #for i in lista:
      #teste.append(x.replace('\0', '') for x in i)
"""

import requests
from bs4 import BeautifulSoup

url = 'https://www.root.cz/'

# Stáhněte obsah webové stránky
response = requests.get(url)


keywords = ['Linux', 'Ubuntu']


def checkForKeywords(title, keywords):
  if title == '':
    return False

  if keywords == None:
    return True
  
  for keyword in keywords:
    if keyword in title:
      return True
    

def findArticles(section, base_url, keywords=None):
  if 'http' not in base_url:
    print("Error: invalid base url")
    return -1


  articles_dict = {}
  articles = section.find_all('h3')
  for article in articles:
    title = article.text.replace('\n', '')
    if checkForKeywords(title, keywords):
      url = article.parent['href']
      if 'http' not in url:
          if url[0] == '/' and base_url[-1] == '/':
            url = url[:-1]
          elif url[0] != '/' and base_url[-1] != '/':
            base_url += '/'
          url = base_url + url

      articles_dict[title] = url
  
  return articles_dict

def printArticles(articles):
  for k, v in articles.items():
    print('\n' + k + ": " + v + '\n') 


if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    #zparvicky
    sidebar = soup.find(id="sidebar")
    sidebar_articles = findArticles(sidebar, url, keywords)
    printArticles(sidebar_articles)

    #clanky
    articles_lists = soup.find_all(class_="design-list--articles")
    for articles_list in articles_lists:
      articles = findArticles(articles_list, url, keywords)
      printArticles(articles)
  

else:
    print('Chyba při načítání stránky:', response.status_code)

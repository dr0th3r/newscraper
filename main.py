import requests
from bs4 import BeautifulSoup

default_webs = ["https://www.root.cz/"]

class Scraper:
  def __init__(self, keywords=None, websites=None):
    self.urls = websites or default_webs
    self.keywords = keywords or []
    self.articles = {}

  def get_all_articles(self):
    for web in self.urls:
      if (web == "https://www.root.cz/"): self.get_rootcz()
      else: print("Tento web zatím neumíme zpracovat.")

      for k, v in self.articles.items():
        print(f"\n{k}: {v}\n")


  def get_rootcz(self):
    response = requests.get("https://www.root.cz/")

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      #zparvicky
      sidebar = soup.find(id="sidebar")
      self.articles = self.articles | self.find_articles(sidebar, "https://www.root.cz/")

      #clanky
      articles_lists = soup.find_all(class_="design-list--articles")
      for articles_list in articles_lists:
        self.articles = self.articles | self.find_articles(articles_list, "https://www.root.cz/")
    else:
      print('Chyba při načítání stránky:', response.status_code)   

  def find_articles(self, section, base_url):
    if 'http' not in base_url:
      print("Error: invalid base url")
      return {}

    articles_dict = {}
    articles = section.find_all('h3')


    for article in articles:
      title = article.text.replace('\n', '')

      if self.check_for_keywords(title):
        url = article.parent['href']
        if 'http' not in url:
            if url[0] == '/' and base_url[-1] == '/':
              url = url[:-1]
            elif url[0] != '/' and base_url[-1] != '/':
              base_url += '/'
            url = base_url + url

        articles_dict[title] = url
  

    return articles_dict

  def check_for_keywords(self, title):
      if title == '':
        return False

      if self.keywords == None or self.keywords == []:
        return True
      
      for keyword in self.keywords:
        if keyword in title:
          return True
    


scraper = Scraper()
scraper.get_all_articles()
  


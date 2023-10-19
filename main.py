import requests
from bs4 import BeautifulSoup

default_webs = ["https://www.root.cz/", "https://www.abclinuxu.cz/", "https://www.lupa.cz/", "https://www.svethardware.cz"]

class Scraper:
  def __init__(self, keywords=None, websites=None):
    self.urls = websites or default_webs
    self.keywords = keywords or []
    self.articles = {}

  def get_all_articles(self):
    for web in self.urls:
      if (web == "https://www.root.cz/"): 
        self.get_rootcz()
        #self.get_zdrojakcz() - currently not working
      if (web == "https://www.abclinuxu.cz/"):
        self.get_abclinuxu()
      if (web == "https://www.lupa.cz/"):
        self.get_lupacz()
      if (web == "https://www.svethardware.cz"):
        self.get_svethwcz()
      else: print(f"Tento web ({web}) zatím neumíme zpracovat.")

      for k, v in self.articles.items():
        print(f"\n{k}: {v}\n")


  def get_rootcz(self):
    response = requests.get("https://www.root.cz/")

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      #zparvicky
      sidebar = soup.find(id="sidebar")
      self.articles = self.articles | self.find_articles_root(sidebar, "https://www.root.cz/")

      #clanky
      articles_lists = soup.find_all(class_="design-list--articles")
      for articles_list in articles_lists:
        self.articles = self.articles | self.find_articles_root(articles_list, "https://www.root.cz/")
    else:
      print('Chyba při načítání stránky root.cz:', response.status_code)   

  def get_zdrojakcz(self):
    response = requests.get("https://zdrojak.cz/clanky/")
    if response.status_code == 200:
      soup = BeautifulSoup(response.text, "html.parser")

      #clanky
      articles_list = soup.find('main')
      self.articles = self.articles | self.find_articles_zdrojak(articles_list, "https://zdrojak.cz/clanky/", 'h1')

    else:
      print('Chyba při načítání stranky zdrojak.cz"', response.status_code)

  def get_abclinuxu(self):
    response = requests.get("https://www.abclinuxu.cz/")

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      articles_list = soup.find(id="st")
      self.articles = self.articles | self.find_articles_abclinuxu(articles_list, "https://www.abclinuxu.cz/")
      
  def get_lupacz(self):
    response = requests.get("https://www.lupa.cz/")

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      articles_list = soup.find(class_="layout-main__content")
      self.articles = self.articles | self.find_articles_lupa(articles_list, "https://www.lupa.cz/")
    else:
      print('Chyba při načítání stranky lupa.cz"', response.status_code)

  def get_svethwcz(self):
    response = requests.get("https://www.svethardware.cz/aktuality/")

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      articles_list = soup.find(id="main")
      self.articles = self.articles | self.find_articles_svethw(articles_list, "https://www.svethardware.cz")
    else:
      print('Chyba při načítání stránky svethardware.cz:', response.status_code)   

  def find_articles_root(self, section, base_url):
    if 'http' not in base_url:
      print("Error: invalid base url")
      return {}

    articles_dict = {}
    articles = section.find_all('h3')


    for article in articles:
      title = article.text.replace('\n', '')

      if self.check_for_keywords(title):
        url = article.parent['href']
        url = self.correct_url(url, base_url)

        articles_dict[title] = url
  

    return articles_dict

  def find_articles_zdrojak(self, section, base_url):
    if 'http' not in base_url:
      print("Error: invalid base url")
      return {}

    articles_dict = {}
    articles = section.find_all(class_="text-zdrojak")

    for article in articles:
      title = article.text.replace('\n', '')

      if self.check_for_keywords(title):
        url = article['href']
        url = self.correct_url(url, base_url)

        articles_dict[title] = url

      return articles_dict

  def find_articles_abclinuxu(self, section, base_url):
    if 'http' not in base_url:
      print("Error: invalid base url")
      return {}

    articles_dict = {}
    articles = section.find_all('h2', class_="st_nadpis")

    for article in articles:
      title = article.find('a').text

      if self.check_for_keywords(title):
        url = article.find('a')['href']
        url = self.correct_url(url, base_url)

        articles_dict[title] = url

    return articles_dict

  def find_articles_lupa(self, section, base_url):
    if 'http' not in base_url:
      print("Error: invalid base url")
      return {}
    
    articles_dict = {}
    articles = section.find_all("h3", class_="element-heading-reset")

    for article in articles:
      title = article.text
      
      if self.check_for_keywords(title):
        url = article.parent['href']
        url = self.correct_url(url, base_url)

      articles_dict[title] = url

    return articles_dict

  def find_articles_svethw(self, section, base_url):
    if 'http' not in base_url:
      print("Error: invalid base url")
      return {}

    articles_dict = {}
    articles = section.find_all("h2")

    for article in articles:
      title = article.text

      if self.check_for_keywords(title):
        url = article.parent['href']
        url = self.correct_url(url, base_url)

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
    
  def correct_url(self, url, base_url):
    if 'http://' not in url and 'https://' not in url:
            if url[0] == '/' and base_url[-1] == '/':
              url = url[:-1]
            elif url[0] != '/' and base_url[-1] != '/':
              base_url += '/'
            url = base_url + url
    return url


scraper = Scraper([],["https://www.svethardware.cz"])
scraper.get_all_articles()
  



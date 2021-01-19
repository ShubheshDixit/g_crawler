from bs4 import BeautifulSoup
import lxml, re, requests, time, sys, os, json, random
from selenium import webdriver

email_regex = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

class EmailScrapper():
    
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'lxml')
        self.html = html
    
    def getURL(self):
        for a in self.soup.find_all('a'):
            print(a.get('href'))
    
    def getEmail(self):
        emails = set(re.findall(email_regex, self.html))
        print(emails, len(emails))


def find_country():
    countries = []
    url = 'https://history.state.gov/countries/all'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    for col in soup.find_all('div', {'class': 'col-md-6'}):
        for a in col.find_all('a'):
            countries.append(a.text)
            print(a.text)
    return countries

def create_json(filename, data):
    os.chdir(os.getcwd())
    with open(f'{filename}.json','w') as f:
        json.dump(data, f, indent=4)


if __name__ == '__main__':
    html = ''
    for i in range(0, 20, 10):
        tag = '%28tours and travels%29'
        region = '%22delhi%22'
        mail_type = '%22%40gmail.com%22'
        country = 'india'
        base_url = 'https://www.google.com/search?q='
        query = tag +  ' ' + region + ' ' + mail_type + ' ' + country + '&' + f'start={i}'
        url = base_url + query + '&' + f'start={i}'
        url = url.replace(' ','+')
        print(url)
        proxyDict = { 
              "http"  : 'http://3.211.17.212:80' 
            #   "https" : 'https://3.211.17.212:80', 
            #   "ftp"   : 'ftp://3.211.17.212:80'
        }
        res = requests.get(url, proxies = proxyDict)
        raw_html = str(res.content)
        html = html + raw_html
        # search_result_list = list(search(query, tld="co.in", num=10, stop=3, pause=1))
        time.sleep(random.randint(5, 15))
    scrapper = EmailScrapper(html)
    scrapper.getEmail()
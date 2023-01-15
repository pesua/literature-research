from mediawiki import MediaWiki
import requests
from bs4 import BeautifulSoup
import time
import csv
import string

wikipedia = MediaWiki()


def backlinks(name):
    p = wikipedia.page(name)
    return p.backlinks


session = requests.Session()


def grab_authors(page, c_code):
    print('Parsing ' + page)
    url = 'https://' + c_code + '.wikipedia.org/wiki/'
    response = session.get(url + page.replace(' ', '_'))
    soup = BeautifulSoup(response.text, "html.parser")
    if c_code == 'en' :
        return {author.a['title']: author.a['href'] for author in soup.select('.div-col li') if author.a}
    elif c_code == 'de':
        return {author['title']: author['href'] for author in soup.select('dd a')}


def parce_autors(c_code, list_pages):
    authors = {}
    for page in list_pages:
        authors.update(grab_authors(page, c_code))
        time.sleep(2)
    return authors


def store(c_code, authors):
    f = open(c_code + '_writers.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['name', 'path', 'domain'])
    for key in sorted(authors):
        writer.writerow([key, authors[key], c_code])
    f.close()


# list_pages = ['List of English writers (A–C)', 'List of English writers (D–J)',
#                    'List of English writers (K–Q)', 'List of English writers (R–Z)']
# c_code = 'en'
list_pages = ['Liste_von_Autoren/' + letter for letter in list(string.ascii_uppercase)]
c_code = 'de'
authors = parce_autors(c_code, list_pages)
store(c_code, authors)

print(len(authors))

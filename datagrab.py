from mediawiki import MediaWiki
import requests
from bs4 import BeautifulSoup
import time
import csv

wikipedia = MediaWiki()


def backlinks(name):
    p = wikipedia.page(name)
    return p.backlinks

# backlinks('List of English writers (A–C)')


session = requests.Session()

URL = 'https://en.wikipedia.org/wiki/'


def grab_authors(author):
    url = URL + author.replace(' ', '_')
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")

    return {author.a['title']: author.a['href'] for author in soup.select('.div-col li') if author.a}


english_authors = ['List of English writers (A–C)', 'List of English writers (D–J)',
                   'List of English writers (K–Q)', 'List of English writers (R–Z)']
# authors = grab_authors(english_authors[0])

authors = {}
for page in english_authors:
    authors.update(grab_authors(page))
    time.sleep(2)


f = open('english_writers.csv', 'w')

writer = csv.writer(f)
writer.writerow(['name', 'path'])
for key in sorted(authors):
    writer.writerow([key, authors[key]])
f.close()

print(len(authors))

import requests as r
from datetime import date
from bs4 import BeautifulSoup
import bs4
import os
import shelve


def apod_exists(d: date):
    if d < date(1995, 6, 20):
        return None
    code = str(d.year)[2:] + ('0' if d.month < 10 else '') + str(d.month) + ('0' if d.day < 10 else '') + str(d.day)
    url = f"https://apod.nasa.gov/apod/ap{code}.html"
    return r.head(url).status_code == 200


def get_apod(d: date):
    if d < date(1995, 6, 20):
        return None
    code = str(d.year)[2:] + ('0' if d.month < 10 else '') + str(d.month) + ('0' if d.day < 10 else '') + str(d.day)
    url = f"https://apod.nasa.gov/apod/ap{code}.html"

    if os.path.isfile(f'storage/{code}.shelf'):
        data = shelve.open(f'storage/{code}.shelf')
        dic = {
            'title': data['title'],
            'image_url': data['image_url'],
            'credits': data['credits'],
            'summary': data['summary'],
            'url': data['url'],
            'date': data['date']
        }
        data.close()
        return dic


    request = r.get(url)
    if request.status_code != 200:
        return None

    soup = BeautifulSoup(request.text, 'html.parser')

    # Image
    for a in soup.find_all('a'):
        if a.findChild('img'):
            break
    img_url = "https://apod.nasa.gov/apod/" + a['href']

    # Title
    title = soup.find('b').text.strip()

    # Credits, very dirty
    st = str(soup)
    spoon = BeautifulSoup(st.split('</b>')[2], 'html.parser')
    credit = ''.join([x.text if isinstance(x, bs4.element.Tag) else str(x) for x in list(spoon.children)[:-1]])
    credit = credit.replace('\n', ' ').replace('  ', ' ').strip()
    try:
        fork = BeautifulSoup(st.split('Explanation:')[1], 'html.parser')
    except IndexError:
        # fix for different format
        credit = BeautifulSoup(request.text.split('\n\n')[5]).text
        credit = credit.replace('\n', ' ').replace('  ', ' ').strip()
        title = title.split('\n')[0].replace('\n', ' ').replace('  ', ' ').strip()
        fork = BeautifulSoup(st.split('Explanation</b>:')[1], 'html.parser')
    ex = fork.text[:fork.text.find('\n\n\n')]
    ex = ex.replace('\n', ' ').replace('  ', ' ').strip()
    ex = ex.split('   ')[0]

    if not os.path.exists('storage'):
        os.mkdir('storage')

    data = shelve.open(f'storage/{code}.shelf')

    data['title'] = title
    data['image_url'] = img_url
    data['credits'] = credit
    data['summary'] = ex
    data['url'] = url
    data['date'] = str(d)

    data.close()

    return {
        'title': title,
        'image_url': img_url,
        'credits': credit,
        'summary': ex,
        'url': url,
        'date': str(d)
    }


if __name__ == '__main__':
    print(get_apod(date(1997, 2, 11)))

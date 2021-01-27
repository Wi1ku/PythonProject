from googlesearch import search
import requests
from bs4 import BeautifulSoup


class NoRequestResultError(Exception):
    def __init__(self, message):
        self.message = message


class NoResultError(Exception):
    def __init__(self, message):
        self.message = message


def search(query):
    query = query.replace(' ', '+')
    url = f"https://www.google.com/search?hl=en&gl=en&q={query}"
    try:
        request_result = requests.get(url)
        request_result.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)

    if request_result is None:
        raise NoRequestResultError("Request result is none")
    else:

        soup = BeautifulSoup(request_result.text, "html.parser")
        # <span class="hgKElc">
        # class="Uo8X3b"
        first_result = soup.find("div", class_='BNeawe')
        if first_result:
            return first_result.text
        else:
            raise NoResultError("Request is none")


def google(q):
    s = requests.Session()
    q = '+'.join(q.split())
    url = f"https://www.google.com/search?hl=en&gl=en&q={q}"

    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'})

    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.find("h2", class_='Uo8X3b').text)

#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re


color = {
        'PURPLE': '\033[95m',
        'CYAN': '\033[96m',
        'DARKCYAN': '\033[36m',
        'BLUE': '\033[94m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'RED': '\033[91m',
        'BOLD': '\033[1m',
        'UNDERLINE': '\033[4m',
        'END': '\033[0m',
        }

available_urls = [
        'https://releases.footshop.com/',
        'https://www.sivasdescalzo.com/en/lifestyle/hot-releases',
        ]

def url_parser(file_name = 'urls.cfg') -> list:
    """
    Function that parses urls file and returns currently selected urls
    """
    urls = []
    try:
        with open(file_name, 'r') as url_file:
            for line in url_file.readlines():
                line = line[:-1]
                if len(line) != 0 and line[0] != '#':
                    urls.append(line)
        return urls
    except FileNotFoundError as e:
        print("A url file was not found!")
        print("Creating one...")
        try:
            with open(file_name, 'w') as url_file:
                url_file.write("# Supported urls, one per line\n")
                url_file.write("# Comment urls out with a single #\n")
                url_file.writelines(available_urls)
            print("File created successfully")
        except Exception as e:
            print("Could not create the file. Please create it manually")
        return urls

def html_parser(url: str) -> BeautifulSoup:
    """
    Function that returns soup of page source from url
    """
    req = requests.get(url);
    response = req.text
    link = BeautifulSoup(response, 'html.parser')
    return link

def pretty_print(sneakers: list, retailer: str) -> str:
    """
    Function that prints raffles from retailer in formatted way
    """
    print(color['BOLD'] + color['UNDERLINE'] + "Raffles from " + retailer 
            + ":" + color['END'])
    for sneaker in sneakers:
        raffle = ""
        colors = ['CYAN', 'DARKCYAN', 'BLUE', 'BOLD']
        i = 0
        for item in sneaker:
            raffle += color[colors[i]]
            i += 1
            raffle += item
            raffle += " - "
        raffle = raffle[:-3]
        raffle += color['END']
        print(raffle)

def footshop_raffle(link: BeautifulSoup) -> list:
    """
    Function that gets the current raffles from FootShop
    """
    sneakers = []
    containers = link.find_all('div', 
            class_=re.compile('container active-or-coming-soon'))
    for container in containers:
        cards = container.find_all('div', class_=re.compile('card.*active'))
        for card in cards:
            sneaker = []
            model = card.find('div', class_=re.compile('model'))
            model = model.get_text()
            sneaker.append(model)
            colorway = card.find('div', class_=re.compile('type'))
            colorway = colorway.get_text()
            sneaker.append(colorway)
            price = card.find('div', class_=re.compile('price'))
            price = price.get_text()
            sneaker.append(price)
            status = card.find('div', class_=re.compile('status'))
            status = status.get_text()
            status += ' '
            timer = card.find('div', class_=re.compile('clearfix timer'))
            parts = timer.find_all('div', class_='part')
            for part in parts:
                elems = part.find_all('div')
                for elem in elems:
                    status += elem.get_text()
                    status += ' '
            sneaker.append(status)
            sneakers.append(sneaker)
    return sneakers

def svd_raffle(link: BeautifulSoup) -> list:
    """
    Function that gets the current raffles from SVD
    """
    sneakers = []
    containers = link.find_all('li', attrs={'class': ['item', 'product']})
    for container in containers:
        state = container.find('span', class_="product-state__tag")
        state = state.get_text()
        if state == "Raffle":
            sneaker = []
            title = container.find('h3', class_="product-card__title")
            title = title.get_text()
            sneaker.append(title)
            name = container.find('a', class_="product-item-link")
            name = name.get_text()
            sneaker.append(name)
            price = container.find('span', class_="price")
            price = price.get_text()
            price = price[1:-2]
            sneaker.append(price)
            sneaker.append(state)
            sneakers.append(sneaker)
    return sneakers

def main():
    """
    Main driver code
    """
    urls = url_parser()
    if urls:
        for i in range(len(urls)):
            link = html_parser(urls[i])
            if i == 0:
                sneakers = footshop_raffle(link)
                pretty_print(sneakers, "FootShop")
            elif i == 1:
                sneakers = svd_raffle(link)
                pretty_print(sneakers, "SVD")

if __name__ == "__main__":
    main()


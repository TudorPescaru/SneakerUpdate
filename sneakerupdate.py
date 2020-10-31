#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import re


def url_parser(file_name = 'urls.cfg') -> list:
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
            f = open(file_name, 'x')
            print("File created successfully. Please add urls")
        except Exception as e:
            print("Could not create the file. Please create it manually")
        return urls

def html_parser(url: str) -> BeautifulSoup:
    req = requests.get(url);
    response = req.text
    link = BeautifulSoup(response, 'html.parser')
    return link

def footshop_raffle(link: BeautifulSoup) -> list:
    sneakers = []
    containers = link.find_all('div', class_=re.compile('container active-or-coming-soon'))
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

def main():
    urls = url_parser()
    if urls:
        link = html_parser(urls[0])
        sneakers = footshop_raffle(link)
        print(sneakers)

if __name__ == "__main__":
    main()


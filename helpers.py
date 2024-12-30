import re
from typing import Generator, Iterator
import requests
import sys

from selectolax.parser import HTMLParser
from loguru import logger
from urllib.parse import urljoin


# 2 loggers: 1 dans un fichier, l'autre dans le terminal, avec des niveaux de log différents.
logger.remove()  # Retire le logger par défaut de loguru
logger.add("books.log",
           level="WARNING",
           rotation="500kb")  # Pas de fichier plus gros que 500kb

logger.add(sys.stderr, level="INFO")  # Ce logger sera affiché dans le terminal

BASE_URL = "https://books.toscrape.com/index.html"


def get_all_books_urls(start_url: str) -> Generator:
    """
    Get all books urls in all pages of catalogue, from start_url.
    :param start_url: url of a catalogue page from which we get books urls 
    :return: generator of all books urls from start url
    """

    with requests.Session() as session:
        while True:
            logger.info(f"Scrap de la page {start_url}...")
            try:
                response = session.get(start_url)
                response.raise_for_status
            except Exception as e:
                logger.error(f"Erreur lors de la requête http sur la page {start_url}: {e}.")
                continue
            tree = HTMLParser(response.text)
            for url in get_all_books_urls_on_page(start_url, tree):
                yield url
            start_url = get_next_page_url(start_url, tree)  # type: ignore
            if not start_url:
                break    


def get_next_page_url(url:str, tree: HTMLParser) -> str| None:
    """
    Get next page url from a given page
    :url: current page url
    :tree: HTMLParser object of the given page
    :return: next page url
    """
    next_page_node = tree.css_first("li.next > a")
    if next_page_node and "href" in next_page_node.attributes:
        return urljoin(url, next_page_node.attributes["href"])
    logger.info(f"Aucun bouton 'next' trouvé sur la page {url}.")
    return None


def get_all_books_urls_on_page(url: str, tree: HTMLParser) -> Iterator:
    """
    Get all books urls on a given page.
    :url: url of the given page
    :tree: HTMLParser object of the given page
    :return: generator of books urls of the page
    """
    try: 
        books_links_nodes = tree.css("h3 > a")
        return (urljoin(url, link.attributes["href"]) for link in books_links_nodes if "href" in link.attributes)
    except Exception as e:
        logger.error(f"Erreur lors de l'extraction des urls des livres sur la page {url}: {e}")
        return iter([]) 


def get_book_price(url: str, session:requests.Session = None) -> float:
    """
    Get the total price for all copies of a book
    :url: book page url
    :return: price of book multiplied by quantity of available copies
    """
    try:
        if session:
            response = session.get(url)
        else:
            response = requests.get(url)
        response.raise_for_status()
        tree = HTMLParser(response.text)
        unit_price = extract_book_price_from_page(tree)
        stock = extract_book_quantity_from_page(tree)
        price_stock = unit_price * stock
        logger.info(f"Montant récupéré sur la page {url}: {price_stock}")
        return price_stock
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la requête HTTP: {e}")
        return 0.0
    

def extract_book_price_from_page(tree: HTMLParser) -> float:
    """ 
    Extract book price from page
    :tree: HTMLParser object of the given page
    :return: price of the book
    """
    price_node = tree.css_first("p.price_color")
    if price_node:
        price_string = price_node.text()
    else:
        logger.error(f"Aucun noeud ne contenantle prix n'a été trouvé.")
        return 0.0
    
    try:
        return float(re.findall(r"\d+\.\d{1,2}", price_string)[0])
    except IndexError as e:
        logger.error(f"La méthode re.findall renvoie une liste vide:{e}")
        return 0.0
    except ValueError as e:
        logger.error(f"Conversion en float impossible: {e}")
        return 0.0


def extract_book_quantity_from_page(tree: HTMLParser) -> int:
    """ 
    Extract book quantity from page
    :tree: HTMLParser object of the given page
    :return: book quantity in stock
    """
    stock_node = tree.css_first("p.instock.availability")

    try:
        return int(re.findall(r"\d+", stock_node.text())[0])
    except AttributeError as e:
        logger.error(f"Aucun noeud p.instock.availability: {e}")
        return 0
    except IndexError as e:
        logger.error(f"La méthode re.findall renvoie une liste vide:{e}")
        return 0
    except ValueError as e:
        logger.error(f"Conversion en int impossible: {e}")
        return 0

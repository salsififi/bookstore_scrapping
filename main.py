"""
BOOKSTORE VALUE
Exercise from the course "Les bases du scrapping" on docstring.fr
Date: 2024-12-30
Author: @salsififi

Entry point
"""

import requests

from helpers import BASE_URL, get_all_books_urls, get_book_price


def main():
    """Get total value of books available in the site"""
    all_books_urls = get_all_books_urls(BASE_URL)
    total_price = []
    with requests.Session() as session:
        for book_url in all_books_urls:
            price = get_book_price(book_url, session)
            total_price.append(price)
    return sum(total_price)


if __name__ == "__main__":
    value = main()
    print(f"\nLa valeur totale de la librairie contenue sur le site '{BASE_URL}' est de:")
    print(f"{value:.2f}£.")

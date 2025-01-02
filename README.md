# BOOKSTORE VALUE
An exercise proposed by Thibault Houdon in the course "Les bases du scrapping" on the website [docstring.fr](https://www.docstring.fr).

## Context
The [books.toscrape.com](https://www.books.toscrape.com) website is a well-known site by beginners in scrapping to practice. 
The aim of the exercise is to get the total value of all available copies of the 1000 books it lists.

## Install
- Clone the repository with `git clone https://github.com/salsififi/bookstore_scrapping.git`.
- Go to the root folder (named "bookstore_value") with the `cd bookstore_value` command.
- Install dependencies with `uv sync`. If you don't have uv installed, create a virtual environnement with `python -m venv .venv`, source it with `source .venv/bin/activate`(on Mac or Linux) or `source .venv/Scripts/activate` (on Windows), then run `pip install -r requirements.txt`.

## Launch
The entry point is the main.py file. Run it with `python main.py`.
The scrap will begin, and you will see INFO logs printed in the terminal. After about 2 minutes, the scrap will end and you will see the total value of available copies of books listed in the whole website.

## Loggers
2 loggers are used:
- the first in the books.log file, for WARNING, ERROR, and CRITICAL levels;
- the second in the terminal, with the same levels and also INFO level.

## Choices
- Parsing: I chose **selectolax** module rather than **beautifulsoup4** to parse html, because selectolax is faster.
- Logging: I chose **loguru** module rather than the standard library **logging** module, because to me loguru is simpler to use.
- Ethical scrapping: as [books.toscrape.com](https://books.toscrape.com) is a solid training ground, I didn't set up a crawl delay nor changed my user agent to indicate a way to contact me. But in real scrapping situation, I would of course have done this.

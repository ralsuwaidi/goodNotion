import os
from pprint import pprint

import click
from dotenv import load_dotenv
from notion_client import Client

from book import Book
from review import Review

load_dotenv()

# get notion and database info
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE"]
REVIEW_NUM = 15
FINISHED_REVIEW = []


@click.command()
@click.option('--books', help='file with books saved as json list')
@click.option('--reviews', help='file with reviews saved as json list')
@click.option('--status', help='status to save in notion database')
def push_books(books, status, reviews):

    # get books and reviews
    file_books = Book.get_books_from_file(books, status, notion, database_id)
    notion_books = Book.get_books_from_notion(notion, database_id)
    review_file = Review.parse_reviews(reviews)

    print(f'found {len(file_books)} notion books')

    for book in file_books:
        should_add = True
        for notion_book in notion_books:
            if book.title.lower() == notion_book.title.lower():
                should_add = False
                print(f'skipping {book.title}, already exists')

        if should_add:
            book_id = book.add_book()
            book.add_metadata()
            print('added book: ', book.title)
            print(f'adding reviews for', book.title)
            book_endpoint = get_endpoint(book.url)
            rev_num = REVIEW_NUM
            for review in review_file:
                if book_endpoint == review.book_id_title and book_endpoint not in FINISHED_REVIEW:
                    review.notion = book.notion
                    review.book_id = book_id
                    review.add_review()
                    rev_num -= 1
                    if rev_num == 0:
                        FINISHED_REVIEW.append(book_endpoint)
            print('finished adding reviews for', book.title)


def get_endpoint(url) -> str:
    return url.replace('https://www.goodreads.com/book/show/', '')


if __name__ == '__main__':
    push_books()

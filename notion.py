import os
from notion_client import Client
from pprint import pprint
from dotenv import load_dotenv
from review import Review
from book import Book

load_dotenv()
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE"]


# books = Book.get_books(notion, database_id)
file_books = Book.get_books_from_file('rashed.jl', 'Finished', notion, database_id)
notion_books = Book.get_books_from_notion(notion, database_id)
reviews = Review.parse_reviews('all_reviews.json')

for book in file_books:
    should_add = True
    for notion_book in notion_books:
        if book.title == notion_book.title:
            should_add = False
            print(f'{book.title} already added')

    if should_add:
        print('adding', book)
        book_id = book.add_book()
        for review in reviews:
            if book.title == review.book_title:
                review.notion = book.notion
                review.book_id = book_id
                print(f'adding {review.user_name} comments to {review.book_title}...')
                review.add_review(book.json_str)


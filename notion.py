import os
from notion_client import Client
from pprint import pprint
from dotenv import load_dotenv
from review import Review
from book import Book

load_dotenv()
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE"]



# book = Book(
#     title='testtitle',
#     author='william',
#     status='Unread',
#     category='History',
#     rating=2,
#     cover='https://images.unsplash.com/photo-1660860551412-a93c5026b034?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwzfHx8ZW58MHx8fHw%3D&auto=format&fit=crop&w=500&q=60',
#     release_date='date',
#     notion=notion,
#     database_id=database_id
# )

# book_id = book.add_book()

# review = Review("this is thess review", "https://review.ssl",
#                 "2022", 4, "Ann", notion, book_id)

# review.add_review()


# books = Book.get_books(notion, database_id)
file_books = Book.get_books_from_file('rashed.jl', 'Finished', notion, database_id)
notion_books = Book.get_books_from_notion(notion, database_id)
reviews = Review.parse_reviews('all_reviews.json')
# for file_book in file_books:
#     for notion_book in notion_books:
#         if file_book.title == notion_book.title:
#             print(file_book.cover)

for book in file_books:
    print('adding', book)
    book_id = book.add_book()
    for review in reviews:
        if book.title == review.book_title:
            review.notion = book.notion
            review.book_id = book_id
            print(f'adding {review.user_name} comments to {review.book_title}...')
            review.add_review()
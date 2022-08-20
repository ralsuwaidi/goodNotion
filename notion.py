import os
from notion_client import Client
from pprint import pprint
from dotenv import load_dotenv
from review import Review
from book import Book

load_dotenv()
notion = Client(auth=os.environ["NOTION_TOKEN"])
database_id = os.environ["NOTION_DATABASE"]


# my_database = notion.databases.query(
#     **{
#         "database_id": os.environ["NOTION_DATABASE"],
#         "filter": {
#             "property": "Title",
#             "rich_text": {
#                 "contains": "Lord of the Flies",
#             },
#         },
#     }
# )


# my_page = notion.pages.retrieve(**{
#     "page_id": "069ab1b5b0f7491a9ab0b1837e552da3",
# })


book = Book(
    title='testtitle',
    author='william',
    status='Unread',
    category='History',
    rating=2,
    cover='https://images.unsplash.com/photo-1660860551412-a93c5026b034?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxlZGl0b3JpYWwtZmVlZHwzfHx8ZW58MHx8fHw%3D&auto=format&fit=crop&w=500&q=60',
    release_date='date',
    notion=notion,
    database_id=database_id
)

page_id = book.add_book()

review = Review("this is thess review", "https://review.ssl",
                "2022", 4, "Ann", notion, page_id)

review.add_review()
# pprint(my_page)

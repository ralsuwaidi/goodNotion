from dataclasses import dataclass
import notion_client
from pprint import pprint
import json


@dataclass
class Book:
    # title, author, status, category, rating, cover, release_date=None, store_link=None
    title: str
    author: str
    status: dict
    category: str
    rating: int
    cover: str
    release_date: str
    url: str
    notion: notion_client.Client
    database_id: str
    book_id: str = None
    json_str: str = None

    STATUS = {
        "Up Next": "yellow",
        "Unread": "blue",
        "Now Reading": "red",
        "Finished": "green",
        "Unfinished": "brown",
    }

    RATING = [
        '★',
        '★★',
        '★★★',
        '★★★★',
        '★★★★★',
    ]

    def add_book(self):
        response = self.notion.pages.create(**{
            "parent": {
                "database_id": self.database_id
            },
            'cover': {'external': {'url': self.cover},
                      'type': 'external'},
            "properties": {
                "title": {
                    "title": [
                        {
                            "text": {
                                "content": self.title
                            }
                        }
                    ]
                },
                'Author': {
                    'id': 'bee%3D',
                    'rich_text': [{'annotations': {'bold': False,
                                                   'code': False,
                                                   'color': 'default',
                                                   'italic': False,
                                                   'strikethrough': False,
                                                   'underline': False},
                                   'href': None,
                                   'plain_text': self.author,
                                   'text': {'content': self.author,
                                            'link': None},
                                   'type': 'text'}],
                    'type': 'rich_text'},
                'Status': {'id': '%3EPAR',
                           'select': {'color': self.STATUS[self.status],
                                      'name': self.status},
                           'type': 'select'},
                'Category': {'id': 'ubSU',
                             'select': {
                                 'name': self.category},
                             'type': 'select'},
                'Rating': {'id': '%5C%40EI',
                           'select': {'color': 'gray',
                                      'name': self.RATING[self.rating-1]},
                           'type': 'select'},
                'Release Date': {'date': {'end': None,
                                          'start': self.release_date[:10],
                                          'time_zone': None},
                                 'type': 'date'},
                'Store Link': {'type': 'url',
                               'url': self.url},

            },
        })

        return response['id']

    @classmethod
    def get_books_from_notion(cls, notion, database_id):

        library = notion.databases.query(
            **{
                "database_id": database_id,
            }
        )

        book_list = []
        for book in library['results']:
            title = book['properties']['Title']['title'][0]['text']['content']
            book_id = book['id']
            try:
                author = book['properties']['Author']['rich_text'][0]['plain_text']
            except:
                author = ''
            try:
                status = book['properties']['Status']['select']['name']
            except:
                status = ''
            try:
                category = book['properties']['Category']['select']['name']
            except:
                category = ''

            try:
                rating = book['properties']['Rating']['select']['name']
            except:
                rating = ''

            try:
                cover = book['cover']['external']['url']
            except:
                cover = ''
            try:
                url = book['Store Link']['url']
            except:
                url = ''

            book_instance = Book(
                title=title,
                author=author,
                status=status,
                category=category,
                rating=len(rating),
                cover=cover,
                release_date='date',
                url=url,
                notion=notion,
                database_id=database_id,
                book_id=book_id
            )

            book_list.append(book_instance)

        return book_list

    @classmethod
    def get_books_from_file(cls, file, status, notion, database_id, book_id=None):
        f = open(file)
        json_data = json.load(f)
        book_list = []

        for book_data in json_data:
            book = Book(
                title=book_data['title'],
                author=book_data['author'],
                status=status,
                category=book_data['genres'][0],
                rating=round(book_data['avg_rating']),
                cover=book_data['cover'],
                release_date=book_data['publish_date'],
                url=book_data['url'],
                notion=notion,
                database_id=database_id,
                book_id=book_id,
                json_str=book_data
            )

            book_list.append(book)

        return book_list


if __name__ == '__main__':

    books = Book.get_books_from_file('rashed.jl', 'd', 'd', 'd')[0].title
    print(books)

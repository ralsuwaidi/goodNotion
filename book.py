from dataclasses import dataclass
import notion_client
from pprint import pprint

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
    notion: notion_client.Client
    database_id: str

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
                             'select': {'color': 'default',
                                        'name': self.category},
                             'type': 'select'},
                'Rating': {'id': '%5C%40EI',
                           'select': {'color': 'gray',
                                      'name': self.RATING[self.rating-1]},
                           'type': 'select'},

            },
        })

        return response['id']

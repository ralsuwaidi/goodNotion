from dataclasses import dataclass
from typing_extensions import reveal_type
import notion_client
import json


@dataclass
class Review:
    """Class for keeping track of an item in inventory."""
    review: str
    review_url: str
    book_title: str
    date: str
    rating: float
    user_name: str
    notion: notion_client.Client = None
    book_id: str = None

    def add_review(self, json_str=None):

        review_title = ''
        if len(self.review) > 50:
            review_title = self.review[:50] + '...'
        else:
            review_title = self.review




        children = [
            {
                "heading_2": {
                    "rich_text": [
                        {
                            "text": {
                                "content": review_title
                            }
                        }
                    ]
                }
            },
            {
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Rating: " + str(self.rating),
                            },
                            "annotations": {
                                "bold": True,
                            }
                        }
                    ]
                }
            },
            {
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "User: " + self.user_name,
                            },
                            "annotations": {
                                "bold": True,
                            }
                        }
                    ]
                }
            },
            {
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": self.review[:1990],
                            }
                        }
                    ]
                }
            }
        ]

        if json_str is not None:
            metadata = {
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": str(json_str['avg_rating']),
                            }
                        }
                    ]
                }
            }

            children.insert(0, metadata)

        response = self.notion.blocks.children.append(**{
            "block_id": self.book_id,
            'children': children
        })

    @classmethod
    def parse_reviews(cls, file):
        f = open(file)
        json_review = json.load(f)
        review_list = []

        for item in json_review:
            review = Review(
                review=item['text'],
                review_url=item['review_url'],
                date=item['date'],
                rating=item['rating'],
                user_name=item['user_name'],
                book_title=item['book_title'],
            )

            review_list.append(review)

        return review_list


if __name__ == '__main__':

    review = Review.parse_reviews('all_reviews.json')

from dataclasses import dataclass
from tkinter.ttk import Style
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

    def add_review(self):

        review_title = ''
        if len(self.review) > 70:
            review_title = self.review[:70] + '...'
        else:
            review_title = self.review

        children = [
            self.child_paragraph(review_title, style='heading_2'),
            self.child_paragraph("User Rating: " + str(self.rating), bold=True),
            self.child_paragraph("User Name: " + self.user_name, bold=True),
            self.child_paragraph(self.review[:1980])
        ]

        response = self.notion.blocks.children.append(**{
            "block_id": self.book_id,
            'children': children
        })

    def child_paragraph(self, text, style='paragraph', bold=False):
        return {
            style: {
                "rich_text": [
                    {
                        "text": {
                            "content": text,
                        },
                        "annotations": {
                            "bold": bold,
                        }
                    }
                ]
            }
        }



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

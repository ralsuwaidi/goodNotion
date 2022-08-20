from dataclasses import dataclass
import notion_client

@dataclass
class Review:
    """Class for keeping track of an item in inventory."""
    review: str
    review_url: str
    date: str
    rating: float
    user_name: str
    notion: notion_client.Client
    page_id: str

    def add_review(self):


            review_title = ''
            if len(self.review) >20:
                review_title = self.review[20:] + '...'
            else:
                review_title = self.review

            response = self.notion.blocks.children.append(**{
                "block_id": self.page_id,
                'children': [
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
                                        "content": self.review,
                                    }
                                }
                            ]
                        }
                    }
                ],
            })

            
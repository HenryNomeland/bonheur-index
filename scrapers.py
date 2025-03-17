from base_classes import ArtReview, ArtScraper
import requests
from bs4 import BeautifulSoup
import pandas as pd


class ArtForumScraper(ArtScraper):
    def scrape(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            promotion_widget = soup.find(
                "div", attrs={"data-component": "promotion-widget"}
            )
            if promotion_widget:
                date_text = promotion_widget.find(
                    "div", attrs={"data-alias": "promotion__primary-text"}
                ).get_text(strip=True)
            cards = soup.find_all("div", attrs={"data-alias": "card__inner"})
            reviews = []
            for card in cards:
                print(card)
                try:
                    city_text = card.find(
                        "div", attrs={"data-alias": "card__location"}
                    ).get_text(strip=True)
                    title_div = card.find(
                        "div", attrs={"data-alias": "card__card-title"}
                    )
                    title_text = title_div.get_text()
                    if title_text[0] == "“":
                        artwork_text = title_text[1:-1]
                        artist_text = "Unknown Artist"
                    else:
                        artist_text = title_text
                        artwork_text = "Unknown Artwork"
                    title_url = title_div.find("a")["href"]
                    review = ArtReview(
                        date=date_text,
                        artist=artist_text,
                        artwork=artwork_text,
                        city=city_text,
                        url=title_url,
                    )
                    reviews.append(review.to_dict())
                    print(f"No Attribute Error - {card}")
                except AttributeError:
                    print(f"Attribute Error - {card}")
                    continue
            self.data = pd.DataFrame(reviews)
        else:
            print(
                f"Failed to get the page - {self.url} - Status code - {response.status_code}"
            )

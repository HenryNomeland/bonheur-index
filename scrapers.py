from base_classes import ArtReview, ArtScraper
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import string
import traceback


class ArtForumScraper(ArtScraper):
    def _get_content_div(self, title_url):
        content_response = requests.get(title_url)
        if content_response.status_code == 200:
            content_soup = BeautifulSoup(content_response.text, "html.parser")
            content_div = content_soup.find("div", attrs={"class": "_main_10r4d_1"})
            if content_div:
                return content_div
            else:
                return "NA"
        else:
            return "NA"

    def _get_review_attributes(self, card, date):
        title_div = card.find("div", attrs={"data-alias": "card__card-title"})
        review = ArtReview(url=title_div.find("a")["href"], date=date)
        title_text = title_div.get_text()
        if title_text[0] == "“":
            review.artwork = title_text[1:-1]
            review.artist = "NA"
        else:
            review.artist = title_text
            review.artwork = "NA"
        div = self._get_content_div(review.url)
        if div == "NA":
            return review
        para_list = []
        for para in div.find_all("p"):
            para_list.append(para.get_text())
        review.content = " ".join(para_list)
        review.city = div.find(
            "div", attrs={"data-alias": "article-header__location"}
        ).get_text(strip=True)
        locations = div.find_all("div", attrs={"data-alias": "article-header__venue"})
        location_list = []
        for location in locations:
            location_list.append(location.get_text(strip=True))
        review.location = ", ".join(location_list)
        review.reviewer = div.find("div", attrs={"data-theme": "byline-lg"}).get_text()
        img_tag = div.find("img")
        img_link = img_tag["src"]
        img_name = img_tag["alt"].rstrip(string.punctuation)
        review.img_path = os.path.join(
            ".", "images", "ArtForum", review.date, f"{img_name}.jpg"
        )
        if not os.path.exists(review.img_path):
            try:
                os.makedirs(os.path.dirname(review.img_path), exist_ok=True)
                response = requests.get(img_link, stream=True)
                response.raise_for_status()
                with open(review.img_path, "wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Image Downloaded - {img_name}")
            except Exception as e:
                print(f"Image download failed - {img_name}")
                print(e)
        else:
            print(f"Already Downloaded - {img_name}")
        return review

    def scrape(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.find_all("div", attrs={"data-alias": "card__inner"})
            promo_widget = soup.find(
                "div", attrs={"data-component": "promotion-widget"}
            )
            if promo_widget:
                date = promo_widget.find(
                    "div", attrs={"data-alias": "promotion__primary-text"}
                ).get_text(strip=True)
            reviews = []
            for card in cards:
                try:
                    review = self._get_review_attributes(card, date)
                    reviews.append(review.to_dict())
                except Exception as e:
                    continue
            self.data = pd.DataFrame(reviews)
        else:
            print(
                f"Failed to get the page - {self.url} - Status code - {response.status_code}"
            )

import pandas as pd
from datetime import datetime
from abc import ABC, abstractmethod
import dateparser
import re


class ArtReview:
    def __init__(
        self,
        title="NA",
        reviewer="NA",
        date="NA",
        content="NA",
        artist="NA",
        artwork="NA",
        location="NA",
        city="NA",
        img_path="NA",
        url="NA",
    ):
        self.title = title
        self.reviewer = reviewer
        self.date = date
        self.content = content
        self.artist = artist
        self.artwork = artwork
        self.location = location
        self.city = city
        self.img_path = img_path
        self.url = url

    def format_title(self, title):
        return title.strip().title() if title != "NA" else "NA"

    def format_date(self, date):
        try:
            parsed_date = dateparser.parse(
                date, settings={"PREFER_DAY_OF_MONTH": "first"}
            )
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return "NA"

    def format_reviewer(self, reviewer):
        return re.sub(r"^by\s+", "", reviewer, flags=re.IGNORECASE).strip()

    def format_content(self, content):
        return " ".join(content.split())

    def to_dict(self):
        return {
            "Title": self.format_title(self.title),
            "Reviewer": self.format_reviewer(self.reviewer),
            "Date": self.format_date(self.date),
            "Content": self.format_content(self.content),
            "Artist": self.artist,
            "Artwork": self.artwork,
            "Location": self.location,
            "City": self.city,
            "Image": self.img_path,
            "URL": self.url,
        }


class ArtScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.data = pd.DataFrame()

    @abstractmethod
    def scrape(self):
        pass

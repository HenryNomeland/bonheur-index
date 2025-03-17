import pandas as pd
from datetime import datetime
from abc import ABC, abstractmethod
import dateparser


class ArtReview:
    def __init__(
        self,
        title="Untitled Review",
        reviewer="Unknown Reviewer",
        date="Unknown Date",
        content="Inaccessible Content",
        artist="Unknown Artist",
        artwork="Unknown Artwork",
        location="Unknown Location",
        city="Unknown City",
        url="",
    ):
        self.title = self.format_title(title)
        self.reviewer = reviewer
        self.date = self.format_date(date)
        self.content = self.format_content(content)
        self.artist = artist
        self.artwork = artwork
        self.location = location
        self.city = city
        self.url = url

    def format_title(self, title):
        return title.strip().title() if title else "Untitled Review"

    def format_date(self, date):
        try:
            print(date)
            parsed_date = dateparser.parse(
                date, settings={"PREFER_DATES_OF_MONTH": "first"}
            )
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            return "Unknown Date"

    def format_content(self, content):
        return " ".join(content.split()) if content else ""

    def to_dict(self):
        return {
            "Title": self.title,
            "Reviewer": self.reviewer,
            "Date": self.date,
            "Content": self.content,
            "Artist": self.artist,
            "Artwork": self.artwork,
            "Location": self.location,
            "City": self.city,
            "URL": self.url,
        }


class ArtScraper(ABC):
    def __init__(self, url):
        self.url = url
        self.data = pd.DataFrame()

    @abstractmethod
    def scrape(self):
        pass

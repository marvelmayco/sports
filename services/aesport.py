from helpers import get_base_url
from bs4 import BeautifulSoup
from . import BaseService
import requests


class AESport(BaseService):
    def __init__(self) -> None:
        super().__init__(
            SERVICE_NAME="AESport",
            SERVICE_URL="https://aesport.tv/live-tv.html",
        )

    def _get_data(self) -> dict:
        soup = BeautifulSoup(self._get_src(), "html.parser")

        channels_data = []

        sections_divs = soup.select(".section-focus")
        for section_div in sections_divs:
            group = section_div.select_one(".head-bar .left").text.strip()
            channels_divs = section_div.select(".content a")
            for channel_div in channels_divs:
                name = channel_div.select_one(".channel-name").text.strip()
                logo = channel_div.select_one("img.hide").get("src")
                html_url = channel_div.get('href')
                response = requests.get(html_url)
                soup = BeautifulSoup(response.content, "html.parser")
                data_urls = [a.get("data-url") for a in soup.find_all("a", {"data-url": True})]
                for data_url in data_urls:
                    stream_url = data_url
                channels_data.append({
                    "name": name,
                    "logo": logo,
                    "group": group,
                    "stream-url": stream_url,
                    "headers": {
                        "referer": get_base_url(stream_url) + "/",
                        "user-agent": self.USER_AGENT
                    }
                })

        return channels_data

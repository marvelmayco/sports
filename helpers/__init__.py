import re
from difflib import get_close_matches
from urllib.parse import urlparse
from typing import List, Dict
from datetime import datetime
from jinja2 import Template
import json
import os

PLAYLISTS_DIR = "playlists"
RESOURCES_DIR = "helpers/res"


def get_base_url(url: str) -> str:
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + "://" + parsed_url.netloc
    return base_url


def generate_playlist(service_name: str, data: List[Dict[str, Dict]]) -> str:
    playlist_data = []
    for channel in data:
        channel_info = {
            "name": channel.get("name"),
            "logo": channel.get("logo"),
            "group": channel.get("group"),
            "url": channel.get("stream-url"),
            "headers": channel.get("headers", {})
        }

        playlist_data.append(channel_info)

    return json.dumps(playlist_data, indent=4)


def get_logo_url(channel_name: str) -> str:
    logo_data = json.load(
        open(os.path.join("helpers", "res", "logo-fraudiay.json"), encoding="utf-8"))

    logo_tree = logo_data.get("tree", [])

    logo_paths = [logo.get("path", "")
                  for logo in logo_tree if ".png" in logo.get("path", "")]
    logo_names = [logo_path.split(
        "/")[-1] if "/" in logo_path else "" for logo_path in logo_paths]

    channel_logo_matches = get_close_matches(
        channel_name, logo_names, cutoff=0.5)
    channel_logo_path = logo_paths[logo_names.index(
        channel_logo_matches[0])] if channel_logo_matches else None

    if channel_logo_path:
        return f"https://raw.githubusercontent.com/fraudiay79/logos/master/{channel_logo_path}"

    return None

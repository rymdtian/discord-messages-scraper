import requests
import json
import sys
import os 
import pathlib
from typing import List
from dotenv import dotenv_values


# scrape messsages in discord dms & channels
class Scraper:

    __DISCORD_AUTHORIZATION_TOKEN = dotenv_values(os.path.join(
        pathlib.Path(__file__).parent.resolve(), "private/.env"))["DISCORD_AUTHORIZATION_TOKEN"]
    __LIMIT_PER_REQUEST = 100

    def __init__(self, channel_id: str):
        self.__channel_id = channel_id
        self.__discord_api_url = f"https://discord.com/api/v9/channels/{self.__channel_id}/messages"

    def retrieve_messages(self, max_calls: int = 5):
        print(f"Retrieving messages from channel {self.__channel_id}\n")
        headers = {
            "authorization": Scraper.__DISCORD_AUTHORIZATION_TOKEN
        }
        params = {
            "limit": Scraper.__LIMIT_PER_REQUEST
        }
        request = requests.get(self.__discord_api_url, params=params, headers=headers)
        response_json = json.loads(request.text)
        recent_message_id: int = -1
        for value in response_json:
            if "author" not in value:
                break
            print(f'{value["author"]["username"]}: {value["content"]}')
            recent_message_id = int(value["id"])

        calls_count: int = 1
        reached_end: bool = False
        while recent_message_id != -1 and (max_calls == 0 or calls_count < max_calls) and not reached_end:
            params["before"] = recent_message_id
            request = requests.get(self.__discord_api_url, params=params, headers=headers)
            response_json = json.loads(request.text)
            for value in response_json:
                if "author" not in value:
                    reached_end = True
                    break
                print(f'{value["author"]["username"]}: {value["content"]}')
                recent_message_id = int(value["id"])
            calls_count += 1

        print(f"\nFinished retrieving messages from channel {self.__channel_id}\n")


# get channel ids from argv
def get_channel_ids() -> List[str]:
    channel_ids = [id.strip() for id in sys.stdin.readlines()]
    return channel_ids


if __name__ == "__main__": 
    channel_ids = get_channel_ids()
    scrapers: List[Scraper] = []
    for channel_id in channel_ids:
        if channel_id.startswith("#"):
            continue
        scrapers.append(Scraper(channel_id=channel_id))
    max_calls = 0
    for scraper in scrapers:
        scraper.retrieve_messages(max_calls=max_calls)
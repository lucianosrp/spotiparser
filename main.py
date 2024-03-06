from typing import Any
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "https://api.spotify.com/v1"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TOKEN = os.getenv("TOKEN")


def get_token() -> str:
    url = "https://accounts.spotify.com/api/token"
    payload = f"grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise requests.exceptions.HTTPError(
            f"Got status {response.status_code}\n{response.text}"
        )


def search(q: str, token: str | None = None):
    url = f"{API_URL}/search"
    token_ = token if token else TOKEN
    querystring = {"q": q, "type": "track", "market": "US"}
    headers = {
        "Authorization": f"Bearer {token_}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        raise requests.exceptions.HTTPError(
            f"Got status {response.status_code}\n{response.text}"
        )


def get_artists_name(artists: list[dict[str, Any]]) -> list[str]:
    return [a["name"] for a in artists]


class TrackResult(BaseModel):
    name: str
    artists: list[str]
    url: str
    api_url: str

    @classmethod
    def load(cls, data: dict[str, Any]):
        return cls(
            name=data["name"],
            artists=get_artists_name(data["artists"]),
            url=data["external_urls"]["spotify"],
            api_url=data["href"],
        )


def get_track_results(q: str, token: str | None = None) -> list[TrackResult]:
    s = search(q, token)
    return [TrackResult.load(data=i) for i in s["tracks"]["items"]]


def get_from_file(fp: str, token: str | None = None) -> list[TrackResult]:
    with open(fp) as f:
        qs = f.readlines()

    results = []

    for q in qs:
        if (query := q.strip()) != "":
            results.append(get_track_results(query, token)[0])

    return results


def save_to_file(fp: str, results: list[TrackResult]):
    with open(fp, "w") as f:
        for t in results:
            artists = ", ".join(t.artists)
            s = f"{t.name} - {artists}\n{t.url}\n\n"
            print(f"Found: {t.name} - {artists}")
            f.write(s)


if __name__ == "__main__":
    file_path = "songs.txt"
    r = get_from_file(file_path)
    save_to_file("parsed.txt", r)

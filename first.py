from riotwatcher import LolWatcher, ApiError
from pathlib import Path


def fetch_key(filename):
    p = Path(filename)

    with open(p) as f:
        key = f.readline().strip()

    if not key:
        raise ValueError(f"Empty api key file ({p})")

    return key


def main():
    api_key = fetch_key("riot_api_key.txt")

    lol_watcher = LolWatcher(api_key)
    region = "euw1"

    print(lol_watcher.summoner.by_name(region, 'spyr03'))


if __name__ == "__main__":
    main()
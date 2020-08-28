from riotwatcher import LolWatcher
from pathlib import Path


def fetch_key(filename):
    p = Path(filename)

    with open(p) as f:
        key = f.readline().strip()

    if not key:
        raise ValueError(f"Empty api key file ({p})")

    return key


def is_interesting(key):
    return key not in ("version", "x", "y")


def _keep_interesting(data):
    if isinstance(data, (str, int, float)):
        return data

    new_data = dict()
    for k, v in data.items():
        # Base case
        if isinstance(v, (str, int, float)):
            if is_interesting(k):
                new_data[k] = v
        elif isinstance(v, list):
            if is_interesting(k):
                new_data[k] = [_keep_interesting(vv) for vv in v]
        elif isinstance(v, dict):
            new_data[k] = _keep_interesting(v)
        else:
            raise ValueError("Don't understand this")

    return new_data


def keep_interesting(original_data):
    return _keep_interesting(original_data)


def champion_differences(lol_watcher, old_version, new_version):
    dd = lol_watcher.data_dragon

    old_data = dd.champions(old_version)
    new_data = dd.champions(new_version)

    old_data = keep_interesting(old_data)
    new_data = keep_interesting(new_data)

    return old_data, new_data


def main():
    api_key = fetch_key("riot_api_key.txt")

    lol_watcher = LolWatcher(api_key)

    old, new = champion_differences(lol_watcher, "10.5.1", "10.16.1")

    import json
    with open("old.json", 'w+') as f:
        json.dump(old, f, indent=4, sort_keys=True)

    with open("new.json", 'w+') as f:
        json.dump(new, f, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()

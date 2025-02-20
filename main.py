import json
import statistics
from collections import Counter

import emoji
import requests
from prettytable import PrettyTable

MATRIX_SERVER = "https://matrix-client.matrix.org"


def get_displayname(user_id: str) -> str:
    url = f"{MATRIX_SERVER}/_matrix/client/r0/profile/{user_id}"

    r = requests.get(url=url, timeout=10)
    data = r.json()

    return data["displayname"]


with open("export.json", "r") as f:
    export = json.load(f)

with open("names.json", "r") as f:
    names = json.load(f)

tally: dict[str, list] = {}

counted_events = [
    "m.room.message",
    "m.sticker",
    "m.image",
    "m.room.encrypted",
    "org.matrix.msc3381.poll.start",
]

for event in export["messages"]:
    t = event["type"]
    if t not in counted_events:
        # print(f"Not counting event with type: {t}")
        continue

    sender: str = event["sender"]

    if sender not in tally:
        tally[sender] = []

    if sender not in names:
        print(f"Requesting name for {sender}...")
        names[sender] = get_displayname(sender)

    tally[sender].append(event)

with open("names.json", "w+", encoding="utf8") as f:
    json.dump(names, f, indent=2)

count = dict(sorted(tally.items(), key=lambda item: len(item[1]), reverse=True))
total_count = sum([len(e) for e in count.values()])

table = PrettyTable(
    [
        "Name",
        "Messages",
        "Images",
        "Stickers",
        "Percentage",
        "Mean length",
        "Top emojis",
    ]
)


for yapper, events in count.items():
    name = names[yapper]

    messages = len(events)

    n_images = len([e for e in events if e["content"].get("msgtype") == "m.image"])
    n_stickers = len([e for e in events if e["type"] == "m.sticker"])

    percent = f"{round(len(events) / total_count * 100, 2)} %"
    mean_length = round(
        statistics.mean(
            [
                len((e["content"]["body"]).split())
                for e in events
                if "body" in e["content"]
            ]
        ),
        2,
    )

    emoji_list = [
        c
        for c in "".join([e["content"].get("body") or "" for e in events])
        if emoji.is_emoji(c)
    ]
    emojis = Counter(emoji_list)
    top_emojis = "".join([emoji[0] for emoji in emojis.most_common(3)])

    row = (name, messages, n_images, n_stickers, percent, mean_length, top_emojis)
    table.add_row(row)


print(table)
print(f"Messages in total: {total_count}")

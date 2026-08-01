import json
from pathlib import Path


memory_file = Path(
    "brain/visual_memory/learned_memory.json"
)


data = json.loads(
    memory_file.read_text(
        encoding="utf-8"
    )
)


unique = {}

for item in data:

    image = item.get("image")

    if image not in unique:
        unique[image] = item


cleaned = list(
    unique.values()
)


memory_file.write_text(
    json.dumps(
        cleaned,
        indent=4,
        ensure_ascii=False
    ),
    encoding="utf-8"
)


print(
    "Before:",
    len(data)
)

print(
    "After:",
    len(cleaned)
)
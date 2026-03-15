import re
import os

project_root = r"c:\Users\ht24a072\Documents\GitHub\child_security_project\child_security_project"
dirs_to_scan = [
    os.path.join(project_root, "game"),
    os.path.join(project_root, "game/events/stranger"),
    os.path.join(project_root, "game/minigames"),
]

kanji_pattern = re.compile(r'[一-龠]+')
all_kanji = set()

for d in dirs_to_scan:
    if not os.path.exists(d): continue
    for filename in os.listdir(d):
        if filename.endswith(".rpy") or filename.endswith(".json"):
            with open(os.path.join(d, filename), 'r', encoding='utf-8') as f:
                content = f.read()
                matches = kanji_pattern.findall(content)
                for m in matches:
                    all_kanji.add(m)

print("FOUND_KANJI_START")
for k in sorted(list(all_kanji), key=len, reverse=True):
    print(k)
print("FOUND_KANJI_END")

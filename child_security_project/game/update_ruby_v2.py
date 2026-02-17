
import re
import os
import sys

# Use relative path to avoid hardcoding user directory if possible, or robust absolute path
file_path = 'game/mapdata.json'
if not os.path.exists(file_path):
    # Fallback to the hardcoded path if running from root isn't working as expected
    file_path = 'c:/Users/hk624/github/child_security_project/child_security_project/game/mapdata.json'

print(f"Target file: {file_path}")

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Debug: print sample of content before
    print("Content length before:", len(content))

    # Pattern: Kanji followed by (Kana) or （Kana）
    pattern = r'([一-龠]+)[（\(]([ぁ-んァ-ヶー]+)[）\)]'
    replacement = r'{rb}\1{/rb}{rt}\2{/rt}'

    new_content, count = re.subn(pattern, replacement, content)
    
    print(f"Replaced {count} occurrences.")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("Successfully updated mapdata.json")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

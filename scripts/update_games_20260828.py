import os
import json

GAME_ROOT = r"D:\workspace\projects\active\jangyoon-s-game"
GAMES_JSON = os.path.join(GAME_ROOT, "games.json")

NEW_GAMES = [
    {
        "id": "turtle-bubble-rescue",
        "title": "Turtle Bubble Rescue",
        "title_ko": "🐢 바다거북 비눗방울 구출",
        "description": "바다거북을 비눗방울로 구출하는 게임입니다.",
        "thumbnail": "turtle-bubble-rescue/thumb.svg",
        "path": "turtle-bubble-rescue/index.html"
    },
    {
        "id": "cosmic-star-baker",
        "title": "Cosmic Star Baker",
        "title_ko": "⭐ 우주 별모양 제빵사",
        "description": "우주에서 별모양 빵을 굽는 게임입니다.",
        "thumbnail": "cosmic-star-baker/thumb.svg",
        "path": "cosmic-star-baker/index.html"
    }
]

def update_games_json():
    with open(GAMES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    existing_ids = {g["id"] for g in data}
    to_add = [g for g in NEW_GAMES if g["id"] not in existing_ids]
    
    if not to_add:
        print("All games already exist in games.json.")
        return len(data)
        
    new_data = to_add + data
    with open(GAMES_JSON, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"Added {len(to_add)} games to games.json")

update_games_json()

with open(os.path.join(GAME_ROOT, "README.md"), "a", encoding="utf-8") as f:
    f.write("\n- 2026-08-28: `turtle-bubble-rescue`, `cosmic-star-baker` 추가됨\n")

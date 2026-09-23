# -*- coding: utf-8 -*-
"""
generate_batch.py — content_data.py dagi matnlardan rasm kartochkalar yasaydi
va har bir kanal uchun channels/<kanal>/posts.json navbat faylini tayyorlaydi.

Ishlatish:
    python generate_batch.py
"""

import json
import os
from make_card import create_card
from content_data import CHANNELS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

for channel, posts in CHANNELS.items():
    ch_dir = os.path.join(BASE_DIR, "channels", channel)
    img_dir = os.path.join(ch_dir, "images")
    os.makedirs(img_dir, exist_ok=True)

    queue = []
    for i, post in enumerate(posts, start=1):
        img_filename = f"{i:03d}.png"
        img_path = os.path.join(img_dir, img_filename)

        create_card(
            text=post["hook"],
            out_path=img_path,
            theme=channel,
            emoji=post["emoji"],
        )

        queue.append({
            "image": os.path.join("images", img_filename),
            "caption": post["caption"],
        })

    posts_json_path = os.path.join(ch_dir, "posts.json")
    with open(posts_json_path, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

    print(f"{channel}: {len(queue)} post tayyor -> {posts_json_path}")

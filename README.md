# Telegram Auto-Post Bot

A Python bot that automatically publishes scheduled posts, each with a generated image card, to four educational Telegram channels. It runs without any paid APIs: posts are prepared in advance, rendered into image cards, and delivered on a schedule.

## Channels

| Channel | Topic |
|---|---|
| [@math_Olimjon](https://t.me/math_Olimjon) | Mathematics |
| [@faktura_uzb](https://t.me/faktura_uzb) | World facts |
| [@matematika_milliy_yahyobek](https://t.me/matematika_milliy_yahyobek) | National exam–level mathematics |
| [@fizika_milliy_yahyobek](https://t.me/fizika_milliy_yahyobek) | National exam–level physics |

## Features

- **Scheduled posting**: each channel has its own posting times (currently 2 posts per day).
- **Generated image cards**: every post gets a styled image card built with Pillow, with a separate color theme per channel.
- **Persistent queue**: `state.json` remembers the last post sent, so after a restart the bot continues where it stopped instead of starting over.
- **One codebase, many channels**: each channel runs as a separate instance with its own config file.
- **Logging**: daily activity is written to log files, with a warning when a channel's queue runs out.

## How it works

```
content_data.py  →  generate_batch.py  →  posts.json + images/  →  posts_bot.py  →  Telegram
 (post texts)       (renders cards,          (queue per channel)    (sends on
                     builds the queue)                               schedule)
```

Post texts are prepared in batches of about two weeks per channel (drafted with AI assistance and reviewed before publishing), then `generate_batch.py` renders the image cards and refreshes each channel's queue.

## Project structure

```
├── posts_bot.py        # the bot: reads the queue and posts on schedule
├── make_card.py        # renders image cards (color themes in THEMES)
├── generate_batch.py   # builds images and posts.json from content_data.py
├── content_data.py     # all post texts, grouped by channel
├── requirements.txt
└── channels/
    └── <channel>/
        ├── config.env  # token and settings (not committed)
        ├── posts.json  # post queue
        ├── state.json  # last sent post (created automatically)
        └── images/     # generated image cards
```

## Tech stack

Python · python-telegram-bot · APScheduler · Pillow

## Setup

1. Install dependencies:
```
   pip install -r requirements.txt
```
2. For each channel, create `channels/<channel>/config.env` based on `config.env.example`, and add your bot token from [@BotFather](https://t.me/BotFather). The bot must be an admin in the channel.
3. Generate images and queues:
```
   python generate_batch.py
```
4. Start one instance per channel, each in its own terminal:
```
   python posts_bot.py --env channels/math_olimjon/config.env
```

To keep the bots running 24/7 on a server, run each instance in its own `tmux` session.

## Security

Bot tokens are stored only in local `config.env` files, which are excluded from the repository. Never commit a real token.

## Author

**Yahyobek Karimov**, Tashkent, Uzbekistan

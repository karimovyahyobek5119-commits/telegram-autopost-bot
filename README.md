# Avtomatik Telegram Post Bot — Rasmli, Bepul, 4 kanal

Hech qanday pullik AI API kerak emas. Har bir post oldindan tayyorlangan
(matn + chiroyli rasm kartochka), bot esa ularni jadval bo'yicha o'zi yuboradi.

**Hozir har bir kanalda 2 haftalik zaxira bor: 28 ta post (kuniga 2 tadan).**

## Papka tuzilishi

```
posts_bot/
├── posts_bot.py          ← botning o'zi (buni ishga tushirasiz)
├── make_card.py           ← rasm kartochka yasovchi funksiya
├── generate_batch.py      ← content_data.py'dan rasm+navbat yasaydi
├── content_data.py        ← barcha post matnlari (shu yerni yangilaysiz)
├── requirements.txt
└── channels/
    ├── math_olimjon/
    │   ├── config.env      ← token va sozlamalar
    │   ├── posts.json       ← navbat (28 post)
    │   ├── state.json       ← qaysi postgacha yuborilgani (avtomatik)
    │   └── images/          ← 28 ta rasm
    ├── faktura/          (xuddi shunday)
    ├── matematika_milliy/  (xuddi shunday)
    └── fizika_milliy/      (xuddi shunday)
```

## 1. O'rnatish

```bash
pip install -r requirements.txt
```

## 2. Har bir kanalning config.env faylini to'ldirish

`channels/<kanal>/config.env` faylini oching, `BOT_TOKEN` qatoriga
@BotFather'dan olingan haqiqiy tokenni yozing. `CHANNEL_ID` va vaqtlar
allaqachon to'g'ri kiritilgan, lekin xohlasangiz `POST_TIMES` ni o'zgartirishingiz mumkin.

**MUHIM**: agar 4 kanal uchun 4 xil bot yaratgan bo'lsangiz — har biriga mos tokenni yozing.
Agar bitta bot orqali barcha kanallarga post qilsangiz (bot barcha kanallarda admin bo'lishi
kerak) — bir xil tokenni hammasiga yozing.

## 3. Botlarni ishga tushirish (har biri alohida terminalda)

```bash
python posts_bot.py --env channels/math_olimjon/config.env
python posts_bot.py --env channels/faktura/config.env
python posts_bot.py --env channels/matematika_milliy/config.env
python posts_bot.py --env channels/fizika_milliy/config.env
```

Har biri terminal/tmux ochiq turgan holda ishlaydi. VS Code'da 4 ta alohida
terminal oynasi ochib, har birida bittasini ishga tushiring.

## 4. 24/7 ishlashi uchun (kompyuterni yopib qo'ymaslik)

```bash
tmux new -s math
python posts_bot.py --env channels/math_olimjon/config.env
# Ctrl+B keyin D — orqa fonga o'tkazasiz, bot ishlab turadi
```

Har bir kanal uchun shunday alohida tmux sessiya oching.

## 5. Navbat tugaganda — YANGI PARTIYA SO'RASH

Har bir kanalda 28 ta post bor (~2 hafta). Tugashiga 2-3 kun qolganda menga
("Claude'ga") shunday yozing:

> "Yana 2 haftalik post kerak, [kanal nomi] uchun"

Men yangi matnlarni yozib beraman, siz ularni `content_data.py` ichidagi
tegishli ro'yxatga (masalan `FAKTURA = [...]`) **qo'shib qo'yasiz**, so'ng:

```bash
python generate_batch.py
```

Bu — yangi rasmlarni yasab, `posts.json` navbatini yangilaydi. Bot ishlab turgan
bo'lsa ham, keyingi ishga tushirishda yangi postlarni ko'radi (botni qayta ishga
tushirish kerak: to'xtatib, qayta yuboring).

## Muhim eslatmalar

- `state.json` — qaysi postgacha yuborilganini eslab qoladi, botni qayta
  ishga tushirsangiz ham navbat DAVOM ETADI, boshidan boshlamaydi.
- `*.log` fayllar orqali har kuni nima yuborilgani ko'rinadi. Agar
  "NAVBAT TUGADI" degan ogohlantirish ko'rsangiz — yangi partiya kerak.
- BOT_TOKEN hech qachon boshqa odamga yoki public joyga (GitHub, chat) yuborilmasin.
- Rasm dizaynini o'zgartirish uchun `make_card.py` ichidagi `THEMES`
  lug'atidagi ranglarni tahrirlashingiz mumkin.

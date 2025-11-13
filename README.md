# 🎵 Song to PDF Converter

This program converts OpenLP song text files into styled PDF song sheets using HTML and CSS.

---

## 📦 Setup Instructions

### 1. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate     # On macOS/Linux
venv\Scripts\activate        # On Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 📝 Usage

Place your song in OpenLP text format inside the file song.txt.
(You can replace the existing contents of song.txt with your own song.)

Example song.txt

```txt
---[Verse:1]---
<b>1) Thank You Jesus</b>
<i>Thank You, Jesus, Thank You, Jesus
Thank You, Lord, For Loving Me x2</i>

You Went To Calvary
There You Died For Me
Thank You, Lord, For Loving Me x2
---[Verse:2]---
<i>Thank You, Jesus, Thank You, Jesus
Thank You, Lord, For Loving Me x2</i>

You Rose Up From The Grave
To Me New Life You Gave
Thank You, Lord, For Loving Me x2
```

Run the program:
```bash
python app.py song.txt
```


The program will generate a PDF file from the song, styled according to the included HTML and CSS.

## 📁 File Structure
```sh
project/
│
├── app.py
├── song.html
├── song.txt
├── requirements.txt
└── README.md
```

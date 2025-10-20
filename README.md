# XBot

**XBot** is an automated scraping bot built with **Python**, **Selenium**, and **pandas** that extracts tweets and user data from **X (Twitter)** using browser automation.  
It supports authentication via saved cookies (exported using a Chrome extension) and saves results to structured CSV files.

## 📁 Project Structure

### App

    Bot/
    ├── auth/
    │      ├── __init__.py
    │      └── authentication.py
    ├── cookies/
    │      ├── __init__.py
    │      └── cookies_manager.py
    ├── driver/
    │      ├── __init__.py
    │      └── webdriver_manager.py
    ├── scraper/
    │      ├── __init__.py
    │      └── twitter_scraper.py
    │── model.py
    ├── x.com.cookies.json
    ├── images/
    |      └── img
    ├── *.csv
    ├── requirements.txt
    ├── main.py
    └── README.md

### Pictures

![Processing](images\img_1.png)
![Finish](images\img_2.png)

### 🧩 Tech Stack

1. Python 3.10+
2. Selenium
3. Pandas

## ⚙️ Setup Instructions

### 1. Clone the repository

```shell
git clone https://github.com/yourusername/XBot.git
cd Bot
```

### 2. Create and Activate Python Virtual Environment

```shell
python -m venv venv
venv\Scripts\activate   # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Cookies

in root dir paste file named x.com.cookies.json

    x.com.cookies.json

### 5. Run Code

```bash
python main.py
```

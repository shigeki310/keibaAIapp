import time
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm #ターミナルで実行する際は from tqdm import tqdm に変更する

headers = {"User-Agent": "Mozilla/5.0"}

def scrape_kaisai_date(from_, to_):
  """_summary_
  fromとtoをyyyy-mmの形で指定すると、間の開催日一覧を取得する関数
  """
  kaisai_date_list = []
  for date in tqdm(pd.date_range(from_, to_, freq="MS")):
    year = date.year
    month = date.month
    url = f"https://race.netkeiba.com/top/calendar.html?year={year}&month={month}"
    response = requests.get(url, headers=headers, verify=True)
    response.raise_for_status() # ステータスコードが200以外の場合に例外を発生させる
    html = response.content # スクレイピング
    time.sleep(1)
    soup = BeautifulSoup(html, 'html.parser') #パーサーを指定
    a_list = soup.find("table", class_ = "Calendar_Table").find_all("a")
    for a in a_list:
      kaisai_date = re.findall(r"kaisai_date=(\d{8})", a["href"])[0]
      kaisai_date_list.append(kaisai_date)
  return kaisai_date_list
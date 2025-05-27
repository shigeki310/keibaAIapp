import pandas as pd
from pathlib import Path
from tqdm.notebook import tqdm

def create_results(html_path_list: list[Path]) -> pd.DataFrame:
  """
  raceページのhtmlを読み込んで、レース結果テーブル」に加工する関数。
  """
  dfs = {}
  for html_path in tqdm(html_path_list):
    with open(html_path, "rb") as f:
      race_id = html_path.stem
      html = f.read()
      df = pd.read_html(html)[0]
      df.index = [race_id] * len(df)
      dfs[race_id] = df
  concat_df = pd.concat(dfs.values())
  concat_df.index.name = "race_id"
  return concat_df
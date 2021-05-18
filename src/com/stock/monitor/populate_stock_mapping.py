from bs4 import BeautifulSoup # for html parsing and scraping
import requests

import json

from src.com.stock.monitor import constants


def populate_dict_and_dump():
  sector_stock_id_tuple_dict = {}
  url_base = "https://www.moneycontrol.com/stocks/marketinfo/marketcap/nse/index.html"
  base_response = requests.get(
    url_base,
    timeout=240
  )
  base_content = BeautifulSoup(base_response.content, "html.parser")
  all_sectors_option = base_content.find_all('select', id="sel_code")[0].find_all("option")
  all_sectors_list = []
  for sector_option in all_sectors_option:
    all_sectors_list.append(sector_option.get("value"))

  # delete first element, as it is empty
  all_sectors_list.pop(0)

  # template for sector url
  sector_url_template = "https://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/{sector}.html"
  count = 0
  for sector in all_sectors_list:
    sector_url = sector_url_template.format(sector=sector)
    response = requests.get(
      sector_url,
      timeout=240
    )
    content = BeautifulSoup(response.content, "html.parser")
    stock_table_name = "tbldata14 bdrtpg"
    stock_table_html = content.find_all("table", class_=stock_table_name)[0]
    all_a = stock_table_html.find_all("a", class_="bl_12")
    for a in all_a:
      count = count + 1
      if count%100==0:
        print(count)
      href = a.get("href")
      split_href = href.split("/")
      sector_id_tuple = (split_href[-3], split_href[-1])
      sector_stock_id_tuple_dict[split_href[-2]] = sector_id_tuple

  print(count)
  mapping_file = open(constants.MAPPING_FILE_PATH, "w")
  json.dump(sector_stock_id_tuple_dict, mapping_file, indent=2, sort_keys=True)
  mapping_file.close()
  return sector_stock_id_tuple_dict

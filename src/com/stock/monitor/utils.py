from bs4 import BeautifulSoup # for html parsing and scraping
import datetime
import json
import matplotlib.pylab as plt
import os

import requests

from src.com.stock.monitor import constants
from src.com.stock.monitor import populate_stock_mapping


DATE_FORMAT = "%b '%y"

def get_epoch_time(date_string):
  return datetime.datetime.strptime(date_string, DATE_FORMAT).timestamp()

def get_time_str_from_epoch(epoch_time):
  ts = datetime.datetime.fromtimestamp(epoch_time)
  return ts.strftime("%b%y")

def plot_graph(datapoints_dict):
  print(datapoints_dict)
  lists = sorted(datapoints_dict.items())
  x, y = zip(*lists)
  ts = []
  for t in x:
    ts.append(get_time_str_from_epoch(t))
  print(x)
  print(ts)
  plt.plot(ts, y)
  plt.show()

def load_mapping():
  if(not os.path.exists(constants.MAPPING_FILE_PATH)):
    return populate_stock_mapping.populate_dict_and_dump()
  else:
    with open(constants.MAPPING_FILE_PATH) as json_file:
      return json.load(json_file)

def get_request_html(url):
  response = requests.get(
    url,
    timeout=240
  )
  return BeautifulSoup(response.content, "html.parser")

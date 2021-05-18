from bs4 import BeautifulSoup # for html parsing and scraping
import requests

from . import constants, utils


def get_quaterly_report_datapoints(company_name, metric_name, quater_count = 20):
  sector_stock_id_tuple_dict = utils.load_mapping()
  company_id = sector_stock_id_tuple_dict[company_name][1]
  quaterly_url = f"https://www.moneycontrol.com/financials/{company_name}/results/quarterly-results/{company_id}/"
  print(quaterly_url)
  full_metric_name = None
  epoch_datapoints_dict = {}
  total_page = int(quater_count/constants.QUATER_PER_PAGE)
  for i in range(1,total_page+1):
    print(quaterly_url+str(i))
    content = utils.get_request_html(quaterly_url+str(i))
    table_entries = content.find_all("table", class_=constants.QUATERLY_TABLE_NAME)
    if len(table_entries)==0:
      break
    table_entries = table_entries[0]
    table_column = table_entries.find_all("tr", class_="lightbg")[0]
    table_column_names = table_column.find_all("td")
    table_row_values = table_entries.find_all("tr", class_="")
    tuple_required = None
    for table_row_value in table_row_values:
      tuple_entries = table_row_value.find_all("td")
      tuple_key_string = tuple_entries[0].text.strip()
      if metric_name.lower() in tuple_key_string.lower():
        tuple_required = tuple_entries
        full_metric_name = tuple_key_string
        break
    print(full_metric_name)

    # dropping last dummy ts (<td class="last_td" style="width: 5%;"> </td>)
    total_columns = len(table_column_names)-1
    for x in range(1,total_columns):
      quater_string = table_column_names[x].text.strip()
      epoch_time = utils.get_epoch_time(quater_string)
      epoch_datapoints_dict[epoch_time] = float(tuple_required[x].text.strip().replace(",", ""))

  print(full_metric_name)
  print(epoch_datapoints_dict)
  return (full_metric_name, epoch_datapoints_dict)

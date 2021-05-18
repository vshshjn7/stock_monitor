from . import cli, utils

import io
from flask import Flask, render_template, request, Response, session
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG


from matplotlib.figure import Figure


app = Flask(__name__)

app.secret_key = 'randomsecret'

@app.route("/")
def index():
  company_name = request.args.get("company_name", "adanipower")
  metric_name = request.args.get("metric_name", "Net Profit/(Loss) For the Period")
  quater_count = request.args.get("quater_count", 10)

  full_metric_name, datapoints_dict = fahrenheit_from(company_name, metric_name, quater_count)

  session["datapoints_dict"] = datapoints_dict

  return (
    """
    <form action="" method="get">
            company_name: <input type="text" name="company_name" value={company_name}>
            metric_name: <input type="text" name="metric_name" value="{metric_name}">
            quater_count: <input type="text" name="quater_count" value={quater_count}>
            <input type="submit" value="plot">
        </form>
        
    <h3>{company_name_upper} {full_metric_name}</h3>
    <img src="/matplot-as-image.png"
         alt="random points as png"
         height="900"
    >
    """
  ).format(metric_name=metric_name, company_name=company_name,
    full_metric_name=full_metric_name, quater_count=quater_count,
    company_name_upper=company_name.upper())

def fahrenheit_from(company_name, metric_name, quater_count):
  """Convert Celsius to Fahrenheit degrees."""
  full_metric_name, datapoints_dict = cli.get_quaterly_report_datapoints(company_name, metric_name, int(quater_count))
  # plt = utils.plot_graph(epoch_datapoints_dict)
  # plot_png(json.dumps(datapoints_dict))
  # plot_svg(json.dumps(datapoints_dict))
  return full_metric_name, datapoints_dict

@app.route("/matplot-as-image.png")
def plot_png():
  """ renders the plot on the fly.
  """
  datapoints_dict = session["datapoints_dict"]
  fig = Figure()
  axis = fig.add_subplot(1, 1, 1)
  lists = sorted(datapoints_dict.items())
  x, y = zip(*lists)
  ts = []
  for t in x:
    ts.append(utils.get_time_str_from_epoch(float(t)))
  print(x)
  print(ts)
  axis.plot(ts, y)

  output = io.BytesIO()
  FigureCanvasAgg(fig).print_png(output)
  return Response(output.getvalue(), mimetype="image/png")


@app.route("/matplot-as-image.svg")
def plot_svg():
  """ renders the plot on the fly.
  """
  datapoints_dict = session["datapoints_dict"]
  fig = Figure()
  axis = fig.add_subplot(1, 1, 1)
  lists = sorted(datapoints_dict.items())
  x, y = zip(*lists)
  ts = []
  for t in x:
    print("#######", t)
    ts.append(utils.get_time_str_from_epoch(float(t)))
  print(x)
  print(ts)
  axis.plot(ts, y)

  output = io.BytesIO()
  FigureCanvasSVG(fig).print_svg(output)
  return Response(output.getvalue(), mimetype="image/svg+xml")

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=8080, debug=True)
#
# company_name = "adanipower"
# metric_name = "Net Profit/(Loss) For the Period"
#
# epoch_datapoints_dict = cli.get_quaterly_report_datapoints(company_name, metric_name)
# utils.plot_graph(epoch_datapoints_dict)

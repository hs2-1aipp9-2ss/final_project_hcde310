# Final Project
# Application

import json
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
# import building_blocks as blocks

# def pretty(obj):
#     return json.dumps(obj, sort_keys=True, indent=2)


# def sort_data(cycle_lst, state="WA"):
#     d = {"DEM": [], "REP": []}
#     for year in cycle_lst:
#         d_yr = blocks.create_graph_data(state=state, cycle=year)
#         if d_yr:
#             i = 0
#             for value in d_yr.values():
#                 if i == 2:
#                     break
#                 if value[2] == "DEM":
#                     d["DEM"].append(value[3])
#                 else:
#                     d["REP"].append(value[3])
#                 i += 1
#         else:
#             d["DEM"].append(0)
#             d["REP"].append(0)
    # if d is not None:
    #     cycle = [str(i) for i in cycle_lst]
    #     dem = d["DEM"]
    #     rep = d["REP"]
    #     return render_template("base.html", data=d, state=state, cycle=cycle, dm=dem, rep=rep)
    # else:
    #   return render_template("base.html", prompt="Something went wrong")
    # return d

# print(sort_data([2022]))
# print(sort_data([2014, 2016, 2018, 2020, 2022]))
# print(sort_data([2014, 2016, 2018, 2020]))

def psuedo_data(year_lst, state="WA"):
    dem = [18778781.04, 0, 9635913.14, 8368803.0, 0]
    rep = [20150770.46, 0, 1933256.38, 449371.0, 0]
    if dem:
        cycle = [str(i) for i in year_lst]
        return render_template("base.html", data=dem, state=state, cycle=cycle, dem=dem, rep=rep)
    else:
        return render_template("base.html", prompt="Something went wrong")

app = Flask(__name__)

# ## ROUTE
@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        state = request.form.get("state")
        cycle = request.form.get("cycle")
        if state and cycle:
            # return sort_data(state, year_lst)
            return psuedo_data([2014, 2016, 2018, 2020, 2022], state)
        else:
            return render_template('base.html',prompt="Need either a correct state and year, please!")
    else:
        return render_template("base.html")

if __name__ == "__main__":
# Used when running locally only
# When deploying to Google AppEngine, a webserver process will
# serve our app.
    app.run(host="localhost", port=8080, debug=True)
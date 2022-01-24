import csv
import json

j_file = "yacht_result.json"

with open(j_file) as j:
   data = json.load(j)

with open("yacht_result.csv", "w") as c_file:
    csv_writer = csv.writer(c_file)
    for values in data.values():
        for value in values:
            csv_writer.writerow(value.values())

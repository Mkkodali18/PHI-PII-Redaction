import json
import csv
import os

def save_json(report):

    os.makedirs("reports", exist_ok=True)

    with open("reports/report.json", "w") as file:
        json.dump(report, file, indent=4)


def save_csv(report):

    os.makedirs("reports", exist_ok=True)

    with open("reports/report.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Category", "Values"])

        for key, value in report.items():
            writer.writerow([key, value])
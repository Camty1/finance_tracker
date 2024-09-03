from flask import Flask
from pathlib import Path

app = Flask(__name__)


@app.route("/")
def main():
    debits_file_name = "data/debits.dat"
    debits_file = open(debits_file_name, "r+")
    debits_lines = debits_file.readlines()
    debits = []
    for line in debits_lines:
        item = {}

        split_line = line.split("|")
        item["name"] = split_line[0]
        item["category"] = split_line[1]
        item["amount"] = float(split_line[2])
        item["desc"] = split_line[3]

        debits.append[item]

    return "\n".join([str(x) for x in debits])

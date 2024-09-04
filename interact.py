#!/usr/bin/env python3
from pymongo.server_api import ServerApi
import pymongo
import os
import glob
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime
import sys


class FinanceDatabase:

    def __init__(self):
        load_dotenv()
        uri = os.environ["MONGODB_URI"]
        # Create a new client and connect to the server
        client = pymongo.mongo_client.MongoClient(
            uri, server_api=pymongo.server_api.ServerApi("1")
        )
        # Send a ping to confirm a successful connection
        try:
            client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
            sys.exit(1)

        self.db = client["finances"]
        self.income = self.db["income"]
        self.spending = self.db["spending"]

    def load_data_file(self, file):
        with open(file, "r") as file:
            lines = file.readlines()

            for line in lines:
                if line[0] == "D":
                    continue
                else:
                    fields = line.split(",")

                    item = {
                        "date": datetime.strptime(fields[0], "%m/%d/%Y"),
                        "amount": float(fields[1]),
                        "category": fields[2],
                        "vendor": fields[3],
                        "card": fields[4],
                        "item": fields[5],
                        "recurring": fields[6][0] == "T",
                    }

    def load_all_data_files(self):
        for file in glob.glob("data/*"):
            self.load_data_file(file)

    def add_spending(self, item):
        if not self.spending.find_one(item):
            self.spending.insert_one(item)
        else:
            print("Duplicate")

    def add_income(self, item):
        if not self.income.find_one(item):
            self.income.insert_one(item)
        else:
            print("Duplicate")

    def prompt_item(self):
        print("Adding an item to the database")
        item_type = input("Income or spending? [i/S] ")

        if item_type.lower() == "i":
            item = {}
            date_prompt = input("Use today's date? [Y/n] ")
            if date_prompt.lower() == "n":
                print("Inputs do not need to be zero padded")
                year = input("Year (YYYY): ")
                month = input("Month (mm): ")
                day = input("Day (dd): ")
                date = datetime(int(year), int(month), int(day))

            else:
                date = datetime.now()
                now = datetime.now()
                date = now.replace(hour=0, minute=0, second=0, microsecond=0)

            item["date"] = date

            amount = input("Amount: ")
            amount = amount.replace(",", "")
            amount = amount.replace("$", "")
            amount = float(amount)
            item["amount"] = amount

            category = input("Category: ")
            item["category"] = category

            print("Do you wish to add the following item to the database? [y/N]")
            for key, value in item.items():
                print(f"    {key}: {value}")
            add = input("")

            if add.lower() == "y":
                self.add_income(item)

        else:
            item = {}
            date_prompt = input("Use today's date? [Y/n] ")
            if date_prompt.lower() == "n":
                print("Inputs do not need to be zero padded")
                year = input("Year (YYYY): ")
                month = input("Month (mm): ")
                day = input("Day (dd): ")
                date = datetime(int(year), int(month), int(day))

            else:
                now = datetime.now()
                date = now.replace(hour=0, minute=0, second=0, microsecond=0)

            item["date"] = date

            amount = input("Amount: ")
            amount.replace(",", "")
            amount.replace("$", "")
            amount = float(amount)
            item["amount"] = amount

            category = input("Category: ")
            item["category"] = category
            vendor = input("Vendor: ")
            item["vendor"] = vendor
            card = input("Card: ")
            item["card"] = card
            item_purchased = input("Item: ")
            item["item"] = item_purchased
            recurring = input("Recurring? [y/N] ")
            if recurring.lower() == "y":
                recurring = True
            else:
                recurring = False

            item["recurring"] = recurring

            print("Do you wish to add the following item to the database? [y/N]")
            for key, value in item.items():
                print(f"    {key}: {value}")
            add = input("")

            if add.lower() == "y":
                self.add_spending(item)

    def print_spending(self):
        print("Spending: ")
        items = sorted(list(self.spending.find()), key=lambda x: x["date"])
        for item in items:
            pprint(item)

    def print_income(self):
        print("Income: ")
        items = sorted(list(self.income.find()), key=lambda x: x["date"])
        for item in items:
            pprint(item)


if __name__ == "__main__":
    database = FinanceDatabase()
    running = True
    while running:
        user_input = input("Add an item, view items in database, or exit? [a/v/E] ")

        if user_input.lower() == "a":
            database.prompt_item()
        elif user_input.lower() == "v":
            user_input = input("Income or spending? [i/S] ")
            if user_input.lower() == "i":
                database.print_income()
            else:
                database.print_spending()
        else:
            running = False
